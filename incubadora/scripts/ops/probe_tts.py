import requests
import json
from rich.console import Console

console = Console()

def probe_gradio_api_info():
    url = "http://localhost:7860/gradio_api/info"
    console.print(f"[bold yellow]🕵️‍♂️ FETCHING API INFO FROM {url}...[/bold yellow]")

    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            
            # Save to file
            with open("d:/AD_LABS/incubadora/api_info.json", "w") as f:
                json.dump(data, f, indent=2)
            
            console.print("[green]✅ Saved api_info.json[/green]")
            
            # List named endpoints
            if "named_endpoints" in data:
                console.print(f"\n[bold cyan]Named Endpoints:[/bold cyan]")
                for key, value in data["named_endpoints"].items():
                    console.print(f" - {key}")
            else:
                console.print("[red]No named_endpoints found.[/red]")
                
            # List unnamed endpoints (fn_index)
            if "unnamed_endpoints" in data:
                console.print(f"\n[bold cyan]Unnamed Endpoints (fn_index):[/bold cyan]")
                for key in data["unnamed_endpoints"]:
                    console.print(f" - fn_index: {key}")

        else:
            console.print(f"[red]❌ Error: {response.status_code}[/red]")
    except Exception as e:
        console.print(f"[red]❌ Connection Error: {e}[/red]")

if __name__ == "__main__":
    probe_gradio_api_info()
