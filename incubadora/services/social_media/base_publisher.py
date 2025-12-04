"""
Base Publisher - Interface para Social Media Publishers

Define contrato abstrato para publicação em redes sociais.
Implementa DIP (Dependency Inversion Principle) do SOLID.

Autor: Refatoração Arquitetural P1
Data: 04/12/2024
"""

import logging
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional

from specs.schemas.social_media_config import PublishMetadata

logger = logging.getLogger(__name__)


class SocialMediaPublisher(ABC):
    """
    Interface abstrata para publishers de redes sociais.
    
    Permite trocar implementações (YouTube → Instagram → TikTok) sem modificar
    código dos agentes que dependem desta interface.
    
    Princípios SOLID implementados:
    - DIP: Agentes dependem de abstração, não de implementação concreta
    - OCP: Extensível (adicionar novos publishers) sem modificar código existente
    - ISP: Interface focada e mínima
    """
    
    def __init__(self, config: dict):
        """
        Inicializa publisher com configuração.
        
        Args:
            config: Dicionário com configurações específicas da plataforma
        """
        self.config = config
        self.logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
    
    @abstractmethod
    def publish(
        self, 
        video_path: Path, 
        metadata: PublishMetadata
    ) -> str:
        """
        Publica vídeo na plataforma.
        
        Args:
            video_path: Caminho do arquivo de vídeo
            metadata: Metadados (título, descrição, tags, etc)
            
        Returns:
            URL do vídeo publicado
            
        Raises:
            RuntimeError: Se publicação falhar
            FileNotFoundError: Se vídeo não existir
            ValidationError: Se metadados inválidos
        """
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """
        Verifica se publisher está disponível.
        
        Checa:
        - Credenciais configuradas
        - APIs acessíveis
        - Bibliotecas instaladas
        
        Returns:
            True se publisher pode ser usado, False caso contrário
        """
        pass
    
    def validate_video(self, video_path: Path) -> bool:
        """
        Valida arquivo de vídeo (implementação base).
        
        Subclasses podem override para validações específicas da plataforma
        (duração, formato, resolução, etc).
        
        Args:
            video_path: Caminho do vídeo
            
        Returns:
            True se vídeo válido
            
        Raises:
            FileNotFoundError: Se arquivo não existe
        """
        if not video_path.exists():
            raise FileNotFoundError(f"Vídeo não encontrado: {video_path}")
        
        if video_path.stat().st_size == 0:
            raise ValueError(f"Vídeo vazio: {video_path}")
        
        self.logger.info(f"✓ Vídeo validado: {video_path.name} ({video_path.stat().st_size / 1024 / 1024:.2f} MB)")
        
        return True
    
    def get_platform_name(self) -> str:
        """Retorna nome da plataforma (para logs e UI)."""
        return self.__class__.__name__.replace("Publisher", "")


class MockPublisher(SocialMediaPublisher):
    """
    Publisher mock para testes.
    
    Simula publicação sem fazer upload real.
    Útil para desenvolvimento e testes automatizados.
    """
    
    def __init__(self, config: Optional[dict] = None):
        super().__init__(config or {})
        self.published_videos = []  # Histórico para assertions em testes
    
    def publish(self, video_path: Path, metadata: PublishMetadata) -> str:
        """Simula publicação."""
        self.validate_video(video_path)
        
        mock_url = f"https://mock-platform.com/watch?v=MOCK_{video_path.stem}"
        
        self.published_videos.append({
            "video_path": video_path,
            "metadata": metadata,
            "url": mock_url
        })
        
        self.logger.info(f"🔧 [MOCK] Vídeo 'publicado': {mock_url}")
        
        return mock_url
    
    def is_available(self) -> bool:
        """Mock sempre disponível."""
        return True


# Export classes
__all__ = ["SocialMediaPublisher", "MockPublisher"]
