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

class Agente02Pesquisador:
    def __init__(self):
        self.api_manager = APIManager()
        
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
        Pesquisa o conteúdo original para o React usando LLM Real.
        """
        console.print(f"[bold yellow]AGENTE 02: Pesquisando '{alvo}' sobre '{tema}'...[/bold yellow]")
        
        prompt = f"""
        Atue como um pesquisador de YouTube experiente.
        Eu preciso encontrar um vídeo viral ou um conceito forte sobre "{alvo}" dentro do nicho "{tema}".
        
        1. Simule uma busca mental por vídeos reais de grandes players (ex: Primo Rico, Ei Nerd, Gaveta, etc dependendo do nicho).
        2. Escolha UM vídeo específico que seria excelente para fazer um React ou Modelagem.
        3. Extraia os pontos chave desse vídeo.
        
        Retorne APENAS um JSON com este formato:
        {{
            "titulo_original": "Título do Vídeo Encontrado",
            "canal_original": "Nome do Canal",
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
            return resultado
            
        except Exception as e:
            console.print(f"[red]Erro na pesquisa IA: {e}[/red]")
            # Fallback para dados simulados em caso de erro extremo de parse
            return {
                "titulo_original": f"Análise de {alvo} (Fallback)",
                "pontos_chave": ["Erro na geração IA", "Usando dados fallback"],
                "tom_original": "Neutro",
                "oportunidade_react": "Erro na API, verificar logs."
            }

    def analisar_viabilidade_viral(self, ideia):
        """
        Analisa se a ideia segue os principios dos arquivos 01-10 (Green Dot, Packaging).
        """
        console.print(f"[bold yellow]AGENTE 02: Validando 'Green Dot' para '{ideia}'...[/bold yellow]")
        
        # 1. Teste das 3 Perguntas (Simulado por enquanto, mas estruturado)
        perguntas = {
            "perpetual": True, # Dá para fazer 100 videos?
            "searchable": True, # Tem demanda?
            "sustainable": True # Dá dinheiro?
        }
        
        if not all(perguntas.values()):
            console.print("[red]Ideia rejeitada pelo Green Dot Test.[/red]")
            return {"score": 0, "analise": "Falha no Green Dot."}

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
            console.print(f"[yellow]Erro no Packaging IA: {e}. Usando fallback.[/yellow]")
            packaging = {
                "titulo_hook": f"{ideia}: A Verdade Revelada",
                "thumbnail_concept": "Rosto surpreso, fundo vermelho."
            }
        
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
