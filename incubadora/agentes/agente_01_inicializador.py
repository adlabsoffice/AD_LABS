import os
import json
from rich.console import Console
from rich.panel import Panel

console = Console()

class Agente01Inicializador:
    def __init__(self):
        self.base_path = "incubadora/canais"
    
    def criar_estrutura_canal(self, config):
        """
        Cria as pastas e arquivos iniciais do canal baseados na config.
        """
        nome_safe = config['nome_canal'].lower().replace(" ", "_")
        canal_path = os.path.join(self.base_path, nome_safe)
        
        pastas = [
            "roteiros",
            "audios",
            "imagens",
            "videos_finais",
            "metadata"
        ]
        
                    "session_id": ""
                }
            }
            with open(os.path.join(canal_path, "credentials.template.json"), "w", encoding="utf-8") as f:
                json.dump(credentials_template, f, indent=4)
                
            console.print(f"[bold green]✅ Canal '{config['nome_canal']}' inicializado com sucesso![/bold green]")
            return True
            
        except Exception as e:
            console.print(f"[red]Erro ao criar canal: {e}[/red]")
            return False
