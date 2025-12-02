import sys
import os
import json
import argparse
from rich.console import Console
from rich.panel import Panel

import requests
from dotenv import load_dotenv

# Carrega variáveis de ambiente (.env)
load_dotenv()

# Adiciona o diretório atual ao path para importar os agentes
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# --- NOVOS AGENTES (PIPELINE DE INCUBAÇÃO) ---
from agentes.agente_02_pesquisador import Agente02Pesquisador
from agentes.agente_03_analista import Agente03Analista
from agentes.agente_04_arquiteto_eixos import Agente04ArquitetoEixos
from agentes.agente_05_gerador_ideias import Agente05GeradorIdeias

# --- AGENTES ANTIGOS (PIPELINE DE PRODUÇÃO - BACKUP/FUTURO) ---
# Renomeados para evitar conflito de nomes
from agentes.agente_05_roteirista import Agente05Roteirista as Agente05RoteiristaOld
from agentes.agente_03_narrador import Agente03Narrador as Agente03NarradorOld
from agentes.agente_06_visual import Agente06Visual
from agentes.agente_07_editor import Agente07Editor
from agentes.agente_09_sound_designer import Agente09SoundDesigner
from agentes.agente_10_director import Agente10Director
from agentes.agente_11_archivist import Agente11Archivist

console = Console()

def enviar_telegram(mensagem):
    """Envia notificação para o Telegram se configurado."""
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    # Tenta pegar o Chat ID do arquivo ou variável (simplificado para o ID do usuário conhecido)
    chat_id = "7757304726" 
    
    if not token or not chat_id:
        return

    try:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = {"chat_id": chat_id, "text": mensagem, "parse_mode": "Markdown"}
        requests.post(url, json=payload, timeout=5)
    except Exception as e:
        console.print(f"[dim]Erro ao enviar Telegram: {e}[/dim]")

def carregar_config_canal(nome_canal):
    """Carrega a configuração do canal específico."""
    base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "canais")
    canal_path = os.path.join(base_path, nome_canal)
    config_file = os.path.join(canal_path, "config.json")

    if not os.path.exists(config_file):
        console.print(f"[bold red]Erro: Configuracao nao encontrada para o canal '{nome_canal}'[/bold red]")
        console.print(f"[dim]Caminho esperado: {config_file}[/dim]")
        sys.exit(1)

    with open(config_file, "r", encoding="utf-8") as f:
        return json.load(f)

def main():
    parser = argparse.ArgumentParser(description="Orquestrador da Incubadora de Canais")
    parser.add_argument("--canal", type=str, required=True, help="Nome da pasta do canal em incubadora/canais/")
    parser.add_argument("--modo", type=str, choices=["incubacao", "producao"], default="incubacao", help="Modo de execução: 'incubacao' (T=1-4) ou 'producao' (T=5-11)")
    args = parser.parse_args()

    console.print(Panel.fit(f"[bold cyan]ORCHESTRATOR: Iniciando Canal '{args.canal}'[/bold cyan]"))

    # 1. Carregar Configuração
    config = carregar_config_canal(args.canal)
    
    # Notifica Inicio
    enviar_telegram(f"🏭 **Orquestrador Iniciado!**\n\n🎬 Canal: `{args.canal}`\n⚙️ Modo: `{args.modo}`")

    if args.modo == "incubacao":
        # === PIPELINE DE INCUBAÇÃO (T=1 até T=4) ===
        console.print("\n[bold yellow]=== MODO INCUBAÇÃO (T=1 -> T=4) ===[/bold yellow]")

        # --- AGENTE 02: PESQUISADOR (T=1) ---
        console.print("\n[bold white]1. INICIANDO AGENTE 02 (PESQUISADOR)...[/bold white]")
        agente02 = Agente02Pesquisador()
        
        tema = config.get("nicho", "Geral")
        pauta = config.get("pauta_inicial", ["Tema Genérico"])[0]
        
        # Executa pesquisa
        agente02.pesquisar_conteudo_base(tema, pauta)
        
        # --- AGENTE 03: ANALISTA (T=2) ---
        console.print("\n[bold white]2. INICIANDO AGENTE 03 (ANALISTA)...[/bold white]")
        agente03 = Agente03Analista()
        agente03.executar()

        # --- AGENTE 04: ARQUITETO DE EIXOS (T=3) ---
        console.print("\n[bold white]3. INICIANDO AGENTE 04 (ARQUITETO DE EIXOS)...[/bold white]")
        agente04 = Agente04ArquitetoEixos()
        agente04.executar()

        # --- AGENTE 05: GERADOR DE IDEIAS (T=4) ---
        console.print("\n[bold white]4. INICIANDO AGENTE 05 (GERADOR DE IDEIAS)...[/bold white]")
        agente05 = Agente05GeradorIdeias()
        agente05.executar()

        console.print("\n[bold green]✅ INCUBAÇÃO CONCLUÍDA![/bold green]")
        console.print("[dim]Agora você tem 150 ideias em 'outputs/T04_ideias'. Escolha uma para produzir![/dim]")
        enviar_telegram("✅ **Incubação Concluída!**\n\n150 Ideias geradas e prontas para seleção.")

    elif args.modo == "producao":
        # === PIPELINE DE PRODUÇÃO (T=5 até T=11) ===
        console.print("\n[bold yellow]=== MODO PRODUÇÃO (T=5 -> T=11) ===[/bold yellow]")
        console.print("[red]⚠️ AVISO: Este modo requer seleção manual de uma ideia do T=4.[/red]")
        console.print("[dim]Funcionalidade em migração para usar as novas ideias geradas.[/dim]")
        
        # TODO: Implementar seleção de ideia e integração com RoteiristaOld
        # Por enquanto, mantemos o código antigo comentado ou adaptado se necessário
        # Mas como o fluxo mudou (Ideia -> Roteiro), o Roteirista precisa ser adaptado para receber JSON de ideia
        
        console.print("[yellow]Funcionalidade de produção pausada para refatoração. Use o modo 'incubacao' por enquanto.[/yellow]")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        console.print(f"\n[bold red]ERRO FATAL: {e}[/bold red]")
        sys.exit(1)
