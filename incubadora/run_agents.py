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

from agentes.agente_02_pesquisador import Agente02Pesquisador
from agentes.agente_05_roteirista import Agente05Roteirista
from agentes.agente_03_narrador import Agente03Narrador
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

def enviar_telegram_arquivo(caminho_arquivo, tipo="photo", legenda=""):
    """Envia arquivo (foto/audio/video) para o Telegram."""
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = "7757304726"
    
    if not token or not chat_id or not os.path.exists(caminho_arquivo):
        return

    try:
        # Mapeia tipos para métodos da API
        metodo = "sendPhoto" if tipo == "photo" else "sendAudio" if tipo == "audio" else "sendDocument"
        url = f"https://api.telegram.org/bot{token}/{metodo}"
        
        with open(caminho_arquivo, 'rb') as f:
            files = {tipo: f}
            data = {'chat_id': chat_id, 'caption': legenda}
            requests.post(url, files=files, data=data)
    except Exception as e:
        console.print(f"[dim]Erro ao enviar Arquivo Telegram: {e}[/dim]")

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

def style_lock_check(config):
    """LOCK STYLE LOCK: Garante que a configuração visual é respeitada."""
    console.print("[bold yellow]LOCK STYLE LOCK CHECK...[/bold yellow]")
    
    required_keys = ["estilo_visual", "formato_video", "provider_imagens"]
    for key in required_keys:
        if key not in config:
            console.print(f"[bold red]VIOLACAO DE ESTILO: Chave '{key}' ausente no config.json![/bold red]")
            sys.exit(1)
            
    console.print(f"[green]Estilo Validado:[/green] {config['estilo_visual']}")
    return True

def budget_check():
    """BUDGET CHECK: Verifica se há orçamento aprovado (Simulado)."""
    # Futuro: Verificar saldo em API ou limite diário
    console.print("[bold yellow]BUDGET CHECK...[/bold yellow]")
    console.print("[green]Orcamento Aprovado para Execucao[/green]")
    return True

