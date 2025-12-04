"""
Social Media Publishing Services

Sistema de publicação em redes sociais usando Strategy Pattern.
Suporta YouTube, Instagram, TikTok e futuras plataformas.

Autor: Refatoração Arquitetural P1
Data: 04/12/2024
"""

from .base_publisher import SocialMediaPublisher
from .youtube_publisher import YouTubePublisher
from .instagram_publisher import InstagramPublisher
from .tiktok_publisher import TikTokPublisher

__all__ = [
    "SocialMediaPublisher",
    "YouTubePublisher", 
    "InstagramPublisher",
    "TikTokPublisher"
]
