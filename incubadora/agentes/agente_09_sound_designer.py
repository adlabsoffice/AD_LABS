import os
import time
import json
from rich.console import Console

console = Console()

class Agente09SoundDesigner:
    def __init__(self):
        self.output_dir = os.path.join(os.getcwd(), "output", "audio_mixed")
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def mixar_audio_cinema(self, audios, roteiro):
        """
        Mixa voz, trilha sonora dinâmica e efeitos sonoros (SFX).
        """
        console.print(f"[bold yellow]AGENTE 09: Iniciando Mixagem de Cinema (Sound Design)...[/bold yellow]")
        
        # Simulação de mixagem complexa (FFmpeg seria chamado aqui)
        # 1. Analisar sentimento do roteiro para escolher trilha (Tensão, Alegria, Mistério)
        # 2. Inserir SFX nos pontos de impacto (ex: "Dinheiro caindo", "Explosão", "Grilo")
        # 3. Normalizar áudio (Loudness Standards -14 LUFS)

        audios_mixados = []
        
        # Garante que 'faixas' existe
        faixas = audios.get('faixas', [])
        if not faixas:
            console.print("[red]ALERTA: Nenhuma faixa de audio recebida para mixagem![/red]")
            return {"faixas_mixadas": []}

        for faixa in faixas:
            bloco_id = faixa['bloco_id']
            # Recuperar texto para análise de sentimento simples
            blocos = roteiro if isinstance(roteiro, list) else roteiro.get('blocos', [])
            texto = ""
            if bloco_id < len(blocos):
                texto = blocos[bloco_id].get('fala', '')
            
            sfx = "Nenhum"
            if "dinheiro" in texto.lower():
                sfx = "SFX_Cash_Register.mp3"
            elif "erro" in texto.lower():
                sfx = "SFX_Error_Buzz.mp3"
                
            console.print(f"   [cyan]Bloco {bloco_id+1}:[/cyan] Mixando Voz + Trilha + {sfx}")
            
            # Mock do arquivo mixado
            output_file = os.path.join(self.output_dir, f"mixed_bloco_{bloco_id:03d}.mp3")
            with open(output_file, "w") as f:
                f.write("AUDIO_MIXADO_MOCK")
            
            # Adiciona à lista de faixas mixadas
            # IMPORTANTE: Manter a estrutura que o Agente 07 espera
            faixa_mixada = faixa.copy()
            faixa_mixada['arquivo_mixado'] = output_file
            audios_mixados.append(faixa_mixada)
            
        console.print(f"[bold green]MIXAGEM CONCLUIDA![/bold green]")
        
        return {"faixas_mixadas": audios_mixados}
