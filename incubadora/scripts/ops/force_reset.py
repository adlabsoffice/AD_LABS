import boto3
import os
import time
from rich.console import Console

console = Console()

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

def force_reset():
    console.print("[bold red]FORCE RESETTING BRAIN...[/bold red]")

    # 1. Terminate Instances
    console.print("Terminating Brain instances...")
    instances = ec2.instances.filter(
        Filters=[{'Name': 'tag:Name', 'Values': ['Brain-n8n']}, 
                 {'Name': 'instance-state-name', 'Values': ['running', 'pending', 'stopped']}]
    )
    ids = [i.id for i in instances]
    if ids:
        ec2.instances.filter(InstanceIds=ids).terminate()
        console.print(f"Terminating: {ids}")
        
        # Wait for termination
        console.print("Waiting for termination...")
        while True:
            response = ec2_client.describe_instances(InstanceIds=ids)
            states = [i['State']['Name'] for r in response['Reservations'] for i in r['Instances']]
            if all(s == 'terminated' for s in states):
                break
            time.sleep(5)
        console.print("Instances Terminated.")
    else:
        console.print("No instances found.")

    # 2. Delete Key Pair on AWS
    console.print("Deleting Key Pair 'brain-key' on AWS...")
    try:
        ec2_client.delete_key_pair(KeyName='brain-key')
        console.print("Key Pair Deleted on AWS.")
    except Exception as e:
        console.print(f"Key Delete Error: {e}")

    # 3. Delete Local Key File
    if os.path.exists("brain-key.pem"):
        try:
            os.remove("brain-key.pem")
            console.print("Local Key File Deleted.")
        except Exception as e:
            console.print(f"Could not delete local file: {e}")
    else:
        console.print("Local Key File not found.")

    console.print("[green]RESET COMPLETE. NOW RUN DEPLOY.[/green]")

if __name__ == "__main__":
    force_reset()
