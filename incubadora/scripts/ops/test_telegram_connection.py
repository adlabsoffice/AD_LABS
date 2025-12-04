import sys
import os
from rich.console import Console

# Adiciona diretório incubadora ao path
current_dir = os.path.dirname(os.path.abspath(__file__)) # scripts/ops
incubadora_root = os.path.dirname(os.path.dirname(current_dir)) # incubadora
sys.path.append(incubadora_root)

from utils.telegram_bot import TelegramBot
from dotenv import load_dotenv

# Carregar .env da raiz da incubadora
load_dotenv(os.path.join(incubadora_root, ".env"))

console = Console()

def main():
    console.print("[bold cyan]🤖 TESTE DE CONEXÃO TELEGRAM[/bold cyan]")
    
    try:
        bot = TelegramBot()
        console.print(f"[green]✓ Bot inicializado. Chat ID: {bot.chat_id}[/green]")
        
        msg = (
            "🚨 **TESTE DE CONEXÃO** 🚨\n\n"
            "Se você está recebendo esta mensagem, o Gatekeeper do Arquiteto está ativo.\n"
            "Clique no botão abaixo para confirmar."
        )
        
        keyboard = [
            [
                bot.InlineKeyboardButton("✅ CONFIRMAR RECEBIMENTO", callback_data="teste_aprovar")
            ]
        ]
        
        console.print("[yellow]Enviando mensagem... Verifique seu Telegram![/yellow]")
        sucesso = bot._enviar_e_aguardar(msg, keyboard, "teste")
        
        if sucesso:
            console.print("[bold green]✅ SUCESSO! Conexão bidirecional confirmada.[/bold green]")
        else:
            console.print("[bold red]❌ FALHA! Não houve confirmação ou ocorreu erro.[/bold red]")
            sys.exit(1)
            
    except Exception as e:
        console.print(f"[bold red]❌ ERRO CRÍTICO: {e}[/bold red]")
        sys.exit(1)

if __name__ == "__main__":
    main()
