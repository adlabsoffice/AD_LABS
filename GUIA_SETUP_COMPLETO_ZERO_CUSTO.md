# 🎓 GUIA DEFINITIVO: SETUP COMPLETO CUSTO ZERO
## Tutorial Passo a Passo com Prints de Cada Tela

---

## 🎯 OBJETIVO

Configurar incubadora gastando **R$ 0,00** nos primeiros 6 meses, usando:
- ✅ Ferramentas 100% grátis (sem créditos)
- ✅ Créditos Google/AWS APENAS se necessário
- ✅ Otimizações para custo mínimo

---

## 📊 ESTRATÉGIA DE CUSTO ZERO

### **Tier 1: SEMPRE GRÁTIS** (Use ESTES primeiro)
```
Groq: 14.4K requests/dia (texto)
Pollinations.AI: Ilimitado (imagens)
Supabase: 500MB (storage)
YouTube Data API: 10K units/dia (pesquisa)
Google TTS: 1M caracteres/mês (narração)
```

### **Tier 2: CRÉDITOS** (Só se Tier 1 não bastar)
```
Google Cloud: U$ 300 (Imagen, se precisar)
AWS: U$ 100 (servidor vídeo, se precisar)
```

### **Tier 3: EVITAR** (Pago)
```
ElevenLabs, MidJourney, Claude, etc.
```

---

## 🗺️ MAPA COMPLETO DE CONFIGURAÇÕES

### **O que você VAI configurar** (tudo tem tutorial):

| # | Ferramenta | Objetivo | Custo | Tutorial |
|---|------------|----------|-------|----------|
| 1 | **Groq** | Gerar texto (roteiros, ideias) | R$ 0 | Abaixo |
| 2 | **Grok** | Backup texto | U$ 25/mês grátis | Abaixo |
| 3 | **Pollinations** | Gerar imagens | R$ 0 | Abaixo |
| 4 | **Supabase** | Hospedar assets | R$ 0 | Abaixo |
| 5 | **Google TTS** | Narração voz | 1M grátis/mês | Abaixo |
| 6 | **YouTube API** | Pesquisar canais | R$ 0 | Abaixo |
| 7 | **AWS EC2** | Servidor vídeo | Free tier | Abaixo |

---

## 📋 TUTORIAL 1: GROQ API (5 minutos)

### **🎯 O que é**: IA grátis, 14.4K requests/dia

### **PASSO 1: Criar Conta**
```
1. Abrir navegador
2. Ir para: groq.com
3. Clicar "Sign In" (canto superior direito)
4. Escolher "Sign up with Google" OU "Email"
   → Se Google: autorizar acesso
   → Se Email: criar senha
5. Confirmar email (checar caixa de entrada)
```

**✅ TELA QUE VOCÊ VÊ**:
```
╔════════════════════════════════════╗
║  Welcome to Groq Console           ║
║                                    ║
║  [  Get Started  ]                 ║
╚════════════════════════════════════╝
```

---

### **PASSO 2: Criar API Key**
```
1. Na tela inicial, clicar "API Keys" (menu esquerdo)
   
   OU ir direto: console.groq.com/keys

2. Clicar botão "Create API Key"

3. Dar nome: "incubadora-key"

4. Clicar "Submit"

5. ⚠️ COPIAR A KEY (mostra só uma vez!)
   Exemplo: gsk_xxxxxxxxxxxxxxxxxxxxx

6. Clicar "Done"
```

**✅ COMO SALVAR**:
```
1. Abrir Notepad
2. Colar:
   GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxx
3. Salvar como: chaves.txt
4. Guardar em local seguro
```

---

### **PASSO 3: Testar API**

**Pelo navegador** (sem código):
```
1. Ir para: console.groq.com/playground

2. Em "Model", selecionar: llama-3.1-70b-versatile

3. Em "Messages", digitar:
   "Escreva uma história curta de vingança"

4. Clicar "Generate"

5. ✅ Se aparecer texto → Funcionou!
```

**Pelo Python** (depois):
```python
import os
from groq import Groq

# Sua key aqui
os.environ['GROQ_API_KEY'] = 'gsk_xxxxx'

client = Groq()
response = client.chat.completions.create(
    model="llama-3.1-70b-versatile",
    messages=[{"role": "user", "content": "Teste"}]
)

print(response.choices[0].message.content)
```

---

## 📋 TUTORIAL 2: GROK API (10 minutos)

### **🎯 O que é**: IA da X, U$ 25/mês grátis até fim 2024

### **PASSO 1: Acessar Console**
```
1. Ir para: console.x.ai

2. Clicar "Sign in"

3. OPÇÃO A (Recomendado):
   → "Continue with X"
   → Login com sua conta Twitter/X
   
   OPÇÃO B:
   → "Sign up with email"
   → Preencher dados
```

