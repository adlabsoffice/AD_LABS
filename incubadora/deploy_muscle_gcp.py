import os
import json
import time
from google.cloud import compute_v1
from google.oauth2 import service_account
from rich.console import Console

console = Console()

# Configuration
CREDENTIALS_FILE = "gcp-credentials.json"
PROJECT_ID = None  # Will be loaded from credentials
ZONE = "southamerica-east1-c"  # Sao Paulo - trying local region
INSTANCE_NAME = "muscle-comfyui"
MACHINE_TYPE = "n1-standard-4"  # Back to n1 for T4
GPU_TYPE = "nvidia-tesla-t4"
GPU_COUNT = 1

def load_credentials():
    """Load GCP credentials and extract project ID"""
    global PROJECT_ID
    
    if not os.path.exists(CREDENTIALS_FILE):
        console.print(f"[red]Error: {CREDENTIALS_FILE} not found![/red]")
        console.print("[yellow]Make sure the JSON key file is in the current directory.[/yellow]")
        return None
    
    with open(CREDENTIALS_FILE, 'r') as f:
        cred_data = json.load(f)
        PROJECT_ID = cred_data.get('project_id')
    
    credentials = service_account.Credentials.from_service_account_file(
        CREDENTIALS_FILE,
        scopes=['https://www.googleapis.com/auth/cloud-platform']
    )
    
    console.print(f"[green]Credentials loaded! Project: {PROJECT_ID}[/green]")
    return credentials

