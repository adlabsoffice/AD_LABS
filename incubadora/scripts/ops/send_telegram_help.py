import requests
import os
from rich.console import Console

console = Console()

TOKEN = "8023515576:AAGxblQlQUcm7QG8MA2ebVN1MbDKimNgTco"
CHAT_ID = "7757304726"
URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

MESSAGE = """🤖 Comandos da Fábrica AD_LABS:

Salve esta mensagem para não esquecer!

🎬 Criar Vídeo:
/video [tema]
Ex: /video Estoicismo Moderno

📊 Ver Status:
/status
(Mostra se estou ocupado ou livre)

❓ Ajuda:
/ajuda
(Reenvia esta lista)

Estou pronto para trabalhar! 🚀"""

def send_help():
    payload = {
        "chat_id": CHAT_ID,
        "text": MESSAGE,
        # "parse_mode": "Markdown" # Removido para evitar erros de parsing
    }
    
    try:
        response = requests.post(URL, json=payload)
        if response.status_code == 200:
            console.print("[green]Mensagem de ajuda enviada com sucesso![/green]")
        else:
            console.print(f"[red]Erro ao enviar: {response.text}[/red]")
    except Exception as e:
        console.print(f"[red]Erro de conexão: {e}[/red]")

if __name__ == "__main__":
    send_help()
