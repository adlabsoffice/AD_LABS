import os
import sys
import argparse
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm

# Adiciona diretório atual ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.orchestrator import Orchestrator

console = Console()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_banner():
    clear_screen()
    console.print(Panel.fit(
        "[bold cyan]🤖 INCUBADORA AD_LABS v3.0 (Core Unificado)[/bold cyan]\n"
        "[dim]Sistema de Criação Automática de Canais Dark[/dim]",
        border_style="cyan"
    ))

def setup_canal_ia(orch: Orchestrator):
    """
    Fluxo de setup guiado por IA (CLI).
    """
    show_banner()
    console.print("\n[bold green]🚀 MODO SETUP IA INICIADO[/bold green]")
    
    # Aqui manteríamos a integração com SAPG, mas agora passando pelo Orchestrator
    # Por enquanto, vamos simplificar para chamar o Orchestrator diretamente
    # TODO: Reintegrar SAPG via Orchestrator.pesquisar_nicho()
    
    nicho = Prompt.ask("Qual nicho deseja pesquisar?", default="Curiosidades Históricas")
    
    config_inicial = {
        "nome_canal": f"Canal {nicho}",
        "nicho": nicho,
        "modo_criacao": "ia_assistida"
    }
    
    # Inicia Projeto via Core
    orch.iniciar_projeto(config_inicial, modo="interativo")

def main():
    parser = argparse.ArgumentParser(description="Incubadora AD_LABS CLI v3")
    parser.add_argument("--setup-canal-ia", action="store_true", help="Iniciar setup guiado por IA")
    args = parser.parse_args()

    orch = Orchestrator()

    if args.setup_canal_ia:
        setup_canal_ia(orch)
    else:
        show_banner()
        console.print("\n[bold white]SELECIONE UMA OPÇÃO:[/bold white]")
        console.print("1. [cyan]Setup de Novo Canal (IA)[/cyan]")
        console.print("2. [green]Gerenciar Canais Existentes[/green]")
        console.print("0. [red]Sair[/red]")
        
        choice = Prompt.ask("\n> ", choices=["1", "2", "0"], default="1")
        
        if choice == "1":
            setup_canal_ia(orch)
        elif choice == "0":
            sys.exit()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[red]Encerrado pelo usuário.[/red]")
        sys.exit()
