import os
import requests
import json
from rich.console import Console

console = Console()

def probe_flash_image():
    # Load Image Key
    env_path = os.path.join(os.getcwd(), ".env")
    api_key = None
    if os.path.exists(env_path):
        with open(env_path, "r") as f:
            for line in f:
                if line.startswith("GOOGLE_API_KEY_IMAGE="):
                    api_key = line.strip().split("=")[1]
                    break
    
    if not api_key:
        console.print("[red]Key not found[/red]")
        return

    # Endpoint for Gemini 2.0 Flash Image Generation
    # Based on standard generateContent endpoint
    model = "gemini-2.0-flash-exp-image-generation"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    
    prompt = "Generate an image of a cute pixar style robot holding a flower"
    
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }
    
    console.print(f"[yellow]Testing {model}...[/yellow]")
    
    try:
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            data = response.json()
            console.print("[green]Success![/green]")
            # Inspect structure
            if "candidates" in data:
                parts = data["candidates"][0]["content"]["parts"]
                for part in parts:
                    if "inlineData" in part:
                        console.print("[blue]Received Image Data![/blue]")
                        # Save it
                        import base64
                        img_data = base64.b64decode(part["inlineData"]["data"])
                        with open("test_flash_gen.jpg", "wb") as f:
                            f.write(img_data)
                        console.print("Saved to test_flash_gen.jpg")
                    else:
                        console.print(f"Text response: {part.get('text')}")
            else:
                console.print(data)
        else:
            console.print(f"[red]Error {response.status_code}: {response.text}[/red]")

    except Exception as e:
        console.print(f"[red]Exception: {e}[/red]")

if __name__ == "__main__":
    probe_flash_image()
