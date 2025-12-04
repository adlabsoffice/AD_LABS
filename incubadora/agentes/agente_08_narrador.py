"""
Agente 08 - Narrador

REFATORADO: 04/12/2024
- Strategy Pattern para TTS (OCP)
- Injeção de dependências (DIP)
- Validação com Pydantic schemas (ISP)
- Suporte a múltiplos speakers

Resolver problemas identificados na auditoria:
1. Voz hardcoded (não extensível)
2. Qualidade de áudio insatisfatória  
3. Falta de suporte a múltiplas vozes/personagens
"""

import os
import json
import time
import logging
from pathlib import Path
from typing import Optional, Dict, List
from rich.console import Console

# Imports de serviços (DIP)
from services.tts_strategy import TTSFactory, TTSStrategy
from specs.schemas.video_pipeline import VideoScript, SceneBlock, AudioConfig

console = Console()
logger = logging.getLogger(__name__)


class Agente08Narrador:
    """
    Narrador - Gera áudios a partir do roteiro com TTS extensível.
    
    Responsabilidades (SRP):
    - Orquestrar geração de áudio
    - Validar ritmo/duração (WPM)
    - Gerenciar múltiplos speakers
    
    NÃO é responsável por:
    - Síntese de voz direta (TTSStrategy)
    - Escolha de provider (TTSFactory)
    """
    
    # Limites ótimos de WPM (palavras por minuto)
    TARGET_WPM_MIN = 168
    TARGET_WPM_MAX = 187
    
    def __init__(
        self,
        canal_id: str,
        tts_strategy: Optional[TTSStrategy] = None,
        fallback_chain: Optional[List[str]] = None,
        config: Optional[Dict] = None
    ):
        """
        Inicializa Agente Narrador com injeção de dependências.
        
        Args:
            canal_id: ID do canal
            tts_strategy: Estratégia de TTS (cria automaticamente se None)
            fallback_chain: Chain de fallback para TTS
            config: Configurações customizadas
        """
        self.canal_id = canal_id
        self.config = config or {}
        
        # Injeção de dependências (DIP)
        if tts_strategy:
            self.tts = tts_strategy
        else:
            # Cria com fallback chain
            primary_provider = self.config.get("tts_provider", "google_cloud")
            fallback = fallback_chain or self.config.get("tts_fallback", ["google_cloud"])
            
            self.tts = TTSFactory.create_with_fallback(
                primary=primary_provider,
                fallback_chain=fallback
            )
        
        # Configuração de áudio padrão
        self.audio_config = AudioConfig(
            provider=self.config.get("tts_provider", "google_cloud"),
            voice_id=self.config.get("voice_id", "pt-BR-Neural2-B"),
            speed=self.config.get("speed", 1.15),
            pitch=self.config.get("pitch", 0.0)
        )
        
        self.output_dir = Path("d:/AD_LABS/outputs/audios")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Agente08Narrador inicializado para canal '{canal_id}' com TTS '{self.audio_config.provider}'")
    
    def gerar_narracao(self, roteiro_data: Dict) -> Dict:
        """
        Gera áudios para cada cena do roteiro com TTS extensível.
        
        Args:
            roteiro_data: Dicionário com dados do roteiro (será validado)
            
        Returns:
            Dict com faixas de áudio e metadados
        """
        console.print(f"[bold yellow]AGENTE 08: Iniciando Narração ({self.audio_config.provider.upper()})...[/bold yellow]")
        
        # Valida roteiro com Pydantic
        try:
            roteiro = VideoScript.model_validate(roteiro_data)
            console.print(f"   ✅ Roteiro validado: {len(roteiro.scenes)} cenas")
        except Exception as e:
            logger.error(f"Erro de validação no roteiro: {e}")
            raise ValueError(f"Roteiro inválido: {e}")
        
        faixas = []
        
        # Processa cada cena
        for i, cena in enumerate(roteiro.scenes):
            console.print(f"\n   [cyan]Cena {i+1}/{len(roteiro.scenes)}:[/cyan] {cena.speaker}")
            console.print(f"      Fala: \"{cena.dialogue[:60]}...\"")
            console.print(f"      Emoção: {cena.emotion}")
            
            try:
                # Gera áudio usando estratégia injetada
                audio_file = self.tts.synthesize(
                    text=cena.dialogue,
                    emotion=cena.emotion,
                    config=self.audio_config
                )
                
                # Obtém duração do arquivo
                duration_sec = self._get_audio_duration(audio_file)
                
                # Valida ritmo (WPM)
                wpm = self._calcular_wpm(cena.dialogue, duration_sec)
                status_ritmo = self._validar_ritmo(wpm)
                
                console.print(f"      ✅ [green]Áudio gerado:[/green] {audio_file.name} ({duration_sec:.1f}s)")
                console.print(f"      📊 Ritmo: {wpm:.0f} WPM - {status_ritmo}")
                
                faixas.append({
                    "cena_id": i,
                    "speaker": cena.speaker,
                    "arquivo": str(audio_file),
                    "duracao": duration_sec,
                    "wpm": wpm,
                    "status_ritmo": status_ritmo,
                    "duracao_alvo": cena.duration_seconds
                })
                
                # Valida diferença entre duração real e alvo
                diff = abs(duration_sec - cena.duration_seconds)
                if diff > 2.0:
                    console.print(f"      ⚠️ [yellow]Diferença de duração:[/yellow] {diff:.1f}s (alvo: {cena.duration_seconds}s)")
                
            except Exception as e:
                logger.error(f"Erro ao gerar áudio da cena {i+1}: {e}")
                console.print(f"      ❌ [bold red]ERRO FATAL:[/bold red] {e}")
                raise RuntimeError(
                    f"Falha na narração da cena {i+1}.\n"
                    f"Speaker: {cena.speaker}\n"
                    f"Texto: {cena.dialogue}\n"
                    f"Erro: {e}"
                )
            
            # Rate limit friendly
            time.sleep(0.5)
        
        console.print(f"\n   ✅ [bold green]{len(faixas)} faixas de áudio geradas![/bold green]")
        
        # Retorna formato compatível com agentes downstream
        return {
            "faixas": faixas,
            "duracao_total": sum(f["duracao"] for f in faixas),
            "provider_usado": self.audio_config.provider
        }
    
    def _get_audio_duration(self, audio_path: Path) -> float:
        """
        Obtém duração real de um arquivo de áudio.
        
        Args:
            audio_path: Caminho do arquivo MP3
            
        Returns:
            Duração em segundos
        """
        try:
            # Tenta usar moviepy (já é dependência do projeto)
            from moviepy.editor import AudioFileClip
            
            clip = AudioFileClip(str(audio_path))
            duration = clip.duration
            clip.close()
            
            return duration
        
        except ImportError:
            # Fallback: estimativa baseada no tamanho do arquivo
            # MP3 size (bytes) * 8 / bitrate (bps) = seconds
            # Google TTS MP3 usually ~32kbps mono
            file_size = audio_path.stat().st_size
            duration_est = (file_size * 8) / 32000
            
            logger.warning("moviepy não disponível, usando estimativa de duração")
            return duration_est
        
        except Exception as e:
            logger.error(f"Erro ao obter duração do áudio: {e}")
            return 0.0
    
    def _calcular_wpm(self, texto: str, duracao_sec: float) -> float:
        """
        Calcula palavras por minuto (Words Per Minute).
        
        Args:
            texto: Texto narrado
            duracao_sec: Duração do áudio em segundos
            
        Returns:
            WPM calculado
        """
        palavras = len(texto.split())
        minutos = duracao_sec / 60
        
        if minutos == 0:
            return 0
        
        return palavras / minutos
    
    def _validar_ritmo(self, wpm: float) -> str:
        """
        Valida se o ritmo está dentro dos limites ideais.
        
        Args:
            wpm: Palavras por minuto
            
        Returns:
            String formatada com status
        """
        if wpm < self.TARGET_WPM_MIN:
            return "[red]LENTO (Acelerar)[/red]"
        elif wpm > self.TARGET_WPM_MAX:
            return "[red]RÁPIDO (Inserir Pausa)[/red]"
        else:
            return "[green]PERFEITO[/green]"


# Compatibilidade com código antigo
Agente03Narrador = Agente08Narrador
