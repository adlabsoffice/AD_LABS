# 18 - Vídeos Longos Virais com IA por $0 (Tutorial n8n)

**Fonte:** Transcrição YouTube  
**Tema:** Sistema completo para gerar vídeos longos automatizados sem APIs pagas usando n8n + Docker + AWS free tier

---

## 🎯 Visão Geral

Sistema 100% gratuito que constrói vídeos automaticamente:
- ✅ Script writing
- ✅ Voice narration  
- ✅ Speaker image overlay
- ✅ Captions
- ✅ Upload YouTube
- ✅ **Sem limites, sem fees, sem subscriptions**

**Nicho demonstrado:** Revenge stories (monetiza em ~1 mês)

---

## 🚀 Duas Opções de Deploy

### **Opção 1: AWS EC2 (RECOMENDADO - mostrado no vídeo)**
- ✅ $200-300 créditos grátis (Google/AWS)
- ✅ 6 meses gratuitos
- ✅ Funciona 24/7
- ✅ Sem necessidade de GPU local

### **Opção 2: Local (Docker)**
- Windows, Mac, Linux
- Usar GPU NVIDIA (CUDA) para aceleração
- Rodando só quando PC ligado

---

## 🛠️ Stack Tecnológica

| Componente | Ferramenta | Função |
|------------|------------|--------|
| Automation | **n8n** | Workflow automation |
| Video Server | **narrated-story-creator** (Docker) | Gera vídeos |
| Storage | **Supabase** | Hospeda assets (vídeos/imagens) |
| Hosting | **AWS EC2 / Local Docker** | Roda servidor |
| Upload | **YouTube API** (via n8n) | Auto-upload |

---

## 📋 Setup Completo (AWS EC2)

### **PASSO 1: Criar Conta AWS**

1. Acessar AWS
2. Criar conta (recebe $200 créditos × 6 meses)
3. Escolher "Free Plan"
4. Preencher dados (não cobra cartão)

---

### **PASSO 2: Criar Instância EC2**

**1. Acessar EC2:**
- Compute → EC2 → Launch Instance

**2. Configurações:**
```
Name: youtube-tutorial
OS: Ubuntu 22.04 LTS HVM SSD
Instance type: t2.medium (4 GB RAM)
Key pair: Criar nova (youtube.pem) - SALVAR!
Storage: 20-30 GB
Security group: 
  - Inbound rules: Custom TCP port 8000, 0.0.0.0/0
```

**3. Launch Instance**

---

### **PASSO 3: Conectar via SSH**

1. Clicar "Connect"
2. Terminal abre no browser
3. Confirmar instance running

---

### **PASSO 4: Instalar Docker**

**Comandos (copiar/colar):**

```bash
# 1. Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh && sudo sh get-docker.sh && sudo usermod -aG docker ubuntu && newgrp docker

# 2. Verify
docker --version

# 3. Pull image
docker pull gyoridavid/narrated-story-creator:latest

# 4. Run container
docker run -d --name narrated-story-creator --restart unless-stopped -p 8000:8000 gyoridavid/narrated-story-creator:latest

# 5. Check status
docker ps

# 6. Test API
curl http://localhost:8000/health
```

**Status esperado:** `ok`

---

### **PASSO 5: Obter IP Público**

```bash
# Get public IP
curl http://169.254.169.254/latest/meta-data/public-ipv4
```

**Testar no browser:**
```
http://SEU_IP:8000/health
```

**Deve retornar:** `{"status": "ok"}`

---

## 🎨 Setup Assets (Supabase)

### **PASSO 1: Criar Conta**
- Acessar `supabase.com`
- Criar projeto gratuito

### **PASSO 2: Storage Bucket**

1. Storage → New Bucket
2. Nome: `youtube-assets`
3. ✅ **Public** (importante!)
4. Create

### **PASSO 3: Upload Assets**

**Arquivos necessários:**
1. **Background video** (1080p fullHD)
   - Source: Pexels.com → Videos → Baixar 1080p
   
2. **Speaker images** (sem fundo!)
   - Male avatar PNG (transparent background)
   - Female avatar PNG (transparent background)
   - Tool para remover bg: `remove.bg`

**Upload:**
- Drag & drop no bucket
- 3 arquivos: 1 vídeo MP4 + 2 imagens PNG

### **PASSO 4: Copiar URLs**

