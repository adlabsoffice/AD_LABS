"""
Publisher Factory - Factory Pattern para criação de publishers

Centraliza criação de publishers de redes sociais.
Permite trocar implementações via configuração.

Autor: Refatoração Arquitetural P1  
Data: 04/12/2024
"""

import logging
from typing import Literal, Optional

from services.social_media.base_publisher import SocialMediaPublisher
from services.social_media.youtube_publisher import YouTubePublisher
from services.social_media.instagram_publisher import InstagramPublisher
from services.social_media.tiktok_publisher import TikTokPublisher

logger = logging.getLogger(__name__)


class PublisherFactory:
    """
    Factory para criação de publishers.
    
    Implementa Factory Pattern para desacoplar criação de objetos.
    """
    
    # Registry de publishers disponíveis
    _publishers = {
        "youtube": YouTubePublisher,
        "instagram": InstagramPublisher,
        "tiktok": TikTokPublisher
    }
    
    @staticmethod
    def create(
        platform: Literal["youtube", "instagram", "tiktok"],
        config: dict
    ) -> SocialMediaPublisher:
        """
        Cria publisher para plataforma especificada.
        
        Args:
            platform: Nome da plataforma ("youtube", "instagram", "tiktok")
            config: Configuração específica da plataforma
            
        Returns:
            Instância de SocialMediaPublisher
            
        Raises:
            ValueError: Se plataforma desconhecida
        """
        if platform not in PublisherFactory._publishers:
            raise ValueError(
                f"Plataforma '{platform}' desconhecida. "
                f"Disponíveis: {list(PublisherFactory._publishers.keys())}"
            )
        
        publisher_class = PublisherFactory._publishers[platform]
        
        logger.info(f"Criando publisher: {publisher_class.__name__}")
        
        return publisher_class(config)
    
    @staticmethod
    def create_all(config: dict) -> dict[str, SocialMediaPublisher]:
        """
        Cria publishers para todas as plataformas configuradas.
        
        Args:
            config: Dicionário com configs de todas as plataformas
                   Ex: {"youtube": {...}, "instagram": {...}}
        
        Returns:
            Dicionário {plataforma: publisher_instance}
        """
        publishers = {}
        
        for platform in PublisherFactory._publishers.keys():
            platform_config = config.get(platform, {})
            
            try:
                publisher = PublisherFactory.create(platform, platform_config)
                
                # Só adiciona se disponível
                if publisher.is_available():
                    publishers[platform] = publisher
                    logger.info(f"✓ {platform.capitalize()} publisher disponível")
                else:
                    logger.warning(f"⚠ {platform.capitalize()} publisher não disponível (config incompleta)")
            
            except Exception as e:
                logger.error(f"❌ Erro ao criar {platform} publisher: {e}")
        
        if not publishers:
            logger.warning("⚠ Nenhum publisher disponível. Verifique configurações.")
        
        return publishers
    
    @staticmethod
    def register_publisher(
        platform: str,
        publisher_class: type[SocialMediaPublisher]
    ):
        """
        Registra novo publisher customizado.
        
        Permite estender factory com publishers externos sem modificar código.
        
        Args:
            platform: Nome da plataforma (ex: "rumble", "vimeo")
            publisher_class: Classe que implementa SocialMediaPublisher
            
        Example:
            >>> class RumblePublisher(SocialMediaPublisher): ...
            >>> PublisherFactory.register_publisher("rumble", RumblePublisher)
        """
        if not issubclass(publisher_class, SocialMediaPublisher):
            raise TypeError(
                f"{publisher_class.__name__} deve herdar de SocialMediaPublisher"
            )
        
        PublisherFactory._publishers[platform] = publisher_class
        logger.info(f"✓ Publisher '{platform}' registrado: {publisher_class.__name__}")


# Export factory
__all__ = ["PublisherFactory"]
