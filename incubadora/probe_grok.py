import os
import requests
import json
from rich.console import Console

console = Console()

def probe_grok():
    # Load Key
    env_path = os.path.join(os.getcwd(), ".env")
    api_key = None
    if os.path.exists(env_path):
        with open(env_path, "r") as f:
            for line in f:
                if line.startswith("XAI_API_KEY="):
                    api_key = line.strip().split("=")[1]
                    break
    
    if not api_key:
        console.print("[red]XAI_API_KEY not found[/red]")
        return

    url = "https://api.x.ai/v1/chat/completions"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    payload = {
        "messages": [
            {
                "role": "system",
                "content": "You are a test assistant."
            },
            {
                "role": "user",
                "content": "Testing. Just say hi and hello world and nothing else."
            }
        ],
        "model": "grok-beta", # Using grok-beta as it's often the standard alias, or we can try grok-4-latest
        "stream": False,
        "temperature": 0
    }
    
    # Try grok-beta first
    console.print("[yellow]Testing Grok API (grok-beta)...[/yellow]")
    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            console.print("[green]Success![/green]")
            console.print(response.json())
        else:
            console.print(f"[red]Error {response.status_code}: {response.text}[/red]")
            
            # Retry with grok-4-latest if beta fails or just to test
            console.print("[yellow]Retrying with grok-2-latest...[/yellow]") # grok-4 might not be public API yet, usually it's grok-beta or grok-2
            payload["model"] = "grok-2-latest" 
            response = requests.post(url, headers=headers, json=payload)
            if response.status_code == 200:
                 console.print("[green]Success with grok-2-latest![/green]")
                 console.print(response.json())
            else:
                 console.print(f"[red]Error {response.status_code}: {response.text}[/red]")

    except Exception as e:
        console.print(f"[red]Exception: {e}[/red]")

if __name__ == "__main__":
    probe_grok()
