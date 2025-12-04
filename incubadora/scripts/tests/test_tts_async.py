import requests
import time
import json
from rich.console import Console

console = Console()

def test_async_tts():
    base_url = "http://localhost:7860"
    call_url = f"{base_url}/gradio_api/call/generate_speech"
    
    payload = {
        "data": [
            "Testing async generation.", 
            "Benedict", 
            1.0
        ]
    }
    
    console.print(f"[yellow]POST {call_url}...[/yellow]")
    resp = requests.post(call_url, json=payload)
    
    if resp.status_code != 200:
        console.print(f"[red]Error: {resp.status_code} {resp.text}[/red]")
        return

    data = resp.json()
    event_id = data.get("event_id")
    console.print(f"[green]Event ID: {event_id}[/green]")
    
    if not event_id:
        console.print(f"Response: {data}")
        return

    # Polling with Stream
    poll_url = f"{call_url}/{event_id}"
    console.print(f"[yellow]Polling {poll_url}...[/yellow]")
    
    response = requests.get(poll_url, stream=True)
    for line in response.iter_lines():
        if line:
            decoded_line = line.decode('utf-8')
            console.print(f"SSE: {decoded_line}")
            if decoded_line.startswith("data:"):
                try:
                    json_str = decoded_line[5:] # remove "data:"
                    data = json.loads(json_str)
                    # Check for completion
                    # Usually data is a list [progress, result, status, ...]
                    console.print(f"Data: {data}")
                except:
                    pass
            if "event: complete" in decoded_line:
                console.print("[green]Completed![/green]")
                break

if __name__ == "__main__":
    test_async_tts()