---

### **PASSO 2: Setup Billing** (Para U$ 25 grátis)
```
1. No console, ir em "Billing" (menu esquerdo)

2. Clicar "Add payment method"

3. Preencher:
   - Cartão (não vai cobrar U$ 25 grátis)
   - Nome
   - Endereço
   
4. Salvar

5. ✅ Confirmar: "Free credits: $25.00"
```

---

### **PASSO 3: Criar API Key**
```
1. Menu esquerdo → "API Keys"

2. Clicar "Create new key"

3. Settings:
   - Name: "incubadora"
   - Permissions: "Full access"
   - Models: "All models"

4. Clicar "Create"

5. ⚠️ COPIAR A KEY
   Exemplo: xai-xxxxxxxxxxxxxxxxxxxxx

6. Salvar em chaves.txt
```

---

## 📋 TUTORIAL 3: POLLINATIONS.AI (1 minuto!)

### **🎯 O que é**: Imagens grátis ilimitadas, SEM cadastro!

### **NÃO PRECISA CADASTRO!**

**Uso direto**:
```python
# Literalmente só isso!
prompt = "dark background video for youtube, cinematic"
url = f"https://image.pollinations.ai/prompt/{prompt}"

# URL já é a imagem PNG!
# Pode usar direto ou baixar
```

**Testar no navegador**:
```
1. Abrir: https://image.pollinations.ai/prompt/dark%20cinematic%20background

2. ✅ Imagem aparece direto!

3. Botão direito → "Salvar imagem"
```

**✅ Zero configuração necessária!**

---

## 📋 TUTORIAL 4: SUPABASE (10 minutos)

### **🎯 O que é**: Storage grátis para assets (500MB)

### **PASSO 1: Criar Conta**
```
1. Ir para: supabase.com

2. Clicar "Start your project"

3. "Sign up with GitHub" (recomendado)
   OU
   "Sign up with email"

4. Autorizar/Confirmar
```

---

### **PASSO 2: Criar Projeto**
```
1. Dashboard → "New project"

2. Preencher:
   - Organization: "New organization" → "Incubadora"
   - Project name: "incubadora-assets"
   - Database password: (criar senha forte, SALVAR!)
   - Region: "South America (São Paulo)" ← mais perto!
   - Plan: "Free" ✅

3. Clicar "Create new project"

4. Aguardar 2-3 minutos (setup automático)
```

---

### **PASSO 3: Criar Bucket (Storage)**
```
1. Menu esquerdo → "Storage"

2. Clicar "Create a new bucket"

3. Config:
   - Name: "assets"
   - ⚠️ IMPORTANTE: Marcar "Public bucket" ✅
   - File size limit: 50MB
   
4. Clicar "Create bucket"
```

---

### **PASSO 4: Upload Assets**
```
1. Clicar no bucket "assets"

2. Clicar "Upload file"

3. Selecionar arquivos:
   - background.mp4 (baixar de pexels.com)
   - avatar_male.png (criar ou baixar)
   - avatar_female.png

4. Aguardar upload

5. Para CADA arquivo:
   - Hover sobre nome
   - Clicar "..."  
   - "Get URL"
   - COPIAR URL
   - Salvar em assets_urls.txt

Exemplo URL:
https://abc123.supabase.co/storage/v1/object/public/assets/background.mp4
```

---

## 📋 TUTORIAL 5: GOOGLE CLOUD TTS (20 minutos)

### **🎯 O que é**: 1 milhão caracteres/mês GRÁTIS

### **PASSO 1: Criar Conta Google Cloud**
```
1. Ir para: console.cloud.google.com

2. Login com Gmail

3. Se PRIMEIRA VEZ:
   - Aceitar termos
   - País: Brasil
   - ✅ Ativar teste gratuito (U$ 300)
   
   Se JÁ TEM CONTA:
   - Pular para Passo 2
```

---

### **PASSO 2: Criar Projeto**
```
1. No topo, clicar dropdown de projetos

2. "New Project"

3. Config:
   - Project name: "Incubadora"
   - Location: "No organization"

4. "Create"

5. Aguardar criação (30 seg)

6. ✅ Selecionar projeto criado (dropdown topo)
```

---

### **PASSO 3: Ativar Text-to-Speech API**
```
1. Menu hamburguer (☰) → "APIs & Services" → "Library"

2. Buscar: "Text-to-Speech"

3. Clicar em "Cloud Text-to-Speech API"

4. Clicar "Enable"

5. Aguardar ativação (1 min)
```

---

### **PASSO 4: Criar Service Account (Chave)**
```
1. Menu (☰) → "APIs & Services" → "Credentials"

2. Clicar "+ Create Credentials" → "Service account"

3. Preencher:
   - Service account name: "incubadora-tts"
   - Description: "TTS para vídeos"
   
4. "Create and Continue"

5. Role: "Basic" → "Owner" (ou "Editor")

6. "Continue" → "Done"
```