def create_gpu_instance(credentials):
    """Create a GPU-enabled VM instance with ComfyUI"""
    console.print(f"[bold cyan]Creating GPU instance: {INSTANCE_NAME}[/bold cyan]")
    
    instance_client = compute_v1.InstancesClient(credentials=credentials)
    
    # Startup script to install everything
    startup_script = """#!/bin/bash
# Update system
apt-get update
apt-get install -y wget gnupg2 software-properties-common

# Install NVIDIA drivers
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.0-1_all.deb
dpkg -i cuda-keyring_1.0-1_all.deb
apt-get update
apt-get -y install cuda-drivers

# Install Python and dependencies
apt-get install -y python3 python3-pip git
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Clone and setup ComfyUI
cd /opt
git clone https://github.com/comfyanonymous/ComfyUI.git
cd ComfyUI
pip3 install -r requirements.txt

# Download base models
mkdir -p models/checkpoints
wget -O models/checkpoints/sd_xl_base_1.0.safetensors https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0/resolve/main/sd_xl_base_1.0.safetensors

# Create systemd service for ComfyUI
cat > /etc/systemd/system/comfyui.service << 'EOF'
[Unit]
Description=ComfyUI Service
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/ComfyUI
ExecStart=/usr/bin/python3 main.py --listen 0.0.0.0 --port 8188
Restart=always

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable comfyui
systemctl start comfyui

# Create auto-shutdown script (shutdown after 2 hours idle)
cat > /usr/local/bin/auto-shutdown.sh << 'EOF'
#!/bin/bash
IDLE_TIME=7200  # 2 hours in seconds
if [ $(cat /proc/uptime | cut -d' ' -f1 | cut -d'.' -f1) -gt $IDLE_TIME ]; then
    systemctl poweroff
fi
EOF
chmod +x /usr/local/bin/auto-shutdown.sh

# Add to cron (check every 30 minutes)
(crontab -l 2>/dev/null; echo "*/30 * * * * /usr/local/bin/auto-shutdown.sh") | crontab -

echo "ComfyUI installation complete!"
"""

    # Instance configuration
    disk = compute_v1.AttachedDisk()
    initialize_params = compute_v1.AttachedDiskInitializeParams()
    initialize_params.source_image = "projects/ubuntu-os-cloud/global/images/family/ubuntu-2204-lts"
    initialize_params.disk_size_gb = 50
    initialize_params.disk_type = f"zones/{ZONE}/diskTypes/pd-standard"
    disk.initialize_params = initialize_params
    disk.auto_delete = True
    disk.boot = True

    # Network configuration
    network_interface = compute_v1.NetworkInterface()
    network_interface.name = "global/networks/default"
    access_config = compute_v1.AccessConfig()
    access_config.name = "External NAT"
    access_config.type_ = "ONE_TO_ONE_NAT"
    network_interface.access_configs = [access_config]

    # GPU configuration
    gpu = compute_v1.AcceleratorConfig()
    gpu.accelerator_count = GPU_COUNT
    gpu.accelerator_type = f"zones/{ZONE}/acceleratorTypes/{GPU_TYPE}"

    # Metadata with startup script
    metadata = compute_v1.Metadata()
    metadata.items = [
        compute_v1.Items(key="startup-script", value=startup_script)
    ]

    # Instance configuration
    instance = compute_v1.Instance()
    instance.name = INSTANCE_NAME
    instance.machine_type = f"zones/{ZONE}/machineTypes/{MACHINE_TYPE}"
    instance.disks = [disk]
    instance.network_interfaces = [network_interface]
    instance.guest_accelerators = [gpu]
    instance.metadata = metadata
    instance.scheduling = compute_v1.Scheduling()
    instance.scheduling.on_host_maintenance = "TERMINATE"  # Required for GPUs
    instance.scheduling.automatic_restart = False

    # Create the instance
    try:
        console.print(f"[yellow]Requesting GPU instance creation...[/yellow]")
        operation = instance_client.insert(
            project=PROJECT_ID,
            zone=ZONE,
            instance_resource=instance
        )
        
        console.print(f"[yellow]Waiting for instance to be created...[/yellow]")
        # Note: In production, you'd wait for the operation to complete
        # For now, we'll just give it a moment
        time.sleep(5)
        
        # Get instance details
        instance_info = instance_client.get(
            project=PROJECT_ID,
            zone=ZONE,
            instance=INSTANCE_NAME
        )
        
        external_ip = instance_info.network_interfaces[0].access_configs[0].nat_i_p
        
        console.print(f"[bold green]GPU Instance Created Successfully![/bold green]")
        console.print(f"[cyan]Instance Name:[/cyan] {INSTANCE_NAME}")
        console.print(f"[cyan]Zone:[/cyan] {ZONE}")
        console.print(f"[cyan]External IP:[/cyan] {external_ip}")
        console.print(f"[cyan]ComfyUI URL:[/cyan] http://{external_ip}:8188")
        console.print(f"\n[yellow]Note: ComfyUI installation takes ~10-15 minutes.[/yellow]")
        console.print(f"[yellow]Auto-shutdown after 2 hours of runtime.[/yellow]")
        
        # Estimated cost
        cost_per_hour = 0.35  # Approximate for n1-standard-4 + T4
        console.print(f"\n[cyan]Estimated cost:[/cyan] ~${cost_per_hour:.2f}/hour")
        console.print(f"[cyan]Your credits:[/cyan] R$ 1,023 (~$190 USD)")
        
        return external_ip
        
    except Exception as e:
        console.print(f"[red]Error creating instance: {e}[/red]")
        return None

def list_instances(credentials):
    """List all instances in the project"""
    instance_client = compute_v1.InstancesClient(credentials=credentials)
    
    console.print(f"[cyan]Listing instances in {PROJECT_ID}...[/cyan]")
    instances = instance_client.list(project=PROJECT_ID, zone=ZONE)
    
    for instance in instances:
        status = instance.status
        name = instance.name
        console.print(f"  - {name}: {status}")

def delete_instance(credentials, instance_name=INSTANCE_NAME):
    """Delete an instance"""
    instance_client = compute_v1.InstancesClient(credentials=credentials)
    
    console.print(f"[yellow]Deleting instance: {instance_name}...[/yellow]")
    
    try:
        operation = instance_client.delete(
            project=PROJECT_ID,
            zone=ZONE,
            instance=instance_name
        )
        console.print(f"[green]Instance {instance_name} deleted successfully![/green]")
    except Exception as e:
        console.print(f"[red]Error deleting instance: {e}[/red]")

if __name__ == "__main__":
    console.print("[bold]Google Cloud GPU Deployer - ComfyUI[/bold]\n")
    
    # Load credentials
    creds = load_credentials()
    if not creds:
        exit(1)
    
    # Create GPU instance
    ip = create_gpu_instance(creds)
    
    if ip:
        console.print(f"\n[bold green]Deployment successful![/bold green]")
        console.print(f"[dim]Access ComfyUI at: http://{ip}:8188[/dim]")
