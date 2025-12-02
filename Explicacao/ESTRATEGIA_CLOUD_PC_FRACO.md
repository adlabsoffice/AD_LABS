# 🌩️ ESTRATÉGIA CLOUD-FIRST (PC Fraco)
## Como Rodar Incubadora 100% na Cloud Sem Gastar Muito

---

## 🚨 PROBLEMA IDENTIFICADO

**PC não aguenta**:
- ❌ New TTS Local (precisa 8GB RAM + tempo)
- ❌ Edição de vídeo local
- ❌ Stable Diffusion local
- ❌ Docker local (pesado)

**SOLUÇÃO**: Migrar TUDO para cloud usando créditos disponíveis!

---

## 💰 ORÇAMENTO DISPONÍVEL

✅ **AWS**: U$ 100 disponíveis AGORA + créditos startup (aguardando)  
✅ **Google Cloud**: Créditos (quantidade a confirmar)  
✅ **Grok**: U$ 25/mês grátis  
✅ **Groq**: 14.4K requests/dia grátis  

---

## 🏗️ ARQUITETURA CLOUD (Baseada no Arquivo 18)

### **Sistema "narrated-story-creator" via AWS**

**Descoberta do arquivo 18**:
- ✅ Sistema COMPLETO de geração de vídeos
- ✅ Roda em Docker na cloud
- ✅ AWS free tier: U$ 200-300 créditos × 6 meses
- ✅ Gera vídeos de 5-6min **automaticamente**
- ✅ Narração + legendas + overlays + background

**Você já tem U$ 100 AWS = pode começar AGORA!**

---

## 🚀 SETUP AWS EC2 (PASSO A PASSO)

### **ETAPA 1: Criar Instância EC2** (15min)

1. **Login AWS Console**:
   - `console.aws.amazon.com`
   - Região: us-east-1 (mais barato)

2. **Launch Instance**:
   ```
   Name: incubadora-video-server
   OS: Ubuntu 22.04 LTS
   Instance type: t2.medium (4GB RAM)
   Key pair: Criar nova → Salvar .pem
   Storage: 30 GB
   Security group: 
     - Port 8000 (Custom TCP, 0.0.0.0/0)
     - Port 22 (SSH, 0.0.0.0/0)
   ```

3. **Launch** → Aguardar "Running"

---

### **ETAPA 2: Conectar via SSH** (5min)

**Opção A: Browser (Fácil)**:
- No console AWS, clicar "Connect"
- Usar EC2 Instance Connect
- Terminal abre no browser

**Opção B: Terminal Local**:
```bash
# Windows PowerShell
ssh -i caminho/para/sua-chave.pem ubuntu@IP_PUBLICO
```

---

### **ETAPA 3: Instalar Docker + Servidor de Vídeo** (10min)

**Copiar/colar estes comandos**:

```bash
# 1. Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu
newgrp docker

# 2. Verificar
docker --version

# 3. Pull imagem do servidor de vídeo
docker pull gyoridavid/narrated-story-creator:latest

# 4. Rodar container
docker run -d \
  --name video-server \
  --restart unless-stopped \
  -p 8000:8000 \
  gyoridavid/narrated-story-creator:latest

# 5. Verificar status
docker ps

# 6. Testar API
curl http://localhost:8000/health
# Deve retornar: {"status": "ok"}
```

---

### **ETAPA 4: Pegar IP Público** (2min)

```bash
# No terminal SSH
curl http://169.254.169.254/latest/meta-data/public-ipv4
```

**Salvar esse IP!** Ex: `54.123.45.67`

**Testar no browser**:
```
http://SEU_IP:8000/health
```

Deve mostrar: `{"status": "ok"}`

---

## 🎬 COMO USAR O SERVIDOR (API Calls)

### **API 1: Gerar Vídeo**

