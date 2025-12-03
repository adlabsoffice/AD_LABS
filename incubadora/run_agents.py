import sys
import os
import argparse
from rich.console import Console
from rich.panel import Panel

# Adiciona diretório atual ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.orchestrator import Orchestrator

# Importa agentes (IDs atualizados)
from agentes.agente_02_pesquisador import Agente02Pesquisador
from agentes.agente_03_analista import Agente03Analista
from agentes.agente_04_arquiteto_eixos import Agente04ArquitetoEixos
from agentes.agente_05_gerador_ideias import Agente05GeradorIdeias
from agentes.agente_06_roteirista import Agente05Roteirista as Agente06Roteirista # Classe ainda chamava 05
from agentes.agente_07_visual import Agente06Visual as Agente07Visual # Classe chamava 06
from agentes.agente_08_narrador import Agente03Narrador as Agente08Narrador # Classe chamava 03
from agentes.agente_09_sound_designer import Agente09SoundDesigner
from agentes.agente_10_editor import Agente07EditorJSON as Agente10Editor # Classe chamava 07
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
            Agente02Pesquisador().pesquisar_conteudo_base(config.get("nicho"), config.get("pauta_inicial", ["Geral"])[0])
        except Exception as e:
            console.print(f"[red]Erro Agente 02: {e}[/red]")

        # T=2: Analista
        console.print("\n[bold white]2. AGENTE 03 (ANALISTA)[/bold white]")
        Agente03Analista().executar()

        # T=3: Arquiteto
        console.print("\n[bold white]3. AGENTE 04 (ARQUITETO)[/bold white]")
        Agente04ArquitetoEixos().executar()

        # T=4: Gerador de Ideias
        console.print("\n[bold white]4. AGENTE 05 (GERADOR DE IDEIAS)[/bold white]")
        Agente05GeradorIdeias().executar()

    # --- FASE 2: PRODUÇÃO (T=5 a T=11) ---
    if args.fase in ["producao", "tudo"]:
        console.print("\n[bold yellow]=== FASE 2: PRODUÇÃO ===[/bold yellow]")
        
        # Selecionar uma ideia para produzir (Mock: pega a primeira gerada ou cria uma dummy)
        # Em produção real, o usuário escolheria a ideia.
        ideia_escolhida = {
            "id": "ideia_pilot_01",
            "titulo": "Jesus Reage: O Primo Rico",
            "hook_visual": "Jesus chocado com grafico",
            "sinopse": "Jesus analisa investimentos modernos.",
            "visual_style_ref": config.get("estilo_visual", "Pixar 3D")
        }
        
        # T=5: Roteirista (Universal)
        console.print("\n[bold white]5. AGENTE 06 (ROTEIRISTA)[/bold white]")
        roteirista = Agente06Roteirista()
        # Usa template definido na config ou 'react' por padrão
        template = config.get("template_padrao", "react")
        roteiro = roteirista.gerar_roteiro(ideia_escolhida, template_name=template)

        # T=6: Visual (Imagens)
        console.print("\n[bold white]6. AGENTE 07 (VISUAL)[/bold white]")
        visual = Agente07Visual()
        imagens = visual.gerar_visuais(roteiro, config)

        # T=7: Narrador (TTS)
        console.print("\n[bold white]7. AGENTE 08 (NARRADOR)[/bold white]")
        narrador = Agente08Narrador()
        audios = narrador.gerar_narracao(roteiro)

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
        
        console.print(f"\n[bold green]🎉 PROCESSO CONCLUÍDO! Vídeo final: {video_path}[/bold green]")

if __name__ == "__main__":
    main()
