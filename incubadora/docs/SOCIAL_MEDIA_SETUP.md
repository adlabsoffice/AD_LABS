# Configuração de Redes Sociais - AD_LABS

Guia completo para configurar publicação automatizada em YouTube, Instagram e TikTok.

---

## 📋 Índice

1. [Visão Geral](#visão-geral)
2. [YouTube Setup](#youtube-setup-oauth2)
3. [Instagram Setup](#instagram-setup)
4. [TikTok Status](#tiktok-futuro)
5. [Telegram Approval](#telegram-approval-flow)
6. [Troubleshooting](#troubleshooting)

---

## Visão Geral

O AD_LABS usa **Strategy Pattern** para publicação em redes sociais:

```python
from agentes.agente_12_publisher import Agente12Publisher
from specs.schemas.social_media_config import PublishMetadata

# Cria agente com configurações
agente = Agente12Publisher(
    canal_id="o_livro_caixa_divino",
    config={
        "youtube": {...},
        "instagram": {...}
    }
)

# Publica em plataforma específica
metadata = PublishMetadata(titulo="...", descricao="...")
url = agente.publicar("youtube", video_path, metadata)

# Ou cross-posting em múltiplas plataformas
urls = agente.publicar_multiplas_plataformas(
    ["youtube", "instagram"],
    video_path,
    metadata
)
```

---

## YouTube Setup (OAuth2)

### Pré-requisitos

- Conta Google com canal YouTube
- Acesso ao [Google Cloud Console](https://console.cloud.google.com)

### Passo 1: Criar Projeto Google Cloud

1. Acesse https://console.cloud.google.com
2. Clique em "Select a project" → "NEW PROJECT"
3. Nome: `AD_LABS_YouTube_Automation`
4. Clique "CREATE"

### Passo 2: Habilitar YouTube Data API v3

1. No projeto criado, vá em "APIs & Services" → "Library"
2. Pesquise "YouTube Data API v3"
3. Clique "ENABLE"

###Passo 3: Criar OAuth 2.0 Credentials

1. "APIs & Services" → "Credentials"
2. "CREATE CREDENTIALS" → "OAuth client ID"
3. Application type: **Desktop app**
4. Name: `AD_LABS_Desktop_Client`
5. Clique "CREATE"

6. **Download JSON:**
   - Clique no ícone de download
   - Salve como: `d:\AD_LABS\incubadora\client_secret.json`
   - ⚠️ **NÃO COMMITE ESTE ARQUIVO!** (já está no .gitignore)

### Passo 4: Gerar Refresh Token

Execute o helper script:

```bash
cd d:\AD_LABS\incubadora
python utils\youtube_oauth_setup.py
```

O script vai:
1. Ler `client_secret.json`
2. Abrir navegador para autorização Google
3. Pedir código de autorização
4. Gerar `refresh_token`
5. Salvar em `youtube_credentials.json`

**Exemplo de interação:**
```
🔐 YouTube OAuth2 Setup
═══════════════════════════════════════

1. Abrindo navegador...
2. Faça login na sua conta Google
3. Autorize acesso ao YouTube
4. Copie o código mostrado

Cole o código aqui: 4/0AfJoh...

✅ Autenticação bem-sucedida!
✓ refresh_token salvo em: youtube_credentials.json

Adicione ao seu canal_config.json:
{
  "youtube": {
    "client_id": "123456.apps.googleusercontent.com",
    "client_secret": "XXX",
    "refresh_token": "1//0gXXX..."
  }
}
```

### Passo 5: Adicionar Credenciais ao Config

Edite `config/o_livro_caixa_divino/canal_config.json`:

```json
{
  "youtube": {
    "client_id": "<COPIE DO youtube_credentials.json>",
    "client_secret": "<COPIE DO youtube_credentials.json>",
    "refresh_token": "<COPIE DO youtube_credentials.json>",
    "default_privacy": "unlisted",
    "default_category": 22
  }
}
```

### Teste

```python
from services.social_media.youtube_publisher import YouTubePublisher

config = {...}  # Config acima
publisher = YouTubePublisher(config)

print(publisher.is_available())  # Deve retornar True
```

---

## Instagram Setup

### Opção 1: instagrapi (Recomendado)

**Prós:** 
- Setup simples
- Funciona imediatamente
- Suporta Reels + Stories

**Contras:**
- API não-oficial
- Pode quebrar se Instagram mudar

### Instalação

```bash
pip install instagrapi
```

### Configuração

Edite `canal_config.json`:

```json
{
  "instagram": {
    "username": "seu_usuario",
    "password": "sua_senha",
    "use_official_api": false,
    "max_retries": 3
  }
}
```

⚠️ **Segurança:** 
- Use conta dedicada (não pessoal)
- Habilite 2FA
- Se receber "Challenge Required", faça login manual no app

### Teste

```python
from services.social_media.instagram_publisher import InstagramPublisher

config = {...}
publisher = InstagramPublisher(config)

print(publisher.is_available())  # True
```

---

### Opção 2: Instagram Graph API (Futuro)

Requer Facebook Business Account e aprovação de App.

**Status:** Não implementado (use instagrapi no interim).

---

## TikTok (Futuro)

**Status:** ⚠️ Aguardando aprovação de Developer App (2-4 semanas)

### Alternativas Atuais

**1. Workflow n8n:**
```
incubadora/n8n_workflows/03_tiktok_posting.json
```

**2. Upload Manual:**
- TikTok Creator Studio: https://www.tiktok.com/creator-center/upload

**3. Aguardar API:**

Quando aprovado, o `TikTokPublisher` será implementado automaticamente.

---

## Telegram Approval Flow

### Setup

1. Crie bot no [@BotFather](https://t.me/BotFather)
2. Copie token → `.env`:
   ```
   TELEGRAM_BOT_TOKEN=123456:ABCDEF...
   ```

3. Obtenha seu Chat ID:
   ```bash
   python get_telegram_id.py
   ```

4. Salve em `telegram_id.txt`

### Fluxo de Aprovação

```python
agente.publicar(
    "youtube",
    video_path,
    metadata,
    approval_required=True  # ← Aguarda Telegram
)
```

**O que acontece:**
1. Agente envia vídeo preview no Telegram
2. Mostra botões "✅ APROVAR" / "❌ CANCELAR"
3. Aguarda resposta (timeout: 10min padrão)
4. Se aprovado → publica
5. Se rejeitado → cancela

**Configurações:**
```json
{
  "approval_flow": {
    "require_telegram_approval": true,
    "timeout_minutos": 10,
    "auto_publish_after_hours": null  // null = nunca auto-publica
  }
}
```

---

## Troubleshooting

### YouTube: "Request had insufficient authentication scopes"

**Causa:** Refresh token expirado ou scopes insuficientes.

**Solução:**
1. Delete `youtube_credentials.json`
2. Re-execute `python utils/youtube_oauth_setup.py`
3. Autorize novamente

---

### Instagram: "Challenge Required"

**Causa:** Instagram detectou login suspeito.

**Solução:**
1. Faça login manual no app Instagram
2. Complete verificação de segurança
3. Tente novamente após 1h

---

### TikTok: "Not Implemented"

**Normal.** TikTok API aguardando aprovação.

**Use:** Workflow n8n ou upload manual no interim.

---

## Arquivos Importantes

```
incubadora/
├── config/
│   ├── social_media_template.json     ← Template de config
│   └── o_livro_caixa_divino/
│       └── canal_config.json          ← Seu config (crie este)
├── client_secret.json                 ← OAuth Google (GITIGNORED)
├── youtube_credentials.json           ← Refresh token (GITIGNORED)
├── utils/
│   └── youtube_oauth_setup.py        ← Helper OAuth2
└── services/
    └── social_media/
        ├── youtube_publisher.py
        ├── instagram_publisher.py
        └── tiktok_publisher.py
```

---

## Segurança

✅ **O que é seguro commitar:**
- `social_media_template.json` (placeholders)
- Código dos publishers

❌ **NUNCA commite:**
- `client_secret.json`
- `youtube_credentials.json`
- `canal_config.json` com credenciais reais
- `.env` com tokens

**Já protegido pelo `.gitignore`!**

---

## Suporte

**Problemas?**
1. Verifique logs: `logger` em cada publisher
2. Teste `publisher.is_available()` retorna `True`
3. Confira `.env` e `canal_config.json`

**Para adicionar nova plataforma:**

```python
# 1. Crie publisher
class RumblePublisher(SocialMediaPublisher):
    # ...

# 2. Registre na factory
PublisherFactory.register_publisher("rumble", RumblePublisher)

# 3. Use
agente.publicar("rumble", video, metadata)
```

---

**✅ Setup completo! Boas publicações automáticas!**
