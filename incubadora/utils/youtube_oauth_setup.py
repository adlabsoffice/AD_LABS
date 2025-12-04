"""
YouTube OAuth2 Setup Helper

Gera refresh_token para YouTube Data API v3.
Salva credenciais em arquivo seguro (gitignored).

Autor: Refatoração Arquitetural P1
Data: 04/12/2024

Uso:
    python utils/youtube_oauth_setup.py
"""

import os
import json
import webbrowser
from pathlib import Path

try:
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    GOOGLE_AUTH_AVAILABLE = True
except ImportError:
    GOOGLE_AUTH_AVAILABLE = False
    print("❌ google-auth-oauthlib não instalado!")
    print("Execute: pip install google-auth-oauthlib")
    exit(1)


# Scopes necessários para YouTube
SCOPES = [
    'https://www.googleapis.com/auth/youtube.upload',
    'https://www.googleapis.com/auth/youtube.readonly',
    'https://www.googleapis.com/auth/youtube.force-ssl'
]


def setup_youtube_oauth():
    """
    Guia interativo para setup OAuth2 YouTube.
    """
    print("\n" + "="*60)
    print("🔐 YouTube OAuth2 Setup")
    print("="*60 + "\n")
    
    # Verifica se client_secret.json existe
    client_secret_path = Path("client_secret.json")
    
    if not client_secret_path.exists():
        print("❌ Arquivo client_secret.json não encontrado!\n")
        print("PASSOS PARA CRIAR:\n")
        print("1. Acesse: https://console.cloud.google.com")
        print("2. Crie projeto (ou selecione existente)")
        print("3. Habilite 'YouTube Data API v3'")
        print("4. Vá em 'Credentials' → 'CREATE CREDENTIALS' → 'OAuth client ID'")
        print("5. Application type: 'Desktop app'")
        print("6. Baixe o JSON e salve como: client_secret.json\n")
        print("="*60)
        return
    
    print("✓ client_secret.json encontrado\n")
    
    try:
        # Cria flow de autenticação
        flow = InstalledAppFlow.from_client_secrets_file(
            str(client_secret_path),
            SCOPES
        )
        
        print("1. Abrindo navegador para autorização Google...")
        print("2. Faça login na sua conta Google")
        print("3. Autorize acesso ao YouTube")
        print("4. Aguarde redirecionamento (pode fechar janela depois)\n")
        
        # Run local server para callback
        credentials = flow.run_local_server(
            port=8080,
            prompt='consent',
            success_message='Autorização concluída! Você pode fechar esta janela.'
        )
        
        print("\n✅ Autenticação bem-sucedida!\n")
        
        # Extrai informações das credenciais
        creds_data = {
            "client_id": credentials.client_id,
            "client_secret": credentials.client_secret,
            "refresh_token": credentials.refresh_token,
            "token_uri": credentials.token_uri
        }
        
        # Salva em arquivo seguro
        output_path = Path("youtube_credentials.json")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(creds_data, f, indent=2)
        
        print(f"✓ Credenciais salvas em: {output_path}")
        print("\n" + "="*60)
        print("⚠️  IMPORTANTE: Este arquivo está no .gitignore")
        print("    NUNCA commite youtube_credentials.json no Git!")
        print("="*60 + "\n")
        
        # Mostra exemplo de uso
        print("📋 PRÓXIMO PASSO: Adicione ao canal_config.json\n")
        print("Copie este trecho:\n")
        print(json.dumps({
            "youtube": {
                "client_id": creds_data["client_id"],
                "client_secret": creds_data["client_secret"],
                "refresh_token": creds_data["refresh_token"],
                "default_privacy": "unlisted",
                "default_category": 22,
                "max_retries": 3
            }
        }, indent=2))
        print("\n" + "="*60)
        print("✅ Setup YouTube completo!")
        print("="*60 + "\n")
    
    except Exception as e:
        print(f"\n❌ Erro durante autenticação: {e}\n")
        print("Tente novamente. Se persistir:")
        print("1. Verifique se client_secret.json está correto")
        print("2. Confirme que YouTube Data API v3 está habilitada")
        print("3. Verifique firewall/proxy (porta 8080 precisa estar aberta)")


if __name__ == "__main__":
    setup_youtube_oauth()
