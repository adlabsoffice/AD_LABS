import requests
import time
import sys
from rich.console import Console

console = Console()

TOKEN = "8023515576:AAGxblQlQUcm7QG8MA2ebVN1MbDKimNgTco"
URL = f"https://api.telegram.org/bot{TOKEN}/getUpdates"

console.print(f"[bold yellow]AGUARDANDO MENSAGEM NO TELEGRAM...[/bold yellow]")
console.print(f"Por favor, envie 'Oi' para o bot [bold cyan]@adlabs_boss_bot[/bold cyan] agora.")

def get_chat_id():
    offset = None
    timeout = 0
    
    # Tenta por 60 segundos
    start_time = time.time()
    
    while (time.time() - start_time) < 60:
        try:
            params = {"timeout": timeout, "offset": offset}
            response = requests.get(URL, params=params)
            data = response.json()
            
            if "result" in data and len(data["result"]) > 0:
                for update in data["result"]:
                    if "message" in update:
                        chat_id = update["message"]["chat"]["id"]
                        user = update["message"]["from"].get("username", "Unknown")
                        text = update["message"].get("text", "")
                        
                        console.print(f"\n[bold green]MENSAGEM RECEBIDA![/bold green]")
                        console.print(f"User: {user} | ID: {chat_id}")
                        console.print(f"Texto: {text}")
                        
                        # Salva em arquivo para eu ler depois
                        with open("telegram_id.txt", "w") as f:
                            f.write(str(chat_id))
                            
                        return chat_id
                    
                    # Atualiza offset para não ler a mesma msg
                    offset = update["update_id"] + 1
                    
            time.sleep(2)
            
        except Exception as e:
            console.print(f"[red]Erro: {e}[/red]")
            time.sleep(2)
            
    console.print("[red]Timeout: Nenhuma mensagem recebida em 60s.[/red]")
    return None

if __name__ == "__main__":
    get_chat_id()
