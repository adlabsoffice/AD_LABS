import os
import json
from google.cloud import compute_v1
from google.oauth2 import service_account
from rich.console import Console

console = Console()

CREDENTIALS_FILE = "gcp-credentials.json"

def create_firewall_rule():
    if not os.path.exists(CREDENTIALS_FILE):
        console.print(f"[red]Erro: {CREDENTIALS_FILE} nao encontrado![/red]")
        return

    with open(CREDENTIALS_FILE, 'r') as f:
        cred_data = json.load(f)
        project_id = cred_data.get('project_id')

    credentials = service_account.Credentials.from_service_account_file(
        CREDENTIALS_FILE,
        scopes=['https://www.googleapis.com/auth/cloud-platform']
    )

    firewall_client = compute_v1.FirewallsClient(credentials=credentials)
    
    firewall_rule = compute_v1.Firewall()
    firewall_rule.name = "allow-comfyui-8188"
    firewall_rule.direction = "INGRESS"
    firewall_rule.priority = 1000
    firewall_rule.network = "global/networks/default"
    
    allow_config = compute_v1.Allowed(I_p_protocol="tcp", ports=["8188"])
    
    firewall_rule.allowed = [allow_config]
    firewall_rule.source_ranges = ["0.0.0.0/0"] # Allow from anywhere
    
    console.print(f"[yellow]Criando regra de firewall 'allow-comfyui-8188' no projeto {project_id}...[/yellow]")
    
    try:
        operation = firewall_client.insert(
            project=project_id,
            firewall_resource=firewall_rule
        )
        
        console.print(f"[green]Regra de Firewall criada com sucesso![/green]")
        console.print("O acesso deve ser liberado em alguns instantes.")
        
    except Exception as e:
        if "already exists" in str(e):
             console.print(f"[green]A regra de firewall ja existe.[/green]")
        else:
            console.print(f"[red]Erro ao criar firewall: {e}[/red]")

if __name__ == "__main__":
    create_firewall_rule()
