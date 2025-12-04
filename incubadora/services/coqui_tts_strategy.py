"""
Coqui XTTS Strategy - Calls remote Coqui XTTS API
"""

import logging
import requests
from pathlib import Path
from typing import Optional
import hashlib
import time

from specs.schemas.video_pipeline import AudioConfig

logger = logging.getLogger(__name__)


class CoquiXTTSTTS:
    """
    Implementação para Coqui XTTS v2 via API remota.
    
    Requer:
        - COQUI_XTTS_URL configurado no .env (ex: https://coqui-xtts-abc.run.app)
        - Referência de voz (upload opcional)
    """
    
    def __init__(self, api_url: Optional[str] = None, reference_voice_path: Optional[str] = None):
        """
        Inicializa Coqui XTTS strategy.
        
        Args:
            api_url: URL da API do Coqui XTTS (ex: https://coqui-xtts.run.app)
            reference_voice_path: Caminho para arquivo de referência de voz (opcional)
        """
        import os
        self.api_url = api_url or os.getenv("COQUI_XTTS_URL")
       
        self.reference_voice_path = reference_voice_path
        
        if self.api_url:
            logger.info(f"CoquiXTTSTTS configurado para: {self.api_url}")
        else:
            logger.warning("COQUI_XTTS_URL não configurado. Coqui XTTS não disponível.")
    
    def is_available(self) -> bool:
        """Verifica se a API está respondendo."""
        if not self.api_url:
            return False
        
        try:
            response = requests.get(f"{self.api_url}/health", timeout=5)
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Coqui XTTS não disponível: {e}")
            return False
    
    def get_voices(self) -> list[str]:
        """Lista vozes disponíveis (uploaded references)."""
        if not self.is_available():
            return []
        
        try:
            response = requests.get(f"{self.api_url}/voices", timeout=5)
            if response.status_code == 200:
                return response.json().get("voices", [])
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
        Sintetiza texto usando Coqui XTTS.
        
        Args:
            text: Texto para sintetizar
            emotion: Emoção (não afeta Coqui, apenas para consistência)
            config: Configurações (não usado no Coqui)
            
        Returns:
            Path do arquivo WAV gerado
        """
        if not self.is_available():
            raise RuntimeError("Coqui XTTS não disponível")
        
        logger.info(f"Sintetizando com Coqui XTTS: {text[:60]}...")
        
        try:
            # Prepara request
            files = {}
            data = {
                "text": text,
                "language": "pt"  # Português
            }
            
            # Adiciona referência de voz se existir
            if self.reference_voice_path and Path(self.reference_voice_path).exists():
                with open(self.reference_voice_path, "rb") as f:
                    files["speaker_wav_file"] = f
                    
                    # Faz request com arquivo
                    response = requests.post(
                        f"{self.api_url}/tts",
                        data=data,
                        files=files,
                        timeout=60
                    )
            else:
                # Sem referência de voz
                response = requests.post(
                    f"{self.api_url}/tts",
                    data=data,
                    timeout=60
                )
            
            response.raise_for_status()
            
            # Salva áudio
            text_hash = hashlib.md5(text.encode()).hexdigest()[:8]
            timestamp = int(time.time())
            filename = f"audio_coqui_{timestamp}_{text_hash}.wav"
            
            output_dir = Path("d:/AD_LABS/outputs/audios")
            output_dir.mkdir(parents=True, exist_ok=True)
            
            output_path = output_dir / filename
            
            with open(output_path, "wb") as f:
                f.write(response.content)
            
            logger.info(f"✅ Áudio Coqui salvo: {output_path}")
            
            return output_path
        
        except Exception as e:
            logger.error(f"❌ Erro Coqui XTTS: {e}")
            raise
