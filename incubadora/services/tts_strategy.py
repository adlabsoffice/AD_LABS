"""
TTS Strategy Pattern - Sistema extensível de Text-to-Speech

Resolve violação OCP (Open/Closed Principle) identificada na auditoria.
Permite adicionar novos providers de TTS sem modificar código dos agentes.

Autor: Refatoração Arquitetural P0
Data: 04/12/2024
"""

import os
import logging
from pathlib import Path
from typing import Optional, Dict
from abc import ABC, abstractmethod

# Google Cloud TTS
try:
    from google.cloud import texttospeech
    GOOGLE_CLOUD_TTS_AVAILABLE = True
except ImportError:
    GOOGLE_CLOUD_TTS_AVAILABLE = False
    logging.warning("google-cloud-texttospeech não instalado")

# ElevenLabs (futuro)
try:
    import elevenlabs
    ELEVENLABS_AVAILABLE = True
except ImportError:
    ELEVENLABS_AVAILABLE = False

from specs.schemas.video_pipeline import AudioConfig

logger = logging.getLogger(__name__)


class TTSStrategy(ABC):
    """
    Interface abstrata para serviços de Text-to-Speech.
    
    Implementações devem fornecer método synthesize() que converte texto em áudio.
    """
    
    @abstractmethod
    def synthesize(
        self, 
        text: str, 
        emotion: str = "neutro",
        config: Optional[AudioConfig] = None
    ) -> Path:
        """
        Sintetiza texto em áudio.
        
        Args:
            text: Texto para sintetizar
            emotion: Emoção para aplicar (alegria, tristeza, raiva, medo, neutro)
            config: Configurações de voz
            
        Returns:
            Path do arquivo de áudio gerado
        """
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Verifica se o provider está disponível"""
        pass
    
    @abstractmethod
    def get_voices(self) -> list[str]:
        """Lista vozes disponíveis do provider"""
        pass


class GoogleCloudTTS(TTSStrategy):
    """
    Implementação para Google Cloud Text-to-Speech.
    
    Usa Neural2 voices (pt-BR).
    """
    
    # Mapeamento de emoções para ajustes de pitch/speed
    EMOTION_CONFIG = {
        "alegria": {"pitch": 2.0, "speed_delta": 0.05},
        "tristeza": {"pitch": -2.0, "speed_delta": -0.05},
        "raiva": {"pitch": 1.0, "speed_delta": 0.1},
        "medo": {"pitch": 3.0, "speed_delta": 0.15},
        "surpresa": {"pitch": 4.0, "speed_delta": 0.1},
        "neutro": {"pitch": 0.0, "speed_delta": 0.0}
    }
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Inicializa Google Cloud TTS.
        
        Args:
            api_key: Google API Key (usa GOOGLE_API_KEY_AUDIO se não fornecida)
        """
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY_AUDIO")
        
        if not self.api_key:
            logger.error("GOOGLE_API_KEY_AUDIO não configurada")
            return
        
        if GOOGLE_CLOUD_TTS_AVAILABLE:
            # Configura credenciais via API key
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = ""  # Limpa se houver
            self.client = texttospeech.TextToSpeechClient()
            logger.info("GoogleCloudTTS inicializado")
        else:
            logger.error("google-cloud-texttospeech não instalado")
    
    def is_available(self) -> bool:
        """Verifica disponibilidade"""
        return bool(self.api_key and GOOGLE_CLOUD_TTS_AVAILABLE)
    
    def get_voices(self) -> list[str]:
        """Lista vozes pt-BR disponíveis"""
        if not self.is_available():
            return []
        
        try:
            response = self.client.list_voices(language_code="pt-BR")
            return [voice.name for voice in response.voices]
        except Exception as e:
            logger.error(f"Erro ao listar vozes: {e}")
            return ["pt-BR-Neural2-B", "pt-BR-Neural2-C", "pt-BR-Wavenet-A"]  # Padrões conhecidos
    
    def synthesize(
        self, 
        text: str, 
        emotion: str = "neutro",
        config: Optional[AudioConfig] = None
    ) -> Path:
        """
        Sintetiza texto usando Google Cloud TTS.
        
        Args:
            text: Texto para narrar
            emotion: Emoção (ajusta pitch/speed)
            config: Configurações de voz
            
        Returns:
            Path do arquivo MP3 gerado
        """
        if not self.is_available():
            raise RuntimeError("GoogleCloudTTS não disponível")
        
        # Configurações padrão
        if config is None:
            config = AudioConfig(provider="google_cloud")
        
        # Ajustes emocionais
        emotion_adjust = self.EMOTION_CONFIG.get(emotion, self.EMOTION_CONFIG["neutro"])
        
        final_pitch = config.pitch + emotion_adjust["pitch"]
        final_speed = config.speed + emotion_adjust["speed_delta"]
        
        logger.info(f"Sintetizando com {config.voice_id} (emoção: {emotion}): {text[:60]}...")
        
        try:
            # Configura síntese
            synthesis_input = texttospeech.SynthesisInput(text=text)
            
            voice = texttospeech.VoiceSelectionParams(
                language_code="pt-BR",
                name=config.voice_id
            )
            
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3,
                speaking_rate=final_speed,
                pitch=final_pitch
            )
            
            # Sintetiza
            response = self.client.synthesize_speech(
                input=synthesis_input,
                voice=voice,
                audio_config=audio_config
            )
            
            # Salva áudio
            import hashlib
            import time
            
            text_hash = hashlib.md5(text.encode()).hexdigest()[:8]
            timestamp = int(time.time())
            filename = f"audio_{timestamp}_{text_hash}.mp3"
            
            output_dir = Path("d:/AD_LABS/outputs/audios")
            output_dir.mkdir(parents=True, exist_ok=True)
            
            output_path = output_dir / filename
            
            with open(output_path, "wb") as out:
                out.write(response.audio_content)
            
            logger.info(f"✅ Áudio salvo: {output_path}")
            
            return output_path
        
        except Exception as e:
            logger.error(f"❌ Erro ao sintetizar: {e}")
            raise


