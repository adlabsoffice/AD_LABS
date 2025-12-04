import sys
import os
from rich.console import Console

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agentes.agente_06_visual import Agente06Visual

console = Console()

def test_connection():
    console.print("[bold cyan]TESTE DE CONEXAO: AGENTE 06 -> GOOGLE CLOUD COMFYUI[/bold cyan]")
    
    agente = Agente06Visual()
    
    # Check if URL is loaded correctly
    comfy_url = os.getenv("COMFYUI_URL")
    console.print(f"URL Configurada: [yellow]{comfy_url}[/yellow]")
    
    if not comfy_url or "127.0.0.1" in comfy_url:
        console.print("[red]ALERTA: URL parece ser local. Verifique o .env[/red]")
    
    # Mock packaging for thumbnail generation
    packaging = {
        "titulo_hook": "TESTE DE CONEXAO REMOTA",
        "thumbnail_concept": "A futuristic robot shaking hands with a human, cyberpunk city background, vibrant colors"
    }
    
    console.print("\n[yellow]Tentando gerar Thumbnail de teste...[/yellow]")
    try:
        # We use gerar_thumbnail because it calls _chamar_api_imagem or _chamar_comfyui depending on config
        # But wait, gerar_thumbnail calls _chamar_api_imagem (Google Imagen) by default in the code I wrote earlier?
        # Let's check the code of Agente 06 again.
        # Ah, gerar_thumbnail calls _chamar_api_imagem. 
        # gerar_visuais calls _chamar_comfyui if provider is ComfyUI.
        
        # Let's try gerar_visuais with a fake script block
        roteiro = {
            "blocos": [
                {"visual": "A futuristic robot shaking hands with a human, cyberpunk city background"}
            ]
        }
        config = {"provider_imagens": "ComfyUI"}
        
        imagens = agente.gerar_visuais(roteiro, config)
        
        if imagens and len(imagens) > 0:
            img = imagens[0]
            if "mock" in img['arquivo'] or "transparent" in str(img['arquivo']):
                 console.print("[red]FALHA: O Agente retornou um MOCK (Falha na conexao ou timeout).[/red]")
            else:
                 console.print(f"[green]SUCESSO! Imagem gerada: {img['arquivo']}[/green]")
        else:
            console.print("[red]Nenhuma imagem retornada.[/red]")
            
    except Exception as e:
        console.print(f"[red]Erro fatal no teste: {e}[/red]")

if __name__ == "__main__":
    test_connection()
