"""
TikTok Publisher - Placeholder para futuro

Aguardando aprovação de App TikTok.
Use n8n workflow como alternativa no interim.

Autor: Refatoração Arquitetural P1
Data: 04/12/2024
"""

import logging
from pathlib import Path

from pydantic import ValidationError

from services.social_media.base_publisher import SocialMediaPublisher
from specs.schemas.social_media_config import TikTokConfig, PublishMetadata

logger = logging.getLogger(__name__)


class TikTokPublisher(SocialMediaPublisher):
    """
    Publisher para TikTok (placeholder).
    
    TikTok requer aprovação de Developer App que leva 2-4 semanas.
    
    Alternativas no interim:
    - Workflow n8n: incubadora/n8n_workflows/03_tiktok_posting.json
    - Upload manual via TikTok Creator Studio
    
    Quando TikTok API estiver aprovada:
    - Implementar publish() com TikTok API
    - Atualizar is_available() para verificar api_key
    """
    
    def __init__(self, config: dict):
        """Inicializa TikTok Publisher."""
        super().__init__(config)
        
        # Valida config
        try:
            self.tiktok_config = TikTokConfig(**config)
        except ValidationError as e:
            self.logger.error(f"Config TikTok inválida: {e}")
            self.tiktok_config = None
    
    def is_available(self) -> bool:
        """
        TikTok não disponível até aprovação de App.
        
        Returns:
            False (sempre, por enquanto)
        """
        if not self.tiktok_config:
            return False
        
        if self.tiktok_config.status == "active":
            # Futuro: verificar api_key válida
            return bool(self.tiktok_config.api_key)
        
        return False
    
    def publish(
        self,
        video_path: Path,
        metadata: PublishMetadata
    ) -> str:
        """
        PublishTikTok (não implementado).
        
        Raises:
            NotImplementedError: Sempre, até TikTok API ser aprovada
        """
        alternative = (
            self.tiktok_config.alternative_workflow 
            if self.tiktok_config 
            else "n8n_workflows/03_tiktok_posting.json"
        )
        
        raise NotImplementedError(
            f"TikTok Publisher ainda não implementado.\n\n"
            f"TikTok requer aprovação de Developer App (2-4 semanas).\n\n"
            f"Alternativas:\n"
            f"  1. Workflow n8n: {alternative}\n"
            f"  2. Upload manual: https://www.tiktok.com/creator-center/upload\n"
            f"  3. Aguardar aprovação da API TikTok\n\n"
            f"Quando aprovado, este publisher será implementado automaticamente."
        )


# Export
__all__ = ["TikTokPublisher"]
