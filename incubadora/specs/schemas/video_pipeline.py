"""
Schemas Pydantic para validação de contratos entre agentes.

Resolve violação ISP (Interface Segregation Principle) identificada na auditoria.
Define contratos formais para comunicação entre T5→T11.
"""

from pydantic import BaseModel, Field, validator, root_validator
from typing import Optional, Literal
from pathlib import Path


# ========== SCENE & SCRIPT SCHEMAS ==========

class SceneBlock(BaseModel):
    """
    Contrato de uma cena individual do vídeo.
    Usado por: T6 (Roteirista) → T7 (Visual) → T8 (Narrador)
    """
    speaker: str = Field(
        ..., 
        description="Nome do personagem que fala (ex: 'Jesus', 'Narrador')",
        min_length=1
    )
    dialogue: str = Field(
        ..., 
        description="Texto da fala do personagem",
        min_length=10,
        max_length=500
    )
    visual_prompt: str = Field(
        ...,
        description="Descrição da cena visual para geração de imagem",
        min_length=20
    )
    duration_seconds: float = Field(
        ...,
        ge=3.0,
        le=15.0,
        description="Duração estimada da cena em segundos"
    )
    emotion: Literal["alegria", "tristeza", "raiva", "medo", "surpresa", "neutro"] = Field(
        default="neutro",
        description="Emoção dominante da cena"
    )
    
    class Config:
        # Permite validação mais estrita
        extra = "forbid"  # Não aceita campos extras


class VideoScript(BaseModel):
    """
    Contrato do roteiro completo de um vídeo.
    Output de: T6 (Roteirista)
    Input para: T7, T8, T9
    """
    title: str = Field(
        ...,
        description="Título do vídeo",
        min_length=5,
        max_length=100
    )
    target_duration: int = Field(
        default=60,
        ge=30,
        le=90,
        description="Duração alvo do vídeo em segundos"
    )
    dominant_emotion: str = Field(
        ...,
        description="Emoção central do vídeo (herdada de T4)"
    )
    template_used: str = Field(
        default="react",
        description="Template usado (react, news, drama, pixar)"
    )
    scenes: list[SceneBlock] = Field(
        ...,
        min_items=4,
        max_items=10,
        description="Lista de blocos/cenas do vídeo"
    )
    
    @validator('scenes')
    def validate_total_duration(cls, scenes, values):
        """Garante que duração total não excede 120% do alvo"""
        total_duration = sum(s.duration_seconds for s in scenes)
        target = values.get('target_duration', 60)
        max_allowed = target * 1.2  # 20% de margem
        
        if total_duration > max_allowed:
            raise ValueError(
                f"Duração total ({total_duration:.1f}s) excede limite de {max_allowed:.1f}s "
                f"(120% de {target}s). Reduza o número de cenas ou suas durações."
            )
        
        return scenes
    
    @validator('scenes')
    def validate_speaker_consistency(cls, scenes):
        """Avisa se houver muitos speakers diferentes (pode indicar erro)"""
        speakers = {s.speaker for s in scenes}
        if len(speakers) > 5:
            # Não bloqueia, mas loga warning
            import logging
            logging.warning(
                f"Roteiro tem {len(speakers)} personagens diferentes. "
                f"Verifique se todos são necessários: {speakers}"
            )
        return scenes
    
    class Config:
        extra = "forbid"


# ========== CHARACTER SCHEMAS ==========

class CharacterProfile(BaseModel):
    """
    Perfil de um personagem para consistência visual.
    Usado por: CharacterManager
    """
    name: str = Field(
        ...,
        description="Nome único do personagem",
        min_length=1
    )
    description: str = Field(
        ...,
        description="Descrição física fixa do personagem para prompts",
        min_length=50,
        max_length=500
    )
    reference_image: Optional[Path] = Field(
        default=None,
        description="Caminho para imagem de referência (primeira aparição)"
    )
    style_keywords: list[str] = Field(
        default_factory=list,
        description="Palavras-chave de estilo (ex: ['cinematic', '4k', 'dramatic lighting'])"
    )
    appearance_count: int = Field(
        default=0,
        ge=0,
        description="Número de vezes que o personagem apareceu (tracking)"
    )
    
    class Config:
        extra = "allow"  # Permite campos customizados por canal


