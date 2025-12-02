import subprocess
import boto3
import os
from rich.console import Console

console = Console()

# Configuration
KEY_FILE = "brain-key-v2.pem"
REMOTE_USER = "ubuntu"
REMOTE_DIR = "/home/ubuntu/incubadora"

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

def sync_files():
    ip = get_brain_ip()
    if not ip:
        console.print("[red]❌ Brain Server not found![/red]")
        return

    # Fix permissions on key file (Windows doesn't enforce strict 600 but scp might complain)
    # Actually on Windows scp usually doesn't care as much as Linux, but let's try.
    
    console.print(f"[cyan]Syncing to {ip} via SCP...[/cyan]")

    # Create remote directory first
    mkdir_cmd = [
        "ssh",
        "-o", "StrictHostKeyChecking=no",
        "-i", KEY_FILE,
        f"{REMOTE_USER}@{ip}",
        f"mkdir -p {REMOTE_DIR}"
    ]
    subprocess.run(mkdir_cmd)

    # We will sync the whole current folder to remote
    # Exclude .git, venv, __pycache__
    # SCP doesn't have easy exclude, so we might need rsync if available, 
    # but Windows usually doesn't have rsync.
    # We will copy specific critical files/folders.
    
    files_to_send = ["incubadora", "requirements.txt", ".env", ".env.aws"]
    
    # Actually, we are IN 'incubadora' folder.
    # So we want to send *everything* in current dir to remote dir.
    # Let's use a wildcard but exclude hidden if possible.
    # Simplest: Send all .py, .json, .txt, .env*
    
    # Construct command
    # scp -i key.pem -r * ec2-user@ip:/path
    # But globbing is shell specific.
    
    # Let's iterate and send.
    import glob
    files = glob.glob("*") + glob.glob(".*")
    
    for f in files:
        if f in [".git", "venv", "__pycache__", ".vscode", "brain-key.pem"]:
            continue
        if os.path.isdir(f) and f not in ["agentes", "output"]: # Only send specific dirs
             continue
             
        # Send file/dir
        cmd = [
            "scp", 
            "-o", "StrictHostKeyChecking=no",
            "-i", KEY_FILE,
            "-r",
            f,
            f"{REMOTE_USER}@{ip}:{REMOTE_DIR}/{f}"
        ]
        
        console.print(f"   Sending {f}...")
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
             console.print(f"[yellow]Failed to send {f}: {result.stderr}[/yellow]")

    console.print("[green]Sync Attempt Complete![/green]")
    
    # Install requirements
    console.print("[cyan]Installing requirements...[/cyan]")
    ssh_cmd = [
        "ssh",
        "-o", "StrictHostKeyChecking=no",
        "-i", KEY_FILE,
        f"{REMOTE_USER}@{ip}",
        f"sudo pip3 install -r {REMOTE_DIR}/requirements.txt"
    ]
    subprocess.run(ssh_cmd)

if __name__ == "__main__":
    sync_files()
