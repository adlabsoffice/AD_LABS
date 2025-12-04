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
    Ordem Correta: Agente01 (guia) → SAPG (opcional) → Orchestrator
    """
    show_banner()
    console.print("\n[bold green]🚀 MODO SETUP IA INICIADO[/bold green]")
    
    # ✅ CORREÇÃO (04/12/2024): Agente 01 é quem GUIA o processo
    try:
        from agentes.agente_01_inicializador import Agente01Inicializador
        from agentes.sapg import SAPG
    except ImportError as e:
        console.print(f"[red]Erro ao importar componentes: {e}[/red]")
        
        # Fallback minimalista
        nicho = Prompt.ask("Qual nicho?", default="Curiosidades Históricas")
        orch.iniciar_projeto({"nome_canal": f"Canal {nicho}", "nicho": nicho, "modo_criacao": "manual"}, modo="interativo")
        return
    
    # 1️⃣ AGENTE 01: Faz as perguntas iniciais (GUIA)
    console.print("\n[cyan]🤖 Agente 01: Inicializador (Perguntas Iniciais)[/cyan]")
    agente01 = Agente01Inicializador()
    
    # Pergunta fundamental: ideia própria ou pesquisa IA?
    tem_ideia = Confirm.ask("\n💡 Você já tem uma ideia de nicho/canal?", default=False)
    
    if tem_ideia:
        # Fluxo Manual: usuário define tudo
        console.print("\n[bold]📝 Modo: Ideia Própria[/bold]")
        config_canal = agente01.executar(nicho=None)  # Faz perguntas completas
        
    else:
        # Fluxo IA: SAPG pesquisa tendências
        console.print("\n[bold]🔍 Modo: Pesquisa de Tendências (SAPG)[/bold]")
        
        try:
            # 2️⃣ SAPG: Pesquisa tendências globais
            console.print("[cyan]📊 SAPG: Analisando YouTube Trends (US + BR)...[/cyan]")
            sapg = SAPG()
            oportunidades = sapg.pesquisar_tendencias_globais()
            
            if not oportunidades:
                console.print("[yellow]⚠ Nenhuma tendência detectada, usando input manual[/yellow]")
                config_canal = agente01.executar(nicho=None)
            else:
                # Mostra oportunidades
                console.print("\n[bold green]✨ Oportunidades Detectadas:[/bold green]")
                for opp in oportunidades:
                    console.print(f"  {opp['id']}. {opp.get('nicho_br', opp.get('nicho_us'))} (Score: {opp.get('score', 0):.1f})")
                
                escolha = Prompt.ask("\nEscolha número ou digite nicho customizado", default="1")
                
                # Extrai nicho escolhido
                if escolha.isdigit() and int(escolha) <= len(oportunidades):
                    opp_selecionada = oportunidades[int(escolha) - 1]
                    nicho_escolhido = opp_selecionada.get('nicho_br', opp_selecionada.get('nicho_us'))
                else:
                    nicho_escolhido = escolha
                
                # 3️⃣ SAPG: Gera config IA completa
                console.print(f"\n[cyan]📝 SAPG: Gerando Configuração IA para '{nicho_escolhido}'...[/cyan]")
                config_ia_gerada = sapg.gerar_configuracao_completa(nicho_escolhido)
                
                console.print(f"[green]✓ Config IA:[/green] {config_ia_gerada.get('nome_canal', 'N/A')}")
                
                # 4️⃣ AGENTE 01: Cria estrutura do canal com config IA
                # ✅ AQUI estava o bug: criar_estrutura_canal nunca era chamado!
                config_canal = agente01.criar_estrutura_canal(config_ia_gerada)
                
        except Exception as e:
            console.print(f"[yellow]⚠ SAPG falhou ({e}), voltando para modo manual[/yellow]")
            config_canal = agente01.executar(nicho=None)
    
    # 5️⃣ ORCHESTRATOR: Inicializa projeto com config final
    console.print("\n[cyan]🎯 Orchestrator: Inicializando Projeto...[/cyan]")
    
    # Adiciona flag de modo
    config_canal["modo_criacao"] = "ia_assistida" if not tem_ideia else "manual_guiado"
    
    orch.iniciar_projeto(config_canal, modo="interativo")
    
    console.print("\n[bold green]✅ Setup Completo![/bold green]")
    console.print(f"[dim]Fluxo: Agente 01 (guia) → {'SAPG (IA)' if not tem_ideia else 'Manual'} → Orchestrator ✓[/dim]")

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
