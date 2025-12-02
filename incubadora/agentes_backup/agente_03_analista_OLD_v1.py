"""
AGENTE 03: ANALISTA
Timestamp: T=2
Responsabilidade: Analisar vídeos coletados, agrupar por emoções e criar clusters
"""

import os
import json
import pandas as pd
from typing import Dict, List
from collections import Counter
from rich.console import Console
from rich.panel import Panel
from rich.progress import track

console = Console()


class ErroCSVInvalido(Exception):
    """Exceção para CSV inválido."""
    pass


class Agente03Analista:
    """
    Agente 03: Analista
    
    O QUE FAZ (em linguagem simples):
    1. Pega lista de vídeos do YouTube (CSV do Agente 02)
    2. Limpa dados ruins (vídeos muito curtos, poucos views, etc.)
    3. Agrupa vídeos que falam sobre emoções parecidas
    4. Identifica padrões emocionais (ex: "humilhação → vingança")
    5. Salva grupos encontrados em JSON
    """
    
    def __init__(self):
        self.input_path = "outputs"
        self.output_path = "outputs"
        self.csv_file = "T01_canais_referencias.csv"
        self.output_file = "T02_clusters.json"
        
        # Padrões emocionais que vamos procurar nos títulos
        self.padroes_emocionais = {
            "humilhação → revanche": [
                "zombar", "humilhar", "se arrepender", "vingança", 
                "justiça", "bullying", "provocar"
            ],
            "segredo → revelação": [
                "segredo", "descobrir", "verdade", "revelar", 
                "esconder", "revelação", "confissão"
            ],
            "medo → alívio": [
                "terror", "medo", "susto", "assustador", 
                "salvação", "escape", "sobrevivência"
            ],
            "injustiça → reparação": [
                "injusto", "cruel", "triste", "final feliz", 
                "justiça", "injustiça"
            ],
            "curiosidade → recompensa": [
                "mistério", "incrível", "surpreendente", 
                "impressionante", "descoberta", "revelado"
            ]
        }
    
    def carregar_csv(self) -> pd.DataFrame:
        """
        Carrega CSV de vídeos do Agente 02.
        
        SIMPLES: Abre o arquivo Excel (CSV) com lista de vídeos
        """
        filepath = os.path.join(self.input_path, self.csv_file)
        
        if not os.path.exists(filepath):
            raise FileNotFoundError(
                f"Arquivo {filepath} não encontrado. "
                "Execute Agente 02 (Pesquisador) primeiro."
            )
        
        try:
            df = pd.read_csv(filepath, encoding='utf-8')
            console.print(f"[green]✓ CSV carregado: {len(df)} vídeos[/green]")
            return df
        except Exception as e:
            raise ErroCSVInvalido(f"Erro ao ler CSV: {e}")
    
    def validar_csv(self, df: pd.DataFrame) -> bool:
        """
        Verifica se CSV tem campos necessários.
        
        SIMPLES: Checa se a planilha tem as colunas que a gente precisa
        """
        campos_obrigatorios = ['video_id', 'titulo', 'views']
        campos_faltantes = [c for c in campos_obrigatorios if c not in df.columns]
        
        if campos_faltantes:
            raise ErroCSVInvalido(
                f"Campos obrigatórios faltando no CSV: {', '.join(campos_faltantes)}"
            )
        
        if len(df) < 50:
            console.print(f"[yellow]⚠ Poucos vídeos ({len(df)}). Ideal: 200+[/yellow]")
        
        return True
    
    def limpar_dados(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Remove vídeos que não servem.
        
        SIMPLES: 
        - Remove vídeos repetidos
        - Remove vídeos muito curtos (menos de 1 minuto)
        - Remove vídeos com poucos views (menos de 5.000)
        - Remove músicas e clipes
        """
        console.print("\n[bold]Limpando dados...[/bold]")
        
        df_original = len(df)
        
        # 1. Remove duplicatas
        df = df.drop_duplicates(subset=['video_id'])
        console.print(f"[dim]Duplicatas removidas: {df_original - len(df)}[/dim]")
        
        # 2. Remove vídeos muito curtos (se tiver coluna de duração)
        if 'duracao_segundos' in df.columns:
            df = df[df['duracao_segundos'] >= 60]
            console.print(f"[dim]Vídeos muito curtos removidos[/dim]")
        
        # 3. Remove vídeos com poucos views
        df = df[df['views'] >= 5000]
        console.print(f"[dim]Vídeos com poucos views removidos[/dim]")
        
        # 4. Remove músicas/clipes (procura por palavras no título)
        palavras_musica = ['official music', 'lyric video', 'música', 'clipe']
        for palavra in palavras_musica:
            df = df[~df['titulo'].str.lower().str.contains(palavra, na=False)]
        console.print(f"[dim]Músicas/clipes removidos[/dim]")
        
        console.print(f"[green]✓ Dados limpos: {len(df)} vídeos (era {df_original})[/green]")
        
        return df
    
    def extrair_palavras_chave(self, titulos: List[str]) -> List[str]:
        """
        Encontra palavras mais comuns nos títulos.
        
        SIMPLES: Pega os títulos e conta quais palavras aparecem mais
        """
        # Junta todos títulos
        texto_completo = ' '.join(titulos).lower()
        
        # Remove pontuação e quebra em palavras
        import re
        palavras = re.findall(r'\b\w+\b', texto_completo)
        
        # Remove palavras muito comuns (stopwords)
        stopwords = [
            'o', 'a', 'de', 'que', 'e', 'do', 'da', 'em', 'um', 'para',
            'é', 'com', 'não', 'uma', 'os', 'no', 'se', 'na', 'por', 'mais',
            'as', 'dos', 'como', 'mas', 'foi', 'ao', 'ele', 'das', 'tem',
            'à', 'seu', 'sua', 'ou', 'ser', 'quando', 'muito', 'há', 'nos'
        ]
        palavras_filtradas = [p for p in palavras if p not in stopwords and len(p) > 3]
        
        # Conta frequência
        contador = Counter(palavras_filtradas)
        
        # Retorna top 10
        return [palavra for palavra, count in contador.most_common(10)]
    
    def identificar_emocao(self, palavras_chave: List[str], titulos: List[str]) -> str:
        """
        Identifica qual emoção domina neste grupo de vídeos.
        
        SIMPLES: Compara palavras dos títulos com nossos padrões emocionais
        """
        scores = {}
        
        # Para cada padrão emocional, conta quantas palavras batem
        for emocao, keywords in self.padroes_emocionais.items():
            score = 0
            
            # Conta palavras-chave que batem
            for palavra in palavras_chave:
                if any(kw in palavra or palavra in kw for kw in keywords):
                    score += 2  # Peso maior para palavras-chave
            
            # Conta também nos títulos completos
            for titulo in titulos[:20]:  # Analisa primeiros 20 títulos
                titulo_lower = titulo.lower()
                for kw in keywords:
                    if kw in titulo_lower:
                        score += 1
            
            scores[emocao] = score
        
        # Retorna emoção com maior score
        if max(scores.values()) > 0:
            return max(scores, key=scores.get)
        else:
            return "emoção genérica"
    
    def fazer_clustering_simples(self, df: pd.DataFrame) -> List[Dict]:
        """
        Agrupa vídeos por palavras-chave similares.
        
        SIMPLES:
        Versão simplificada sem IA complexa.
        Agrupa baseado em palavras-chave comuns nos títulos.
        """
        console.print("\n[bold]Agrupando vídeos por similaridade...[/bold]")
        
        # Para simplificar, vamos agrupar por palavras-chave dominantes
        # Cria grupos baseados em palavras mais comuns
        
        clusters = []
        df_restante = df.copy()
        cluster_id = 0
        
        while len(df_restante) > 0 and cluster_id < 6:
            # Pega amostra de títulos
            sample_titulos = df_restante['titulo'].head(50).tolist()
            
            # Extrai palavras-chave desta amostra
            palavras_chave = self.extrair_palavras_chave(sample_titulos)
            
            if not palavras_chave:
                break
            
            # Palavra mais comum define este cluster
            palavra_principal = palavras_chave[0]
            
            # Pega vídeos que contém essa palavra
            mask = df_restante['titulo'].str.lower().str.contains(palavra_principal, na=False)
            cluster_videos = df_restante[mask]
            
            if len(cluster_videos) < 15:
                # Cluster muito pequeno, pula
                df_restante = df_restante[~mask]
                continue
            
            # Identifica emoção deste cluster
            emocao = self.identificar_emocao(
                palavras_chave,
                cluster_videos['titulo'].tolist()
            )
            
            # Calcula métricas
            views_medias = int(cluster_videos['views'].mean())
            
            # Cria cluster
            cluster = {
                "id": f"cluster_{cluster_id}",
                "nome": f"Cluster {cluster_id + 1}: {emocao.split('→')[0].strip().title()}",
                "descricao": f"Vídeos dominados por: {emocao}",
                "tamanho": len(cluster_videos),
                "exemplos_titulos": cluster_videos['titulo'].head(5).tolist(),
                "metricas": {
                    "views_medias": views_medias,
                    "engajamento_medio": 0.08,  # Placeholder
                    "viral_score_medio": 1.5    # Placeholder
                },
                "palavras_chave": palavras_chave[:10],
                "emocao_central": emocao,
                "saturacao": "média",
                "forca_viral": "alta" if views_medias > 300000 else "média"
            }
            
            clusters.append(cluster)
            console.print(f"[green]✓ Cluster {cluster_id}: {len(cluster_videos)} vídeos ({emocao})[/green]")
            
            # Remove vídeos já processados
            df_restante = df_restante[~mask]
            cluster_id += 1
        
        return clusters
    
    def salvar_json(self, dados: Dict, filename: str):
        """Salva resultado em JSON."""
        filepath = os.path.join(self.output_path, filename)
        
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(dados, f, indent=2, ensure_ascii=False)
            console.print(f"[green]✅ Arquivo salvo: {filepath}[/green]")
        except Exception as e:
            console.print(f"[red]Erro ao salvar {filename}: {e}[/red]")
            raise
    
    def atualizar_progress(self, num_clusters: int):
        """Atualiza arquivo progress.json."""
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
                
        except Exception as e:
            console.print(f"[yellow]Aviso: Não foi possível atualizar progress.json: {e}[/yellow]")
    
    def executar(self) -> Dict:
        """
        Método principal - executa análise completa.
        
        SIMPLES:
        1. Carrega lista de vídeos
        2. Limpa dados ruins
        3. Agrupa vídeos similares
        4. Identifica emoções de cada grupo
        5. Salva resultado
        """
        console.print(Panel.fit(
            "[bold cyan]🧠 AGENTE 03: ANALISTA[/bold cyan]\n"
            "[Analisa vídeos e identifica padrões emocionais (T=2)]",
            title="Análise de Clusters"
        ))
        
        try:
            # 1. Carregar CSV
            console.print("\n[bold]Passo 1: Carregando vídeos[/bold]")
            df = self.carregar_csv()
            self.validar_csv(df)
            
            # 2. Limpar dados
            console.print("\n[bold]Passo 2: Limpando dados[/bold]")
            df_limpo = self.limpar_dados(df)
            
            # 3. Fazer clustering
            console.print("\n[bold]Passo 3: Agrupando vídeos similares[/bold]")
            clusters = self.fazer_clustering_simples(df_limpo)
            
            if len(clusters) == 0:
                console.print("[yellow]⚠ Nenhum cluster identificado. Ajustando...[/yellow]")
                # Fallback: cria pelo menos 1 cluster com todos vídeos
                clusters = [{
                    "id": "cluster_0",
                    "nome": "Cluster Geral",
                    "tamanho": len(df_limpo),
                    "exemplos_titulos": df_limpo['titulo'].head(5).tolist(),
                    "palavras_chave": self.extrair_palavras_chave(df_limpo['titulo'].tolist()),
                    "emocao_central": "emoção mista",
                    "saturacao": "média",
                    "forca_viral": "média"
                }]
            
            # 4. Criar output
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
            
            # 5. Salvar
            self.salvar_json(resultado, self.output_file)
            self.atualizar_progress(len(clusters))
            
            # 6. Resumo
            console.print("\n" + "="*60)
            console.print(f"[bold green]✅ {len(clusters)} CLUSTERS IDENTIFICADOS![/bold green]")
            console.print(f"[dim]De {len(df)} vídeos → {len(df_limpo)} limpos → {len(clusters)} grupos[/dim]")
            console.print(f"[dim]Próxima etapa: T=3 (Agente 04: Arquiteto de Eixos)[/dim]")
            console.print("="*60 + "\n")
            
            # Mostrar clusters
            console.print("[bold cyan]Clusters Encontrados:[/bold cyan]")
            for cluster in clusters:
                console.print(f"  • {cluster['nome']} ({cluster['tamanho']} vídeos)")
                console.print(f"    Emoção: {cluster['emocao_central']}")
            
            return resultado
            
        except FileNotFoundError as e:
            console.print(f"[bold red]❌ Arquivo não encontrado: {e}[/bold red]")
            raise
        except ErroCSVInvalido as e:
            console.print(f"[bold red]❌ CSV inválido: {e}[/bold red]")
            raise
        except Exception as e:
            console.print(f"[bold red]❌ Erro inesperado: {e}[/bold red]")
            raise


def main():
    """Função para teste standalone do agente."""
    agente = Agente03Analista()
    resultado = agente.executar()
    
    console.print("\n[bold cyan]Resumo Final:[/bold cyan]")
    console.print(json.dumps(resultado['estatisticas'], indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
