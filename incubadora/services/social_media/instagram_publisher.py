"""
Instagram Publisher - Publicação automatizada no Instagram

Implementa Strategy Pattern para Instagram.
Suporta API oficial e instagrapi como fallback.

Autor: Refatoração Arquitetural P1
Data: 04/12/2024
"""

import logging
import time
from pathlib import Path
from typing import Optional

from pydantic import ValidationError

from services.social_media.base_publisher import SocialMediaPublisher
from specs.schemas.social_media_config import InstagramConfig, PublishMetadata

# instagrapi (Instagram unofficial API)
try:
    from instagrapi import Client
    from instagrapi.exceptions import LoginRequired, ChallengeRequired
    INSTAGRAPI_AVAILABLE = True
except ImportError:
    INSTAGRAPI_AVAILABLE = False

logger = logging.getLogger(__name__)


class InstagramPublisher(SocialMediaPublisher):
    """
    Publisher para Instagram.
    
    Features:
    - Login seguro com instagrapi
    - Publicação de Reels
    - Suporte a Stories (futuro)
    - Retry automático em falhas
    - Validação Pydantic
    
    Nota: Instagram Graph API requer aprovação.
          Usando instagrapi (não-oficial mas estável).
    """
    
    def __init__(self, config: dict):
        """
        Inicializa Instagram Publisher.
        
        Args:
            config: Dicionário com username, password ou access_token
        """
        super().__init__(config)
        
        # Valida config
        try:
            self.instagram_config = InstagramConfig(**config)
        except ValidationError as e:
            self.logger.error(f"Config Instagram inválida: {e}")
            self.instagram_config = None
            return
        
        # Cliente instagrapi
        self.client: Optional[Client] = None
        self._logged_in = False
        
        if INSTAGRAPI_AVAILABLE and self.instagram_config:
            if not self.instagram_config.use_official_api:
                self.client = Client()
    
    def is_available(self) -> bool:
        """Verifica disponibilidade."""
        if not INSTAGRAPI_AVAILABLE:
            self.logger.warning("instagrapi não instalado. Execute: pip install instagrapi")
            return False
        
        if not self.instagram_config:
            self.logger.warning("Config Instagram inválida")
            return False
        
        # Verifica se credenciais estão configuradas
        if self.instagram_config.use_official_api:
            if not self.instagram_config.access_token:
                self.logger.warning("access_token não configurado para Instagram Graph API")
                return False
        else:
            if not (self.instagram_config.username and self.instagram_config.password):
                self.logger.warning("username/password não configurados para instagrapi")
                return False
        
        return True
    
    def _login(self) -> bool:
        """
        Faz login no Instagram.
        
        Returns:
            True se login bem-sucedido
        """
        if self._logged_in:
            return True
        
        if not self.client:
            return False
        
        try:
            self.logger.info(f"🔐 Tentando login como @{self.instagram_config.username}...")
            
            self.client.login(
                self.instagram_config.username,
                self.instagram_config.password
            )
            
            self._logged_in = True
            self.logger.info("✅ Login Instagram realizado")
            
            return True
        
        except LoginRequired as e:
            self.logger.error(f"❌ Login falhou: {e}")
            return False
        
        except ChallengeRequired as e:
            self.logger.error(
                f"❌ Challenge requerido (verificação de segurança). "
                f"Faça login manual no Instagram para resolver: {e}"
            )
            return False
        
        except Exception as e:
            self.logger.error(f"❌ Erro no login: {e}")
            return False
    
    def _validate_video_for_instagram(self, video_path: Path):
        """
        Valida vídeo para Instagram.
        
        Instagram Reels Requirements:
        - Duração: 15-90s
        - Aspect ratio: 9:16 (vertical) recomendado
        - Formato: MP4
        """
        # Validação base
        self.validate_video(video_path)
        
        # TODO: Validar duração e aspect ratio usando moviepy
        # Por enquanto, assume que vídeo já foi gerado no formato correto
        
        if not video_path.suffix.lower() in ['.mp4', '.mov']:
            self.logger.warning(f"⚠ Formato {video_path.suffix} pode não ser suportado. Use .mp4")
    
    def publish(
        self,
        video_path: Path,
        metadata: PublishMetadata
    ) -> str:
        """
        Publica vídeo como Reel no Instagram.
        
        Args:
            video_path: Caminho do vídeo
            metadata: Metadados (caption, tags)
        
        Returns:
            URL do Reel publicado
        """
        if not self.is_available():
            raise RuntimeError(
                "Instagram Publisher não disponível. "
                "Verifique: instagrapi instalado, username/password configurados."
            )
        
        # Login
        if not self._login():
            raise RuntimeError("Falha no login Instagram")
        
        # Valida vídeo
        self._validate_video_for_instagram(video_path)
        
        # Prepara caption
        caption = self._prepare_caption(metadata)
        
        # Upload com retry
        media_id = self._upload_with_retry(video_path, caption)
        
        # Retorna URL
        media_url = f"https://www.instagram.com/reel/{media_id}/"
        self.logger.info(f"✅ Reel publicado no Instagram: {media_url}")
        
        return media_url
    
    def _prepare_caption(self, metadata: PublishMetadata) -> str:
        """Prepara caption do Instagram."""
        
        # Usa caption customizada se fornecida
        if metadata.instagram_caption:
            caption = metadata.instagram_caption
        else:
            # Usa título + descrição padrão
            caption = f"{metadata.titulo}\n\n{metadata.descricao}"
        
        # Adiciona hashtags (Instagram permite até 30)
        if metadata.tags:
            hashtags = " ".join([f"#{tag}" for tag in metadata.tags[:30]])
            caption = f"{caption}\n\n{hashtags}"
        
        # Limita a 2200 caracteres (limite Instagram)
        if len(caption) > 2200:
            caption = caption[:2197] + "..."
            self.logger.warning("⚠ Caption truncada para 2200 caracteres")
        
        return caption
    
    def _upload_with_retry(
        self,
        video_path: Path,
        caption: str
    ) -> str:
        """
        Upload com retry.
        
        Returns:
            media_id do Reel publicado
        """
        max_retries = self.instagram_config.max_retries
        
        for attempt in range(1, max_retries + 1):
            try:
                self.logger.info(
                    f"📤 Uploading Reel (tentativa {attempt}/{max_retries}): "
                    f"{video_path.name}"
                )
                
                # Upload como Reel (clip)
                media = self.client.clip_upload(
                    path=str(video_path),
                    caption=caption
                )
                
                media_id = media.pk
                self.logger.info(f"✅ Upload concluído: {media_id}")
                
                return media_id
            
            except Exception as e:
                if attempt < max_retries:
                    wait_time = 2 ** attempt
                    self.logger.warning(
                        f"⚠ Erro no upload: {e}. Retry em {wait_time}s..."
                    )
                    time.sleep(wait_time)
                else:
                    self.logger.error(f"❌ Upload falhou após {max_retries} tentativas")
                    raise RuntimeError(f"Falha no upload Instagram: {e}")
        
        raise RuntimeError("Falha no upload (max retries)")


# Export
__all__ = ["InstagramPublisher"]
