import os
import requests
from rich.console import Console

console = Console()

def list_models():
    # Load env manually
    env_path = os.path.join(os.getcwd(), ".env")
    api_key = None
    if os.path.exists(env_path):
        with open(env_path, "r") as f:
            for line in f:
                if line.startswith("GOOGLE_API_KEY_VIDEO="):
                    api_key = line.strip().split("=")[1]
                    break
    
    if not api_key:
        console.print("[red]Key not found in .env[/red]")
        return

    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
    
    try:
        resp = requests.get(url)
        if resp.status_code == 200:
            data = resp.json()
            console.print("[bold green]Available Models:[/bold green]")
            for model in data.get("models", []):
                name = model.get("name")
                methods = model.get("supportedGenerationMethods")
                console.print(f" - [cyan]{name}[/cyan] ({methods})")
        else:
            console.print(f"[red]Error {resp.status_code}: {resp.text}[/red]")
    except Exception as e:
        console.print(f"[red]Exception: {e}[/red]")

if __name__ == "__main__":
    list_models()
