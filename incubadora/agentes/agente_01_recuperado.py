import os
import json
import time
from typing import Dict, List, Optional
from rich.console import Console
from rich.panel import Panel

console = Console()

class Agente01Inicializador:
    """
    Agente 01: Inicializador (Recuperado)
    Responsável por carregar a configuração inicial e preparar o ambiente.
    Reconstruído a partir de evidências forenses do arquivo compilado .pyc.
    """
    def __init__(self):
        self.base_path = "incubadora/canais"
        self.output_path = "outputs"
        self.config_file = "T00_config.json"
        self.progress_file = "progress.json"

    def carregar_config(self) -> Dict:
        """
        Carrega a configuração inicial.
        Na versão original, parecia ler de um input ou arquivo mock.
        """
        console.print("[bold yellow]AGENTE 01: Iniciando carga de configuração...[/bold yellow]")
        
        # Estrutura recuperada das strings do binário
        config = {
            "timestamp": "T=0",
            "projeto": {
                "nicho": "Prosperidade Bíblica", # String encontrada no .pyc
                "status": "inicializado"
            },
            "apis_disponiveis": {
                "gemini": True,
                "youtube_data": True
            },
            "restricoes": {
                "orcamento_maximo_mensal": 0,
                "prazo_dias": 7
            }
        }
        return config

    def validar_regras(self, config: Dict) -> bool:
        """
        Valida as regras de negócio básicas da configuração.
        """
        if not config.get("projeto", {}).get("nicho"):
            console.print("[red]Erro: Nicho não definido.[/red]")
            return False
            
        console.print("[green]Regras validadas com sucesso.[/green]")
        return True

    def salvar_json(self, dados: Dict, filename: str):
        """
        Salva os dados em arquivo JSON na pasta de outputs.
        """
        os.makedirs(self.output_path, exist_ok=True)
        filepath = os.path.join(self.output_path, filename)
        
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(dados, f, indent=2, ensure_ascii=False)
            console.print(f"[blue]Arquivo salvo: {filepath}[/blue]")
        except Exception as e:
            console.print(f"[red]Erro ao salvar {filename}: {e}[/red]")

    def atualizar_progress(self, etapa: str, status: str):
        """
        Atualiza o arquivo de progresso global.
        """
        dados = {
            "timestamp_atual": etapa,
            "status": status,
            "ultimo_update": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        self.salvar_json(dados, self.progress_file)

    def executar(self):
        """
        Fluxo principal de execução recuperado.
        """
        console.print(Panel.fit("🚀 INCUBADORA AD_LABS v2.0 - Inicializador"))
        
        try:
            config = self.carregar_config()
            
            if self.validar_regras(config):
                self.salvar_json(config, self.config_file)
                self.atualizar_progress("T=0", "Configuração Inicializada")
                console.print("[bold green]✅ INICIALIZAÇÃO CONCLUÍDA COM SUCESSO![/bold green]")
                return True
            else:
                console.print("[bold red]❌ Falha na validação das regras.[/bold red]")
                return False
                
        except Exception as e:
            console.print(f"[bold red]❌ Erro inesperado: {e}[/bold red]")
            return False

if __name__ == "__main__":
    agente = Agente01Inicializador()
    agente.executar()
