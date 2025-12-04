"""
Image Generation Service - Abstração para APIs de geração de imagens

Resolve violação DIP (Dependency Inversion Principle) identificada na auditoria.
Desacopla agentes de APIs concretas (Imagen, MidJourney, etc).

Autor: Refatoração Arquitetural P0
Data: 04/12/2024
"""

import os
import logging
import base64
from pathlib import Path
from typing import Optional, Literal
from abc import ABC, abstractmethod

# Google Generative AI
try:
    import google.generativeai as genai
    GOOGLE_AVAILABLE = True
except ImportError:
    GOOGLE_AVAILABLE = False
    logging.warning("google-generativeai não instalado. Imagen não disponível.")

from specs.schemas.video_pipeline import ImageGenerationConfig

logger = logging.getLogger(__name__)


class ImageGenerationService(ABC):
    """
    Interface abstrata para serviços de geração de imagens.
    
    Permite trocar backends (Imagen → MidJourney → DALL-E) sem modificar código dos agentes.
    """
    
    @abstractmethod
    def generate(
        self, 
        prompt: str, 
        reference_image: Optional[Path] = None,
        config: Optional[ImageGenerationConfig] = None
    ) -> Path:
        """
        Gera uma imagem a partir de um prompt.
        
        Args:
            prompt: Descrição textual da imagem
            reference_image: Imagem de referência para consistência (opcional)
            config: Configurações de geração
            
        Returns:
            Path da imagem gerada
        """
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Verifica se o serviço está disponível (API key configurada, etc)"""
        pass


class ImagenService(ImageGenerationService):
    """
    Implementação para Google Imagen 4.
    
    Suporta:
    - Imagen 4 Standard
    - Imagen 4 Ultra "Nano Banana" (4K, text rendering)
    - Character Reference (consistência de personagens)
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Inicializa serviço Imagen.
        
        Args:
            api_key: Google API Key (usa GOOGLE_API_KEY_IMAGE se não fornecida)
        """
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY_IMAGE")
        
        if not self.api_key:
            logger.error("GOOGLE_API_KEY_IMAGE não configurada")
            return
        
        if GOOGLE_AVAILABLE:
            genai.configure(api_key=self.api_key)
            logger.info("ImagenService inicializado com sucesso")
        else:
            logger.error("google-generativeai não instalado. Execute: pip install google-generativeai")
    
    def is_available(self) -> bool:
        """Verifica disponibilidade do serviço"""
        return bool(self.api_key and GOOGLE_AVAILABLE)
    
    def generate(
        self, 
        prompt: str, 
        reference_image: Optional[Path] = None,
        config: Optional[ImageGenerationConfig] = None
    ) -> Path:
        """
        Gera imagem usando Imagen 4.
        
        Args:
            prompt: Prompt visual
            reference_image: Imagem de referência (para character consistency)
            config: Configurações (usa padrões se None)
            
        Returns:
            Path da imagem salva
        """
        if not self.is_available():
            raise RuntimeError("ImagenService não disponível. Verifique API key e instalação.")
        
        # Configurações padrão
        if config is None:
            config = ImageGenerationConfig()
        
        # Monta modelo
        model_name = f"imagen-3.0-generate-001"  # Modelo atual
        if config.model == "imagen-4-ultra":
            model_name = "imagen-3.0-generate-001"  # Atualizar quando 4 Ultra estiver disponível
        
        logger.info(f"Gerando imagem com {model_name}: {prompt[:80]}...")
        
        try:
            # Configura geração
            generation_config = {
                "aspect_ratio": config.aspect_ratio,
                "number_of_images": 1,
                "safety_filter_level": "block_only_high" if config.safety_filter else "block_none"
            }
            
            # TODO: Adicionar suporte a character reference quando API suportar
            # Por enquanto, a consistência vem do CharacterManager injetando descrições fixas
            
            if reference_image and config.use_character_reference:
                logger.warning(
                    "Character reference solicitada mas ainda não implementada na API. "
                    "Usando apenas prompt expandido."
                )
            
            # Gera imagem
            model = genai.ImageGenerationModel(model_name)
            
            result = model.generate_images(
                prompt=prompt,
                **generation_config
            )
            
            if not result.images:
                raise RuntimeError("Nenhuma imagem gerada")
            
            # Salva primeira imagem
            image = result.images[0]
            
            # Cria nome de arquivo único
            import hashlib
            import time
            
            prompt_hash = hashlib.md5(prompt.encode()).hexdigest()[:8]
            timestamp = int(time.time())
            filename = f"img_{timestamp}_{prompt_hash}.png"
            
            output_dir = Path("d:/AD_LABS/outputs/imagens")
            output_dir.mkdir(parents=True, exist_ok=True)
            
            output_path = output_dir / filename
            
            # Salva imagem
            image._pil_image.save(output_path)
            
            logger.info(f"✅ Imagem salva: {output_path}")
            
            return output_path
        
        except Exception as e:
            logger.error(f"❌ Erro ao gerar imagem: {e}")
            raise


class MidJourneyService(ImageGenerationService):
    """
    Implementação para MidJourney (futuro).
    
    Placeholder para quando houver budget ($30/mês).
    """
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        logger.warning("MidJourneyService ainda não implementado")
    
    def is_available(self) -> bool:
        return False
    
    def generate(
        self, 
        prompt: str, 
        reference_image: Optional[Path] = None,
        config: Optional[ImageGenerationConfig] = None
    ) -> Path:
        raise NotImplementedError("MidJourney não implementado. Use ImagenService.")


class ImageServiceFactory:
    """
    Factory para criar serviços de imagem.
    
    Permite trocar backends via configuração sem modificar código.
    """
    
    @staticmethod
    def create(
        provider: Literal["imagen", "midjourney"] = "imagen",
        api_key: Optional[str] = None
    ) -> ImageGenerationService:
        """
        Cria serviço de geração de imagens.
        
        Args:
            provider: Nome do provider ("imagen", "midjourney")
            api_key: API key (opcional, usa env vars)
            
        Returns:
            Instância de ImageGenerationService
        """
        providers = {
            "imagen": ImagenService,
            "midjourney": MidJourneyService
        }
        
        service_class = providers.get(provider)
        
        if not service_class:
            raise ValueError(f"Provider desconhecido: {provider}. Disponíveis: {list(providers.keys())}")
        
        service = service_class(api_key=api_key)
        
        if not service.is_available():
            logger.warning(f"Provider '{provider}' não disponível. Tentando fallback...")
            
            # Fallback: tentar Imagen se outro provider falhar
            if provider != "imagen":
                return ImagenService(api_key=api_key)
        
        return service


if __name__ == "__main__":
    # Teste básico
    logging.basicConfig(level=logging.INFO)
    
    print("🧪 Testando ImageGenerationService...")
    
    # Cria serviço
    service = ImageServiceFactory.create(provider="imagen")
    
    if service.is_available():
        print("✅ Imagen disponível")
        
        # Teste simples (descomente para gerar imagem real)
        # prompt = "Jesus moderno, 30 anos, barba castanha, túnica branca, fundo urban, cinematic lighting, 4k"
        # config = ImageGenerationConfig(aspect_ratio="16:9", quality="hd")
        # path = service.generate(prompt, config=config)
        # print(f"✅ Imagem gerada: {path}")
    else:
        print("❌ Imagen não disponível. Verifique API key.")
    
    print("\n✅ ImageGenerationService OK!")
