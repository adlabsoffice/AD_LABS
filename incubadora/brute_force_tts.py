import requests
import json
from rich.console import Console

console = Console()

def brute_force_fn_index():
    base_url = "http://localhost:7860/gradio_api/predict"
    
    payload_template = {
        "data": [
            "Testing brute force.", 
            "Benedict", 
            1.0
        ]
    }

    for i in range(5):
        console.print(f"[yellow]Trying fn_index={i}...[/yellow]")
        payload = payload_template.copy()
        payload["fn_index"] = i
        
        try:
            resp = requests.post(base_url, json=payload, timeout=5)
            if resp.status_code == 200:
                console.print(f"[green]✅ Success with fn_index={i}![/green]")
                console.print(resp.json())
                break
            else:
                console.print(f"[dim]❌ fn_index={i}: {resp.status_code} {resp.text[:100]}[/dim]")
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")

if __name__ == "__main__":
    brute_force_fn_index()