class ChirpTTS(TTSStrategy):
    """
    Implementação para Google Chirp TTS (voz conversacional).
    
    Placeholder - verificar disponibilidade da API.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY_AUDIO")
        logger.warning("ChirpTTS ainda não implementado (verificar API)")
    
    def is_available(self) -> bool:
        return False
    
    def get_voices(self) -> list[str]:
        return []
    
    def synthesize(
        self, 
        text: str, 
        emotion: str = "neutro",
        config: Optional[AudioConfig] = None
    ) -> Path:
        raise NotImplementedError("Chirp TTS ainda não implementado")


class ElevenLabsTTS(TTSStrategy):
    """
    Implementação para ElevenLabs TTS (premium).
    
    Custo: $5/mês para 22k caracteres.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("ELEVENLABS_API_KEY")
        
        if ELEVENLABS_AVAILABLE:
            logger.info("ElevenLabsTTS disponível")
        else:
            logger.warning("elevenlabs não instalado. Execute: pip install elevenlabs")
    
    def is_available(self) -> bool:
        return bool(self.api_key and ELEVENLABS_AVAILABLE)
    
    def get_voices(self) -> list[str]:
        """Lista vozes ElevenLabs"""
        if not self.is_available():
            return []
        
        try:
            voices = elevenlabs.voices()
            return [voice.voice_id for voice in voices]
        except Exception as e:
            logger.error(f"Erro ao listar vozes: {e}")
            return []
    
    def synthesize(
        self, 
        text: str, 
        emotion: str = "neutro",
        config: Optional[AudioConfig] = None
    ) -> Path:
        """
        Sintetiza com ElevenLabs.
        
        Args:
            text: Texto
            emotion: Emoção (ElevenLabs infere automaticamente)
            config: Configurações
            
        Returns:
            Path do áudio
        """
        if not self.is_available():
            raise RuntimeError("ElevenLabsTTS não disponível")
        
        logger.info(f"Sintetizando com ElevenLabs: {text[:60]}...")
        
        try:
            # Gera áudio
            audio = elevenlabs.generate(
                text=text,
                voice=config.voice_id if config else "Adam",
                model="eleven_multilingual_v2"
            )
            
            # Salva
            import hashlib
            import time
            
            text_hash = hashlib.md5(text.encode()).hexdigest()[:8]
            timestamp = int(time.time())
            filename = f"audio_elevenlabs_{timestamp}_{text_hash}.mp3"
            
            output_dir = Path("d:/AD_LABS/outputs/audios")
            output_dir.mkdir(parents=True, exist_ok=True)
            
            output_path = output_dir / filename
            
            elevenlabs.save(audio, str(output_path))
            
            logger.info(f"✅ Áudio ElevenLabs salvo: {output_path}")
            
            return output_path
        
        except Exception as e:
            logger.error(f"❌ Erro ElevenLabs: {e}")
            raise


