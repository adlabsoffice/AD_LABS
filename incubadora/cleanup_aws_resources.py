import boto3
import os
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

# Initialize Clients
lambda_client = boto3.client('lambda')
rds = boto3.client('rds')
budgets = boto3.client('budgets')
sts = boto3.client('sts')
iam = boto3.client('iam')

def get_account_id():
    return sts.get_caller_identity()["Account"]

def cleanup_lambda():
    console.print("[bold cyan]Cleaning up Lambda...[/bold cyan]")
    try:
        lambda_client.delete_function(FunctionName='CreditTaskFunction')
        console.print("[green]✅ Lambda Function Deleted[/green]")
    except Exception as e:
        console.print(f"[yellow]⚠️ Lambda Delete: {e}[/yellow]")

    try:
        iam.detach_role_policy(RoleName='CreditTaskLambdaRole', PolicyArn='arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole')
    except:
        pass

    try:
        iam.delete_role(RoleName='CreditTaskLambdaRole')
        console.print("[green]✅ Lambda Role Deleted[/green]")
    except Exception as e:
        console.print(f"[yellow]⚠️ Role Delete: {e}[/yellow]")

def cleanup_rds():
    console.print("[bold cyan]Cleaning up RDS...[/bold cyan]")
    try:
        rds.delete_db_instance(
            DBInstanceIdentifier='credittaskdb',
            SkipFinalSnapshot=True,
            DeleteAutomatedBackups=True
        )
        console.print("[green]✅ RDS Deletion Initiated[/green]")
    except Exception as e:
        console.print(f"[yellow]⚠️ RDS Delete: {e}[/yellow]")

def cleanup_budget():
    console.print("[bold cyan]Cleaning up Budget...[/bold cyan]")
    try:
        account_id = get_account_id()
        budgets.delete_budget(
            AccountId=account_id,
            BudgetName='ZeroSpendCreditTask'
        )
        console.print("[green]✅ Budget Deleted[/green]")
    except Exception as e:
        console.print(f"[yellow]⚠️ Budget Delete: {e}[/yellow]")

if __name__ == "__main__":
    console.print("[bold red]🧹 Starting AWS Resource Cleanup...[/bold red]")
    cleanup_lambda()
    cleanup_rds()
    cleanup_budget()
    console.print("[bold green]✨ Cleanup Finished! (RDS takes a while to disappear)[/bold green]")
