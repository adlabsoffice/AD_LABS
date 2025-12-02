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

def create_key_pair(key_name='brain-key-v2'):
    console.print(f"[cyan]Creating Key Pair: {key_name}...[/cyan]")
    try:
        key_pair = ec2_client.create_key_pair(KeyName=key_name)
        with open(f'{key_name}.pem', 'w') as f:
            f.write(key_pair['KeyMaterial'])
        console.print(f"[green]Key Pair created and saved to {key_name}.pem[/green]")
        return key_name
    except Exception as e:
        if 'InvalidKeyPair.Duplicate' in str(e):
            console.print(f"[yellow]Key Pair {key_name} already exists. Using existing.[/yellow]")
            return key_name
        else:
            console.print(f"[red]Key Pair Failed: {e}[/red]")
            raise e

def create_security_group(group_name='brain-sg'):
    console.print(f"[cyan]Creating Security Group: {group_name}...[/cyan]")
    try:
        response = ec2_client.describe_vpcs()
        vpc_id = response['Vpcs'][0]['VpcId']

        try:
            sg = ec2.create_security_group(GroupName=group_name, Description='Brain Server Security Group', VpcId=vpc_id)
            sg_id = sg.id
            console.print(f"[green]Security Group created: {sg_id}[/green]")
        except Exception as e:
            if 'InvalidGroup.Duplicate' in str(e):
                console.print(f"[yellow]Security Group {group_name} already exists. Using existing.[/yellow]")
                response = ec2_client.describe_security_groups(GroupNames=[group_name])
                sg_id = response['SecurityGroups'][0]['GroupId']
                sg = ec2.SecurityGroup(sg_id)
            else:
                raise e

        # Allow SSH, HTTP, HTTPS, n8n (5678)
        try:
            sg.authorize_ingress(
                IpPermissions=[
                    {'IpProtocol': 'tcp', 'FromPort': 22, 'ToPort': 22, 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
                    {'IpProtocol': 'tcp', 'FromPort': 80, 'ToPort': 80, 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
                    {'IpProtocol': 'tcp', 'FromPort': 443, 'ToPort': 443, 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
                    {'IpProtocol': 'tcp', 'FromPort': 5678, 'ToPort': 5678, 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
                ]
            )
            console.print("[green]Ingress rules added (SSH, 80, 443, 5678)[/green]")
        except Exception as e:
            if 'InvalidPermission.Duplicate' not in str(e):
                console.print(f"[yellow]Ingress Rules: {e}[/yellow]")
        
        return sg_id
    except Exception as e:
        console.print(f"[red]Security Group Failed: {e}[/red]")
        raise e

def launch_brain_instance(key_name, sg_id):
    console.print("[bold cyan]Launching Brain Instance (t3.micro)...[/bold cyan]")
    
    user_data = '''#!/bin/bash
yum update -y
yum install -y docker
service docker start
usermod -a -G docker ec2-user
systemctl enable docker
docker run -d --restart always --name n8n -p 5678:5678 -e N8N_BASIC_AUTH_ACTIVE=true -e N8N_BASIC_AUTH_USER=admin -e N8N_BASIC_AUTH_PASSWORD=password123 n8nio/n8n
'''

    try:
        instances = ec2.create_instances(
            ImageId='ami-0c7217cdde317cfec', # Amazon Linux 2023 (us-east-1)
            MinCount=1,
            MaxCount=1,
            InstanceType='t3.micro',
            KeyName=key_name,
            SecurityGroupIds=[sg_id],
            UserData=user_data,
            TagSpecifications=[{'ResourceType': 'instance', 'Tags': [{'Key': 'Name', 'Value': 'Brain-n8n'}]}],
            MetadataOptions={'HttpTokens': 'optional', 'HttpEndpoint': 'enabled'}
        )
        instance = instances[0]
        console.print(f"   Instance {instance.id} launched. Waiting for running state...")
        instance.wait_until_running()
        instance.reload()
        
        public_ip = instance.public_ip_address
        console.print(f"[bold green]Brain is ALIVE![/bold green]")
        console.print(f"   IP: {public_ip}")
        console.print(f"   n8n URL: http://{public_ip}:5678")
        console.print(f"   User: admin")
        console.print(f"   Pass: password123")
        console.print(f"[yellow]Note: It takes about 2-3 minutes for Docker to install and start n8n. Be patient![/yellow]")
        
        return public_ip
    except Exception as e:
        console.print(f"[red]Launch Failed: {e}[/red]")
        raise e

if __name__ == "__main__":
    try:
        key_name = create_key_pair()
        sg_id = create_security_group()
        launch_brain_instance(key_name, sg_id)
    except Exception as e:
        console.print(f"[bold red]Deployment Failed: {e}[/bold red]")
