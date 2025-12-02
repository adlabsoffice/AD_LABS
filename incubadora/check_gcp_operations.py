import os
import json
from google.cloud import compute_v1
from google.oauth2 import service_account
from rich.console import Console

console = Console()

CREDENTIALS_FILE = "gcp-credentials.json"
ZONE = "southamerica-east1-c"

def list_operations():
    if not os.path.exists(CREDENTIALS_FILE):
        return

    with open(CREDENTIALS_FILE, 'r') as f:
        cred_data = json.load(f)
        project_id = cred_data.get('project_id')

    credentials = service_account.Credentials.from_service_account_file(
        CREDENTIALS_FILE,
        scopes=['https://www.googleapis.com/auth/cloud-platform']
    )

    op_client = compute_v1.ZoneOperationsClient(credentials=credentials)
    
    console.print(f"[bold cyan]Verificando Operacoes Recentes em {ZONE}...[/bold cyan]")
    
    # List last 5 operations
    request = compute_v1.ListZoneOperationsRequest(
        project=project_id,
        zone=ZONE,
        max_results=5
    )
    
    ops = op_client.list(request=request)
    
    for op in ops:
        status = op.status
        op_type = op.operation_type
        error = op.error
        
        console.print(f"Op: {op_type} | Status: {status}")
        if error:
            console.print(f"[red]  ERRO: {error}[/red]")
            for err in error.errors:
                console.print(f"[red]    - {err.message}[/red]")

if __name__ == "__main__":
    list_operations()
