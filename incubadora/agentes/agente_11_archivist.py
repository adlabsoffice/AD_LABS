import os
import shutil
import time
from rich.console import Console

# Imports para upload real em cloud
try:
    import boto3
    from botocore.exceptions import ClientError, NoCredentialsError
    BOTO3_AVAILABLE = True
except ImportError:
    BOTO3_AVAILABLE = False
    print("WARNING: boto3 não instalado. S3 não funcionará. Instale com: pip install boto3")

try:
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload
    from googleapiclient.errors import HttpError
    GOOGLE_DRIVE_AVAILABLE = True
except ImportError:
    GOOGLE_DRIVE_AVAILABLE = False
    print("WARNING: google-api-python-client não instalado. Drive não funcionará.")

console = Console()

class Agente11Archivist:
    def __init__(self):
        # Configurações AWS S3
        if BOTO3_AVAILABLE:
            try:
                self.s3_client = boto3.client(
                    's3',
                    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
                    region_name=os.getenv('AWS_REGION', 'us-east-1')
                )
                self.s3_bucket = os.getenv('S3_BUCKET_NAME', 'adlabs-videos')
            except Exception as e:
                console.print(f"[yellow]Aviso S3: {e}[/yellow]")
                self.s3_client = None
                self.s3_bucket = None
        else:
            self.s3_client = None
            self.s3_bucket = None
        
        # Configurações Google Drive
        self.drive_service = None
        if GOOGLE_DRIVE_AVAILABLE:
            credentials_path = os.getenv('GOOGLE_DRIVE_CREDENTIALS', 'client_secret.json')
            if os.path.exists(credentials_path):
                try:
                    creds = service_account.Credentials.from_service_account_file(
                        credentials_path,
                        scopes=['https://www.googleapis.com/auth/drive.file']
                    )
                    self.drive_service = build('drive', 'v3', credentials=creds)
                except Exception as e:
                    console.print(f"[yellow]Aviso Drive: {e}[/yellow]")

    def arquivar_projeto(self, config, video_path=None):
        """
        Gerencia o upload para Google Drive (Aprovação) e S3 (Arquivo Morto).
        """
        console.print(f"[bold yellow]AGENTE 11 (ALMOXARIFE): Iniciando Arquivamento Hibrido...[/bold yellow]")
        
        nome_canal = config.get('nome_canal', 'Canal_Desconhecido')
        projeto_id = f"{time.strftime('%Y-%m-%d')}_{nome_canal.replace(' ', '_')}"
        
        # 1. Upload para Google Drive (Vitrine) - REAL
        console.print(f"   [cyan]Google Drive (Vitrine):[/cyan] Enviando assets de aprovacao...")
        
        if self.drive_service:
            # Tenta encontrar vídeo se não fornecido
            if not video_path:
                # Procura no diretório de saída padrão
                default_dir = os.path.join("outputs", "T08_videos_finais")
                if os.path.exists(default_dir):
                    files = [f for f in os.listdir(default_dir) if f.endswith(".mp4")]
                    if files:
                        # Pega o mais recente
                        files.sort(key=lambda x: os.path.getmtime(os.path.join(default_dir, x)), reverse=True)
                        video_path = os.path.join(default_dir, files[0])

            if video_path and os.path.exists(video_path):
                try:
                    file_metadata = {
                        'name': f'{projeto_id}_video_final.mp4',
                        'parents': [os.getenv('GOOGLE_DRIVE_FOLDER_ID', 'root')]
                    }
                    media = MediaFileUpload(
                        video_path,
                        mimetype='video/mp4',
                        resumable=True
                    )
                file = self.drive_service.files().create(
                    body=file_metadata,
                    media_body=media,
                    fields='id, webViewLink'
                ).execute()
                
                console.print(f"      -> [green]Video no Drive: {file.get('webViewLink')}[/green]")
            except HttpError as e:
                console.print(f"      -> [yellow]Aviso Drive: {e}[/yellow]")
            except Exception as e:
                console.print(f"      -> [yellow]Erro Drive: {e}[/yellow]")
        else:
            if not self.drive_service:
                console.print(f"      -> [yellow]Google Drive não configurado (credenciais ausentes)[/yellow]")
            elif not video_path or not os.path.exists(video_path):
                console.print(f"      -> [yellow]Vídeo final não encontrado para upload (caminho: {video_path})[/yellow]")
        
        # 2. Upload para AWS S3 (Cofre) - REAL
        console.print(f"   [cyan]AWS S3 (Cofre):[/cyan] Arquivando projeto completo...")
        
        if self.s3_client and self.s3_bucket:
            try:
                # Upload de todos os arquivos da pasta outputs
                upload_count = 0
                for root, dirs, files in os.walk("outputs"):
                    for file in files:
                        local_path = os.path.join(root, file)
                        s3_key = f"{projeto_id}/{os.path.relpath(local_path, 'outputs').replace(os.sep, '/')}"
                        
                        try:
                            self.s3_client.upload_file(
                                local_path,
                                self.s3_bucket,
                                s3_key
                            )
                            upload_count += 1
                            console.print(f"      -> [green]Uploaded: {file}[/green]")
                        except ClientError as e:
                            console.print(f"      -> [red]Erro ao fazer upload de {file}: {e}[/red]")
                
                console.print(f"      -> [bold green]Backup S3 Completo! ({upload_count} arquivos)[/bold green]")
            except NoCredentialsError:
                console.print(f"      -> [red]ERRO: Credenciais AWS não configuradas![/red]")
                console.print(f"      -> [yellow]Configure AWS_ACCESS_KEY_ID e AWS_SECRET_ACCESS_KEY no .env[/yellow]")
                raise
            except Exception as e:
                console.print(f"      -> [red]Erro S3: {e}[/red]")
                raise
        else:
            if not BOTO3_AVAILABLE:
                console.print(f"      -> [red]ERRO: boto3 não instalado. Instale com: pip install boto3[/red]")
            elif not self.s3_client:
                console.print(f"      -> [red]ERRO: S3 não configurado (credenciais ausentes no .env)[/red]")
            raise RuntimeError("S3 upload falhou: configuração incompleta")

        # 3. Limpeza do Chão de Fábrica (Muscle)
        console.print(f"   [cyan]Limpeza:[/cyan] Removendo arquivos temporarios locais...")
        # Na produção real: shutil.rmtree("output")
        # Por segurança, apenas logando por enquanto
        console.print(f"      -> [green]Espaço será liberado após confirmação de uploads[/green]")

        return True

