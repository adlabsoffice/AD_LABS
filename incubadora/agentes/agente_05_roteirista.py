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
        
        # Simulação de chamada ao Gemini
        time.sleep(2)
        
        # Mock do Roteiro (Estrutura de Retenção)
        roteiro = {
            "titulo_otimizado": titulo_hook,
            "blocos": [
                {
                    # HOOK (0-5s): Curiosidade Imediata. Sem "Oi galera".
                    "tempo": "00:00-00:05",
                    "personagem": "Jesus",
                    "fala": "Você prefere ser rico na terra ou herdeiro do universo? A escolha é agora.",
                    "visual": "Close extremo no rosto de Jesus, olho no olho. Corte rápido para pilha de ouro vs luz divina."
                },
                {
                    # RE-HOOK (5-15s): Contexto Rápido
                    "tempo": "00:05-00:15",
                    "personagem": "Jesus",
                    "fala": "O Primo Rico ensina a multiplicar moedas. Eu ensino a multiplicar vidas. Vamos ver onde ele errou.",
                    "visual": "Jesus assistindo o vídeo do Primo Rico em um tablet holográfico. Expressão analítica."
                },
                {
                    # CONTEUDO (15s+): Entrega de Valor
                    "tempo": "00:15-00:45",
                    "personagem": "Jesus",
                    "fala": "Juros compostos são poderosos, mas a generosidade rende 100 por 1. O erro não é investir, é amar o investimento.",
                    "visual": "Gráfico de juros subindo, mas sendo ultrapassado por uma árvore dourada crescendo rapidamente."
                }
            ]
        }
        
        return roteiro

    def _roteiro_mock(self):
        # Fallback simples
        return [
            {
                "tempo": "00:00",
                "personagem": "Jesus",
                "fala": "Pare de correr atrás do vento. Escute isso.",
                "visual": "Jesus parando o scroll da tela com a mão."
            }
        ]
