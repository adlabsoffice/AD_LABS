import os
import json
import sys
from typing import Dict, Optional
from rich.console import Console
from rich.panel import Panel

# Tenta importar bibliotecas de imagem e google
try:
    from PIL import Image, ImageDraw, ImageFont, ImageEnhance
    PILLOW_AVAILABLE = True
except ImportError:
    PILLOW_AVAILABLE = False
    print("WARNING: Pillow não instalado. Instale com: pip install pillow")

try:
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload
    GOOGLE_API_AVAILABLE = True
except ImportError:
    GOOGLE_API_AVAILABLE = False
    print("WARNING: Google API Client não instalado. Instale com: pip install google-api-python-client google-auth-oauthlib google-auth-httplib2")

# Importar Telegram Bot
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.telegram_bot import TelegramBot

console = Console()

class Agente12Publisher:
    def __init__(self):
        self.output_dir = os.path.join("outputs", "T12_publicacao")
        os.makedirs(self.output_dir, exist_ok=True)
        self.telegram = TelegramBot()
        # TODO: Carregar credenciais do YouTube de arquivo seguro
        self.youtube = None 

    def preparar_thumbnail(self, imagem_base_path: str, texto_thumb: str) -> str:
        """
        Processa a imagem base para criar uma Thumbnail de alta conversão.
        Aplica filtros e texto conforme Blueprint.
        """
        console.print(f"[cyan]AGENTE 12: Preparando Thumbnail...[/cyan]")
        
        if not PILLOW_AVAILABLE:
            console.print("[red]Pillow não disponível. Usando imagem original.[/red]")
            return imagem_base_path

        try:
            with Image.open(imagem_base_path) as img:
                # 1. Ajuste de Tamanho (YouTube recomenda 1280x720)
                img = img.resize((1280, 720))
                
                # 2. Filtros de "Pop" (Contraste e Saturação)
                enhancer = ImageEnhance.Contrast(img)
                img = enhancer.enhance(1.2) # +20% Contraste
                
                enhancer = ImageEnhance.Color(img)
                img = enhancer.enhance(1.3) # +30% Saturação (Vibrance)
                
                # 3. Adicionar Texto (Se houver)
                if texto_thumb:
                    draw = ImageDraw.Draw(img)
                    # Tenta carregar fonte impactante (Impact ou Arial Bold)
                    try:
                        font = ImageFont.truetype("arialbd.ttf", 100)
                    except:
                        font = ImageFont.load_default()
                    
                    # Desenhar texto com contorno (Stroke) para legibilidade
                    # Posição: Canto inferior esquerdo ou centro
                    text_pos = (50, 550)
                    draw.text(text_pos, texto_thumb.upper(), font=font, fill="white", stroke_width=5, stroke_fill="black")

                # Salvar
                thumb_filename = f"thumb_{os.path.basename(imagem_base_path)}"
                output_path = os.path.join(self.output_dir, thumb_filename)
                img.save(output_path, "JPEG", quality=95)
                
                console.print(f"[green]Thumbnail salva: {output_path}[/green]")
                return output_path

        except Exception as e:
            console.print(f"[red]Erro ao gerar thumb: {e}[/red]")
            return imagem_base_path

    def upload_youtube(self, video_path: str, metadados: Dict, thumb_path: str = None):
        """
        Simula (ou realiza) o upload para o YouTube.
        """
        console.print(Panel.fit(f"[bold red]AGENTE 12: Iniciando Upload para YouTube...[/bold red]"))
        console.print(f"   Vídeo: {os.path.basename(video_path)}")
        console.print(f"   Título: {metadados.get('titulo')}")
        console.print(f"   Visibilidade: PRIVADO (Aguardando Aprovação)")

        if not GOOGLE_API_AVAILABLE:
            console.print("[yellow]Google API Client ausente. Simulando upload...[/yellow]")
            # Simulação
            import time
            time.sleep(2)
            video_id = "MOCK_VIDEO_ID_123"
            console.print(f"[green]✅ Upload Simulado Concluído! ID: {video_id}[/green]")
            return video_id

        # TODO: Implementar autenticação real OAuth2 aqui
        console.print("[yellow]Autenticação OAuth2 pendente. Simulando upload...[/yellow]")
        video_id = "MOCK_VIDEO_ID_OAUTH"
        
        # Notificar Aprovação
        self.telegram.enviar_aprovacao(video_path, thumb_path, metadados)
        
        return video_id

if __name__ == "__main__":
    # Teste
    agente = Agente12Publisher()
    # Mock image path (precisa existir para testar pillow)
    # agente.preparar_thumbnail("outputs/images/scene_000.png", "PRIMO RICO?")
