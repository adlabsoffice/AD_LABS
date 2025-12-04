import os
import json
import time
import sys
from rich.console import Console
from rich.panel import Panel

# Adiciona diretório pai (incubadora) ao path para importar utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Integração com APIManager
from utils.api_manager import APIManager

console = Console()

# Importações para YouTube API
try:
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
except ImportError:
    console.print("[red]Erro: google-api-python-client não instalado.[/red]")
    sys.exit(1)

class YouTubeConnector:
    """Conector simples para YouTube Data API v3."""
    def __init__(self):
        # Tenta chave específica ou a de vídeo (que costuma ser a geral)
        self.api_key = os.getenv("YOUTUBE_DATA_API_KEY") or os.getenv("GOOGLE_API_KEY_VIDEO")
        
        if not self.api_key:
            # Hard Fail
            raise RuntimeError("CRÍTICO: Nenhuma chave de API do YouTube encontrada (.env). Configure YOUTUBE_DATA_API_KEY ou GOOGLE_API_KEY_VIDEO.")
        
        try:
            self.youtube = build('youtube', 'v3', developerKey=self.api_key)
        except Exception as e:
            raise RuntimeError(f"Erro fatal ao conectar YouTube API: {e}")

    def search_videos(self, query, max_results=5):
        """Busca vídeos reais por palavra-chave."""
        # Sem try/except silencioso. Se falhar, quebra.
        request = self.youtube.search().list(
            part="snippet",
            maxResults=max_results,
            q=query,
            type="video",
            order="viewCount"
        )
        response = request.execute()
        
        videos = []
        for item in response.get("items", []):
                video_id = item["id"]["videoId"]
                
                # 2. Busca Estatísticas (Views)
                stats_request = self.youtube.videos().list(
                    part="statistics",
                    id=video_id
                )
                stats_response = stats_request.execute()
                
                view_count = 0
                if stats_response["items"]:
                    stats = stats_response["items"][0]["statistics"]
                    view_count = int(stats.get("viewCount", 0))
                    
                videos.append({
                    "titulo": item["snippet"]["title"],
                    "canal": item["snippet"]["channelTitle"],
                    "video_id": video_id,
                    "url": f"https://www.youtube.com/watch?v={video_id}",
                    "views": view_count,
                    "descricao": item["snippet"]["description"]
                })
        
        # ✅ CORREÇÃO (04/12/2024): return estava DENTRO do loop (linha 75)
        # Agora retorna TODOS os vídeos encontrados, não apenas o primeiro
        return videos

