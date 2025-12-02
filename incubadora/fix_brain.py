import subprocess
import boto3
import os
from rich.console import Console

console = Console()

# Configuration
KEY_FILE = "brain-key-v2.pem"
REMOTE_USER = "ubuntu"

def load_aws_env():
    env_path = os.path.join(os.getcwd(), ".env.aws")
    if os.path.exists(env_path):
        with open(env_path, "r") as f:
            for line in f:
                if "=" in line:
                    key, value = line.strip().split("=", 1)
                    os.environ[key] = value

load_aws_env()

def get_brain_ip():
    ec2 = boto3.resource('ec2')
    instances = ec2.instances.filter(
        Filters=[{'Name': 'tag:Name', 'Values': ['Brain-n8n']}, 
                 {'Name': 'instance-state-name', 'Values': ['running']}]
    )
    for instance in instances:
        return instance.public_ip_address
    return None

def fix_brain():
    ip = get_brain_ip()
    if not ip:
        console.print("[red]Brain Server not found![/red]")
        return

    console.print(f"[cyan]Fixing Brain at {ip}...[/cyan]")

    commands = [
        "sudo apt-get update -y",
        "sudo apt-get install -y docker.io",
        "sudo systemctl start docker",
        "sudo systemctl enable docker",
        "sudo usermod -aG docker ubuntu",
        # Stop existing if any (ignore error)
        "sudo docker stop n8n || true",
        "sudo docker rm n8n || true",
        # Run n8n
        "sudo docker run -d --restart always --name n8n -p 5678:5678 -e N8N_BASIC_AUTH_ACTIVE=true -e N8N_BASIC_AUTH_USER=admin -e N8N_BASIC_AUTH_PASSWORD=password123 -e N8N_SECURE_COOKIE=false n8nio/n8n"
    ]

    for cmd in commands:
        console.print(f"   Running: {cmd}")
        ssh_cmd = [
            "ssh",
            "-o", "StrictHostKeyChecking=no",
            "-i", KEY_FILE,
            f"{REMOTE_USER}@{ip}",
            cmd
        ]
        result = subprocess.run(ssh_cmd, capture_output=True, text=True)
        if result.returncode != 0:
            console.print(f"[yellow]Warning: {result.stderr}[/yellow]")
        else:
            console.print("[green]OK[/green]")

    console.print("[bold green]Brain Fixed! Try accessing the link again.[/bold green]")

if __name__ == "__main__":
    fix_brain()