class ChannelCharacters(BaseModel):
    """Coleção de personagens de um canal"""
    canal_id: str
    personagens: dict[str, CharacterProfile] = Field(
        default_factory=dict,
        description="Mapeamento nome → perfil"
    )
    
    def get_character(self, name: str) -> Optional[CharacterProfile]:
        """Busca personagem (case-insensitive)"""
        return self.personagens.get(name.lower())
    
    def add_character(self, profile: CharacterProfile):
        """Adiciona ou atualiza personagem"""
        self.personagens[profile.name.lower()] = profile


# ========== AUDIO SCHEMAS ==========

class AudioConfig(BaseModel):
    """
    Configuração de TTS para um canal ou cena.
    Usado por: T8 (Narrador)
    """
    provider: Literal["google_cloud", "chirp", "elevenlabs"] = Field(
        default="google_cloud",
        description="Provider primário de TTS"
    )
    fallback: list[str] = Field(
        default_factory=lambda: ["google_cloud"],
        description="Chain de fallback em caso de falha"
    )
    voice_id: str = Field(
        default="pt-BR-Neural2-B",
        description="ID da voz no provider (ex: pt-BR-Neural2-B, pt-BR-Wavenet-A)"
    )
    speed: float = Field(
        default=1.0,
        ge=0.5,
        le=2.0,
        description="Velocidade da fala (1.0 = normal)"
    )
    pitch: float = Field(
        default=0.0,
        ge=-20.0,
        le=20.0,
        description="Tom da voz em semitons"
    )
    
    @root_validator
    def validate_fallback_chain(cls, values):
        """Garante que fallback não inclui o provider primário"""
        provider = values.get('provider')
        fallback = values.get('fallback', [])
        
        if provider in fallback:
            # Remove duplicatas
            values['fallback'] = [f for f in fallback if f != provider]
        
        return values
    
    class Config:
        extra = "forbid"


class VoiceMapping(BaseModel):
    """Mapeamento de personagens para vozes específicas"""
    character_name: str
    audio_config: AudioConfig
    
    class Config:
        extra = "forbid"


# ========== IMAGE GENERATION SCHEMAS ==========

class ImageGenerationConfig(BaseModel):
    """
    Configuração para geração de imagens.
    Usado por: T7 (Visual)
    """
    model: Literal["imagen-4-standard", "imagen-4-ultra"] = Field(
        default="imagen-4-standard",
        description="Modelo Imagen a usar"
    )
    aspect_ratio: Literal["16:9", "9:16", "1:1", "4:3"] = Field(
        default="16:9",
        description="Proporção da imagem"
    )
    quality: Literal["standard", "hd", "ultra"] = Field(
        default="hd",
        description="Qualidade da imagem"
    )
    use_character_reference: bool = Field(
        default=True,
        description="Se deve usar imagem de referência para consistência"
    )
    safety_filter: bool = Field(
        default=True,
        description="Se deve aplicar filtros de segurança"
    )
    
    class Config:
        extra = "forbid"


# ========== UTILITY FUNCTIONS ==========

def validate_roteiro_json(data: dict) -> VideoScript:
    """
    Helper para validar JSON de roteiro.
    Uso: roteiro = validate_roteiro_json(json.loads(llm_output))
    """
    return VideoScript.model_validate(data)


def validate_cena_json(data: dict) -> SceneBlock:
    """
    Helper para validar JSON de cena individual.
    """
    return SceneBlock.model_validate(data)


if __name__ == "__main__":
    # Testes básicos
    print("✅ Schemas Pydantic carregados com sucesso!")
    
    # Teste de cena válida
    cena = SceneBlock(
        speaker="Jesus",
        dialogue="Bem-aventurados os que têm fome de justiça, pois serão saciados.",
        visual_prompt="Jesus moderno, 30 anos, barba castanha, túnica branca, fundo urban noturno, dramatic lighting",
        duration_seconds=8.5,
        emotion="alegria"
    )
    print(f"✅ Cena válida: {cena.speaker} ({cena.duration_seconds}s)")
    
    # Teste de roteiro válido
    roteiro = VideoScript(
        title="O Sermão da Montanha Hoje",
        target_duration=60,
        dominant_emotion="esperança",
        scenes=[cena] * 6  # 6 cenas idênticas = 51s
    )
    print(f"✅ Roteiro válido: {roteiro.title} ({len(roteiro.scenes)} cenas)")
    
    # Teste de validação (deve falhar)
    try:
        cena_invalida = SceneBlock(
            speaker="",  # ❌ Nome vazio
            dialogue="oi",  # ❌ Muito curto
            visual_prompt="x",  # ❌ Muito curto
            duration_seconds=20  # ❌ Excede 15s
        )
    except Exception as e:
        print(f"✅ Validação funcionou: {type(e).__name__}")
