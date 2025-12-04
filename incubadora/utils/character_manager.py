"""
Character Manager - Gerenciador de Consistência de Personagens

Resolve violação SRP (Single Responsibility Principle) identificada na auditoria.
Separa lógica de consistência visual da geração de imagens.

Autor: Refatoração Arquitetural P0
Data: 04/12/2024
"""

import json
import logging
from pathlib import Path
from typing import Optional, Dict
from specs.schemas.video_pipeline import CharacterProfile, ChannelCharacters

logger = logging.getLogger(__name__)


class CharacterManager:
    """
    Gerencia personagens de um canal para garantir consistência visual.
    
    Responsabilidades:
    1. Carregar perfis de personagens do config do canal
    2. Injetar descrições fixas nos prompts visuais
    3. Salvar e gerenciar imagens de referência
    4. Tracking de aparições de personagens
    
    Uso:
        manager = CharacterManager(canal_id="o_livro_caixa_divino")
        prompt = manager.inject_consistency("Jesus sentado", "Jesus")
        manager.save_reference("Jesus", "path/to/image.png")
    """
    
    def __init__(self, canal_id: str, config_path: Optional[Path] = None):
        """
        Inicializa o gerenciador de personagens.
        
        Args:
            canal_id: ID do canal (ex: "o_livro_caixa_divino")
            config_path: Caminho customizado para o config (opcional)
        """
        self.canal_id = canal_id
        self.config_path = config_path or Path(f"d:/AD_LABS/incubadora/config/{canal_id}/personagens.json")
        self.characters = self._load_characters()
        
        logger.info(f"CharacterManager inicializado para canal '{canal_id}' com {len(self.characters.personagens)} personagens")
    
    def _load_characters(self) -> ChannelCharacters:
        """
        Carrega perfis de personagens do arquivo JSON.
        
        Returns:
            ChannelCharacters com personagens carregados
        """
        if not self.config_path.exists():
            logger.warning(f"Arquivo de personagens não encontrado: {self.config_path}")
            logger.info("Criando configuração padrão de personagens")
            return self._create_default_characters()
        
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Converte para Pydantic model
            return ChannelCharacters.model_validate(data)
        
        except Exception as e:
            logger.error(f"Erro ao carregar personagens: {e}")
            return self._create_default_characters()
    
    def _create_default_characters(self) -> ChannelCharacters:
        """
        Cria perfis padrão para o canal O Livro Caixa Divino.
        
        Returns:
            ChannelCharacters com personagens padrão
        """
        default_personagens = {
            "jesus": CharacterProfile(
                name="Jesus",
                description=(
                    "Homem de 30 anos, pele morena clara, cabelos castanhos ondulados até os ombros, "
                    "barba castanha bem cuidada, olhos castanhos profundos e expressivos, "
                    "túnica branca simples com cinto de corda, sandálias de couro, "
                    "expressão serena e compassiva, postura confiante mas acessível"
                ),
                style_keywords=[
                    "cinematic lighting",
                    "4k quality",
                    "dramatic composition",
                    "realistic style",
                    "warm color grading"
                ]
            ),
            "narrador": CharacterProfile(
                name="Narrador",
                description=(
                    "Voz neutra e confiável, sem representação visual. "
                    "Usado para contexto narrativo e transições."
                ),
                style_keywords=[]
            )
        }
        
        characters = ChannelCharacters(
            canal_id=self.canal_id,
            personagens=default_personagens
        )
        
        # Salva configuração padrão
        self.save_characters(characters)
        
        return characters
    
    def get_character(self, name: str) -> Optional[CharacterProfile]:
        """
        Busca perfil de um personagem (case-insensitive).
        
        Args:
            name: Nome do personagem
            
        Returns:
            CharacterProfile ou None se não encontrado
        """
        profile = self.characters.get_character(name)
        
        if not profile:
            logger.warning(f"Personagem '{name}' não encontrado. Personagens disponíveis: {list(self.characters.personagens.keys())}")
        
        return profile
    
    def inject_consistency(self, prompt: str, character_name: str) -> str:
        """
        Injeta descrição fixa do personagem no prompt visual.
        
        Args:
            prompt: Prompt original da cena (ex: "Jesus sentado em uma mesa")
            character_name: Nome do personagem (ex: "Jesus")
            
        Returns:
            Prompt expandido com descrição fixa do personagem
            
        Example:
            >>> manager.inject_consistency("Jesus pregando", "Jesus")
            "Homem de 30 anos, pele morena clara, barba castanha..., Jesus pregando, cinematic lighting, 4k quality..."
        """
        profile = self.get_character(character_name)
        
        if not profile:
            logger.warning(f"Personagem '{character_name}' não encontrado. Usando prompt original.")
            return prompt
        
        # Incrementa contador de aparições
        profile.appearance_count += 1
        
        # Monta prompt consistente
        consistent_prompt = f"{profile.description}, {prompt}"
        
        # Adiciona keywords de estilo
        if profile.style_keywords:
            style_suffix = ", ".join(profile.style_keywords)
            consistent_prompt = f"{consistent_prompt}, {style_suffix}"
        
        logger.debug(f"Prompt expandido para '{character_name}' (aparição #{profile.appearance_count}): {consistent_prompt[:100]}...")
        
        return consistent_prompt
    
    def save_reference(self, character_name: str, image_path: str) -> bool:
        """
        Salva caminho da imagem de referência para um personagem.
        
        Deve ser chamado após gerar a PRIMEIRA imagem do personagem.
        
        Args:
            character_name: Nome do personagem
            image_path: Caminho da imagem de referência
            
        Returns:
            True se salvou com sucesso, False caso contrário
        """
        profile = self.get_character(character_name)
        
        if not profile:
            logger.error(f"Não foi possível salvar referência: personagem '{character_name}' não encontrado")
            return False
        
        # Valida que o arquivo existe
        if not Path(image_path).exists():
            logger.error(f"Arquivo de imagem não encontrado: {image_path}")
            return False
        
        # Salva referência
        profile.reference_image = Path(image_path)
        logger.info(f"Imagem de referência salva para '{character_name}': {image_path}")
        
        # Persiste no arquivo JSON
        self.save_characters(self.characters)
        
        return True
    
    def get_reference_image(self, character_name: str) -> Optional[Path]:
        """
        Obtém caminho da imagem de referência de um personagem.
        
        Args:
            character_name: Nome do personagem
            
        Returns:
            Path da imagem ou None se não houver referência
        """
        profile = self.get_character(character_name)
        
        if not profile or not profile.reference_image:
            return None
        
        return profile.reference_image
    
    def add_character(self, profile: CharacterProfile) -> bool:
        """
        Adiciona ou atualiza um personagem.
        
        Args:
            profile: Perfil do personagem
            
        Returns:
            True se adicionou com sucesso
        """
        self.characters.add_character(profile)
        self.save_characters(self.characters)
        
        logger.info(f"Personagem '{profile.name}' adicionado/atualizado")
        return True
    
    def save_characters(self, characters: ChannelCharacters):
        """
        Persiste personagens no arquivo JSON.
        
        Args:
            characters: ChannelCharacters para salvar
        """
        # Cria diretório se não existir
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Serializa para JSON
        data = characters.model_dump(mode='json')
        
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        logger.debug(f"Personagens salvos em {self.config_path}")
    
    def list_characters(self) -> list[str]:
        """
        Lista nomes de todos os personagens disponíveis.
        
        Returns:
            Lista de nomes de personagens
        """
        return list(self.characters.personagens.keys())
    
    def get_appearance_count(self, character_name: str) -> int:
        """
        Retorna quantas vezes um personagem apareceu.
        
        Args:
            character_name: Nome do personagem
            
        Returns:
            Número de aparições
        """
        profile = self.get_character(character_name)
        return profile.appearance_count if profile else 0


if __name__ == "__main__":
    # Teste básico
    logging.basicConfig(level=logging.DEBUG)
    
    print("🧪 Testando CharacterManager...")
    
    # Inicializa
    manager = CharacterManager(canal_id="o_livro_caixa_divino")
    
    # Lista personagens
    print(f"\n✅ Personagens disponíveis: {manager.list_characters()}")
    
    # Testa injeção de consistência
    prompt_original = "Jesus pregando para multidão, fundo urban noturno"
    prompt_consistente = manager.inject_consistency(prompt_original, "Jesus")
    print(f"\n✅ Prompt original: {prompt_original}")
    print(f"✅ Prompt consistente: {prompt_consistente[:150]}...")
    
    # Testa aparições
    manager.inject_consistency("Jesus sentado", "Jesus")
    manager.inject_consistency("Jesus caminhando", "Jesus")
    print(f"\n✅ Aparições de Jesus: {manager.get_appearance_count('Jesus')}")
    
    print("\n✅ CharacterManager funcionando corretamente!")
