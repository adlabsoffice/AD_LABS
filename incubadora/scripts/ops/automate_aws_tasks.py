import boto3
import time
import os
import json
from rich.console import Console

console = Console()

# Load credentials from .env.aws
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
ec2 = boto3.resource('ec2')
ec2_client = boto3.client('ec2')
iam = boto3.client('iam')
bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')
budgets = boto3.client('budgets')
lambda_client = boto3.client('lambda')
rds = boto3.client('rds')
sts = boto3.client('sts')

def get_account_id():
    return sts.get_caller_identity()["Account"]

def create_lambda_role():
    role_name = 'CreditTaskLambdaRole'
    trust_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {"Service": "lambda.amazonaws.com"},
                "Action": "sts:AssumeRole"
            }
        ]
    }
    try:
        role = iam.create_role(
            RoleName=role_name,
            AssumeRolePolicyDocument=json.dumps(trust_policy)
        )
        return role['Role']['Arn']
    except Exception as e:
        if "EntityAlreadyExists" in str(e):
            return f"arn:aws:iam::{get_account_id()}:role/{role_name}"
        else:
            raise e

def task_1_ec2():
    console.print("[bold cyan]1. Executing EC2 Task...[/bold cyan]")
    try:
        # Launch t3.micro (often free tier eligible now)
        instances = ec2.create_instances(
            ImageId='ami-0c7217cdde317cfec', # Amazon Linux 2023 (us-east-1)
            MinCount=1,
            MaxCount=1,
            InstanceType='t3.micro', 
            TagSpecifications=[{'ResourceType': 'instance', 'Tags': [{'Key': 'Name', 'Value': 'CreditTask'}]}]
        )
        instance = instances[0]
        console.print(f"   Instance {instance.id} launched. Waiting for running state...")
        instance.wait_until_running()
        console.print("   Instance is running!")
        
        # Terminate
        console.print("   Terminating instance...")
        instance.terminate()
        console.print("[green]✅ EC2 Task Completed![/green]")
    except Exception as e:
        console.print(f"[red]❌ EC2 Failed: {e}[/red]")

def task_2_bedrock():
    console.print("[bold cyan]2. Executing Bedrock Task...[/bold cyan]")
    try:
        # Invoke Titan Lite
        body = '{"inputText": "Hello", "textGenerationConfig": {"maxTokenCount": 10, "stopSequences": [], "temperature": 0, "topP": 1}}'
        response = bedrock.invoke_model(
            modelId='amazon.titan-text-lite-v1',
            contentType='application/json',
            accept='application/json',
            body=body
        )
        console.print("   Model invoked successfully.")
        console.print("[green]✅ Bedrock Task Completed![/green]")
    except Exception as e:
        console.print(f"[red]❌ Bedrock Failed (Maybe enable model first?): {e}[/red]")

def task_3_billing():
    console.print("[bold cyan]3. Executing Billing Task...[/bold cyan]")
    try:
        account_id = get_account_id()
        budgets.create_budget(
            AccountId=account_id,
            Budget={
                'BudgetName': 'ZeroSpendCreditTask',
                'BudgetLimit': {'Amount': '10', 'Unit': 'USD'},
                'CostTypes': {'IncludeTax': True, 'IncludeSubscription': True, 'UseBlended': False},
                'TimeUnit': 'MONTHLY',
                'BudgetType': 'COST'
            }
        )
        console.print("[green]✅ Billing Task Completed![/green]")
    except Exception as e:
        if "Duplicate" in str(e):
             console.print("[green]✅ Billing Task Completed (Budget already exists)![/green]")
        else:
            console.print(f"[red]❌ Billing Failed: {e}[/red]")

def task_4_lambda():
    console.print("[bold cyan]4. Executing Lambda Task...[/bold cyan]")
    try:
        # Create Role first
        role_arn = create_lambda_role()
        time.sleep(10) # Wait for role propagation

        # Create a dummy zip for lambda
        import zipfile
        with zipfile.ZipFile('function.zip', 'w') as z:
            z.writestr('lambda_function.py', 'def lambda_handler(event, context): return "Hello"')
        
        with open('function.zip', 'rb') as f:
            zipped_code = f.read()

        lambda_client.create_function(
            FunctionName='CreditTaskFunction',
            Runtime='python3.9',
            Role=role_arn,
            Handler='lambda_function.lambda_handler',
            Code={'ZipFile': zipped_code},
            Timeout=3
        )
        console.print("[green]✅ Lambda Task Completed![/green]")
    except Exception as e:
        if "ResourceConflictException" in str(e):
             console.print("[green]✅ Lambda Task Completed (Function already exists)![/green]")
        else:
             console.print(f"[red]❌ Lambda Failed: {e}[/red]")

def task_5_rds():
    console.print("[bold cyan]5. Executing RDS Task...[/bold cyan]")
    try:
        # Create a very small one.
        rds.create_db_instance(
            DBInstanceIdentifier='credittaskdb',
            DBInstanceClass='db.t3.micro',
            Engine='mysql',
            MasterUsername='admin',
            MasterUserPassword='password1234',
            AllocatedStorage=20,
            BackupRetentionPeriod=0, # Disable backups for faster delete
            MultiAZ=False,
            PubliclyAccessible=False
        )
        console.print("   RDS Creation Initiated.")
        console.print("[green]✅ RDS Task Initiated![/green]")
        console.print("[bold red]⚠️ IMPORTANT: Go to RDS Console later and DELETE 'credittaskdb' to avoid mess![/bold red]")

    except Exception as e:
        if "DBInstanceAlreadyExists" in str(e):
             console.print("[green]✅ RDS Task Completed (DB already exists)![/green]")
        else:
             console.print(f"[red]❌ RDS Failed: {e}[/red]")

if __name__ == "__main__":
    console.print("[bold magenta]🚀 Starting AWS Automation for Credits...[/bold magenta]")
    # task_1_ec2() # Done
    task_2_bedrock()
    task_3_billing()
    task_4_lambda()
    task_5_rds()
    console.print("[bold magenta]✨ Automation Finished![/bold magenta]")