---

### **PASSO 5: Baixar JSON Key**
```
1. Na lista de Service Accounts, achar "incubadora-tts@..."

2. Clicar nos 3 pontinhos (⋮)

3. "Manage keys"

4. "Add Key" → "Create new key"

5. Tipo: "JSON" ✅

6. "Create"

7. ✅ Arquivo .json baixa automaticamente

8. RENOMEAR para: google-tts-key.json

9. Mover para pasta segura
```

---

### **PASSO 6: Testar TTS**
```python
from google.cloud import texttospeech
import os

# Apontar para arquivo JSON
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'caminho/para/google-tts-key.json'

client = texttospeech.TextToSpeechClient()

# Configurar
synthesis_input = texttospeech.SynthesisInput(text="Olá, teste de voz")
voice = texttospeech.VoiceSelectionParams(
    language_code="pt-BR",
    name="pt-BR-Wavenet-A"  # Voz feminina
)
audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.MP3
)

# Gerar
response = client.synthesize_speech(
    input=synthesis_input,
    voice=voice,
    audio_config=audio_config
)

# Salvar
with open("teste.mp3", "wb") as out:
    out.write(response.audio_content)
    
print("✅ Áudio criado: teste.mp3")
```

---

## 📋 TUTORIAL 6: YOUTUBE DATA API (15 minutos)

### **🎯 O que é**: Pesquisar canais, GRÁTIS 10K units/dia

### **PASSO 1: Ativar API** (Mesmo projeto Google Cloud)
```
1. console.cloud.google.com

2. Selecionar projeto "Incubadora"

3. Menu (☰) → "APIs & Services" → "Library"

4. Buscar: "YouTube Data API v3"

5. Clicar nela

6. "Enable"
```

---

### **PASSO 2: Criar API Key**
```
1. Menu (☰) → "APIs & Services" → "Credentials"

2. "+ Create Credentials" → "API key"

3. ✅ Key criada automaticamente!
   Exemplo: AIzaSyXXXXXXXXXXXXXX

4. COPIAR key

5. (Opcional) Clicar "Edit API key":
   - Name: "YouTube Search"
   - Restrict key → "YouTube Data API v3"
   - Save

6. Salvar em chaves.txt
```

---

### **PASSO 3: Testar**
```python
from googleapiclient.discovery import build

YOUTUBE_KEY = "AIzaSyxxxxxxx"

youtube = build('youtube', 'v3', developerKey=YOUTUBE_KEY)

# Buscar vídeos
request = youtube.search().list(
    part="snippet",
    q="mistérios perturbadores",
    maxResults=5,
    type="video"
)

response = request.execute()

for item in response['items']:
    print(f"📹 {item['snippet']['title']}")
    print(f"   Canal: {item['snippet']['channelTitle']}")
    print()
```

---

## 📋 TUTORIAL 7: AWS EC2 (30 minutos)

### **🎯 O que é**: Servidor cloud com free tier (12 meses)

### **PASSO 1: Criar Conta AWS**
```
1. Ir para: aws.amazon.com

2. "Create an AWS Account"

3. Preencher:
   - Email
   - Nome conta: "Incubadora"
   - Senha

4. "Continue"

5. Tipo de conta: "Personal"

6. Preencher dados pessoais

7. ⚠️ CARTÃO DE CRÉDITO:
   - Necessário (mas não cobra se ficar no free tier)
   - Confirmar identidade

8. Plano: "Basic support - Free" ✅

9. "Complete sign up"
```

---

### **PASSO 2: Acessar Console EC2**
```
1. Login: console.aws.amazon.com

2. Região (canto superior direito):
   - Trocar para: "US East (N. Virginia)" us-east-1
   - ← MAS barato!

3. Buscar: "EC2" na barra de busca

4. Clicar em "EC2"
```

---

### **PASSO 3: Launch Instance**
```
1. Botão laranja "Launch instance"

2. Config:
   
   Name: incubadora-video
   
   OS:
   - Quick Start: Ubuntu
   - AMI: Ubuntu Server 22.04 LTS (Free tier eligible) ✅
   
   Instance type:
   - t2.micro (Free tier eligible) ✅ ← IMPORTANTE!
   - 1 vCPU, 1 GB RAM
   
   Key pair:
   - "Create new key pair"
   - Name: incubadora-key
   - Type: RSA
   - Format: .pem (Mac/Linux) ou .ppk (Windows)
   - "Create key pair"
   - ⚠️ SALVAR ARQUIVO .pem/ppk!
   
   Network settings:
   - ✅ Allow SSH (port 22)
   - ✅ Allow HTTP (port 80)
   - ✅ Custom TCP port 8000 (para API)
   
   Storage:
   - 8 GB (Free tier: até 30GB) ✅

3. "Launch instance"

4. Aguardar "Instance state: Running" (2 min)
```

