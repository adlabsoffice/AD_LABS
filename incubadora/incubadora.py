import os
import sys
import argparse
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.table import Table

# Configuração do Rich Console
console = Console()

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_banner():
    clear_screen()
    console.print(Panel.fit(
        "[bold cyan]🤖 INCUBADORA AD_LABS v2.4[/bold cyan]\n"
        "[dim]Sistema de Criação Automática de Canais Dark[/dim]",
        border_style="cyan"
    ))

def setup_canal_ia():
    """
    Inicia o fluxo de setup 100% guiado por IA.
    """
    show_banner()
    console.print("\n[bold green]🚀 MODO SETUP IA INICIADO[/bold green]")
    console.print("[dim]A IA irá pesquisar tendências globais, comparar nichos e configurar o canal.[/dim]\n")
    
    if not Confirm.ask("Deseja iniciar a pesquisa global agora?"):
        console.print("[yellow]Operação cancelada.[/yellow]")
        return

    # Integrar com Agente 01 e SAPG
    try:
        from agentes.sapg import SAPG
        sapg = SAPG()
    except ImportError:
        # Fallback para desenvolvimento se rodar fora do pacote
        sys.path.append(os.path.join(os.path.dirname(__file__)))
        from agentes.sapg import SAPG
        sapg = SAPG()

    console.print("\n[bold yellow]🧠 SAPG: Iniciando Motor de Pesquisa IA...[/bold yellow]")
    
    # 1. Pesquisa Global
    oportunidades = sapg.pesquisar_tendencias_globais()
    
    console.print("\n[bold cyan]✨ Oportunidades Encontradas (Top 3):[/bold cyan]")
    for op in oportunidades[:3]:
        console.print(f"{op['id']}. [bold]{op['nicho_us']}[/bold] (Score: {op['score']})")
        console.print(f"   🇧🇷 {op['nicho_br']}")

    # 2. Seleção do Usuário
    console.print("\n[dim]Digite os números para selecionar (ex: '1, 3')[/dim]")
    escolha = Prompt.ask("[bold green]Sua escolha[/bold green]", default="1, 3")
    
    ids_escolhidos = [int(x.strip()) for x in escolha.split(",") if x.strip().isdigit()]
    nichos_selecionados = [op for op in oportunidades if op['id'] in ids_escolhidos]
    
    # 3. Comparativo e Híbridos
    if len(nichos_selecionados) > 1:
        console.print(f"\n[bold yellow]⚖️  Gerando Comparativo entre {len(nichos_selecionados)} nichos...[/bold yellow]")
        resultado = sapg.gerar_comparativo_hibrido(nichos_selecionados)
        
        console.print("\n[bold white]💡 SUGESTÕES DE HÍBRIDOS (IA):[/bold white]")
        for i, sug in enumerate(resultado['sugestoes'], 1):
            console.print(f"[bold]{chr(64+i)}.[/bold] [cyan]{sug['nome']}[/cyan] (Score: {sug['score']})")
            console.print(f"   {sug['justificativa']}")
            
        escolha_final = Prompt.ask("\n[bold green]Qual caminho seguir? (A/B/C ou ID original)[/bold green]", default="A")
        # Lógica simplificada para demo
        if escolha_final.upper() in ['A', 'B', 'C']:
            idx = ord(escolha_final.upper()) - 65
            if idx < len(resultado['sugestoes']):
                nicho_final = resultado['sugestoes'][idx]['nome']
            else:
                nicho_final = nichos_selecionados[0]['nicho_br']
        else:
             nicho_final = nichos_selecionados[0]['nicho_br']
    else:
        nicho_final = nichos_selecionados[0]['nicho_br']

    # 4. Configuração Automática
    console.print(f"\n[bold green]🛠️  Configurando canal para: {nicho_final}[/bold green]")
    config = sapg.gerar_configuracao_completa(nicho_final)
    
    # 5. Estratégia de Conteúdo (30 Ideias)
    console.print(f"\n[bold yellow]🧠 Gerando Estratégia de Conteúdo (5 Eixos)...[/bold yellow]")
    estrategia = sapg.gerar_estrategia_conteudo(nicho_final)
    
    for eixo, ideias in estrategia.items():
        console.print(f"\n[bold cyan]EIXO: {eixo}[/bold cyan]")
        for ideia in ideias[:3]: # Mostra top 3 de cada eixo para não poluir
            console.print(f"  • [{ideia['score']}] {ideia['titulo']}")
            
    console.print("\n[dim]... (Total 30 ideias geradas)[/dim]")

    # Painel Final
    console.print(Panel.fit(
        f"[bold]Canal:[/bold] {config['nome_canal']}\n"
        f"[bold]Visual:[/bold] {config['estilo_visual']}\n"
        f"[bold]Voz:[/bold] {config['voz']}\n"
        f"[bold]Imagens:[/bold] {config['provider_imagens']}\n"
        f"[bold]Duração Ideal:[/bold] {config['duracao_ideal']}\n"
        f"[dim]{config['analise_retencao']}[/dim]\n"
        f"[bold]Formato:[/bold] {config['formato_video']}\n"
        f"[bold]Transições:[/bold] {config['transicoes_ritmo']}\n"
        f"[bold]VFX:[/bold] {config['efeitos_visuais']}\n"
        f"[bold]Áudio/SFX:[/bold] {config['audio_musica']}\n"
        f"[bold]Frequência:[/bold] {config['frequencia_upload']}\n"
        f"[bold]Thumbnails:[/bold] {config['thumb_estrategia']}\n"
        f"[dim]Prompt: {config['thumb_prompt']}[/dim]\n"
        f"[bold red]{config['regra_integridade']}[/bold red]\n",
        title="📋 CONFIGURAÇÃO FINAL",
        border_style="green"
    ))
    
    if Confirm.ask("Salvar e Iniciar Produção?"):
        console.print("[bold green]🚀 Iniciando Agente 01 (Inicializador)...[/bold green]")
        try:
            from agentes.agente_01_inicializador import Agente01Inicializador
            agente01 = Agente01Inicializador()
            agente01.criar_estrutura_canal(config)
        except Exception as e:
             console.print(f"[red]Erro ao iniciar Agente 01: {e}[/red]")

    else:
        console.print("[yellow]Setup pausado.[/yellow]")

def main():
    parser = argparse.ArgumentParser(description="Incubadora AD_LABS CLI")
    parser.add_argument("--setup-canal-ia", action="store_true", help="Iniciar setup guiado por IA")
    parser.add_argument("--test-agents", action="store_true", help="Testar conexão com agentes")
    
    args = parser.parse_args()

    if args.setup_canal_ia:
        setup_canal_ia()
    elif args.test_agents:
        console.print("[green]Testando agentes...[/green]")
    else:
        # Menu Principal Interativo
        show_banner()
        console.print("\n[bold white]SELECIONE UMA OPÇÃO:[/bold white]")
        console.print("1. [cyan]Setup de Novo Canal (IA)[/cyan]")
        console.print("2. [green]Gerenciar Canais Existentes[/green]")
        console.print("3. [yellow]Ferramentas & Utilitários[/yellow]")
        console.print("0. [red]Sair[/red]")
        
        choice = Prompt.ask("\n> ", choices=["1", "2", "3", "0"], default="1")
        
        if choice == "1":
            setup_canal_ia()
        elif choice == "0":
            sys.exit()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[red]Encerrado pelo usuário.[/red]")
        sys.exit()