def main():
    parser = argparse.ArgumentParser(description="Orquestrador da Incubadora de Canais")
    parser.add_argument("--canal", type=str, required=True, help="Nome da pasta do canal em incubadora/canais/")
    parser.add_argument("--tema", type=str, required=False, help="Tema específico para o vídeo (sobrescreve o config)")
    args = parser.parse_args()

    console.print(Panel.fit(f"[bold cyan]ORCHESTRATOR: Iniciando Canal '{args.canal}'[/bold cyan]"))

    # 1. Carregar e Validar Configuração
    config = carregar_config_canal(args.canal)
    style_lock_check(config)
    budget_check()

    # Notifica Inicio
    tema_display = args.tema if args.tema else "Tema do Config"
    enviar_telegram(f"🏭 **Fábrica Iniciada!**\n\n🎬 Canal: `{args.canal}`\n📌 Tema: `{tema_display}`\n\n_Vou te mandar os materiais conforme ficarem prontos..._")

    # --- AGENTE 02: PESQUISADOR ---
    console.print("\n[bold white]1. INICIANDO AGENTE 02 (PESQUISADOR)...[/bold white]")
    agente02 = Agente02Pesquisador()
    
    # Usa pauta do config ou argumento --tema
    if args.tema:
        pauta = args.tema
        tema = config.get("nicho", "Geral")
    else:
        pauta = config.get("pauta_inicial", ["Tema Genérico"])[0]
        tema = config.get("nicho", "Geral")
    
    # 1.1 Pesquisa
    pesquisa = agente02.pesquisar_conteudo_base(tema, pauta)
    
    # 1.2 Análise de Viabilidade
    viabilidade = agente02.analisar_viabilidade_viral(pauta)
    console.print(f"[dim]Viabilidade Score: {viabilidade['score']}[/dim]")

    # --- AGENTE 05: ROTEIRISTA ---
    console.print("\n[bold white]2. INICIANDO AGENTE 05 (ROTEIRISTA)...[/bold white]")
    agente05 = Agente05Roteirista()
    
    # 2.1 Geração de Roteiro
    roteiro = agente05.gerar_roteiro_react(pesquisa, config_canal=config)
    
    console.print("\n[bold green]ROTEIRO GERADO![/bold green]")
    
    # NOTIFICACAO: Roteiro
    msg_roteiro = f"📜 **Roteiro Gerado!**\n\n**Título:** {roteiro.get('titulo_otimizado', 'Sem Título')}\n\n**Hook:** {roteiro['blocos'][0]['fala'] if roteiro['blocos'] else '...'}"
    enviar_telegram(msg_roteiro)

    # --- AGENTE 10: DIRETOR (QA & CONTINUIDADE) ---
    console.print("\n[bold white]2.5. INICIANDO AGENTE 10 (DIRETOR)...[/bold white]")
    agente10 = Agente10Director()
    
    # 2.5.1 Revisão de Roteiro
    aprovado = agente10.revisar_roteiro(roteiro, config)
    if not aprovado:
        console.print("[bold red]PARADA DE EMERGENCIA: Roteiro reprovado pelo Diretor.[/bold red]")
        sys.exit(1)

    # --- AGENTE 03: NARRADOR ---
    console.print("\n[bold white]3. INICIANDO AGENTE 03 (NARRADOR)...[/bold white]")
    agente03 = Agente03Narrador()
    
    # 3.1 Geração de Áudio (TTS)
    audios = agente03.gerar_narracao(roteiro)
    
    # NOTIFICACAO: Audio Exemplo
    if audios and len(audios) > 0:
        enviar_telegram_arquivo(audios[0]['arquivo'], "audio", "🎙️ Exemplo de Narração (Hook)")

    # --- AGENTE 09: SOUND DESIGNER ---
    console.print("\n[bold white]3.5. INICIANDO AGENTE 09 (SOUND DESIGNER)...[/bold white]")
    agente09 = Agente09SoundDesigner()
    
    # 3.5.1 Mixagem (Mock por enquanto)
    audios_mixados = agente09.mixar_faixas(audios, config)

    # --- AGENTE 06: VISUAL ---
    console.print("\n[bold white]4. INICIANDO AGENTE 06 (VISUAL)...[/bold white]")
    agente06 = Agente06Visual()
    
    # 4.1 Geração de Imagens
    # Modificado para enviar previews
    imagens = []
    for i, bloco in enumerate(roteiro['blocos']):
        img = agente06.gerar_visuais({"blocos": [bloco]}, config)[0] # Gera 1 por vez para notificar
        imagens.append(img)
        
        # Envia as 5 primeiras imagens
        if i < 5:
            enviar_telegram_arquivo(img['arquivo'], "photo", f"🎨 Cena {i+1}: {bloco.get('visual', '')[:50]}...")
    
    # 4.2 Thumbnail
    if "packaging" in viabilidade:
        thumb_path = agente06.gerar_thumbnail(viabilidade["packaging"])
        enviar_telegram_arquivo(thumb_path, "photo", "🖼️ Thumbnail Oficial")
    
    console.print("\n[bold green]GERACAO VISUAL CONCLUIDA![/bold green]")

    # --- AGENTE 07: EDITOR ---
    console.print("\n[bold white]5. INICIANDO AGENTE 07 (EDITOR)...[/bold white]")
    agente07 = Agente07Editor()
    
    # 5.1 Montagem da Timeline (Usando áudio mixado)
    audios_finais = {"faixas": audios_mixados["faixas_mixadas"]}
    
    timeline = agente07.montar_timeline(roteiro, audios_finais, imagens)
    
    if timeline:
        console.print("\n[bold green]PROCESSO COMPLETO COM SUCESSO![/bold green]")
        console.print(f"[dim]Canal: {config['nome_canal']} | Estilo: {config['estilo_visual']}[/dim]")
        
        enviar_telegram(f"✅ **Vídeo Concluído!**\n\n📁 Arquivo: `{timeline}`\n\n_Pronto para Upload!_")
        
        # --- AGENTE 11: ALMOXARIFE (ARQUIVAMENTO) ---
        console.print("\n[bold white]6. INICIANDO AGENTE 11 (ALMOXARIFE)...[/bold white]")
        agente11 = Agente11Archivist()
        agente11.arquivar_projeto(config, timeline)
        
    else:
        console.print("\n[bold red]FALHA NA MONTAGEM DA TIMELINE[/bold red]")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        console.print(f"\n[bold red]ERRO FATAL: {e}[/bold red]")
        try:
            enviar_telegram(f"🚨 **ERRO CRÍTICO NA FÁBRICA!**\n\nOcorreu um erro não tratado:\n`{str(e)}`\n\n_Verifique o terminal para mais detalhes._")
        except:
            pass
        sys.exit(1)