Para cada arquivo:
1. Clicar arquivo → "Get URL"
2. Copiar URL público
3. Salvar para usar no n8n

---

## ⚙️ Setup n8n Workflow

### **Workflow Components:**

**Structure:**
```
Form Trigger → Write Story → Clean Text → Create Title → 
Generate Video (API) → Wait Loop → Check Status → 
Download Video → Upload YouTube
```

### **Node "Set Me Up First" (Configurações):**

**Valores a configurar:**
```json
{
  "background_video_url": "https://supabase.../video.mp4",
  "person_male_image_url": "https://supabase.../male.png",
  "person_female_image_url": "https://supabase.../female.png",
  "server_url": "http://SEU_IP_PUBLICO:8000",
  "language_code": "en-US",
  "voice": "af_heart"  // ou am_eric (male)
}
```

---

### **Verificar Vozes Disponíveis:**

**URL:**
```
http://SEU_IP:8000/api/languages
```

**Retorna:** Lista de idiomas + vozes

**Formato voice code:**
- `af_*` = Female
- `am_*` = Male
- Exemplos: `af_heart`, `am_eric`, `af_sarah`

---

### **Node: Form Trigger**

**Campos:**
- Story idea (texto curto)
- Character name

**Exemplo:**
```
Idea: "Wife cheating on husband with his brother"
Character: Tyler
```

---

### **Node: Write Story (OpenAI)**

**Prompt:**
```
System: You're an expert creative writer. You write revenge stories for a living.

User: Write a revenge story based on:
Character name: {{$json.character_name}}
Story idea: {{$json.story_idea}}
```

**Output:** Story completa (~5-6 minutos narração)

---

### **Node: Create Title (OpenAI)**

**Prompt:**
```
Based on this story: {{$json.story}}

Create a YouTube title under 100 characters that is:
- Clickbait but not misleading
- Emotional hooks
- Curiosity-driven
```

---

### **Node: HTTP Request (Generate Video)**

**Method:** POST  
**URL:** `{{$node["Set Me Up First"].json.server_url}}/api/videos`

**Body:**
```json
{
  "text": "{{$json.story}}",
  "person_image_url": "{{$node["Set Me Up First"].json.person_female_image_url}}",
  "person_name": "{{$json.character_name}}",
  "background_url": "{{$node["Set Me Up First"].json.background_video_url}}",
  "voice": "{{$node["Set Me Up First"].json.voice}}"
}
```

**Response:** `{ "video_id": "xyz123", "status": "processing" }`

---

### **Node: Wait + Loop (Check Status)**

**Loop structure:**
```
Wait 10s → Check status → If processing: loop, If complete: continue
```

**Check status API:**
```
GET http://SERVER:8000/api/videos/{video_id}
```

---

### **Node: Download Video**

**URL from API:**
```
http://SERVER:8000/api/videos/{video_id}/download
```

---

### **Node: Upload YouTube**

**YouTube API integration:**
- OAuth credentials
- Title: {{$json.title}}
- Description: Auto-generated
- Tags: revenge stories, etc.

---

## 🎬 Exemplo de Vídeo Resultado

**Características:**
- ✅ 5-6 minutos duração
- ✅ Voz narrada (TTS realistic)
- ✅ Speaker image overlay
- ✅ Background video
- ✅ Captions automáticas
- ✅ Layout formatado

**⚠️ Nota visual:** Se imagem PNG tem espaço transparente nas laterais, avatar fica deslocado - crop PNG para fix.

---

## 🤖 Workflow Avançado (Automação Completa)

**Versão 2 (mencionada no vídeo):**

```
Reddit Scraper → Database (stories) → 
Check DB (status = queued?) → Create Character → 
Write Story → Title → Voice Selection → 
Generate Video → Update DB (status = created) → 
Upload YouTube → Update DB (status = uploaded)
```

**Benefícios:**
- ✅ Scrape stories do Reddit automaticamente
- ✅ Queue system
- ✅ Track status
- ✅ 100% autopilot

**Trigger:** Telegram message (ex: "hi") = executa

---

## 📊 Performance e Custos

### **Tempo de Geração:**
- Simple story: **4-5 minutos**
- Complex story: ~6-8 minutos

### **Custos AWS Free Tier:**
- $200-300 créditos
- **6 meses** grátis
- t2.medium: suficiente

### **Após free tier acabar:**
- t2.medium: ~$30-40/mês
- Alternative: Migrar para local Docker