```python
import requests

# Seu IP público AWS
SERVER = "http://54.123.45.67:8000"

# Parâmetros
payload = {
    "text": "Era uma vez um garoto que foi humilhado na escola...",
    "person_name": "Tyler",
    "person_image_url": "https://supabase.../avatar.png",
    "background_url": "https://supabase.../background.mp4",
    "voice": "af_heart",  # Female voice
    "language_code": "en-US"
}

# Criar vídeo
response = requests.post(f"{SERVER}/api/videos", json=payload)
video_id = response.json()["video_id"]
print(f"Vídeo criando... ID: {video_id}")
```

### **API 2: Checar Status**

```python
import time

while True:
    status = requests.get(f"{SERVER}/api/videos/{video_id}")
    
    if status.json()["status"] == "complete":
        print("✅ Vídeo pronto!")
        break
    
    print("⏳ Processando...")
    time.sleep(10)
```

### **API 3: Download Vídeo**

```python
video_url = f"{SERVER}/api/videos/{video_id}/download"
video_file = requests.get(video_url)

with open("video_final.mp4", "wb") as f:
    f.write(video_file.content)

print("📥 Vídeo baixado!")
```

---

## 📊 STACK REVISADO (Cloud-First)

### **Geração de Texto**:
```
PRIMARY: Groq (14.4K/dia grátis)
  → Roteiros
  → Títulos
  → Ideias
  
BACKUP: Grok (U$ 25/mês)
  → Se Groq exceder quota
```

### **Geração de Imagens**:
```
MVP: Pollinations.AI (grátis, ilimitado)
  → Avatares
  → Backgrounds
  
FUTURO: Google Imagen (créditos)
  → Qualidade premium
```

### **Geração de Vídeos** (MUDANÇA CHAVE):
```
✅ AWS EC2 (t2.medium, U$ 100 créditos)
  → Docker: narrated-story-creator
  → TTS integrado
  → Legendas automáticas
  → Overlays
  → Background video
  
CUSTO: ~U$ 30-40/mês (depois dos créditos)
  → MAS: 6 meses grátis com créditos
```

### **Storage**:
```
Supabase (grátis, 500MB)
  → Avatares PNG
  → Background videos
  → Assets fixos
```

### **YouTube**:
```
YouTube Data API v3 (grátis)
  → Pesquisa
  → Análise
  
Upload: Manual MVP → n8n depois
```

---

## 💰 CUSTO REAL (Com AWS)

### **Primeiros 6 Meses** (Créditos):
```
AWS EC2: U$ 0 (créditos cobrem)
Groq: U$ 0 (grátis perpétuo)
Pollinations: U$ 0 (grátis perpétuo)
Supabase: U$ 0 (tier grátis)

TOTAL: U$ 0/mês × 6 meses
```

### **Depois dos Créditos**:
```
AWS t2.medium: ~U$ 35/mês (24/7)
Groq: U$ 0
Pollinations: U$ 0
Supabase: U$ 0 (até 500MB)

TOTAL: ~U$ 35/mês
```

### **Otimização** (Liga/Desliga):
```
AWS apenas quando produzindo: ~U$ 10-15/mês
  → Stop instance quando não usar
  → Paga só horas usadas
```

---

## 🎯 WORKFLOW COMPLETO (Seu PC → AWS → YouTube)

### **No SEU PC** (Leve):
```python
# 1. Gerar roteiro (Groq API)
roteiro = groq.generate("Escreva história de revanche...")

# 2. Enviar para AWS criar vídeo
response = requests.post(
    "http://SEU_IP_AWS:8000/api/videos",
    json={
        "text": roteiro,
        "person_name": "Tyler",
        ...
    }
)

# 3. Aguardar (AWS faz vídeo)
# Seu PC pode fazer outras coisas!

# 4. Download vídeo pronto
video = download_from_aws(video_id)

# 5. Upload YouTube (manual ou API)
```

**Seu PC só faz**: Chamadas API leves!  
**AWS faz**: Processamento pesado (TTS, edição, render)

---

## 📋 ASSETS NECESSÁRIOS (Cloud Storage)

### **Supabase Setup** (10min):

1. **Criar conta**: `supabase.com`
2. **Novo projeto**: "incubadora-assets"
3. **Storage → New Bucket**: "assets" (PUBLIC)
4. **Upload**:
   - `background.mp4` (1080p, Pexels)
   - `avatar_male.png` (sem fundo, Remove.bg)
   - `avatar_female.png` (sem fundo)

