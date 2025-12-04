import os
import time
import json
from typing import Optional, List
from rich.console import Console
from rich.panel import Panel

console = Console()

class TelegramBot:
    def __init__(self):
        self.token = os.getenv("TELEGRAM_BOT_TOKEN")
        
        # Carregar Chat ID do arquivo
        chat_id_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "telegram_id.txt")
        if os.path.exists(chat_id_file):
            with open(chat_id_file, "r") as f:
                self.chat_id = f.read().strip()
        else:
            self.chat_id = os.getenv("TELEGRAM_CHAT_ID")
        
        self.timeout_minutos = int(os.getenv("TELEGRAM_TIMEOUT_MINUTOS", "10"))
        self.response_received = None
        
        if not self.token or not self.chat_id:
            raise RuntimeError(
                "TELEGRAM NÃO CONFIGURADO!\n"
                "Configure:\n"
                "  - TELEGRAM_BOT_TOKEN no .env\n"
                "  - telegram_id.txt com seu Chat ID"
            )
        
        # Importar biblioteca real
        try:
            from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup, Update
            from telegram.ext import Application, CallbackQueryHandler
            self.Bot = Bot
            self.InlineKeyboardButton = InlineKeyboardButton
            self.InlineKeyboardMarkup = InlineKeyboardMarkup
            self.Application = Application
            self.CallbackQueryHandler = CallbackQueryHandler
        except ImportError:
            raise RuntimeError(
                "Biblioteca python-telegram-bot NÃO INSTALADA!\n"
                "Execute: pip install python-telegram-bot"
            )
        
        console.print("[green]✓ TelegramBot configurado (Modo Real)[/green]")

    def enviar_roteiro_aprovacao(self, roteiro: dict) -> bool:
        """Envia roteiro para aprovação via Telegram."""
        console.print("[bold yellow]📱 Enviando roteiro para aprovação no Telegram...[/bold yellow]")
        
        titulo = roteiro.get('titulo_final', 'Sem Título')
        duracao = roteiro.get('estimativa_duracao', 'N/A')
        num_blocos = len(roteiro.get('blocos', []))
        
        msg = (
            f"📝 **ROTEIRO GERADO**\n\n"
            f"**Título:** {titulo}\n"
            f"**Duração:** {duracao}\n"
            f"**Blocos:** {num_blocos} cenas\n\n"
            f"Aprovar este roteiro para prosseguir com produção?"
        )
        
        keyboard = [
            [
                self.InlineKeyboardButton("✅ APROVAR", callback_data="roteiro_aprovar"),
                self.InlineKeyboardButton("❌ REFAZER", callback_data="roteiro_refazer")
            ]
        ]
        
        return self._enviar_e_aguardar(msg, keyboard, "roteiro")

    def enviar_imagens_aprovacao(self, imagens_paths: List[str]) -> bool:
        """Envia preview de imagens para aprovação."""
        console.print(f"[bold yellow]📱 Enviando {len(imagens_paths)} imagens para aprovação...[/bold yellow]")
        
        bot = self.Bot(token=self.token)
        
        # Enviar cada imagem
        for idx, img_path in enumerate(imagens_paths[:6]):  # Máximo 6 imagens
            try:
                with open(img_path, 'rb') as img:
                    bot.send_photo(
                        chat_id=self.chat_id,
                        photo=img,
                        caption=f"Cena {idx+1}/{len(imagens_paths)}"
                    )
            except Exception as e:
                console.print(f"[red]Erro ao enviar imagem {idx+1}: {e}[/red]")
        
        msg = f"🎨 **{len(imagens_paths)} IMAGENS GERADAS**\n\nAprovar essas imagens?"
        
        keyboard = [
            [
                self.InlineKeyboardButton("✅ APROVAR", callback_data="imagens_aprovar"),
                self.InlineKeyboardButton("🔄 REFAZER", callback_data="imagens_refazer")
            ]
        ]
        
        return self._enviar_e_aguardar(msg, keyboard, "imagens")

    def enviar_audio_aprovacao(self, audio_path: str) -> bool:
        """Envia sample de áudio para aprovação."""
        console.print("[bold yellow]📱 Enviando áudio para aprovação...[/bold yellow]")
        
        bot = self.Bot(token=self.token)
        
        # Enviar arquivo de áudio
        try:
            with open(audio_path, 'rb') as audio:
                bot.send_audio(
                    chat_id=self.chat_id,
                    audio=audio,
                    caption="🎤 Sample da Narração (Primeira Cena)"
                )
        except Exception as e:
            console.print(f"[red]Erro ao enviar áudio: {e}[/red]")
        
        msg = "🎤 **NARRAÇÃO GERADA**\n\nAprovar qualidade da voz?"
        
        keyboard = [
            [
                self.InlineKeyboardButton("✅ APROVAR", callback_data="audio_aprovar"),
                self.InlineKeyboardButton("🔄 REFAZER", callback_data="audio_refazer")
            ]
        ]
        
        return self._enviar_e_aguardar(msg, keyboard, "audio")

    def enviar_video_aprovacao(self, video_path: str) -> bool:
        """Envia vídeo final para aprovação."""
        console.print("[bold yellow]📱 Enviando vídeo final para aprovação...[/bold yellow]")
        
        bot = self.Bot(token=self.token)
        
        # Enviar vídeo
        try:
            with open(video_path, 'rb') as video:
                bot.send_video(
                    chat_id=self.chat_id,
                    video=video,
                    caption="🎬 VÍDEO FINAL RENDERIZADO",
                    supports_streaming=True
                )
        except Exception as e:
            console.print(f"[red]Erro ao enviar vídeo: {e}[/red]")
        
        msg = "🎬 **VÍDEO PRONTO**\n\nAprovar para publicação?"
        
        keyboard = [
            [
                self.InlineKeyboardButton("✅ PUBLICAR", callback_data="video_aprovar"),
                self.InlineKeyboardButton("❌ CANCELAR", callback_data="video_rejeitar")
            ]
        ]
        
        return self._enviar_e_aguardar(msg, keyboard, "video")

    def _enviar_e_aguardar(self, mensagem: str, keyboard: list, tipo: str) -> bool:
        """
        Envia mensagem com botões e aguarda resposta do usuário.
        Retorna True se aprovado, False se rejeitado.
        """
        bot = self.Bot(token=self.token)
        reply_markup = self.InlineKeyboardMarkup(keyboard)
        
        # Enviar mensagem
        try:
            msg = bot.send_message(
                chat_id=self.chat_id,
                text=mensagem,
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
            console.print(f"[green]✓ Mensagem enviada para Telegram (ID: {msg.message_id})[/green]")
        except Exception as e:
            console.print(f"[red]ERRO ao enviar para Telegram: {e}[/red]")
            raise RuntimeError(f"Falha na comunicação com Telegram: {e}")
        
        # Aguardar resposta
        console.print(f"[yellow]⏳ Aguardando aprovação no Telegram (timeout: {self.timeout_minutos}min)...[/yellow]")
        
        self.response_received = None
        resposta_esperada_prefix = f"{tipo}_"
        
        # Configurar handler de callback
        async def callback_handler(update, context):
            query = update.callback_query
            await query.answer()
            
            if query.data.startswith(resposta_esperada_prefix):
                self.response_received = query.data
                await query.edit_message_text(f"✓ Resposta registrada: {query.data}")
        
        # Polling simplificado (blocking)
        import asyncio
        
        async def aguardar_resposta():
            app = self.Application.builder().token(self.token).build()
            app.add_handler(self.CallbackQueryHandler(callback_handler))
            
            await app.initialize()
            await app.start()
            
            # Polling com timeout
            inicio = time.time()
            timeout_segundos = self.timeout_minutos * 60
            
            while self.response_received is None:
                await app.update_queue.get()
                await asyncio.sleep(1)
                
                if time.time() - inicio > timeout_segundos:
                    await app.stop()
                    await app.shutdown()
                    return False
            
            await app.stop()
            await app.shutdown()
            return True
        
        # Executar polling
        try:
            resultado = asyncio.run(aguardar_resposta())
        except Exception as e:
            console.print(f"[red]Erro no polling: {e}[/red]")
            raise RuntimeError(f"Falha ao aguardar resposta: {e}")
        
        if not resultado:
            console.print(f"[red]⏱️ TIMEOUT! Nenhuma resposta em {self.timeout_minutos} minutos.[/red]")
            return False
        
        # Processar resposta
        if self.response_received.endswith("_aprovar") or self.response_received.endswith("_publicar"):
            console.print("[bold green]✅ APROVADO pelo usuário![/bold green]")
            return True
        else:
            console.print("[bold red]❌ REJEITADO pelo usuário.[/bold red]")
            return False

    def enviar_alerta_emergencia(self, mensagem: str):
        """Envia alerta urgente."""
        bot = self.Bot(token=self.token)
        try:
            bot.send_message(
                chat_id=self.chat_id,
                text=f"🚨 **ALERTA URGENTE**\n\n{mensagem}",
                parse_mode='Markdown'
            )
            console.print(f"[red]🚨 Alerta enviado: {mensagem}[/red]")
        except Exception as e:
            console.print(f"[red]Erro ao enviar alerta: {e}[/red]")
