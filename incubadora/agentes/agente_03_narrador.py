import os
import json
import time
import requests
import base64
from rich.console import Console

console = Console()

class Agente03Narrador:
    def __init__(self):
        self._load_env()
        self.api_key = os.getenv("GOOGLE_API_KEY_AUDIO")
        self.api_url = "https://texttospeech.googleapis.com/v1/text:synthesize"
        self.target_wpm_min = 168
        self.target_wpm_max = 187
        self.output_dir = os.path.join(os.getcwd(), "output", "audio")
        
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def _load_env(self):
        """Carrega variáveis do .env manualmente para evitar dependências extras."""
        env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
        if os.path.exists(env_path):
            with open(env_path, "r") as f:
                for line in f:
                    if "=" in line and not line.startswith("#"):
                        key, value = line.strip().split("=", 1)
                        os.environ[key] = value

    def gerar_narracao(self, roteiro):
        """
        Gera áudio para cada bloco do roteiro.
        """
        console.print(f"[bold yellow]AGENTE 03: Iniciando Narracao (Google TTS)...[/bold yellow]")
        
        audios_gerados = []
        faixas = []

        blocos = roteiro if isinstance(roteiro, list) else roteiro.get('blocos', [])
        
        for i, bloco in enumerate(blocos):
            
            fala = bloco.get("fala", "")
            if not fala:
                continue

            console.print(f"   [cyan]Bloco {i+1}:[/cyan] \"{fala[:30]}...\"")
            
            # Gerar Áudio
            audio_file, duration_sec = self._chamar_google_tts(fala, i)
            
            if audio_file:
                # Validar Ritmo
                wpm = self._calcular_wpm(fala, duration_sec)
                status_ritmo = self._validar_ritmo(wpm)
                
                console.print(f"      -> [green]Audio Salvo:[/green] {os.path.basename(audio_file)} ({duration_sec:.1f}s)")
                console.print(f"      -> Ritmo: {wpm:.0f} WPM - {status_ritmo}")
                
                faixas.append({
                    "bloco_id": i,
                    "arquivo": audio_file,
                    "duracao": duration_sec,
                    "wpm": wpm,
                    "status": status_ritmo
                })
            else:
                console.print(f"      -> [red]Falha na geracao do audio.[/red]")

            # Rate limit friendly
            time.sleep(0.5)

        return {"faixas": faixas}

    def _chamar_google_tts(self, texto, index):
        """
        Chama a API do Google Cloud TTS.
        """
        if not self.api_key:
            console.print("[red]ERRO: GOOGLE_API_KEY_AUDIO não encontrada.[/red]")
            return None, 0

        # Configuração de Velocidade (Hook mais rápido)
        speaking_rate = 1.15
        if index == 0: # HOOK
            speaking_rate = 1.25
            console.print(f"      -> [yellow]HOOK DETECTADO: Acelerando para {speaking_rate}x[/yellow]")

        payload = {
            "input": {"text": texto},
            "voice": {
                "languageCode": "pt-BR",
                "name": "pt-BR-Neural2-B" # Voz masculina profunda
            },
            "audioConfig": {
                "audioEncoding": "MP3",
                "speakingRate": speaking_rate
            }
        }

        try:
            response = requests.post(
                f"{self.api_url}?key={self.api_key}",
                json=payload
            )
            
            if response.status_code == 200:
                data = response.json()
                audio_content = base64.b64decode(data["audioContent"])
                
                filename = f"audio_bloco_{index:03d}.mp3"
                filepath = os.path.join(self.output_dir, filename)
                
                with open(filepath, "wb") as f:
                    f.write(audio_content)
                
                # Estimar duração baseada no tamanho do arquivo MP3 (aprox)
                # MP3 size (bytes) * 8 / bitrate (bps) = seconds
                # Google TTS MP3 usually ~32kbps mono text
                file_size = len(audio_content)
                duration_est = (file_size * 8) / 32000 
                
                return filepath, duration_est
            else:
                console.print(f"[red]Erro API Google: {response.text}[/red]")
                return None, 0

        except Exception as e:
            console.print(f"[red]Erro na requisição: {e}[/red]")
            return None, 0

    def _calcular_wpm(self, texto, duracao_sec):
        palavras = len(texto.split())
        minutos = duracao_sec / 60
        if minutos == 0: return 0
        return palavras / minutos

    def _validar_ritmo(self, wpm):
        if wpm < self.target_wpm_min:
            return "[red]LENTO (Acelerar)[/red]"
        elif wpm > self.target_wpm_max:
            return "[red]RÁPIDO (Inserir Pausa)[/red]"
        else:
            return "[green]PERFEITO[/green]"
