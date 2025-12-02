import json
import os
from rich.console import Console

console = Console()

class Agente07Editor:
    def __init__(self):
        self.output_file = os.path.join(os.getcwd(), "output", "timeline.json")
        output_dir = os.path.dirname(self.output_file)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def montar_timeline(self, roteiro, audios, imagens):
        """
        Cria a timeline de edição (EDL) juntando áudio, imagem e texto.
        """
        console.print(f"[bold yellow]AGENTE 07: Montando Timeline Final (EDL)...[/bold yellow]")
        
        timeline = {
            "projeto": "Incubadora v5",
            "fps": 30,
            "resolucao": [1080, 1920], # Shorts Vertical
            "clips": []
        }

        current_time = 0.0

        # Mapear assets por bloco_id para acesso rápido
        mapa_audios = {a['bloco_id']: a for a in audios.get('faixas', [])}
        mapa_imagens = {img['bloco_id']: img for img in imagens}

        blocos = roteiro if isinstance(roteiro, list) else roteiro.get("blocos", [])
        total_blocos = len(blocos)

        for i, bloco in enumerate(blocos):
            # Recuperar Assets
            audio_asset = mapa_audios.get(i)
            imagem_asset = mapa_imagens.get(i)

            # Validação de Integridade (Regra: PARADA TOTAL se faltar asset)
            if not audio_asset or not imagem_asset:
                console.print(f"[bold red]ERRO CRITICO NO BLOCO {i+1}: Asset faltando![/bold red]")
                console.print(f"   Audio: {'OK' if audio_asset else 'FALHA'} | Imagem: {'OK' if imagem_asset else 'FALHA'}")
                return None # Aborta

            duracao_clip = audio_asset['duracao']
            
            clip_data = {
                "id": i,
                "start_time": round(current_time, 2),
                "end_time": round(current_time + duracao_clip, 2),
                "duration": round(duracao_clip, 2),
                "assets": {
                    "audio_path": audio_asset['arquivo'],
                    "image_path": imagem_asset['arquivo'],
                    "text_content": bloco['fala']
                }
            }
            
            timeline["clips"].append(clip_data)
            
            console.print(f"   [cyan]Clip {i+1}:[/cyan] {clip_data['start_time']}s -> {clip_data['end_time']}s (Dur: {duracao_clip}s)")
            
            current_time += duracao_clip

        # Salvar Timeline
        with open(self.output_file, "w", encoding="utf-8") as f:
            json.dump(timeline, f, indent=2, ensure_ascii=False)

        console.print(f"[bold green]TIMELINE SALVA:[/bold green] {self.output_file}")
        console.print(f"[dim]Duração Total: {current_time:.2f}s | Clips: {len(timeline['clips'])}[/dim]")
        
        return timeline
