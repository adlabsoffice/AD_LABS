"""
AGENTE 04: ARQUITETO DE EIXOS
Timestamp: T=3
Responsabilidade: Transformar clusters em 5 "eixos emocionais" estruturados
"""

import os
import json
from typing import Dict, List
from rich.console import Console
from rich.panel import Panel
from rich.progress import track

console = Console()


class ErroClusterInvalido(Exception):
    """Exceção para cluster inválido."""
    pass


class Agente04ArquitetoEixos:
    """
    Agente 04: Arquiteto de Eixos
    Transforma cada cluster em "eixo emocional" (formato de conteúdo estruturado)
    """
    
    def __init__(self):
        self.input_path = "outputs"
        self.output_path = "outputs/T03_eixos"
        self.clusters_file = "T02_clusters.json"
        self.num_eixos = 5
    
    def criar_estrutura_outputs(self):
        """Cria pasta de output para eixos."""
        os.makedirs(self.output_path, exist_ok=True)
        console.print(f"[dim]Pasta {self.output_path}/ verificada[/dim]")
    
    def carregar_clusters(self) -> Dict:
        """Carrega arquivo de clusters gerado pelo Agente 03."""
        filepath = os.path.join(self.input_path, self.clusters_file)
        
        if not os.path.exists(filepath):
            raise FileNotFoundError(
                f"Arquivo {filepath} não encontrado. "
                "Execute Agente 03 (Analista) primeiro."
            )
        
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
            console.print(f"[green]✓ Clusters carregados: {filepath}[/green]")
            return data
        except json.JSONDecodeError as e:
            raise ErroClusterInvalido(f"JSON inválido em {filepath}: {e}")
    
    def validar_clusters(self, clusters_data: Dict) -> bool:
        """Valida se dados de clusters estão no formato esperado."""
        if "clusters" not in clusters_data:
            raise ErroClusterInvalido("Campo 'clusters' não encontrado no JSON")
        
        clusters = clusters_data["clusters"]
        if not isinstance(clusters, list):
            raise ErroClusterInvalido("'clusters' deve ser uma lista")
        
        if len(clusters) < 1:
            raise ErroClusterInvalido("Pelo menos 1 cluster deve existir")
        
        return True
    
    def criar_eixo_de_cluster(self, cluster: Dict, eixo_numero: int) -> Dict:
        """
        Cria um eixo emocional estruturado a partir de um cluster.
        
        Args:
            cluster: Dados do cluster
            eixo_numero: Número do eixo (1-5)
        
        Returns:
            Dict com estrutura completa do eixo
        """
        # Extrai informações do cluster (formato flexível)
        cluster_id = cluster.get("id", f"cluster_{eixo_numero}")
        emocao_principal = cluster.get("emocao_central", cluster.get("tema", "Emoção Genérica"))
        
        # Define padrões dramáticos comuns por tipo de emoção
        padroes_dramaticos = {
            "humilhacao": "conflito injusto → virada → justiça",
            "medo": "ameaça → tensão → alívio/revelação",
            "curiosidade": "mistério → investigação → descoberta",
            "raiva": "injustiça → confronto → reparação",
            "tristeza": "perda → luto → superação"
        }
        
        # Tenta identificar padrão ou usa genérico
        emocao_lower = emocao_principal.lower()
        padrao = None
        for key, value in padroes_dramaticos.items():
            if key in emocao_lower:
                padrao = value
                break
        
        if not padrao:
            padrao = "setup → conflito → resolução"
        
        # Categorias possíveis (genéricas)
        categorias = cluster.get("categorias", ["escola", "trabalho", "família", "relacionamentos"])
        
        # Scores (usa valores do cluster ou defaults)
        saturacao = cluster.get("saturacao", "média")
        forca = cluster.get("forca", "média")
        risco = cluster.get("risco", "baixo")
        rpm_esperado = cluster.get("rpm_esperado", "médio")
        
        # Nome do eixo
        nome_eixo = cluster.get("nome", f"Eixo {eixo_numero}: {emocao_principal}")
        
        # Monta eixo estruturado
        eixo = {
            "id": f"eixo_{eixo_numero:02d}",
            "nome": nome_eixo,
            "cluster_origem": cluster_id,
            "emocao_central": emocao_principal,
            "personagem_tipo": cluster.get("personagem", "pessoa comum enfrentando desafio"),
            "formato_video": cluster.get("formato", "1-3min"),
            "padrao_dramatico": padrao,
            "categorias_possiveis": categorias if isinstance(categorias, list) else ["geral"],
            "saturacao": saturacao,
            "forca": forca,
            "risco": risco,
            "rpm_esperado": rpm_esperado,
            "timestamp": "T=3",
            "status": "validado"
        }
        
        return eixo
    
    def validar_eixo(self, eixo: Dict) -> bool:
        """Valida se eixo tem todos campos obrigatórios."""
        campos_obrigatorios = [
            "id", "nome", "emocao_central", "padrao_dramatico",
            "saturacao", "forca", "risco"
        ]
        
        for campo in campos_obrigatorios:
            if campo not in eixo:
                console.print(f"[yellow]⚠ Campo obrigatório ausente: {campo}[/yellow]")
                return False
        
        return True
    
    def salvar_eixo(self, eixo: Dict, eixo_numero: int):
        """Salva eixo em arquivo JSON individual."""
        filename = f"eixo_{eixo_numero:02d}.json"
        filepath = os.path.join(self.output_path, filename)
        
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(eixo, f, indent=2, ensure_ascii=False)
            console.print(f"[green]✓ Eixo salvo: {filename}[/green]")
        except Exception as e:
            console.print(f"[red]Erro ao salvar {filename}: {e}[/red]")
            raise
    
    def atualizar_progress(self):
        """Atualiza arquivo progress.json."""
        progress_file = os.path.join(self.input_path, "progress.json")
        
        try:
            # Carrega progress existente
            if os.path.exists(progress_file):
                with open(progress_file, "r", encoding="utf-8") as f:
                    progress = json.load(f)
            else:
                progress = {}
            
            # Atualiza
            progress.update({
                "timestamp_atual": "T=3",
                "ultimo_agente": "arquiteto_eixos",
                "status": "eixos_criados",
                "proxima_acao": "Executar Agente 05: Gerador de Ideias",
                "checkpoint": {
                    "eixos_criados": self.num_eixos,
                    "ideias_geradas": 0,
                    "videos_produzidos": 0,
                    "mare_identificada": False
                }
            })
            
            # Salva
            with open(progress_file, "w", encoding="utf-8") as f:
                json.dump(progress, f, indent=2, ensure_ascii=False)
            
        except Exception as e:
            console.print(f"[yellow]Aviso: Não foi possível atualizar progress.json: {e}[/yellow]")
    
    def executar(self) -> List[Dict]:
        """
        Método principal - executa o agente arquiteto de eixos.
        
        Returns:
            Lista com os 5 eixos criados
        """
        console.print(Panel.fit(
            "[bold cyan]📐 AGENTE 04: ARQUITETO DE EIXOS[/bold cyan]\n"
            "[dim]Transformando clusters em eixos emocionais (T=3)[/dim]",
            title="Criação de Eixos"
        ))
        
        try:
            # 1. Criar estrutura
            self.criar_estrutura_outputs()
            
            # 2. Carregar clusters
            console.print("\n[bold]Passo 1: Carregando Clusters[/bold]")
            clusters_data = self.carregar_clusters()
            self.validar_clusters(clusters_data)
            
            clusters = clusters_data["clusters"]
            console.print(f"[green]✓ {len(clusters)} cluster(s) encontrado(s)[/green]")
            
            # 3. Criar eixos (sempre 5, mesmo se houver menos clusters)
            console.print(f"\n[bold]Passo 2: Criando {self.num_eixos} Eixos[/bold]")
            eixos_criados = []
            
            for i in track(range(self.num_eixos), description="Gerando eixos..."):
                eixo_numero = i + 1
                
                # Se temos cluster correspondente, usa ele
                # Se não, reutiliza clusters (round-robin)
                cluster_idx = i % len(clusters)
                cluster = clusters[cluster_idx]
                
                # Cria eixo
                eixo = self.criar_eixo_de_cluster(cluster, eixo_numero)
                
                # Valida
                if not self.validar_eixo(eixo):
                    console.print(f"[red]⚠ Eixo {eixo_numero} inválido, pulando...[/red]")
                    continue
                
                # Salva
                self.salvar_eixo(eixo, eixo_numero)
                eixos_criados.append(eixo)
            
            # 4. Atualizar progress
            self.atualizar_progress()
            
            # 5. Resumo
            console.print("\n" + "="*60)
            console.print(f"[bold green]✅ {len(eixos_criados)} EIXOS CRIADOS COM SUCESSO![/bold green]")
            console.print(f"[dim]Arquivos salvos em: {self.output_path}/[/dim]")
            console.print(f"[dim]Próxima etapa: T=4 (Agente 05: Gerador de Ideias)[/dim]")
            console.print("="*60 + "\n")
            
            # Mostrar resumo dos eixos
            console.print("[bold cyan]Resumo dos Eixos:[/bold cyan]")
            for eixo in eixos_criados:
                console.print(f"  • {eixo['nome']} - {eixo['emocao_central']}")
            
            return eixos_criados
            
        except FileNotFoundError as e:
            console.print(f"[bold red]❌ Arquivo não encontrado: {e}[/bold red]")
            raise
        except ErroClusterInvalido as e:
            console.print(f"[bold red]❌ Erro nos clusters: {e}[/bold red]")
            raise
        except Exception as e:
            console.print(f"[bold red]❌ Erro inesperado: {e}[/bold red]")
            raise


def main():
    """Função para teste standalone do agente."""
    agente = Agente04ArquitetoEixos()
    eixos = agente.executar()
    
    console.print("\n[bold cyan]Eixos Criados:[/bold cyan]")
    for i, eixo in enumerate(eixos, 1):
        console.print(f"\n[bold]Eixo {i}:[/bold]")
        console.print(json.dumps(eixo, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
