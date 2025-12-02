import os
import json
from google.cloud import compute_v1
from google.oauth2 import service_account
from rich.console import Console

console = Console()

CREDENTIALS_FILE = "gcp-credentials.json"
ZONE = "us-central1-a"

def list_instances():
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

    instance_client = compute_v1.InstancesClient(credentials=credentials)
    
    console.print(f"[bold cyan]Verificando instancias no projeto: {project_id} (Zona: {ZONE})[/bold cyan]")
    
    try:
        instances = instance_client.list(project=project_id, zone=ZONE)
        found = False
        for instance in instances:
            found = True
            ip = "N/A"
            if len(instance.network_interfaces) > 0 and len(instance.network_interfaces[0].access_configs) > 0:
                ip = instance.network_interfaces[0].access_configs[0].nat_i_p
            
            console.print(f"  - [green]{instance.name}[/green] | Status: {instance.status} | IP: {ip}")
            
        if not found:
            console.print("[yellow]Nenhuma instancia encontrada nesta zona.[/yellow]")
            
    except Exception as e:
        console.print(f"[red]Erro ao listar: {e}[/red]")

if __name__ == "__main__":
    list_instances()
