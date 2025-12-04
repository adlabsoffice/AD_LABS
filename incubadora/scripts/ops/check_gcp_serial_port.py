import os
import json
from google.cloud import compute_v1
from google.oauth2 import service_account
from rich.console import Console

console = Console()

CREDENTIALS_FILE = "gcp-credentials.json"
ZONE = "us-central1-a"
INSTANCE_NAME = "muscle-comfyui-cpu"

def get_serial_port_output():
    if not os.path.exists(CREDENTIALS_FILE):
        return

    with open(CREDENTIALS_FILE, 'r') as f:
        cred_data = json.load(f)
        project_id = cred_data.get('project_id')

    credentials = service_account.Credentials.from_service_account_file(
        CREDENTIALS_FILE,
        scopes=['https://www.googleapis.com/auth/cloud-platform']
    )

    instance_client = compute_v1.InstancesClient(credentials=credentials)
    
    console.print(f"[bold cyan]Lendo logs da instancia {INSTANCE_NAME}...[/bold cyan]")
    
    try:
        response = instance_client.get_serial_port_output(
            project=project_id,
            zone=ZONE,
            instance=INSTANCE_NAME
        )
        
        output = response.contents
        
        # Filter for relevant lines (startup script)
        console.print("\n[bold]--- ULTIMAS 30 LINHAS DO LOG ---[/bold]")
        lines = output.split('\n')
        for line in lines[-30:]:
            console.print(line)
            
        if "ComfyUI installation complete" in output:
            console.print("\n[green]Instalacao concluida com sucesso![/green]")
        elif "startup-script" in output:
             console.print("\n[yellow]Startup script ainda rodando ou finalizado...[/yellow]")
        else:
             console.print("\n[red]Startup script nao parece ter rodado ainda.[/red]")

    except Exception as e:
        console.print(f"[red]Erro ao ler logs: {e}[/red]")

if __name__ == "__main__":
    get_serial_port_output()