5. **Copiar URLs**:
   - Cada arquivo → "Get URL"
   - Ex: `https://xyz.supabase.co/storage/v1/object/public/assets/background.mp4`

---

## 🚀 ROADMAP ATUALIZADO (3 Dias Cloud)

### **DIA 1 - Setup Cloud** (4h):
- [ ] Criar EC2 instance AWS
- [ ] Instalar Docker + video-server
- [ ] Pegar IP público
- [ ] Criar Supabase + upload assets
- [ ] Testar 1 vídeo end-to-end

**Output**: Servidor funcionando, 1 vídeo teste gerado

---

### **DIA 2 - Automação** (6h):
- [ ] Script Python: Groq → AWS → Download
- [ ] Agente Pesquisador (YouTube API)
- [ ] Agente Analista (clustering)
- [ ] Agente Eixos (gerar 5 eixos)
- [ ] Agente Ideias (150 ideias)

**Output**: Pipeline T=0 → T=4 funcionando

---

### **DIA 3 - Produção** (6h):
- [ ] Agente Produtor (5 vídeos)
  - Usar API AWS para cada
- [ ] Organizar vídeos finais
- [ ] Subir 1 vídeo no YouTube (teste)
- [ ] Documentar processo

**Output**: 5 vídeos prontos, sistema documentado

---

## ⚡ OTIMIZAÇÕES (Economizar AWS)

### **1. Stop/Start Instance**:
```bash
# No console AWS
# Stop instance quando não estiver produzindo
# Start quando for produzir lote de vídeos

# Economia: 70%+ nos custos
```

### **2. Usar Spot Instances** (Avançado):
- 90% mais barato que On-Demand
- Pode ser interrompido (mas raro)
- Ideal para produção em massa

### **3. Produção em Batch**:
```python
# Ao invés de 1 vídeo por vez:
# Gerar 10 roteiros
# Enviar todos para AWS
# Deixar processando batch
# Desligar instance

# Economia: Paga só pelas horas de batch
```

---

## 🆚 COMPARAÇÃO: Local vs Cloud

| Aspecto | Local (PC Fraco) | Cloud (AWS) |
|---------|------------------|-------------|
| **Viável?** | ❌ PC não aguenta | ✅ Sim |
| **Custo 6 meses** | N/A | U$ 0 (créditos) |
| **Custo depois** | N/A | U$ 10-35/mês |
| **Velocidade** | ❌ Travaria | ✅ Rápido (4GB RAM) |
| **Disponibilidade** | PC ligado | ✅ 24/7 |
| **Escalabilidade** | ❌ Limitado | ✅ Infinita |

**VEREDITO**: Cloud é a ÚNICA opção viável

---

## ✅ PRÓXIMOS PASSOS IMEDIATOS

### **VOCÊ FAZ AGORA** (30min):

1. **Login AWS**:
   - `console.aws.amazon.com`
   - Escolher região: us-east-1
   - Confirmar U$ 100 disponíveis

2. **Criar EC2 Instance** (seguir tutorial acima)

3. **Me confirmar**:
   - IP público do servidor
   - Status: `http://IP:8000/health` funcionando

### **EU FAÇO DEPOIS** (Quando você confirmar):

- Criar scripts Python para integração
- Implementar agentes 1-6
- Testar pipeline completo
- Documentar uso

---

## 🔥 VANTAGEM INESPERADA

**PC fraco forçou solução MELHOR**:
- ✅ Escalável (10, 100, 1000 canais)
- ✅ 24/7 disponível
- ✅ Não trava seu PC
- ✅ Profissionalmente hostado
- ✅ Fácil de replicar (Docker)

**Se PC fosse forte, você teria limitações. Agora tem sistema enterprise!** 🚀

---

**Status**: 🟡 AGUARDANDO VOCÊ CRIAR EC2  
**Tempo**: 30min para setup AWS  
**Depois**: EU codifico integração completa!
