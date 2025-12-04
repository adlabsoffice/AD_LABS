"""
Agente 07 - Diretora Visual

REFATORADO: 04/12/2024
- Separação de responsabilidades (SRP)
- Injeção de dependências (DIP)
- Validação com Pydantic schemas (ISP)

Resolver problemas identificados na auditoria:
1. Inconsistência visual de personagens
2. Acoplamento a APIs concretas
3. Falta de validação de contratos
"""

import os
import time
import logging
from pathlib import Path
from typing import Optional, Dict, List
from rich.console import Console

# Imports de serviços (DIP - Dependency Inversion)
from utils.character_manager import CharacterManager
from services.image_generation import ImageServiceFactory, ImageGenerationService
from specs.schemas.video_pipeline import (
    VideoScript, 
    SceneBlock, 
    ImageGenerationConfig
)

console = Console()
logger = logging.getLogger(__name__)


class Agente07Visual:
    """
    Diretora Visual - Gera imagens consistentes para o vídeo.
    
    Responsabilidades (SRP):
    - Orquestrar geração de visuais
    - Aplicar estilo do canal
    - Gerar thumbnail
    
    NÃO é responsável por:
    - Consistência de personagens (CharacterManager)
    - Chamadas diretas a APIs (ImageGenerationService)
    """
    
    def __init__(
        self,
        canal_id: str,
        character_manager: Optional[CharacterManager] = None,
        image_service: Optional[ImageGenerationService] = None,
        config: Optional[Dict] = None
    ):
        """
        Inicializa Agente Visual com injeção de dependências.
        
        Args:
            canal_id: ID do canal (ex: "o_livro_caixa_divino")
            character_manager: Gerenciador de personagens (cria automaticamente se None)
            image_service: Serviço de geração de imagens (cria automaticamente se None)
            config: Configurações customizadas
        """
        self.canal_id = canal_id
        self.config = config or {}
        
        # Injeção de dependências (DIP)
        self.character_manager = character_manager or CharacterManager(canal_id=canal_id)
        
        provider = self.config.get("image_provider", "imagen")
        self.image_service = image_service or ImageServiceFactory.create(provider=provider)
        
        # Configuração de geração padrão
        self.gen_config = ImageGenerationConfig(
            model=self.config.get("imagen_model", "imagen-4-standard"),
            aspect_ratio="16:9",
            quality="hd",
            use_character_reference=True
        )
        
        self.output_dir = Path("d:/AD_LABS/outputs/imagens")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Agente07Visual inicializado para canal '{canal_id}' com provider '{provider}'")
    
    def gerar_visuais(self, roteiro_data: Dict, config: Optional[Dict] = None) -> List[Dict]:
        """
        Gera imagens para cada cena do roteiro COM consistência de personagens.
        
        Args:
            roteiro_data: Dicionário com dados do roteiro (será validado)
            config: Configurações adicionais (opcional)
            
        Returns:
            Lista de imagens geradas com metadados
        """
        console.print(f"[bold yellow]AGENTE 07: Iniciando Geração Visual Consistente...[/bold yellow]")
        
        # Valida roteiro com Pydantic (ISP - Interface Segregation)
        try:
            roteiro = VideoScript.model_validate(roteiro_data)
            console.print(f"   ✅ Roteiro validado: {len(roteiro.scenes)} cenas")
        except Exception as e:
            logger.error(f"Erro de validação no roteiro: {e}")
            raise ValueError(f"Roteiro inválido: {e}")
        
        imagens_geradas = []
        
        # Processa cada cena
        for i, cena in enumerate(roteiro.scenes):
            console.print(f"\n   [cyan]Cena {i+1}/{len(roteiro.scenes)}:[/cyan] {cena.speaker}")
            console.print(f"      Fala: \"{cena.dialogue[:50]}...\"")
            console.print(f"      Visual: {cena.visual_prompt[:60]}...")
            
            try:
                # NOVO: Injeta consistência de personagem
                prompt_consistente = self._preparar_prompt_consistente(cena)
                
                # Obtém imagem de referência se houver
                ref_image = self.character_manager.get_reference_image(cena.speaker)
                
                # Gera imagem usando serviço injetado
                caminho_imagem = self.image_service.generate(
                    prompt=prompt_consistente,
                    reference_image=ref_image,
                    config=self.gen_config
                )
                
                # Se é primeira aparição do personagem, salva como referência
                if not ref_image and cena.speaker.lower() != "narrador":
                    self.character_manager.save_reference(cena.speaker, str(caminho_imagem))
                    console.print(f"      ✨ Primeira aparição de '{cena.speaker}' - salva como referência")
                
                console.print(f"      ✅ [green]Imagem gerada:[/green] {caminho_imagem.name}")
                
                imagens_geradas.append({
                    "cena_id": i,
                    "speaker": cena.speaker,
                    "prompt_original": cena.visual_prompt,
                    "prompt_consistente": prompt_consistente,
                    "arquivo": str(caminho_imagem),
                    "duration_seconds": cena.duration_seconds
                })
                
            except Exception as e:
                logger.error(f"Erro ao gerar imagem da cena {i+1}: {e}")
                console.print(f"      ❌ [bold red]ERRO FATAL:[/bold red] {e}")
                raise RuntimeError(
                    f"Falha na geração da cena {i+1}.\n"
                   f"Speaker: {cena.speaker}\n"
                    f"Prompt: {cena.visual_prompt}\n"
                    f"Erro: {e}"
                )
            
            # Delay entre requisições
            time.sleep(2)
        
        console.print(f"\n   ✅ [bold green]{len(imagens_geradas)} imagens geradas com sucesso![/bold green]")
        
        return imagens_geradas
    
    def _preparar_prompt_consistente(self, cena: SceneBlock) -> str:
        """
        Prepara prompt com consistência de personagem + estilo do canal.
        
        Args:
            cena: Bloco de cena validado (Pydantic)
            
        Returns:
            Prompt otimizado e consistente
        """
        # 1. Injeta consistência de personagem (CharacterManager)
        prompt_base = self.character_manager.inject_consistency(
            prompt=cena.visual_prompt,
            character_name=cena.speaker
        )
        
        # 2. Adiciona estilo do canal (pode vir do config)
        estilo_canal = self.config.get(
            "visual_style",
            "cinematic lighting, 4k quality, dramatic composition, realistic style"
        )
        
        prompt_final = f"{prompt_base}, {estilo_canal}"
        
        return prompt_final


# Compatibilidade com código antigo
Agente06Visual = Agente07Visual
