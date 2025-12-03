import os
import json
import requests
import time
from rich.console import Console

console = Console()

class Agente05Roteirista:
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY_VIDEO") or os.getenv("GOOGLE_API_KEY")
        self.model = "gemini-2.0-flash-exp" 

    def gerar_roteiro_react(self, pesquisa, config_canal):
        """
        Gera um roteiro de React focado em RETENÇÃO (Hook 0-5s).
        """
        # Recupera o Packaging definido pelo Agente 02 (se disponivel)
        packaging = pesquisa.get("packaging", {})
        titulo_hook = packaging.get("titulo_hook", "Titulo Padrao")
        
        console.print(f"[bold yellow]AGENTE 05: Escrevendo Roteiro 'Retention-First'...[/bold yellow]")
        console.print(f"   [cyan]Foco:[/cyan] Hook de 5s para '{titulo_hook}'")
        
        # Chamada REAL ao LLM para gerar o roteiro
        prompt = f"""
        Você é um Roteirista Expert em retenção para vídeos curtos (Reels/TikTok).
        
        CONTEXTO:
        - Título/Hook: "{titulo_hook}"
        - Objetivo: Segurar a atenção nos primeiros 3 segundos e manter até o final.
        
        TAREFA:
        Crie um roteiro JSON para um vídeo de 45-60 segundos.
        Estrutura obrigatória:
        1. HOOK (0-5s): Frase impactante, visual chocante.
        2. RE-HOOK (5-15s): Contexto rápido, conexão com o espectador.
        3. CORPO (15-45s): Entrega de valor, história ou curiosidade.
        4. CTA (45-60s): Chamada para ação clara.

        FORMATO DE SAÍDA (JSON Puro):
        {{
            "titulo_otimizado": "Titulo Final",
            "blocos": [
                {{
                    "tempo": "00:00-00:05",
                    "personagem": "Narrador",
                    "fala": "Texto falado...",
                    "visual": "Descrição visual detalhada para IA de imagem..."
                }}
            ]
        }}
        """

        try:
            # Importação tardia para evitar ciclo, ou assumindo que utils está no path
            from utils.api_manager import APIManager
            api = APIManager()
            
            console.print(f"   [cyan]Solicitando roteiro ao LLM...[/cyan]")
            resposta_json = api.generate_json(prompt)
            
            if not resposta_json:
                raise RuntimeError("LLM retornou resposta vazia para o roteiro.")
                
            console.print(f"      -> [green]Roteiro Gerado com Sucesso![/green]")
            return resposta_json

        except Exception as e:
            console.print(f"      -> [bold red]ERRO FATAL: Falha ao gerar roteiro real![/bold red]")
            console.print(f"      -> [red]{e}[/red]")
            raise RuntimeError(f"Falha na geração do roteiro: {e}")
