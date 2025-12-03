import os
import json
import time
import random
from rich.console import Console
from groq import Groq

# Importações para YouTube API
try:
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
except ImportError:
    print("Erro: google-api-python-client não instalado.")

console = Console()

class SAPG:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        # Tenta chave específica ou a de vídeo (que costuma ser a geral)
        self.youtube_key = os.getenv("YOUTUBE_DATA_API_KEY") or os.getenv("GOOGLE_API_KEY_VIDEO")
        
        self.client = Groq(api_key=self.api_key) if self.api_key else None
        
        if self.youtube_key:
            try:
                self.youtube = build('youtube', 'v3', developerKey=self.youtube_key)
            except Exception as e:
                # Hard Fail na inicialização se a chave for inválida
                raise RuntimeError(f"Erro fatal ao conectar YouTube API: {e}")
        else:
            # Hard Fail se não houver chave
            raise RuntimeError("CRÍTICO: Nenhuma chave de API do YouTube encontrada (.env). Configure YOUTUBE_DATA_API_KEY ou GOOGLE_API_KEY_VIDEO.")

    def _get_trending_videos(self, region_code="US", max_results=10):
        """Busca vídeos em alta (Most Popular) na região especificada."""
        # Sem try/except silencioso. Se falhar, quebra.
        request = self.youtube.videos().list(
            part="snippet",
            chart="mostPopular",
            regionCode=region_code,
            maxResults=max_results
        )
        response = request.execute()
        return [item["snippet"]["title"] for item in response.get("items", [])]

    def _call_llm_json(self, prompt, system_prompt="Você é um analista de tendências."):
        """Helper para chamar Groq e retornar JSON."""
        if not self.client:
            raise RuntimeError("GROQ_API_KEY não configurada.")
            
        completion = self.client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.7,
            response_format={"type": "json_object"}
        )
        return json.loads(completion.choices[0].message.content)

    def pesquisar_tendencias_globais(self):
        """
        Realiza pesquisa REAL de tendências globais usando YouTube Data API + LLM.
        """
        console.print("[bold cyan]🔄 SAPG: Buscando Tendências Reais no YouTube (US & BR)...[/bold cyan]")
        
        # 1. Busca Dados Reais (Vai quebrar se der erro, como solicitado)
        trends_us = self._get_trending_videos("US", 15)
        trends_br = self._get_trending_videos("BR", 15)
        
        console.print(f"[dim]Analisando {len(trends_us)} vídeos US e {len(trends_br)} vídeos BR...[/dim]")

        # 2. Análise LLM
        prompt = f"""
        Analise estas listas de vídeos em alta no YouTube agora:
        
        TRENDS US: {json.dumps(trends_us)}
        TRENDS BR: {json.dumps(trends_br)}
        
        Identifique 3 "Nichos/Subculturas" emergentes que conectam esses vídeos ou que estão em alta implícita.
        Não quero notícias do dia, quero TÓPICOS DE CANAL (ex: True Crime, Tech Fails, ASMR, Finanças Pessoais).
        
        Retorne JSON:
        {{
            "oportunidades": [
                {{"id": 1, "nicho_us": "Nome em Inglês", "nicho_br": "Nome em Português", "score": 9.5}},
                {{"id": 2, "nicho_us": "Nome em Inglês", "nicho_br": "Nome em Português", "score": 9.0}},
                {{"id": 3, "nicho_us": "Nome em Inglês", "nicho_br": "Nome em Português", "score": 8.5}}
            ]
        }}
        """
        
        try:
            resultado = self._call_llm_json(prompt)
            return resultado.get("oportunidades", [])
        except Exception as e:
            console.print(f"[red]Erro na análise IA: {e}[/red]")
            return []

    def gerar_comparativo_hibrido(self, nichos_selecionados):
        """
        Gera comparativo e híbridos via LLM.
        """
        prompt = f"""
        Analise estes nichos selecionados:
        {json.dumps(nichos_selecionados)}
        
        Sugira 3 ideias de canais HÍBRIDOS que misturem esses conceitos.
        
        Retorne JSON:
        {{
            "sugestoes": [
                {{"nome": "Nome do Híbrido", "score": 9.9, "justificativa": "Por que vai viralizar"}}
            ]
        }}
        """
        try:
            return self._call_llm_json(prompt)
        except Exception:
            return {"sugestoes": []}

    def gerar_estrategia_conteudo(self, nicho):
        """
        Gera 30 sugestões reais via LLM.
        """
        prompt = f"""
        Crie uma estratégia de conteúdo para um canal sobre "{nicho}".
        Gere 5 Eixos Editoriais e 6 ideias de vídeo para cada eixo (Total 30).
        
        Retorne JSON:
        {{
            "Eixo 1": [{{"titulo": "Ideia 1", "score": 95}}, ...],
            ...
        }}
        """
        try:
            return self._call_llm_json(prompt)
        except Exception:
            return {}

    def gerar_configuracao_completa(self, nicho_escolhido):
        """
        Gera configuração completa via LLM baseada no nicho.
        """
        prompt = f"""
        Crie a configuração técnica PERFEITA para um canal Dark sobre "{nicho_escolhido}".
        Baseie-se em canais de sucesso atuais.
        
        Retorne JSON:
        {{
            "nome_canal": "Nome Criativo",
            "estilo_visual": "Estilo (ex: Dark Cinematic, Minimalist)",
            "voz": "Estilo da voz",
            "provider_imagens": "Melhor IA para isso",
            "duracao_ideal": "Tempo ideal",
            "analise_retencao": "Dica de retenção",
            "formato_video": "16:9",
            "transicoes_ritmo": "Ritmo de edição",
            "efeitos_visuais": "VFX sugeridos",
            "regra_integridade": "Regra de ouro",
            "audio_musica": "Estilo musical",
            "frequencia_upload": "Frequência ideal",
            "thumb_estrategia": "Estratégia de Thumbnail",
            "thumb_prompt": "Prompt base para thumb",
            "pauta_inicial": ["Ideia 1", "Ideia 2", "Ideia 3"]
        }}
        """
        try:
            return self._call_llm_json(prompt)
        except Exception:
            return {"nome_canal": "Erro na Geração", "pauta_inicial": []}
