"""
CORE ORCHESTRATOR
Responsável por centralizar o estado e a lógica de execução do sistema.
"""

import os
import json
import uuid
from datetime import datetime
from typing import Dict, Optional, Any
from rich.console import Console
from rich.panel import Panel

# Importa APIManager para garantir que está disponível globalmente
try:
    from ..utils.api_manager import APIManager
except ImportError:
    # Fallback para execução direta
    import sys
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from utils.api_manager import APIManager

console = Console()

class Orchestrator:
    def __init__(self):
        self.root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.incubadora_dir = os.path.join(self.root_dir, "incubadora")
        self.output_dir = os.path.join(self.root_dir, "outputs")
        self.config_dir = os.path.join(self.incubadora_dir, "canais")
        
        self.api_manager = APIManager()
        self.current_project_id = None
        self.current_config = {}
        
        # Garante estrutura básica
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.config_dir, exist_ok=True)

    def iniciar_projeto(self, config_inicial: Dict[str, Any], modo: str = "interativo") -> Dict:
        """
        Inicializa um novo projeto ou carrega um existente.
        
        Args:
            config_inicial: Dicionário com configurações (nome_canal, nicho, etc)
            modo: 'interativo' ou 'batch'
            
        Returns:
            Configuração completa do projeto
        """
        console.print(Panel(f"[bold cyan]ORCHESTRATOR CORE[/bold cyan]\nModo: {modo}", expand=False))
        
        # 1. Gera ID se não existir
        if "id" not in config_inicial:
            config_inicial["id"] = f"proj_{uuid.uuid4().hex[:8]}"
            
        self.current_project_id = config_inicial["id"]
        
        # 2. Define caminhos
        nome_canal_safe = config_inicial.get("nome_canal", "sem_nome").replace(" ", "_").lower()
        project_path = os.path.join(self.config_dir, nome_canal_safe)
        os.makedirs(project_path, exist_ok=True)
        
        config_file = os.path.join(project_path, "config.json")
        
        # 3. Mescla com defaults
        config_final = self._aplicar_defaults(config_inicial)
        config_final["paths"] = {
            "root": project_path,
            "config": config_file,
            "outputs": os.path.join(project_path, "outputs")
        }
        os.makedirs(config_final["paths"]["outputs"], exist_ok=True)
        
        # 4. Salva Config
        self._salvar_json(config_final, config_file)
        self.current_config = config_final
        
        console.print(f"[green]✅ Projeto '{config_final['nome_canal']}' inicializado![/green]")
        console.print(f"[dim]ID: {self.current_project_id}[/dim]")
        
        return config_final

    def carregar_projeto(self, nome_canal: str) -> Optional[Dict]:
        """Carrega configuração de um projeto existente."""
        nome_canal_safe = nome_canal.replace(" ", "_").lower()
        config_file = os.path.join(self.config_dir, nome_canal_safe, "config.json")
        
        if os.path.exists(config_file):
            with open(config_file, "r", encoding="utf-8") as f:
                self.current_config = json.load(f)
                self.current_project_id = self.current_config.get("id")
                return self.current_config
        return None

    def _aplicar_defaults(self, config: Dict) -> Dict:
        """Aplica valores padrão para campos faltantes."""
        defaults = {
            "timestamp": datetime.now().isoformat(),
            "status": "inicializado",
            "fase_atual": "T0",
            "apis_config": {
                "imagem": "imagen-4.0-fast",
                "llm": "gemini-2.5-flash",
                "audio": "google_tts"
            }
        }
        # Merge raso (poderia ser deep merge se necessário)
        return {**defaults, **config}

    def _salvar_json(self, dados: Dict, filepath: str):
        """Salva JSON com tratamento de erro."""
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(dados, f, indent=2, ensure_ascii=False)
        except Exception as e:
            console.print(f"[red]Erro ao salvar config: {e}[/red]")
            raise

    def validar_schema(self, dados: Dict, schema_name: str) -> bool:
        """
        Valida dados contra um schema JSON.
        Requer biblioteca jsonschema instalada.
        """
        try:
            import jsonschema
            schema_path = os.path.join(self.root_dir, "specs", "schemas", f"{schema_name}.json")
            
            if not os.path.exists(schema_path):
                console.print(f"[yellow]Schema {schema_name} não encontrado. Pulando validação.[/yellow]")
                return True
                
            with open(schema_path, "r", encoding="utf-8") as f:
                schema = json.load(f)
                
            jsonschema.validate(instance=dados, schema=schema)
            return True
            
        except ImportError:
            console.print("[dim]jsonschema não instalado. Validação ignorada.[/dim]")
            return True
        except Exception as e:
            console.print(f"[red]Falha na validação do schema {schema_name}: {e}[/red]")
            return False

if __name__ == "__main__":
    # Teste rápido
    orch = Orchestrator()
    orch.iniciar_projeto({"nome_canal": "Teste Core", "nicho": "DevOps"}, modo="teste")