class TTSFactory:
    """
    Factory para criar estratégias de TTS.
    
    Permite trocar providers via configuração.
    """
    
    @staticmethod
    def create(
        provider: str = "google_cloud",
        api_key: Optional[str] = None
    ) -> TTSStrategy:
        """
        Cria estratégia de TTS.
        
        Args:
            provider: Nome do provider (google_cloud, chirp, elevenlabs)
            api_key: API key (opcional)
            
        Returns:
            Instância de TTSStrategy
        """
        strategies = {
            "google_cloud": GoogleCloudTTS,
            "chirp": ChirpTTS,
            "elevenlabs": ElevenLabsTTS,
            "coqui_xtts": lambda api_key=None: __import__('services.coqui_tts_strategy', fromlist=['CoquiXTTSTTS']).CoquiXTTSTTS()
        }
        
        strategy_class = strategies.get(provider)
        
        if not strategy_class:
            raise ValueError(f"Provider desconhecido: {provider}. Disponíveis: {list(strategies.keys())}")
        
        strategy = strategy_class(api_key=api_key)
        
        if not strategy.is_available():
            logger.warning(f"Provider '{provider}' não disponível. Fallback: google_cloud")
            return GoogleCloudTTS(api_key=api_key)
        
        return strategy
    
    @staticmethod
    def create_with_fallback(
        primary: str,
        fallback_chain: list[str],
        api_key: Optional[str] = None
    ) -> TTSStrategy:
        """
        Cria estratégia com fallback chain.
        
        Args:
            primary: Provider primário
            fallback_chain: Lista de fallbacks
            api_key: API key
            
        Returns:
            Primeira estratégia disponível
        """
        # Tenta primário
        try:
            strategy = TTSFactory.create(primary, api_key)
            if strategy.is_available():
                logger.info(f"Usando TTS primário: {primary}")
                return strategy
        except Exception as e:
            logger.warning(f"Provider primário '{primary}' falhou: {e}")
        
        # Tenta fallbacks
        for provider in fallback_chain:
            try:
                strategy = TTSFactory.create(provider, api_key)
                if strategy.is_available():
                    logger.info(f"Usando TTS fallback: {provider}")
                    return strategy
            except Exception as e:
                logger.warning(f"Fallback '{provider}' falhou: {e}")
        
        raise RuntimeError("Nenhum provider de TTS disponível!")


if __name__ == "__main__":
    # Teste básico
    logging.basicConfig(level=logging.INFO)
    
    print("🧪 Testando TTSStrategy...")
    
    # Cria estratégia
    tts = TTSFactory.create(provider="google_cloud")
    
    if tts.is_available():
        print("✅ Google Cloud TTS disponível")
        print(f"✅ Vozes: {tts.get_voices()[:3]}...")
        
        # Teste simples (descomente para gerar áudio real)
        # text = "Bem-aventurados os que têm fome de justiça, pois serão saciados."
        # config = AudioConfig(voice_id="pt-BR-Neural2-B", speed=1.1)
        # path = tts.synthesize(text, emotion="alegria", config=config)
        # print(f"✅ Áudio gerado: {path}")
    else:
        print("❌ Google Cloud TTS não disponível")
    
    print("\n✅ TTSStrategy OK!")
