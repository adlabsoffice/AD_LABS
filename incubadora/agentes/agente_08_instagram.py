import os
from instagrapi import Client
from rich.console import Console
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
console = Console()

class Agente08Instagram:
    def __init__(self):
        self.username = os.getenv("INSTAGRAM_USER")
        self.password = os.getenv("INSTAGRAM_PASSWORD")
        self.client = Client()

    def login(self):
        """Autentica no Instagram."""
        if not self.username or not self.password:
            console.print("[red]❌ Erro: INSTAGRAM_USER ou INSTAGRAM_PASSWORD não definidos no .env[/red]")
            return False

        try:
            console.print(f"[yellow]🔄 Tentando login como {self.username}...[/yellow]")
            self.client.login(self.username, self.password)
            console.print("[green]✅ Login no Instagram realizado com sucesso![/green]")
            return True
        except Exception as e:
            console.print(f"[red]❌ Falha no login do Instagram: {e}[/red]")
            return False

    def solicitar_aprovacao(self, caption):
        """Pede aprovação do usuário antes de postar."""
        console.print("\n[bold yellow]⚠️ APROVAÇÃO NECESSÁRIA[/bold yellow]")
        console.print(f"Legenda: {caption}")
        console.print("[cyan]O vídeo está pronto. Deseja postar no Instagram agora?[/cyan]")
        resposta = input("Digite 'S' para postar ou 'N' para cancelar: ").strip().upper()
        return resposta == 'S'

    def postar_reels(self, video_path, caption, pedir_aprovacao=True):
        """Posta um vídeo como Reels."""
        if not os.path.exists(video_path):
            console.print(f"[red]❌ Arquivo de vídeo não encontrado: {video_path}[/red]")
            return None

        # Etapa de Aprovação
        if pedir_aprovacao:
            if not self.solicitar_aprovacao(caption):
                console.print("[red]❌ Postagem cancelada pelo usuário.[/red]")
                return None

        if not self.login():
            return None

        try:
            console.print(f"[yellow]🚀 Enviando Reels: {video_path}...[/yellow]")
            media = self.client.clip_upload(
                path=video_path,
                caption=caption
            )
            console.print(f"[green]✅ Reels postado com sucesso! Media ID: {media.pk}[/green]")
            return media.pk
        except Exception as e:
            console.print(f"[red]❌ Erro ao postar Reels: {e}[/red]")
            return None

if __name__ == "__main__":
    # Teste manual
    agente = Agente08Instagram()
    # Exemplo de uso:
    # agente.postar_reels("output/video_final.mp4", "Teste de automação #ia #tech")
    console.print("[cyan]Agente Instagram inicializado. Configure o .env para usar.[/cyan]")
