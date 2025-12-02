import boto3
import os
import time
from rich.console import Console

console = Console()

# Load credentials
def load_aws_env():
    env_path = os.path.join(os.getcwd(), ".env.aws")
    if os.path.exists(env_path):
        with open(env_path, "r") as f:
            for line in f:
                if "=" in line:
                    key, value = line.strip().split("=", 1)
                    os.environ[key] = value

load_aws_env()

ec2 = boto3.resource('ec2')
ec2_client = boto3.client('ec2')

def get_latest_ubuntu_ami():
    # Find latest Ubuntu 22.04 LTS AMI
    response = ec2_client.describe_images(
        Filters=[
            {'Name': 'name', 'Values': ['ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*']},
            {'Name': 'virtualization-type', 'Values': ['hvm']},
            {'Name': 'owner-id', 'Values': ['099720109477']} # Canonical
        ],
        Owners=['099720109477']
    )
    # Sort by CreationDate
    images = sorted(response['Images'], key=lambda x: x['CreationDate'], reverse=True)
    return images[0]['ImageId']

def create_security_group(group_name='muscle-sg'):
    console.print(f"[cyan]Creating Security Group: {group_name}...[/cyan]")
    try:
        response = ec2_client.describe_vpcs()
        vpc_id = response['Vpcs'][0]['VpcId']

        try:
            sg = ec2.create_security_group(GroupName=group_name, Description='Muscle GPU Server Security Group', VpcId=vpc_id)
            sg_id = sg.id
            console.print(f"[green]✅ Security Group created: {sg_id}[/green]")
        except Exception as e:
            if 'InvalidGroup.Duplicate' in str(e):
                console.print(f"[yellow]⚠️ Security Group {group_name} already exists. Using existing.[/yellow]")
                response = ec2_client.describe_security_groups(GroupNames=[group_name])
                sg_id = response['SecurityGroups'][0]['GroupId']
                sg = ec2.SecurityGroup(sg_id)
            else:
                raise e

        # Allow SSH, ComfyUI (8188)
        try:
            sg.authorize_ingress(
                IpPermissions=[
                    {'IpProtocol': 'tcp', 'FromPort': 22, 'ToPort': 22, 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
                    {'IpProtocol': 'tcp', 'FromPort': 8188, 'ToPort': 8188, 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
                ]
            )
            console.print("[green]✅ Ingress rules added (SSH, 8188)[/green]")
        except Exception as e:
            if 'InvalidPermission.Duplicate' not in str(e):
                console.print(f"[yellow]⚠️ Ingress Rules: {e}[/yellow]")
        
        return sg_id
    except Exception as e:
        console.print(f"[red]❌ Security Group Failed: {e}[/red]")
        raise e

def launch_muscle_instance(key_name, sg_id):
    console.print("[bold cyan]🚀 Launching Muscle Instance (g4dn.xlarge)...[/bold cyan]")
    
    ami_id = get_latest_ubuntu_ami()
    console.print(f"   Using AMI: {ami_id} (Ubuntu 22.04)")

    # User Data to install Drivers + ComfyUI
    user_data = '''#!/bin/bash
# Log output
exec > >(tee /var/log/user-data.log|logger -t user-data -s 2>/dev/console) 2>&1

echo "Starting Install..."
apt-get update
apt-get upgrade -y

# 1. Install Dependencies
apt-get install -y python3-pip python3-venv git wget

# 2. Install NVIDIA Drivers (This takes a while)
apt-get install -y ubuntu-drivers-common
ubuntu-drivers autoinstall

# 3. Setup ComfyUI
mkdir -p /home/ubuntu/AI
cd /home/ubuntu/AI
git clone https://github.com/comfyanonymous/ComfyUI
cd ComfyUI

# Create venv
python3 -m venv venv
source venv/bin/activate

# Install Torch (CUDA 12.1)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
pip install -r requirements.txt

# 4. Download Manager
cd custom_nodes
git clone https://github.com/ltdrdata/ComfyUI-Manager.git
cd ..

# 5. Create Systemd Service for Auto-Start
cat <<EOF > /etc/systemd/system/comfyui.service
[Unit]
Description=ComfyUI
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/AI/ComfyUI
ExecStart=/home/ubuntu/AI/ComfyUI/venv/bin/python main.py --listen 0.0.0.0 --port 8188
Restart=always

[Install]
WantedBy=multi-user.target
EOF

systemctl enable comfyui
systemctl start comfyui

echo "Install Complete!"
'''

    try:
        instances = ec2.create_instances(
            ImageId=ami_id,
            MinCount=1,
            MaxCount=1,
            InstanceType='g4dn.xlarge',
            KeyName=key_name,
            SecurityGroupIds=[sg_id],
            UserData=user_data,
            TagSpecifications=[{'ResourceType': 'instance', 'Tags': [{'Key': 'Name', 'Value': 'Muscle-ComfyUI'}]}],
            BlockDeviceMappings=[
                {
                    'DeviceName': '/dev/sda1',
                    'Ebs': {
                        'VolumeSize': 100, # 100GB for Models
                        'VolumeType': 'gp3'
                    }
                }
            ]
        )
        instance = instances[0]
        console.print(f"   Instance {instance.id} launched. Waiting for running state...")
        instance.wait_until_running()
        instance.reload()
        
        public_ip = instance.public_ip_address
        console.print(f"[bold green]✅ Muscle is ALIVE![/bold green]")
        console.print(f"   IP: {public_ip}")
        console.print(f"   ComfyUI URL: http://{public_ip}:8188")
        console.print(f"[yellow]⏳ Note: It takes about 10-15 minutes for NVIDIA Drivers to install. Go grab a coffee![/yellow]")
        
        return public_ip
    except Exception as e:
        console.print(f"[red]❌ Launch Failed: {e}[/red]")
        raise e

if __name__ == "__main__":
    try:
        # Reuse the key from Brain
        key_name = 'brain-key' 
        sg_id = create_security_group()
        launch_muscle_instance(key_name, sg_id)
    except Exception as e:
        console.print(f"[bold red]🔥 Deployment Failed: {e}[/bold red]")