---

## 💻 Setup Local (Alternative)

### **Windows:**

```powershell
# Install Docker Desktop (Windows Store)
# Install WSL2
# Start Docker Desktop

# Run servidor
docker run -it --rm --name narrated-story-creator -p 8000:8000 gyoridavid/narrated-story-creator:latest

# Test
http://localhost:8000/health

# n8n connection
http://host.docker.internal:8000
```

### **Mac / Linux:**

```bash
# Run servidor
docker run -it --rm --name narrated-story-creator -p 8000:8000 gyoridavid/narrated-story-creator:latest

# Test
http://localhost:8000/health

# n8n connection
http://host.docker.internal:8000
```

### **NVIDIA GPU (CUDA):**

```bash
# GPU-accelerated version
docker run --rm --gpus=all -e NVIDIA_VISIBLE_DEVICES=all -e NVIDIA_DRIVER_CAPABILITIES=all -p 8000:8000 -it gyoridavid/narrated-story-creator:latest-cuda
```

**Benefício:** Geração **muito mais rápida**

---

## 🔧 Comandos de Manutenção

```bash
# Restart container
docker restart narrated-story-creator

# Stop
docker stop narrated-story-creator

# Start
docker start narrated-story-creator

# Remove (redeploy)
docker stop narrated-story-creator && docker rm narrated-story-creator

# Resource usage
docker stats narrated-story-creator

# System resources
free -h && df -h

# Live logs
docker logs -f narrated-story-creator
```

---

## 📈 Estratégia de Monetização

**Case study (clientes do autor):**
- ✅ Cliente 1: **Monetizado em 1 mês** (4 vídeos/dia)
- ⏳ Cliente 2: Ainda postando (crescimento gradual)

**Fórmula:**
```
4 vídeos/dia × 30 dias = 120 vídeos/mês
→ Potencial monetização rápida
```

**Depende de:**
- Qualidade das histórias
- Consistência de upload
- Engagement (titles + thumbnails)

---

## ✅ Checklist Completo

### **Setup Inicial (1-2 horas):**
- [ ] Criar conta AWS / preparar Docker local
- [ ] Lançar EC2 instance (ou rodar Docker local)
- [ ] Instalar Docker + pull image
- [ ] Testar servidor (curl health)
- [ ] Criar conta Supabase
- [ ] Upload assets (video + images)
- [ ] Copiar URLs públicas

### **n8n Configuration:**
- [ ] Importar workflow template (links no vídeo)
- [ ] Configurar "Set Me Up First" node
- [ ] Testar geração manual
- [ ] Configurar YouTube OAuth
- [ ] Testar upload automático

### **Production:**
- [ ] Gerar 3-5 vídeos teste
- [ ] Review quality
- [ ] Adjust voice/images if needed
- [ ] Schedule uploads (4/dia recomendado)
- [ ] Monitor performance

---

## 🎓 Lições-Chave

1. **Free tier = Suficiente** - AWS $200 dura 6+ meses
2. **Docker = Portabilidade** - AWS ou local, mesma setup
3. **Supabase = Storage grátis** - Public URLs para assets
4. **n8n = Orchestration** - Visual workflow > código
5. **Revenge sto ries = Monetiza rápido** - Niche engajante

---

## 🚨 Troubleshooting

**Problema:** Container não inicia  
**Fix:** Check logs `docker logs narrated-story-creator`

**Problema:** API retorna erro  
**Fix:** Verify JSON body format no HTTP node

**Problema:** Video stuck "processing"  
**Fix:** Check server resources (`free -h`)

**Problema:** Image positioning ruim  
**Fix:** Crop PNG transparente corretamente

---

## 🔗 Links e Downloads

**Templates:**
- Basic workflow: (Google Drive link no vídeo)
- Complex workflow: (Google Drive link no vídeo)
- Command cheat sheet: (fornecido acima)

**Tools:**
- Docker: `docker.com`
- n8n: `n8n.io`
- Supabase: `supabase.com`
- Pexels: `pexels.com` (free videos)
- Remove.bg: `remove.bg` (background remover)

---

**Conclusão:** Sistema completo de $0 para gerar vídeos longos automatizados. Docker + n8n + AWS free tier = Factory de conteúdo sem custos mensais. Revenge stories nicho de exemplo, mas aplicável a qualquer formato narrativo.
