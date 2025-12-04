"""
Thumbnail Processor - Serviço de processamento de thumbnails

Extrai responsabilidade do Agente 12 (SRP).
Cria thumbnails otimizadas para cada plataforma.

Autor: Refatoração Arquitetural P1
Data: 04/12/2024
"""

import logging
from pathlib import Path
from typing import Optional, Literal

try:
    from PIL import Image, ImageDraw, ImageFont, ImageEnhance
    PILLOW_AVAILABLE = True
except ImportError:
    PILLOW_AVAILABLE = False

logger = logging.getLogger(__name__)


class ThumbnailProcessor:
    """
    Processador de thumbnails para redes sociais.
    
    Features:
    - Templates pré-definidos por plataforma (YouTube, Instagram, etc)
    - Filtros de "pop" (contrast, saturation)
    - Adição de texto com stroke
    - Resize automático
    """
    
    # Templates de resolução por plataforma
    TEMPLATES = {
        "youtube": (1280, 720),       # 16:9 - YouTube thumbnail padrão
        "instagram_post": (1080, 1080),  # 1:1 - Instagram square post
        "instagram_story": (1080, 1920), # 9:16 - Instagram story/reel
        "tiktok": (1080, 1920),       # 9:16 - TikTok vertical
        "twitter": (1200, 675)        # 16:9 - Twitter card
    }
    
    def __init__(self, output_dir: Optional[Path] = None):
        """
        Inicializa processor.
        
        Args:
            output_dir: Diretório de saída (padrão: outputs/thumbnails/)
        """
        if not PILLOW_AVAILABLE:
            logger.warning(
                "Pillow não disponível. Execute: pip install pillow\n"
                "Thumbnails não poderão ser processadas."
            )
        
        self.output_dir = output_dir or Path("outputs/thumbnails")
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def process(
        self,
        image_path: Path,
        platform: Literal["youtube", "instagram_post", "instagram_story", "tiktok", "twitter"] = "youtube",
        text: Optional[str] = None,
        enhance: bool = True
    ) -> Path:
        """
        Processa imagem para thumbnail.
        
        Args:
            image_path: Caminho da imagem base
            platform: Plataforma alvo (define dimensões)
            text: Texto para adicionar (opcional)
            enhance: Se True, aplica filtros de contrast/saturation
        
        Returns:
            Path da thumbnail processada
        
        Raises:
            RuntimeError: Se Pillow não disponível
            FileNotFoundError: Se imagem base não existe
        """
        if not PILLOW_AVAILABLE:
            raise RuntimeError(
                "Pillow não instalado. Execute: pip install pillow"
            )
        
        if not image_path.exists():
            raise FileNotFoundError(f"Imagem não encontrada: {image_path}")
        
        logger.info(f"🖼️ Processando thumbnail: {image_path.name} → {platform}")
        
        # Abre imagem
        with Image.open(image_path) as img:
            # Converte para RGB se necessário
            if img.mode != "RGB":
                img = img.convert("RGB")
            
            # Resize para template da plataforma
            target_size = self.TEMPLATES[platform]
            img = self._smart_resize(img, target_size)
            
            # Aplica filtros de "pop"
            if enhance:
                img = self._apply_enhancements(img)
            
            # Adiciona texto
            if text:
                img = self._add_text(img, text, platform)
            
            # Salva thumbnail
            output_path = self._generate_output_path(image_path, platform)
            img.save(output_path, "JPEG", quality=95, optimize=True)
            
            logger.info(f"✅ Thumbnail salva: {output_path}")
            
            return output_path
    
    def _smart_resize(self, img: Image.Image, target_size: tuple[int, int]) -> Image.Image:
        """
        Resize inteligente mantendo aspect ratio.
        
        Faz crop central se aspect ratios diferentes.
        """
        target_width, target_height = target_size
        target_ratio = target_width / target_height
        
        img_width, img_height = img.size
        img_ratio = img_width / img_height
        
        if abs(img_ratio - target_ratio) < 0.01:
            # Aspect ratio similar, apenas resize
            return img.resize(target_size, Image.LANCZOS)
        
        # Aspect ratio diferente, crop central
        if img_ratio > target_ratio:
            # Imagem mais larga, crop horizontal
            new_width = int(img_height * target_ratio)
            left = (img_width - new_width) // 2
            img = img.crop((left, 0, left + new_width, img_height))
        else:
            # Imagem mais alta, crop vertical
            new_height = int(img_width / target_ratio)
            top = (img_height - new_height) // 2
            img = img.crop((0, top, img_width, top + new_height))
        
        return img.resize(target_size, Image.LANCZOS)
    
    def _apply_enhancements(self, img: Image.Image) -> Image.Image:
        """
        Aplica filtros de "pop" (contraste e saturação).
        
        Faz thumbnail se destacar no feed.
        """
        # Aumenta contraste (+20%)
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.2)
        
        # Aumenta saturação (+30%)
        enhancer = ImageEnhance.Color(img)
        img = enhancer.enhance(1.3)
        
        return img
    
    def _add_text(
        self,
        img: Image.Image,
        text: str,
        platform: str
    ) -> Image.Image:
        """
        Adiciona texto com stroke (contorno) para legibilidade.
        """
        draw = ImageDraw.Draw(img)
        
        # Tamanho de fonte baseado na altura da imagem
        img_height = img.size[1]
        font_size = int(img_height * 0.12)  # 12% da altura
        
        # Tenta carregar fonte impactante
        try:
            # Windows: Arial Bold
            font = ImageFont.truetype("arialbd.ttf", font_size)
        except:
            try:
                # Fallback: Arial regular
                font = ImageFont.truetype("arial.ttf", font_size)
            except:
                # Fallback: fonte padrão
                font = ImageFont.load_default()
                logger.warning("Fonte Arial não encontrada, usando padrão")
        
        # Posição do texto (canto inferior, centralizado)
        # Pega bounding box para centralizar
        bbox = draw.textbbox((0, 0), text.upper(), font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        img_width, img_height = img.size
        
        x = (img_width - text_width) // 2  # Centralizado horizontalmente
        y = img_height - text_height - int(img_height * 0.1)  # 10% do fundo
        
        # Desenha texto com stroke (contorno preto)
        stroke_width = max(3, int(font_size * 0.05))
        draw.text(
            (x, y),
            text.upper(),
            font=font,
            fill="white",
            stroke_width=stroke_width,
            stroke_fill="black"
        )
        
        return img
    
    def _generate_output_path(self, original_path: Path, platform: str) -> Path:
        """Gera nome único para thumbnail."""
        stem = original_path.stem
        filename = f"thumb_{platform}_{stem}.jpg"
        return self.output_dir / filename


# Export
__all__ = ["ThumbnailProcessor"]
