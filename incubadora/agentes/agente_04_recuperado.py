import os
import json
from typing import Dict, List
from rich.console import Console
from rich.panel import Panel

console = Console()

class Agente04Arquiteto:
    """
    Agente 04: Arquiteto de Eixos (Recuperado)
    Responsável por transformar clusters de pesquisa em eixos editoriais.
    Reconstruído a partir de evidências forenses do arquivo compilado .pyc.
    """
    def __init__(self):
        self.input_file = "outputs/T02_clusters.json"
        self.output_dir = "outputs/T03_eixos"
        
    def carregar_clusters(self) -> Dict:
        """
        Carrega os clusters gerados pelo Agente 03.
        """
        if not os.path.exists(self.input_file):
            console.print(f"[red]Arquivo {self.input_file} não encontrado.[/red]")
            # Mock para recuperação se arquivo não existir
            return {"clusters": [{"nome": "Prosperidade Bíblica", "score": 95}]}
            
        with open(self.input_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def validar_clusters(self, clusters: Dict) -> bool:
        """
        Valida se os clusters são suficientes para gerar eixos.
        """
        if not clusters.get("clusters"):
            return False
        return True

    def criar_eixo(self, cluster: Dict, id_eixo: int) -> Dict:
        """
        Cria um objeto de Eixo estruturado a partir de um cluster.
        Lógica reconstruída baseada nas strings encontradas.
        """
        # Strings recuperadas sugerem campos como 'emocao_central', 'padrao_dramatico'
        eixo = {
            "id": f"eixo_{id_eixo:02d}",
            "nome": cluster.get("nome", "Eixo Genérico"),
            "cluster_origem": cluster.get("id", "unknown"),
            "emocao_central": "Humilhação -> Revanche", # Exemplo encontrado nas specs
            "formato_video": "4-6min", # Ajustado conforme config atual
            "padrao_dramatico": "Conflito -> Virada -> Resolução",
            "status": "criado"
        }
        return eixo

    def salvar_eixos(self, eixos: List[Dict]):
        """
        Salva os eixos gerados na pasta de output.
        """
        os.makedirs(self.output_dir, exist_ok=True)
        
        for eixo in eixos:
            filename = f"{eixo['id']}.json"
            filepath = os.path.join(self.output_dir, filename)
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(eixo, f, indent=2, ensure_ascii=False)
            console.print(f"[green]Eixo salvo: {filename}[/green]")

    def executar(self):
        """
        Fluxo principal de execução.
        """
        console.print(Panel.fit("🏗️ AGENTE 04: ARQUITETO DE EIXOS"))
        
        try:
            dados = self.carregar_clusters()
            if not self.validar_clusters(dados):
                console.print("[red]Clusters inválidos ou vazios.[/red]")
                return

            eixos = []
            for i, cluster in enumerate(dados.get("clusters", [])):
                eixo = self.criar_eixo(cluster, i+1)
                eixos.append(eixo)
            
            self.salvar_eixos(eixos)
            console.print(f"[bold green]✅ {len(eixos)} Eixos criados com sucesso![/bold green]")
            
        except Exception as e:
            console.print(f"[bold red]❌ Erro na execução: {e}[/bold red]")

if __name__ == "__main__":
    agente = Agente04Arquiteto()
    agente.executar()
