import os
import json
import sys
from rich.console import Console
from rich.progress import track

# Tenta importar MoviePy
try:
    # MoviePy 2.0 imports
    from moviepy import (
        ImageClip, AudioFileClip, TextClip, CompositeVideoClip, 
        concatenate_videoclips, vfx
    )
    MOVIEPY_AVAILABLE = True
except ImportError:
    MOVIEPY_AVAILABLE = False
    print("ERRO: MoviePy não instalado ou erro de importação. Instale com: pip install moviepy")

console = Console()

class RenderEngine:
    def __init__(self):
        self.output_dir = os.path.join("outputs", "T08_videos_finais")
        os.makedirs(self.output_dir, exist_ok=True)

    def renderizar_projeto(self, projeto_path: str):
        """
        Lê um arquivo JSON de projeto e renderiza o MP4.
        """
        if not MOVIEPY_AVAILABLE:
            console.print("[red]MoviePy não disponível. Renderização abortada.[/red]")
            return

        with open(projeto_path, "r", encoding="utf-8") as f:
            projeto = json.load(f)

        console.print(f"[bold yellow]RENDER ENGINE: Iniciando renderização de '{projeto['titulo']}'...[/bold yellow]")
        
        clips = []
        timeline = projeto.get("timeline", [])
        
        for i, item in enumerate(track(timeline, description="Processando clips...")):
            # 1. Carregar Imagem
            img_path = item["assets"]["image"]
            if not os.path.exists(img_path):
                console.print(f"[red]Imagem não encontrada: {img_path}. Pulando clip.[/red]")
                continue
                
            # Criar Clip de Imagem
            duration = item["duration"]
            clip = ImageClip(img_path).with_duration(duration)
            
            # 2. Aplicar Efeitos (Ken Burns Simples)
            # Zoom In: Começa em 100% e vai para 115%
            # Implementação simplificada: Resize progressivo
            clip = clip.resized(lambda t: 1 + 0.15 * (t / duration)) 
            
            # Centralizar (necessário após resize para manter enquadramento)
            clip = clip.with_position("center")
            
            # 3. Adicionar Áudio
            audio_path = item["assets"]["audio"]
            if audio_path and os.path.exists(audio_path):
                audio = AudioFileClip(audio_path)
                clip = clip.with_audio(audio)
            
            clips.append(clip)
            
        # Concatenar tudo
        console.print("[dim]Concatenando clips...[/dim]")
        final_video = concatenate_videoclips(clips, method="compose")
        
        # Exportar
        output_filename = f"{projeto['id']}.mp4"
        output_path = os.path.join(self.output_dir, output_filename)
        
        console.print(f"[bold cyan]Renderizando para {output_path}... (Isso pode demorar)[/bold cyan]")
        
        # Configuração para renderização rápida (CPU)
        final_video.write_videofile(
            output_path, 
            fps=24, 
            codec="libx264", 
            audio_codec="aac",
            preset="ultrafast", # Mais rápido, arquivo maior
            threads=4
        )
        
        console.print(f"[bold green]✅ Vídeo Renderizado com Sucesso![/bold green]")
        return output_path

if __name__ == "__main__":
    if len(sys.argv) > 1:
        engine = RenderEngine()
        engine.renderizar_projeto(sys.argv[1])
    else:
        print("Uso: python render_engine.py <caminho_projeto.json>")
