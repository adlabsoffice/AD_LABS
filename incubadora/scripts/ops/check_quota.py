import boto3
import os
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

client = boto3.client('service-quotas', region_name='us-east-1')

def check_g_quota():
    console.print("[cyan]Checking vCPU Quota for G instances...[/cyan]")
    try:
        # L-DB2E81BA is the code for "Running On-Demand G instances"
        response = client.get_service_quota(
            ServiceCode='ec2',
            QuotaCode='L-DB2E81BA' 
        )
        quota = response['Quota']['Value']
        console.print(f"[bold]Current Quota for G Instances:[/bold] {quota} vCPUs")
        
        if quota < 4:
            console.print("[red]❌ Quota too low! We need at least 4 vCPUs for g4dn.xlarge.[/red]")
            return False
        else:
            console.print("[green]✅ Quota is sufficient![/green]")
            return True
            
    except Exception as e:
        console.print(f"[yellow]⚠️ Could not fetch specific quota (might need permissions): {e}[/yellow]")
        # Fallback: Try to describe account attributes
        ec2 = boto3.client('ec2')
        try:
            attrs = ec2.describe_account_attributes(AttributeNames=['max-instances'])
            console.print(attrs)
        except:
            pass
        return False

if __name__ == "__main__":
    check_g_quota()
