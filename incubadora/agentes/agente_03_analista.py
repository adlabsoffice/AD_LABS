"""
AGENTE 03: ANALISTA
Timestamp: T=2
Responsabilidade: Analisar vídeos coletados, agrupar por emoções e criar clusters
"""

import os
import json
import sys
import pandas as pd
from typing import Dict, List
from collections import Counter
from rich.console import Console
from rich.panel import Panel
from rich.progress import track

# Adiciona diretório pai (incubadora) ao path para importar utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Integração com APIManager
from utils.api_manager import APIManager

console = Console()


class ErroCSVInvalido(Exception):
    """Exceção para CSV inválido."""
    pass


class Agente03Analista:
    """
    Agente 03: Analista
    
    O QUE FAZ:
    1. Pega lista de vídeos do YouTube (CSV do Agente 02)
    2. Limpa dados ruins
    3. Agrupa vídeos por palavras-chave (Clustering Simples)
    4. Usa LLM (via APIManager) para analisar e descrever cada cluster
    5. Salva grupos encontrados em JSON
    """
    
    def __init__(self, config: Dict = None):
        self.input_path = "outputs"
        self.output_path = "outputs"
        self.csv_file = "T01_canais_referencias.csv"
        self.output_file = "T02_clusters.json"
        self.api_manager = APIManager()
        self.config = config or {}
        
        # Padrões emocionais (Dinâmico via Config ou Fallback Genérico)
        self.padroes_emocionais = self.config.get("padroes_emocionais", {
            "humilhação → revanche": ["zombar", "humilhar", "vingança", "justiça", "bullying"],
            "segredo → revelação": ["segredo", "descobrir", "verdade", "revelar", "esconder"],
            "medo → alívio": ["terror", "medo", "susto", "sobrevivência"],
            "injustiça → reparação": ["injusto", "cruel", "triste", "justiça"],
            "curiosidade → recompensa": ["mistério", "incrível", "surpreendente", "descoberta"]
        })
    
    def _call_llm(self, api_key, modelo, prompt, system_prompt="Você é um analista de dados especialista em YouTube."):
        """Função auxiliar para chamar LLM via APIManager."""
        import requests
        
        if "gemini" in modelo or "google" in modelo:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{modelo}:generateContent?key={api_key}"
            payload = {"contents": [{"parts": [{"text": f"{system_prompt}\n\n{prompt}"}]}]}
            response = requests.post(url, json=payload, timeout=30)
            response.raise_for_status()
            return response.json()["candidates"][0]["content"]["parts"][0]["text"]
            
        elif "llama" in modelo or "groq" in modelo:
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
            import anthropic
            client = anthropic.Anthropic(api_key=api_key)
            message = client.messages.create(
                model=modelo,
                max_tokens=2000,
                system=system_prompt,
                messages=[{"role": "user", "content": prompt}]
            )
            return message.content[0].text
        else:
            raise ValueError(f"Modelo desconhecido: {modelo}")

    def carregar_csv(self) -> pd.DataFrame:
        filepath = os.path.join(self.input_path, self.csv_file)
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Arquivo {filepath} não encontrado.")
        try:
            df = pd.read_csv(filepath, encoding='utf-8')
            console.print(f"[green]✓ CSV carregado: {len(df)} vídeos[/green]")
            return df
        except Exception as e:
            raise ErroCSVInvalido(f"Erro ao ler CSV: {e}")
    
    def validar_csv(self, df: pd.DataFrame) -> bool:
        campos_obrigatorios = ['video_id', 'titulo', 'views']
        campos_faltantes = [c for c in campos_obrigatorios if c not in df.columns]
        if campos_faltantes:
            raise ErroCSVInvalido(f"Campos faltando: {', '.join(campos_faltantes)}")
        return True
    
    def limpar_dados(self, df: pd.DataFrame) -> pd.DataFrame:
        console.print("\n[bold]Limpando dados...[/bold]")
        df_original = len(df)
        df = df.drop_duplicates(subset=['video_id'])
        if 'duracao_segundos' in df.columns:
            df = df[df['duracao_segundos'] >= 60]
        df = df[df['views'] >= 5000]
        palavras_musica = ['official music', 'lyric video', 'música', 'clipe']
        for palavra in palavras_musica:
            df = df[~df['titulo'].str.lower().str.contains(palavra, na=False)]
        console.print(f"[green]✓ Dados limpos: {len(df)} vídeos (era {df_original})[/green]")
        return df
    
    def extrair_palavras_chave(self, titulos: List[str]) -> List[str]:
        texto_completo = ' '.join(titulos).lower()
        import re
        palavras = re.findall(r'\b\w+\b', texto_completo)
        stopwords = ['o', 'a', 'de', 'que', 'e', 'do', 'da', 'em', 'um', 'para', 'é', 'com', 'não', 'uma', 'os', 'no', 'se', 'na', 'por', 'mais', 'as', 'dos', 'como', 'mas', 'foi', 'ao', 'ele', 'das', 'tem', 'à', 'seu', 'sua', 'ou', 'ser', 'quando', 'muito', 'há', 'nos', 'vídeo', 'video']
        palavras_filtradas = [p for p in palavras if p not in stopwords and len(p) > 3]
        contador = Counter(palavras_filtradas)
        return [palavra for palavra, count in contador.most_common(10)]
    
    def analisar_cluster_com_ia(self, titulos: List[str], palavras_chave: List[str]) -> Dict:
        """Usa LLM para analisar o cluster e dar nome/emoção."""
        
        prompt = f"""
        Analise este grupo de títulos de vídeos do YouTube:
        {json.dumps(titulos[:15], ensure_ascii=False)}
        
        Palavras-chave: {', '.join(palavras_chave)}
        
        Identifique o padrão emocional e narrativo que une esses vídeos.
        Retorne JSON:
        {{
            "nome_cluster": "Nome curto e descritivo (ex: Vingança no Trabalho)",
            "emocao_central": "Emoção dominante (ex: Humilhação -> Revanche)",
            "descricao": "Explicação breve do padrão encontrado",
            "saturacao": "alta/média/baixa",
            "forca_viral": "alta/média/baixa"
        }}
        """
        
        try:
            resposta_json_str = self.api_manager.chamar_com_fallback(
                "llm_roteiro",
                self._call_llm,
                prompt=prompt,
                system_prompt="Você é um analista de tendências do YouTube. Retorne apenas JSON."
            )
            
            if "```json" in resposta_json_str:
                resposta_json_str = resposta_json_str.split("```json")[1].split("```")[0]
            elif "```" in resposta_json_str:
                resposta_json_str = resposta_json_str.split("```")[1].split("```")[0]
                
            return json.loads(resposta_json_str)
            
        except Exception as e:
            console.print(f"[yellow]Erro na análise IA do cluster: {e}. Usando fallback.[/yellow]")
            return {
                "nome_cluster": f"Cluster {palavras_chave[0].title()}",
                "emocao_central": "Mista",
                "descricao": "Análise automática falhou, cluster baseado em palavras-chave.",
                "saturacao": "média",
                "forca_viral": "média"
            }

    def fazer_clustering_simples(self, df: pd.DataFrame) -> List[Dict]:
        console.print("\n[bold]Agrupando vídeos e analisando com IA...[/bold]")
        clusters = []
        df_restante = df.copy()
        cluster_id = 0
        
        while len(df_restante) > 0 and cluster_id < 6:
            sample_titulos = df_restante['titulo'].head(50).tolist()
            palavras_chave = self.extrair_palavras_chave(sample_titulos)
            
            if not palavras_chave:
                break
            
            palavra_principal = palavras_chave[0]
            mask = df_restante['titulo'].str.lower().str.contains(palavra_principal, na=False)
            cluster_videos = df_restante[mask]
            
            if len(cluster_videos) < 10: # Tolerância menor
                df_restante = df_restante[~mask]
                continue
            
            # Análise IA
            analise = self.analisar_cluster_com_ia(
                cluster_videos['titulo'].tolist(),
                palavras_chave
            )
            
            views_medias = int(cluster_videos['views'].mean())
            
            cluster = {
                "id": f"cluster_{cluster_id}",
                "nome": analise['nome_cluster'],
                "descricao": analise['descricao'],
                "tamanho": len(cluster_videos),
                "exemplos_titulos": cluster_videos['titulo'].head(5).tolist(),
                "metricas": {
                    "views_medias": views_medias,
                    "engajamento_medio": 0.05,
                    "viral_score_medio": 1.0
                },
                "palavras_chave": palavras_chave[:10],
                "emocao_central": analise['emocao_central'],
                "saturacao": analise['saturacao'],
                "forca_viral": analise['forca_viral']
            }
            
            clusters.append(cluster)
            console.print(f"[green]✓ Cluster {cluster_id}: {analise['nome_cluster']} ({len(cluster_videos)} vídeos)[/green]")
            
            df_restante = df_restante[~mask]
            cluster_id += 1
        
        return clusters
    
    def salvar_json(self, dados: Dict, filename: str):
        filepath = os.path.join(self.output_path, filename)
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(dados, f, indent=2, ensure_ascii=False)
            console.print(f"[green]✅ Arquivo salvo: {filepath}[/green]")
        except Exception as e:
            console.print(f"[red]Erro ao salvar {filename}: {e}[/red]")
            raise
    
    def atualizar_progress(self, num_clusters: int):
        progress_file = os.path.join(self.output_path, "progress.json")
        try:
            if os.path.exists(progress_file):
                with open(progress_file, "r", encoding="utf-8") as f:
                    progress = json.load(f)
            else:
                progress = {}
            
            progress.update({
                "timestamp_atual": "T=2",
                "ultimo_agente": "analista",
                "status": "clusters_criados",
                "proxima_acao": "Executar Agente 04: Arquiteto de Eixos",
                "checkpoint": {
                    "clusters_identificados": num_clusters,
                    "eixos_criados": 0,
                    "ideias_geradas": 0,
                    "videos_produzidos": 0
                }
            })
            
            with open(progress_file, "w", encoding="utf-8") as f:
                json.dump(progress, f, indent=2, ensure_ascii=False)
        except Exception:
            pass
    
    def executar(self) -> Dict:
        console.print(Panel.fit(
            "[bold cyan]🧠 AGENTE 03: ANALISTA[/bold cyan]\n"
            "[Analisa vídeos e identifica padrões emocionais (T=2)]",
            title="Análise de Clusters"
        ))
        
        try:
            console.print("\n[bold]Passo 1: Carregando vídeos[/bold]")
            df = self.carregar_csv()
            self.validar_csv(df)
            
            console.print("\n[bold]Passo 2: Limpando dados[/bold]")
            df_limpo = self.limpar_dados(df)
            
            console.print("\n[bold]Passo 3: Agrupando vídeos similares[/bold]")
            clusters = self.fazer_clustering_simples(df_limpo)
            
            if len(clusters) == 0:
                console.print("[yellow]⚠ Nenhum cluster identificado. Criando cluster geral...[/yellow]")
                analise = self.analisar_cluster_com_ia(df_limpo['titulo'].tolist(), ["geral"])
                clusters = [{
                    "id": "cluster_0",
                    "nome": analise['nome_cluster'],
                    "tamanho": len(df_limpo),
                    "exemplos_titulos": df_limpo['titulo'].head(5).tolist(),
                    "palavras_chave": ["geral"],
                    "emocao_central": analise['emocao_central'],
                    "saturacao": "média",
                    "forca_viral": "média"
                }]
            
            resultado = {
                "timestamp": "T=2",
                "estatisticas": {
                    "videos_brutos": len(df),
                    "videos_limpos": len(df_limpo),
                    "clusters_identificados": len(clusters),
                    "videos_descartados": len(df) - len(df_limpo)
                },
                "clusters": clusters
            }
            
            self.salvar_json(resultado, self.output_file)
            self.atualizar_progress(len(clusters))
            
            console.print("\n" + "="*60)
            console.print(f"[bold green]✅ {len(clusters)} CLUSTERS IDENTIFICADOS![/bold green]")
            console.print("="*60 + "\n")
            
            return resultado
            
        except Exception as e:
            console.print(f"[bold red]❌ Erro: {e}[/bold red]")

def main():
    """Teste standalone do agente."""
    agente = Agente03Analista(config={})
    agente.executar()


if __name__ == "__main__":
    main()
