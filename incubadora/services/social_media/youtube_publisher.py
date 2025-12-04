"""
YouTube Publisher - Publicação automatizada no YouTube

Implementa Strategy Pattern para YouTube Data API v3.
Usa OAuth2 para autenticação segura.

Autor: Refatoração Arquitetural P1
Data: 04/12/2024
"""

import logging
import time
from pathlib import Path
from typing import Optional

from pydantic import ValidationError

from services.social_media.base_publisher import SocialMediaPublisher
from specs.schemas.social_media_config import YouTubeConfig, PublishMetadata

# Google APIs
try:
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload
    from googleapiclient.errors import HttpError
    from google.oauth2.credentials import Credentials
    GOOGLE_API_AVAILABLE = True
except ImportError:
    GOOGLE_API_AVAILABLE = False

logger = logging.getLogger(__name__)


class YouTubePublisher(SocialMediaPublisher):
    """
    Publisher para YouTube usando OAuth2.
    
    Features:
    - Autenticação OAuth2 real (não mock)
    - Upload de vídeos via YouTube Data API v3
    - Upload de thumbnails customizadas
    - Retry automático em falhas transientes
    - Validação Pydantic de configurações
    """
    
    def __init__(self, config: dict):
        """
        Inicializa YouTube Publisher.
        
        Args:
            config: Dicionário com client_id, client_secret, refresh_token, etc.
        
        Raises:
            ValidationError: Se config inválida
        """
        super().__init__(config)
        
        # Valida config com Pydantic
        try:
            self.youtube_config = YouTubeConfig(**config)
        except ValidationError as e:
            self.logger.error(f"Config YouTube inválida: {e}")
            # Configura como indisponível
            self.youtube_config = None
            return
        
        # Inicializa cliente YouTube
        self.youtube_client = None
        
        if GOOGLE_API_AVAILABLE and self.youtube_config:
            self._init_youtube_client()
    
    def _init_youtube_client(self):
        """Inicializa cliente YouTube com OAuth2."""
        try:
            # Cria credenciais OAuth2 a partir do refresh token
            credentials = Credentials(
                None,  # access_token será gerado automaticamente
                refresh_token=self.youtube_config.refresh_token,
                token_uri="https://oauth2.googleapis.com/token",
                client_id=self.youtube_config.client_id,
                client_secret=self.youtube_config.client_secret
            )
            
            # Build YouTube API service
            self.youtube_client = build(
                "youtube",
                "v3",
                credentials=credentials,
                cache_discovery=False
            )
            
            self.logger.info("✓ Cliente YouTube inicializado com OAuth2")
        
        except Exception as e:
            self.logger.error(f"❌ Erro ao inicializar YouTube client: {e}")
            self.youtube_client = None
    
    def is_available(self) -> bool:
        """Verifica se YouTube publisher está disponível."""
        if not GOOGLE_API_AVAILABLE:
            self.logger.warning("google-api-python-client não instalado")
            return False
        
        if not self.youtube_config:
            self.logger.warning("Config YouTube inválida")
            return False
        
        if not self.youtube_client:
            self.logger.warning("Cliente YouTube não inicializado")
            return False
        
        return True
    
    def publish(
        self,
        video_path: Path,
        metadata: PublishMetadata
    ) -> str:
        """
        Publica vídeo no YouTube.
        
        Args:
            video_path: Caminho do vídeo
            metadata: Metadados (título, descrição, tags)
        
        Returns:
            URL do vídeo publicado (ex: https://youtube.com/watch?v=VIDEO_ID)
        
        Raises:
            RuntimeError: Se publisher não disponível ou upload falhar
        """
        if not self.is_available():
            raise RuntimeError(
                "YouTube Publisher não disponível. "
                "Verifique: google-api-python-client instalado, "
                "client_id/client_secret/refresh_token configurados."
            )
        
        # Valida vídeo
        self.validate_video(video_path)
        
        # Prepara metadados
        body = self._prepare_video_metadata(metadata)
        
        # Upload com retry
        video_id = self._upload_with_retry(video_path, body)
        
        # Upload thumbnail (se fornecida)
        if metadata.thumbnail_path:
            self._upload_thumbnail(video_id, metadata.thumbnail_path)
        
        # Retorna URL
        video_url = f"https://youtube.com/watch?v={video_id}"
        self.logger.info(f"✅ Vídeo publicado no YouTube: {video_url}")
        
        return video_url
    
    def _prepare_video_metadata(self, metadata: PublishMetadata) -> dict:
        """Prepara body request para YouTube API."""
        
        # Privacy: usa override de metadata ou padrão da config
        privacy = metadata.youtube_privacy or self.youtube_config.default_privacy
        
        # Category: usa override ou padrão
        category_id = str(metadata.youtube_category or self.youtube_config.default_category)
        
        # Tags: limita a 500 caracteres totais (limite YouTube)
        tags = metadata.tags[:30]  # Máximo 30 tags
        
        body = {
            "snippet": {
                "title": metadata.titulo,
                "description": metadata.descricao,
                "tags": tags,
                "categoryId": category_id
            },
            "status": {
                "privacyStatus": privacy,
                "selfDeclaredMadeForKids": False
            }
        }
        
        return body
    
    def _upload_with_retry(
        self,
        video_path: Path,
        body: dict
    ) -> str:
        """
        Faz upload com retry automático.
        
        Returns:
            video_id do vídeo publicado
        """
        max_retries = self.youtube_config.max_retries
        
        for attempt in range(1, max_retries + 1):
            try:
                self.logger.info(
                    f"📤 Iniciando upload YouTube (tentativa {attempt}/{max_retries}): "
                    f"{video_path.name}"
                )
                
                # Cria media upload
                media = MediaFileUpload(
                    str(video_path),
                    mimetype="video/*",
                    resumable=True,
                    chunksize=1024 * 1024  # 1MB chunks
                )
                
                # Insere vídeo
                request = self.youtube_client.videos().insert(
                    part="snippet,status",
                    body=body,
                    media_body=media
                )
                
                # Upload com progress (resumable)
                response = None
                while response is None:
                    status, response = request.next_chunk()
                    if status:
                        progress = int(status.progress() * 100)
                        self.logger.info(f"⏳ Upload: {progress}%")
                
                video_id = response["id"]
                self.logger.info(f"✅ Upload concluído: {video_id}")
                
                return video_id
            
            except HttpError as e:
                if attempt < max_retries:
                    wait_time = 2 ** attempt  # Exponential backoff
                    self.logger.warning(
                        f"⚠ Erro HTTP {e.resp.status}: {e.content}. "
                        f"Retry em {wait_time}s..."
                    )
                    time.sleep(wait_time)
                else:
                    self.logger.error(f"❌ Upload falhou após {max_retries} tentativas")
                    raise RuntimeError(f"Falha no upload YouTube: {e}")
            
            except Exception as e:
                self.logger.error(f"❌ Erro inesperado no upload: {e}")
                raise RuntimeError(f"Erro no upload YouTube: {e}")
        
        raise RuntimeError("Falha no upload (max retries alcançado)")
    
    def _upload_thumbnail(self, video_id: str, thumbnail_path: Path):
        """Upload de thumbnail customizada."""
        if not thumbnail_path.exists():
            self.logger.warning(f"Thumbnail não encontrada: {thumbnail_path}")
            return
        
        try:
            self.logger.info(f"🖼️ Uploading thumbnail: {thumbnail_path.name}")
            
            self.youtube_client.thumbnails().set(
                videoId=video_id,
                media_body=MediaFileUpload(str(thumbnail_path))
            ).execute()
            
            self.logger.info("✅ Thumbnail uploaded")
        
        except Exception as e:
            self.logger.warning(f"⚠ Erro ao fazer upload da thumbnail: {e}")
            # Não falha publicação se thumbnail falhar


# Export
__all__ = ["YouTubePublisher"]
