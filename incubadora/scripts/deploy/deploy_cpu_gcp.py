import os
import json
import time
from google.cloud import compute_v1
from google.oauth2 import service_account
from rich.console import Console

console = Console()

# Configuration
CREDENTIALS_FILE = "gcp-credentials.json"
PROJECT_ID = None
ZONE = "us-central1-a"
INSTANCE_NAME = "muscle-comfyui-cpu"
MACHINE_TYPE = "n1-standard-4"  # 4 vCPUs, 15GB RAM

def load_credentials():
    global PROJECT_ID
    if not os.path.exists(CREDENTIALS_FILE):
        console.print(f"[red]Error: {CREDENTIALS_FILE} not found![/red]")
        return None
    
    with open(CREDENTIALS_FILE, 'r') as f:
        cred_data = json.load(f)
        PROJECT_ID = cred_data.get('project_id')
    
    credentials = service_account.Credentials.from_service_account_file(
        CREDENTIALS_FILE,
        scopes=['https://www.googleapis.com/auth/cloud-platform']
    )
    return credentials

def create_cpu_instance(credentials):
    console.print(f"[bold cyan]Creating CPU instance: {INSTANCE_NAME}[/bold cyan]")
    
    instance_client = compute_v1.InstancesClient(credentials=credentials)
    
    # Startup script (Modified for CPU-only Torch)
    startup_script = """#!/bin/bash
# Update system
apt-get update
apt-get install -y python3 python3-pip git wget

# Install Python dependencies (CPU version of Torch)
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# Clone and setup ComfyUI
cd /opt
git clone https://github.com/comfyanonymous/ComfyUI.git
cd ComfyUI
pip3 install -r requirements.txt

# Download base models (SDXL Base)
mkdir -p models/checkpoints
wget -O models/checkpoints/sd_xl_base_1.0.safetensors https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0/resolve/main/sd_xl_base_1.0.safetensors

# Create systemd service
cat > /etc/systemd/system/comfyui.service << 'EOF'
[Unit]
Description=ComfyUI Service
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/ComfyUI
ExecStart=/usr/bin/python3 main.py --listen 0.0.0.0 --port 8188 --cpu
Restart=always

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable comfyui
systemctl start comfyui

# Auto-shutdown after 2 hours
cat > /usr/local/bin/auto-shutdown.sh << 'EOF'
#!/bin/bash
IDLE_TIME=7200
if [ $(cat /proc/uptime | cut -d' ' -f1 | cut -d'.' -f1) -gt $IDLE_TIME ]; then
    systemctl poweroff
fi
EOF
chmod +x /usr/local/bin/auto-shutdown.sh
(crontab -l 2>/dev/null; echo "*/30 * * * * /usr/local/bin/auto-shutdown.sh") | crontab -
"""

    disk = compute_v1.AttachedDisk()
    initialize_params = compute_v1.AttachedDiskInitializeParams()
    initialize_params.source_image = "projects/ubuntu-os-cloud/global/images/family/ubuntu-2204-lts"
    initialize_params.disk_size_gb = 50
    initialize_params.disk_type = f"zones/{ZONE}/diskTypes/pd-standard"
    disk.initialize_params = initialize_params
    disk.auto_delete = True
    disk.boot = True

    network_interface = compute_v1.NetworkInterface()
    network_interface.name = "global/networks/default"
    access_config = compute_v1.AccessConfig()
    access_config.name = "External NAT"
    access_config.type_ = "ONE_TO_ONE_NAT"
    network_interface.access_configs = [access_config]

    metadata = compute_v1.Metadata()
    metadata.items = [compute_v1.Items(key="startup-script", value=startup_script)]

    instance = compute_v1.Instance()
    instance.name = INSTANCE_NAME
    instance.machine_type = f"zones/{ZONE}/machineTypes/{MACHINE_TYPE}"
    instance.disks = [disk]
    instance.network_interfaces = [network_interface]
    instance.metadata = metadata
    
    # No guest_accelerators (GPU)

    try:
        console.print(f"[yellow]Requesting CPU instance creation...[/yellow]")
        operation = instance_client.insert(
            project=PROJECT_ID,
            zone=ZONE,
            instance_resource=instance
        )
        
        console.print(f"[yellow]Waiting for instance...[/yellow]")
        time.sleep(10)
        
        instance_info = instance_client.get(
            project=PROJECT_ID,
            zone=ZONE,
            instance=INSTANCE_NAME
        )
        
        external_ip = instance_info.network_interfaces[0].access_configs[0].nat_i_p
        
        console.print(f"[bold green]CPU Instance Created Successfully![/bold green]")
        console.print(f"[cyan]IP:[/cyan] {external_ip}")
        console.print(f"[cyan]URL:[/cyan] http://{external_ip}:8188")
        
        return external_ip
        
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        return None

if __name__ == "__main__":
    creds = load_credentials()
    if creds:
        create_cpu_instance(creds)
