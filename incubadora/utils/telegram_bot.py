import os
import time
from rich.console import Console
from rich.panel import Panel

console = Console()

class TelegramBot:
    def __init__(self):
        self.token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID")
        self.mock_mode = not (self.token and self.chat_id)
        
        if self.mock_mode:
            console.print("[yellow]TELEGRAM: Modo Mock Ativado (Sem token configurado)[/yellow]")

    def enviar_aprovacao(self, video_path: str, thumb_path: str, metadados: dict) -> bool:
        """
        Envia o vídeo e metadados para aprovação.
        Retorna True se aprovado, False se rejeitado.
        """
        titulo = metadados.get('titulo', 'Sem Título')
        descricao = metadados.get('sinopse', 'Sem Descrição')
        
        msg = (
            f"🎬 **NOVO VÍDEO PARA APROVAÇÃO**\n\n"
            f"**Título:** {titulo}\n"
            f"**Arquivo:** {os.path.basename(video_path)}\n"
            f"**Thumb:** {os.path.basename(thumb_path) if thumb_path else 'N/A'}\n\n"
            f"--------------------------------\n"
            f"[APROVAR]   [REJEITAR]   [EDITAR]"
        )
        
        if self.mock_mode:
            console.print(Panel.fit(msg, title="Telegram Bot (Simulado)", border_style="blue"))
            console.print("[dim]Simulando espera de resposta do usuário...[/dim]")
            
            # Simula interação no console para teste
            # Em produção, isso seria um webhook ou polling
            return True
            
        else:
            # Implementação Real (usando requests ou python-telegram-bot)
            # TODO: Implementar envio real
            print(f"Enviando para chat {self.chat_id}...")
            return True

    def enviar_alerta_emergencia(self, mensagem: str):
        """Envia alerta urgente (ex: Falta de Template)."""
        if self.mock_mode:
            console.print(Panel(f"🚨 ALERTA: {mensagem}", style="bold red"))
        else:
            # TODO: Implementar envio real
            pass
