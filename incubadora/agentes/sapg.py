import os
import json
import time
import random
from rich.console import Console
from groq import Groq

console = Console()

class SAPG:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        self.client = Groq(api_key=self.api_key) if self.api_key else None

    def pesquisar_tendencias_globais(self):
        """
        Simula (ou realiza) a pesquisa de tendências globais.
        """
        console.print("[dim]🔄 SAPG: Conectando ao Google Trends (US/Global)...[/dim]")
        time.sleep(1.5)
        return [
            {"id": 1, "nicho_us": "Digital Folklore", "nicho_br": "Lendas da Internet", "score": 9.8},
            {"id": 2, "nicho_us": "Engineering Failures", "nicho_br": "Engenharia do Caos", "score": 9.6},
            {"id": 3, "nicho_us": "True Crime: Cults", "nicho_br": "Seitas Obscuras", "score": 9.4}
        ]

    def gerar_comparativo_hibrido(self, nichos_selecionados):
        """
        Gera comparativo e híbridos.
        """
        return {
            "sugestoes": [
                {"nome": "Cultos Digitais", "score": 9.9, "justificativa": "Alta demanda viral."},
                {"nome": "Arquivos Obscuros", "score": 9.5, "justificativa": "Mistério evergreen."},
                {"nome": "Psicologia das Seitas", "score": 9.2, "justificativa": "Educativo + Curiosidade."}
            ]
        }

    def gerar_estrategia_conteudo(self, nicho):
        """
        Gera 30 sugestões divididas em 5 eixos com notas.
        """
        eixos = ["Curiosidade", "Medo", "Conspiração", "Futuro", "História"]
        sugestoes = {}
        for eixo in eixos:
            sugestoes[eixo] = []
            for i in range(6):
                sugestoes[eixo].append({
                    "titulo": f"Ideia {i+1} para {eixo}",
                    "score": random.randint(85, 99)
                })
            sugestoes[eixo].sort(key=lambda x: x['score'], reverse=True)
        return sugestoes

    def gerar_configuracao_completa(self, nicho_escolhido):
        """
        Gera a configuração completa baseada no BLUEPRINT TOP 100.
        """
        return {
            "nome_canal": "Algoritmo Obscuro",
            "estilo_visual": "Glitch Art + Dark Cinematic",
            "voz": "pt-BR-Wavenet-B",
            "provider_imagens": "AWS EC2 Spot (Flux.1)",
            "duracao_ideal": "5 minutos (Foco em Retenção Máxima)",
            "analise_retencao": "Foco em retenção > 50%. Ritmo 168-187 wpm.",
            "formato_video": "LONGO (16:9) - Qualidade > Quantidade",
            "transicoes_ritmo": "Rápido (Cortes a cada 3-5s)",
            "efeitos_visuais": "Film Grain + VHS Overlay",
            "regra_integridade": "⚠️ FALHA DE CENA = REVISAR LOOP ATÉ PERFEIÇÃO (NÃO PARAR)",
            "audio_musica": "AUTOMÁTICO (IA Escolhe por Vídeo)",
            "frequencia_upload": "1 Vídeo por Semana (Sábado) - Regra Top 100",
            "thumb_estrategia": "Rosto + Fundo Escuro + Texto Curto (0-3 palavras)",
            "thumb_prompt": "hyper-realistic close-up of terrified face, dark background, 8k, high contrast",
            "pauta_inicial": [
                "Cicada 3301: O Mistério",
                "Heaven's Gate: A Verdade",
                "TikTok Cults: O Perigo"
            ]
        }