---

### **PASSO 4: Conectar Instance**
```
1. Lista de instances → Selecionar sua instance

2. Botão "Connect"

3. Aba "EC2 Instance Connect"

4. "Connect" ← Abre terminal no browser!

✅ TERMINAL ABERTO = Sucesso!
```

---

### **PASSO 5: Instalar Docker + Servidor** (Copiar/Colar)
```bash
# COPIAR TODOS ESTES COMANDOS DE UMA VEZ:

# 1. Atualizar sistema
sudo apt update

# 2. Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu

# 3. Recarregar permissões
newgrp docker

# 4. Verificar
docker --version

# ✅ Deve mostrar: Docker version 24.x.x
```

---

### **PASSO 6: Rodar Servidor de Vídeo**
```bash
# Pull imagem
docker pull gyoridavid/narrated-story-creator:latest

# Rodar (não fechar terminal!)
docker run -d \
  --name video-server \
  --restart unless-stopped \
  -p 8000:8000 \
  gyoridavid/narrated-story-creator:latest

# Verificar se rodando
docker ps

# ✅ Deve mostrar container "video-server" UP
```

---

### **PASSO 7: Pegar IP Público**
```
1. Voltar para console AWS EC2

2. Selecionar instance

3. Copiar "Public IPv4 address"
   Exemplo: 54.123.45.67

4. Testar no navegador:
   http://54.123.45.67:8000/health

5. ✅ Deve mostrar: {"status":"ok"}
```

---

## 💰 RESUMO DE CUSTOS (6 Meses)

### **Ferramentas Sempre Grátis**:
```
✅ Groq: R$ 0 (14.4K/dia perpétuo)
✅ Pollinations: R$ 0 (ilimitado)
✅ Supabase: R$ 0 (500MB)
✅ YouTube API: R$ 0 (10K units/dia)
```

### **Google Cloud** (Se usar TTS):
```
Mês 1-3: R$ 0 (U$ 300 créditos)
Mês 4-6: R$ 0 (1M caracteres grátis/mês)
Total: R$ 0
```

### **AWS EC2** (t2.micro free tier):
```
Mês 1-12: R$ 0 (750 horas grátis/mês)
  → t2.micro 24/7 = 720h/mês ✅
Total: R$ 0 nos primeiros 12 meses!
```

### **TOTAL 6 MESES: R$ 0,00** 🎉

---

## ⚡ OTIMIZAÇÕES DE CUSTO

### **1. Usar t2.micro (NÃO t2.medium)**
```
t2.micro: GRÁTIS (free tier)
t2.medium: ~U$ 35/mês

Economia: 100% nos primeiros 12 meses
```

### **2. Stop Instance Quando Não Usar**
```
# No console AWS
Actions → Instance State → Stop

Quando precisar:
Actions → Instance State → Start

Economia: Paga só horas usadas
```

### **3. Pollinations > Google Imagen**
```
Pollinations: R$ 0
Google Imagen: Gasta créditos

Usar Imagen SÓ se qualidade Pollinations não servir
```

---

## 📋 CHECKLIST FINAL

Marque o que JÁ configurou:

**APIs Grátis**:
- [ ] Groq API key
- [ ] Grok API key (opcional)
- [ ] Pollinations (sem config!)
- [ ] Supabase bucket + URLs
- [ ] Google TTS + JSON key
- [ ] YouTube API key

**Cloud**:
- [ ] AWS EC2 instance (t2.micro)
- [ ] Docker instalado
- [ ] Servidor vídeo rodando
- [ ] IP público testado

**Arquivo de Chaves** (chaves.txt):
```
GROQ_API_KEY=gsk_xxxxx
GROK_API_KEY=xai_xxxxx
YOUTUBE_API_KEY=AIza_xxxxx
GOOGLE_CREDENTIALS=/caminho/google-tts-key.json
AWS_IP=54.123.45.67

SUPABASE_BACKGROUND=https://...supabase.../background.mp4
SUPABASE_AVATAR_MALE=https://...supabase.../male.png
SUPABASE_AVATAR_FEMALE=https://...supabase.../female.png
```

---

## 🚀 PRÓXIMO PASSO

**Quando terminar checklist acima, me confirme**:
- ✅ "Groq funcionando"
- ✅ "Supabase com 3 assets"
- ✅ "AWS EC2 respondendo na porta 8000"
- ✅ "Arquivo chaves.txt criado"

**Daí EU CODIFICO** toda integração! 🎯

---

**Tempo total setup**: 2-3 horas  
**Custo**: R$ 0,00  
**Próximo**: Integração Python completa!
