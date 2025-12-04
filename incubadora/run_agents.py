import sys
import os
import json
import argparse
from rich.console import Console
from rich.panel import Panel

# Adiciona diretório atual ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.orchestrator import Orchestrator

# Importa sistema de checkpoints
from utils.telegram_bot import TelegramBot
from utils.checkpoint_manager import CheckpointManager

# Importa agentes (IDs atualizados)
from agentes.agente_02_pesquisador import Agente02Pesquisador
from agentes.agente_03_analista import Agente03Analista
from agentes.agente_04_arquiteto_eixos import Agente04ArquitetoEixos
from agentes.agente_05_gerador_ideias import Agente05GeradorIdeias
from agentes.agente_06_roteirista import Agente06Roteirista
from agentes.agente_07_visual import Agente07Visual
from agentes.agente_08_narrador import Agente08Narrador
from agentes.agente_09_sound_designer import Agente09SoundDesigner
from agentes.agente_10_director import Agente10Director
from agentes.agente_10_editor import Agente10Editor
from agentes.agente_11_archivist import Agente11Archivist
from render_engine import RenderEngine

console = Console()

def main():
    parser = argparse.ArgumentParser(description="Executor de Pipeline AD_LABS v3")
    parser.add_argument("--canal", type=str, required=True, help="Nome do canal (pasta)")
    parser.add_argument("--fase", type=str, default="tudo", choices=["incubacao", "producao", "tudo"])
    args = parser.parse_args()

    orch = Orchestrator()
    console.print(Panel.fit(f"[bold cyan]PIPELINE EXECUTOR: {args.canal}[/bold cyan]"))

    # 1. Carregar Projeto via Core
    config = orch.carregar_projeto(args.canal)
    if not config:
        console.print(f"[red]Erro: Projeto '{args.canal}' não encontrado. Use incubadora.py para criar.[/red]")
        sys.exit(1)

    console.print(f"[green]Projeto carregado: {config['nome_canal']} (ID: {config.get('id')})[/green]")

    # --- FASE 1: INCUBAÇÃO (T=1 a T=4) ---
    if args.fase in ["incubacao", "tudo"]:
        console.print("\n[bold yellow]=== FASE 1: INCUBAÇÃO ===[/bold yellow]")
        
        # T=1: Pesquisador
        console.print("\n[bold white]1. AGENTE 02 (PESQUISADOR)[/bold white]")
        try:
            director = Agente10Director()
            if not director.revisar_roteiro(roteiro, config):
                console.print("[red]❌ Roteiro rejeitado pelo Director. Pipeline abortado.[/red]")
                checkpoint.marcar_etapa("roteiro", "rejeitado_director")
                sys.exit(1)
            
            director.verificar_continuidade(roteiro)
            
            # CHECKPOINT 2: Aprovação via Telegram
            console.print("\n[bold cyan]📱 CHECKPOINT: Aprovação de Roteiro[/bold cyan]")
            aprovado = telegram.enviar_roteiro_aprovacao(roteiro)
            
            if not aprovado:
                console.print("[yellow]⏸️ Roteiro rejeitado. Pipeline pausado.[/yellow]")
                checkpoint.marcar_etapa("roteiro", "rejeitado")
                sys.exit(0)
            
            # Salvar aprovação
            roteiro_path = os.path.join("outputs", "T05_roteiros", f"{roteiro['id']}.json")
            checkpoint.marcar_etapa("roteiro", "aprovado", {"arquivo": roteiro_path})
            console.print("[green]✅ Roteiro aprovado! Prosseguindo...[/green]")

        # T=6: Visual (Imagens)
        console.print("\n[bold white]6. AGENTE 07 (VISUAL)[/bold white]")
        
        if checkpoint.pode_pular_etapa("imagens"):
            console.print("[green]✓ Imagens já aprovadas anteriormente. Pulando...[/green]")
            imagens = checkpoint.obter_dados_etapa("imagens")["lista"]
        else:
            visual = Agente07Visual()
            imagens = visual.gerar_visuais(roteiro, config)
            
            # CHECKPOINT 3: Aprovação de Imagens
            console.print("\n[bold cyan]📱 CHECKPOINT: Aprovação de Imagens[/bold cyan]")
            imagens_paths = [img['arquivo'] for img in imagens]
            aprovado = telegram.enviar_imagens_aprovacao(imagens_paths)
            
            if not aprovado:
                console.print("[yellow]⏸️ Imagens rejeitadas. Pipeline pausado.[/yellow]")
                checkpoint.marcar_etapa("imagens", "rejeitado")
                sys.exit(0)
            
            checkpoint.marcar_etapa("imagens", "aprovado", {"lista": imagens})
            console.print("[green]✅ Imagens aprovadas![/green]")

        # T=7: Narrador (TTS)
        console.print("\n[bold white]7. AGENTE 08 (NARRADOR)[/bold white]")
        
        if checkpoint.pode_pular_etapa("audio"):
            console.print("[green]✓ Áudio já aprovado anteriormente. Pulando...[/green]")
            audios = checkpoint.obter_dados_etapa("audio")["dados"]
        else:
            narrador = Agente08Narrador()
            audios = narrador.gerar_narracao(roteiro)
            
            # CHECKPOINT 4: Aprovação de Áudio
            console.print("\n[bold cyan]📱 CHECKPOINT: Aprovação de Áudio[/bold cyan]")
            primeiro_audio = audios['faixas'][0]['arquivo']
            aprovado = telegram.enviar_audio_aprovacao(primeiro_audio)
            
            if not aprovado:
                console.print("[yellow]⏸️ Qualidade de áudio rejeitada. Pipeline pausado.[/yellow]")
                checkpoint.marcar_etapa("audio", "rejeitado")
                sys.exit(0)
            
            checkpoint.marcar_etapa("audio", "aprovado", {"dados": audios})
            console.print("[green]✅ Áudio aprovado![/green]")

        # T=8: Sound Designer (Mixagem)
        console.print("\n[bold white]8. AGENTE 09 (SOUND DESIGNER)[/bold white]")
        sound = Agente09SoundDesigner(config)
        audios_mixados = sound.mixar_audio_cinema(audios, roteiro)

        # T=9: Editor (JSON Timeline)
        console.print("\n[bold white]9. AGENTE 10 (EDITOR LÓGICO)[/bold white]")
        editor = Agente10Editor()
        projeto_video = editor.criar_projeto_video(roteiro, imagens, audios_mixados)

        # T=10: Render Engine (MP4)
        console.print("\n[bold white]10. RENDER ENGINE (MOVIEPY)[/bold white]")
        engine = RenderEngine()
        video_path = engine.renderizar_projeto(os.path.join(editor.output_dir, f"{projeto_video['id']}.json"))
        
        # CHECKPOINT 5: Aprovação de Vídeo Final
        console.print("\n[bold cyan]📱 CHECKPOINT: Aprovação de Vídeo Final[/bold cyan]")
        aprovado = telegram.enviar_video_aprovacao(video_path)
        
        if not aprovado:
            console.print("[yellow]⏸️ Vídeo rejeitado. NÃO será publicado.[/yellow]")
            checkpoint.marcar_etapa("video", "rejeitado")
            sys.exit(0)
        
        checkpoint.marcar_etapa("video", "aprovado", {"arquivo": video_path})
        checkpoint.limpar()  # Remove checkpoint após sucesso total
        
        console.print(f"\n[bold green]🎉 VÍDEO APROVADO E PRONTO PARA PUBLICAÇÃO![/bold green]")
        console.print(f"[bold green]Arquivo: {video_path}[/bold green]")

        # T=11: Archivist (Upload & Backup)
        console.print("\n[bold white]11. AGENTE 11 (ALMOXARIFE)[/bold white]")
        archivist = Agente11Archivist()
        # Passa o caminho do vídeo explicitamente
        archivist.arquivar_projeto(config, video_path=video_path)
        
        console.print("\n[bold green]🏁 PIPELINE CONCLUÍDO COM SUCESSO! 🏁[/bold green]")

if __name__ == "__main__":
    main()