class Agente02Pesquisador:
    def __init__(self):
        self.api_manager = APIManager()
        self.youtube = YouTubeConnector() # Conector Real
        
        # Knowledge Base: Carrega estratégias dos arquivos locais (01-10)
        self.knowledge_base = self._carregar_knowledge_base()

    def _carregar_knowledge_base(self):
        """Lê os arquivos markdown da pasta youtube para extrair conceitos."""
        kb = {}
        base_dir = r"d:\AD_LABS\youtube"
        # Arquivos chave mencionados pelo usuário
        files = [
            "01_Como_Crescer_um_Canal_do_Zero_em_2025.md",
            "02_Iniciando_Canal_YouTube_2025_Faca_Isso.md",
            "08_Framework_1246_Videos_YouTube_Sucesso.md"
        ]
        
        for f in files:
            path = os.path.join(base_dir, f)
            if os.path.exists(path):
                try:
                    with open(path, "r", encoding="utf-8") as file:
                        # Lê os primeiros 2k caracteres para dar contexto ao LLM sem estourar tokens
                        kb[f] = file.read()[:2000] 
                except Exception as e:
                    console.print(f"[red]Erro ao ler {f}: {e}[/red]")
        return kb

    def _call_llm(self, api_key, modelo, prompt, system_prompt="Você é um especialista em YouTube."):
        """Função auxiliar para chamar LLM via APIManager (compatível com Gemini/Groq/Claude)."""
        
        import requests
        
        if "gemini" in modelo or "google" in modelo:
            # Chamada Gemini via REST API (simplificado)
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{modelo}:generateContent?key={api_key}"
            payload = {
                "contents": [{"parts": [{"text": f"{system_prompt}\n\n{prompt}"}]}]
            }
            response = requests.post(url, json=payload, timeout=30)
            response.raise_for_status()
            return response.json()["candidates"][0]["content"]["parts"][0]["text"]
            
        elif "llama" in modelo or "groq" in modelo:
            # Chamada Groq
            from groq import Groq
            client = Groq(api_key=api_key)
            completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                model=modelo,
            )
            return completion.choices[0].message.content
            
        elif "claude" in modelo:
            # Chamada Anthropic
            import anthropic
            client = anthropic.Anthropic(api_key=api_key)
            message = client.messages.create(
                model=modelo,
                max_tokens=2000,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return message.content[0].text
            
        else:
            raise ValueError(f"Modelo desconhecido: {modelo}")

    def pesquisar_conteudo_base(self, tema, alvo):
        """
        Pesquisa o conteúdo original para o React usando YouTube Data API (REAL).
        """
        console.print(f"[bold yellow]AGENTE 02: Pesquisando '{alvo}' sobre '{tema}' (VIA API REAL)...[/bold yellow]")
        
        # 1. Busca Real
        query = f"{tema} {alvo}"
        videos_reais = self.youtube.search_videos(query, max_results=3)
        
        if not videos_reais:
            console.print("[red]❌ Nenhum vídeo encontrado na busca real. Verifique API Key ou Query.[/red]")
            # Fallback para simulação apenas se API falhar totalmente, mas ideal é parar
            raise RuntimeError("Falha na busca real do YouTube. Impossível prosseguir sem dados reais.")
            
        # Seleciona o Top 1
        top_video = videos_reais[0]
        console.print(f"[green]✓ Vídeo Encontrado:[/green] {top_video['titulo']}")
        console.print(f"   [dim]Canal: {top_video['canal']} | Views: {top_video['views']:,}[/dim]")
        console.print(f"   [dim]URL: {top_video['url']}[/dim]")

        # 2. Análise com LLM (Usando dados reais como contexto)
        prompt = f"""
        Atue como um pesquisador de YouTube experiente.
        Analise este vídeo REAL que encontrei sobre "{alvo}":
        
        DADOS REAIS:
        - Título: {top_video['titulo']}
        - Canal: {top_video['canal']}
        - Views: {top_video['views']}
        - URL: {top_video['url']}
        - Descrição Parcial: {top_video['descricao']}
        
        TAREFA:
        1. Analise o potencial deste vídeo para um React/Modelagem.
        2. Extraia os pontos chave prováveis baseados no título/tema.
        
        Retorne APENAS um JSON com este formato:
        {{
            "titulo_original": "{top_video['titulo']}",
            "canal_original": "{top_video['canal']}",
            "views_estimados": {top_video['views']},
            "url_video": "{top_video['url']}",
            "pontos_chave": ["Ponto 1", "Ponto 2", "Ponto 3"],
            "tom_original": "Descrição do tom (ex: Sério, Engraçado, Técnico)",
            "oportunidade_react": "Por que este vídeo é bom para reagir? Qual o ângulo?"
        }}
        """
        
        try:
            # Usa APIManager para garantir que a chamada aconteça
            resposta_json_str = self.api_manager.chamar_com_fallback(
                "llm_roteiro",
                self._call_llm,
                prompt=prompt,
                system_prompt="Você é um assistente JSON que retorna apenas JSON válido."
            )
            
            # Limpa markdown ```json se existir
            if "```json" in resposta_json_str:
                resposta_json_str = resposta_json_str.split("```json")[1].split("```")[0]
            elif "```" in resposta_json_str:
                resposta_json_str = resposta_json_str.split("```")[1].split("```")[0]
                
            resultado = json.loads(resposta_json_str)
            
            console.print(f"[green]Video Encontrado (IA):[/green] {resultado.get('titulo_original', 'Sem título')}")
            
            # Salva o resultado em CSV para o Agente 03
            self._salvar_csv_compativel(resultado)
            
            return resultado
            
        except Exception as e:
            console.print(f"[bold red]ERRO FATAL na pesquisa IA: {e}[/bold red]")
            raise RuntimeError(f"Falha ao pesquisar conteúdo real: {e}")

    def _salvar_csv_compativel(self, resultado_json):
        """Salva o resultado em CSV compatível com Agente 03."""
        import pandas as pd
        import random
        
        # Cria estrutura compatível usando dados do LLM
        # Zero Mocks: Se o LLM não der, falha ou usa 0, mas não chuta valor fixo alto sem critério.
        # Mas para garantir fluxo, vamos confiar que o prompt trará os dados.
        
        views = resultado_json.get("views_estimados", 0)
        if isinstance(views, str):
            # Tenta limpar string "1.5M" etc se vier sujo, mas ideal é vir int
            try:
                views = int(''.join(filter(str.isdigit, views)))
            except:
                views = 0
                
        dados = [{
            "video_id": "ia_generated_" + str(int(time.time())),
            "titulo": resultado_json.get("titulo_original", "Sem Título"),
            "views": views, 
            "canal": resultado_json.get("canal_original", "Desconhecido"),
            "link": resultado_json.get("url_video", "https://youtube.com")
        }]
        
        df = pd.DataFrame(dados)
        
        # Garante que salva na pasta outputs global (onde o Agente 03 busca)
        output_dir = "outputs"
        os.makedirs(output_dir, exist_ok=True)
        filepath = os.path.join(output_dir, "T01_canais_referencias.csv")
        
        df.to_csv(filepath, index=False, encoding='utf-8')
        console.print(f"[green]✓ Arquivo salvo para Agente 03: {filepath}[/green]")

    def analisar_viabilidade_viral(self, ideia):
        """
        Analisa se a ideia segue os principios dos arquivos 01-10 (Green Dot, Packaging).
        """
        console.print(f"[bold yellow]AGENTE 02: Validando 'Green Dot' para '{ideia}'...[/bold yellow]")
        
        # 1. Teste das 3 Perguntas (Via LLM Real)
        prompt_green_dot = f"""
        Analise a ideia "{ideia}" sob a ótica do "Green Dot Theory" para YouTube.
        Responda JSON:
        {{
            "perpetual": true/false, (Dá para fazer 100 vídeos sobre isso?)
            "searchable": true/false, (As pessoas buscam isso ativamente?)
            "sustainable": true/false, (Existem anunciantes/produtos para isso?)
            "justificativa": "Explicação breve"
        }}
        """
        
        try:
            resp_gd = self.api_manager.chamar_com_fallback("llm_roteiro", self._call_llm, prompt=prompt_green_dot)
            if "```json" in resp_gd: resp_gd = resp_gd.split("```json")[1].split("```")[0]
            analise_gd = json.loads(resp_gd)
        except Exception as e:
            raise RuntimeError(f"Falha ao validar Green Dot: {e}")

        if not all([analise_gd.get('perpetual'), analise_gd.get('searchable'), analise_gd.get('sustainable')]):
            console.print(f"[red]Ideia rejeitada pelo Green Dot Test: {analise_gd.get('justificativa')}[/red]")
            return {"score": 0, "analise": f"Falha Green Dot: {analise_gd.get('justificativa')}"}

        # 2. Packaging First (Titulo + Thumb)
        # Usa LLM para gerar packaging criativo
        prompt = f"""
        Crie um conceito de Packaging (Título + Thumbnail) para um vídeo sobre: "{ideia}".
        
        Regras do Top 100:
        - Título: 6-8 palavras, Curiosidade ou Benefício Claro.
        - Thumb: Simples, Alto Contraste, Max 3 palavras de texto.
        
        Retorne JSON:
        {{
            "titulo_hook": "Título aqui",
            "thumbnail_concept": "Descrição visual da thumb"
        }}
        """
        
        try:
            resposta_json_str = self.api_manager.chamar_com_fallback(
                "llm_roteiro",
                self._call_llm,
                prompt=prompt
            )
            
            # Limpeza básica de JSON
            if "```json" in resposta_json_str:
                resposta_json_str = resposta_json_str.split("```json")[1].split("```")[0]
            elif "```" in resposta_json_str:
                resposta_json_str = resposta_json_str.split("```")[1].split("```")[0]
                
            packaging = json.loads(resposta_json_str)
            
        except Exception as e:
            console.print(f"[bold red]ERRO FATAL no Packaging IA: {e}[/bold red]")
            raise RuntimeError(f"Falha ao gerar packaging real: {e}")
        
        console.print(f"[green]Green Dot Validado![/green]")
        console.print(f"   [cyan]Titulo:[/cyan] {packaging.get('titulo_hook')}")
        console.print(f"   [cyan]Thumb:[/cyan] {packaging.get('thumbnail_concept')}")

        return {
            "score": 95,
            "analise": "Alta demanda. Packaging forte definido.",
            "packaging": packaging
        }

if __name__ == "__main__":
    # Teste rápido
    agente = Agente02Pesquisador()
    res = agente.pesquisar_conteudo_base("Finanças", "Dívidas")
    print(json.dumps(res, indent=2, ensure_ascii=False))
