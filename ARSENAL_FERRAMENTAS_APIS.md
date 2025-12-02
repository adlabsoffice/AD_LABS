# 🔧 ARSENAL DE FERRAMENTAS - INCUBADORA AD_LABS
## APIs, Ferramentas Grátis e Integrações Disponíveis

> **Objetivo**: Documentar TODAS as ferramentas/APIs que temos acesso para usar na incubadora  
> **Prioridade**: Ferramentas GRÁTIS ou com créditos disponíveis  
> **Status**: Aguardando confirmação do usuário sobre o que realmente está disponível

---

## 🎯 CONFIRMAÇÕES NECESSÁRIAS

**Antes de começar desenvolvimento, confirmar**:
- [ ] Google Cloud APIs - quais exatamente?
- [ ] Créditos Google Cloud - quanto disponível?
- [ ] Grok API - acesso confirmado?
- [ ] AWS startup credits - confirmado?
- [ ] n8n - já configurado?
- [ ] Outras ferramentas?

---

## 🤖 APIs DE IA (Geração de Texto)

### **1. Groq (CONFIRMADO - Via Arquivo 15)**
- **Custo**: 100% GRÁTIS
- **Limites**:
  - Llama 3.1: **14.400 requests/dia** 🔥
  - DeepSeek: 1.000 requests/dia
  - GPT-4o: 1.000 requests/dia
  - Qwen 3: 1.000 requests/dia (60 RPM!)
  
**Use cases na incubadora**:
- ✅ Geração de roteiros
- ✅ Títulos virais
- ✅ Descrições
- ✅ Análise de clusters

**Setup**:
```python
import groq

groq_client = groq.Groq(api_key=os.getenv("GROQ_API_KEY"))

response = groq_client.chat.completions.create(
    model="llama-3.1-70b-versatile",
    messages=[{"role": "user", "content": "Generate script..."}]
)
```

---

### **2. Grok (X.AI) - AGUARDANDO CONFIRMAÇÃO**
- **Custo**: ???
- **Acesso**: Usuário mencionou "usar grok"

**Precisa confirmar**:
- Tem API key?
- Pricing?
- Limites?

---

### **3. Gemini (Google) - AGUARDANDO CONFIRMAÇÃO**
- **Custo**: Gratuito (com limites)
- **Acesso**: Usuário tem créditos Google Cloud

**Precisa confirmar**:
- Qual tier? (gratuito vs créditos)
- Limites atuais?

---

## 🎨 GERAÇÃO DE IMAGENS

### **Opção 1: Google Imagen (via Vertex AI) - AGUARDANDO CONFIRMAÇÃO**
**Se tem créditos Google Cloud**:
- Imagen 2
- Imagen 3  
- Text-to-image
- Image editing

**Precisa pesquisar**:
- [ ] Preços Imagen via Vertex AI
- [ ] Como integrar Python
- [ ] Limites com créditos grátis

---

### **Opção 2: Stable Diffusion Local**
- **Custo**: R$ 0 (roda local)
- **Setup**: ComfyUI (usuário mencionou)

**Precisa confirmar**:
- [ ] AWS startup credits para rodar em cloud?
- [ ] Ou rodar local?

---

### **Opção 3: APIs Grátis Alternativas**
- Pollinations.ai (grátis, sem API key)
- Replicate (alguns modelos grátis)
- Segmind (tier gratuito)

---

## 🎙️ TTS (Text-to-Speech)

### **Opção 1: New TTS Local (CONFIRMADO - Arquivo 11)**
- **Custo**: R$ 0 (100% local)
- **Qualidade**: Comparável a ElevenLabs
- **Voice cloning**: 3 segundos de sample
- **Limites**: ZERO (roda local)

**Requisitos**:
- 8GB RAM mínimo
- GPU NVIDIA (opcional, mas 10x mais rápido)

**Vozes incluídas**:
- Dave, Joe (defaults)
- Jar vis, Morgan Freeman, Joe Rogan, etc.
- **Clone QUALQUER VOZ** (sample de 3s)

**Setup**:
```bash
# Download da versão Oracle Guy (GUI)
# Rodar run_new_tts.bat
# Browser abre automaticamente
```

---

### **Opção 2: Google Cloud TTS - AGUARDANDO CONFIRMAÇÃO**
**Se tem créditos Google Cloud**:
- Neural voices (alta qualidade)
- Múltiplos idiomas
- WaveNet voices

**Precisa pesquisar**:
- [ ] Preço por caractere
- [ ] Quanto dos créditos Google cobre?

---

### **Opção 3: Whisper API (Speech-to-Text) via Groq**
- **Custo**: GRÁTIS
- **Limite**: 2.000 requests/dia
- **Qualidade**: Excelente

**Não é TTS, mas útil para**:
- Transcrever referências
- Análise de vídeos competidores

---

## 🎬 EDIÇÃO DE VÍDEO

### **Opção 1: n8n + narrated-story-creator (CONFIRMADO - Arquivo 18)**
**Stack**:
- n8n (workflow automation)
- Docker container (narrated-story-creator)
- AWS EC2 free tier OU local

**Features**:
- ✅ Gera vídeos completos automatizados
- ✅ Narração + legendas + overlay
- ✅ Background video
- ✅ Speaker image overlay

**Custo**:
- AWS free tier: $200-300 créditos × 6 meses
- OU local Docker: R$ 0

**Precisa confirmar**:
- [ ] n8n já está rodando?
- [ ] AWS startup credits confirmados?

---

### **Opção 2: CapCut (Manual/Semi-automático)**
- **Custo**: Grátis (versão desktop)
- **Automação**: Template + instruções
- **Integração**: API não oficial existe

Ver arquivo 33: CapCut Pro Grátis PC

---

### **Opção 3: FFmpeg (Programático)**
- **Custo**: R$ 0 (open-source)
- **Automação**: 100% via Python
- **Use cases**:
  - Combinar áudio + imagens
  - Adicionar legendas (SRT)
  - Cortes/transições

---

## 🔧 AUTOMAÇÃO E WORKFLOW

### **n8n (MENCIONADO PELO USUÁRIO)**
- **Custo**: Self-hosted = grátis
- **Features**:
  - Visual workflow builder
  - 400+ integrações
  - YouTube upload automático
  - Webhooks, schedules

**Precisa confirmar**:
- [ ] Já está configurado?
- [ ] Onde está rodando? (local/cloud)

---

## ☁️ CLOUD E HOSTING

### **AWS (Startup Credits) - AGUARDANDO CONFIRMAÇÃO**
**Usuário mencionou**: "estamos para conseguir credito de startup na aws"

**Se aprovado**:
- EC2 para rodar n8n
- S3 para storage
- Lambda para funções
- ComfyUI para Stable Diffusion

**Precisa confirmar**:
- [ ] Créditos aprovados?
- [ ] Valor disponível?

---

### **Google Cloud (Créditos Existentes) - CONFIRMADO**
**Usuário disse**: "tudo feito via api do google que temos creditos"

**Precisa mapear**:
- [ ] Quais APIs Google estão disponíveis?
- [ ] Vertex AI (Imagen, PaLM, Gemini)?
- [ ] Cloud Storage?
- [ ] Text-to-Speech?
- [ ] Quanto de crédito resta?

---

## 📊 STORAGE DE ASSETS

### **Opção 1: Supabase (CONFIRMADO - Arquivo 18)**
- **Custo**: Gratuito (500MB + hosting)
- **Features**:
  - Public URLs
  - S3-compatible
  - Fácil integração

---

### **Opção 2: Google Cloud Storage**
**Se tem créditos**:
- Maior capacidade
- CDN global
- Integração nativa com outras APIs Google

---

## 📹 YOUTUBE API

### **YouTube Data API v3 (SEMPRE GRÁTIS)**
- **Custo**: R$ 0
- **Quota**: 10.000 unidades/dia (suficiente)
- **Features**:
  - Search (pesquisa de canais)
  - Videos list (metadados)
  - Channels (info de canais)
  - Analytics (métricas)

**Limitações**:
- ❌ Não faz upload (precisa OAuth)
- ✅ Ótimo para pesquisa/análise

---

### **YouTube Upload API (OAuth Required)**
- **Custo**: R$ 0
- **Setup**: OAuth 2.0 (workflow manual 1x)
- **Automação**: n8n tem integração nativa

---

## 🎨 FERRAMENTAS GRATUITAS EXTRAS

### **Baseado nos arquivos 11-42**:

1. **Groq** (Arquivo 15) - ✅ CONFIRMADO
2. **New TTS Local** (Arquivo 11) - ✅ CONFIRMADO
3. **n8n + Docker** (Arquivo 18) - ⚠️ AGUARDANDO SETUP
4. **CapCut Pro** (Arquivo 33) - ✅ DISPONÍVEL
5. **Pexels** - Vídeos/imagens stock grátis
6. **Remove.bg** - Remover background de imagens

---

## 🚨 DECISÕES NECESSÁRIAS ANTES DE CODIFICAR

### **DECISÃO 1: IA de Geração de Texto**
Opções:
- [ ] A. Groq (GRÁTIS, 14.4K/dia) ← RECOMENDO
- [ ] B. Gemini (Google Cloud credits)
- [ ] C. Grok (se acessível)

**Recomendação**: **Groq como principal**, Gemini como fallback

---

### **DECISÃO 2: Geração de Imagens**
Opções:
- [ ] A. Google Imagen (se créditos suficientes)
- [ ] B. Stable Diffusion local/ComfyUI
- [ ] C. APIs grátis (Pollinations)

**Recomendação**: Precisa pesquisar custos Imagen primeiro

---

### **DECISÃO 3: TTS (Narração)**
Opções:
- [ ] A. New TTS Local (GRÁTIS, sem limites) ← RECOMENDO
- [ ] B. Google Cloud TTS (com créditos)
- [ ] C. Misto (local para MVP, cloud para escala)

**Recomendação**: **New TTS local para MVP**

---

### **DECISÃO 4: Edição de Vídeo**
Opções:
- [ ] A. n8n + Docker (GRÁTIS local, ou AWS credits)
- [ ] B. FFmpeg programático (GRÁTIS, mais controle)
- [ ] C. CapCut semi-automático (GRÁTIS, menos automação)

**Recomendação**: **Híbrido - FFmpeg para MVP, n8n para escala**

---

### **DECISÃO 5: Hosting**
Opções:
- [ ] A. Local (R$ 0, mas PC precisa ficar ligado)
- [ ] B. AWS (com startup credits)
- [ ] C. Google Cloud (com créditos existentes)

**Recomendação**: **Local para MVP (3 dias), migrar cloud depois**

---

## 📋 PRÓXIMA AÇÃO (AGUARDANDO USUÁRIO)

**Preciso que você confirme**:

1. **APIs Google Cloud disponíveis**:
   - Vertex AI (Imagen)?
   - Gemini API?
   - Text-to-Speech?
   - Quanto de crédito restante?

2. **Grok**:
   - Tem acesso à API?
   - Pricing?

3. **AWS**:
   - Startup credits aprovados?
   - Ou ainda em processo?

4. **n8n**:
   - Já está configurado?
   - Rodando onde?

5. **ComfyUI**:
   - Plano é rodar local ou AWS?
   - Já testou?

---

## 💡 STACK RECOMENDADO (Baseado no Que Temos Confirmado)

### **Para MVP de 3 Dias**:

```
IA Texto: Groq (Llama 3.1 - 14.4K/dia grátis)
Imagens: Pollinations.ai (grátis temporário) → migrar Imagen depois
TTS: New TTS Local (grátis, sem limites)
Edição: FFmpeg (Python) + Templates
Storage: Supabase (500MB grátis)
YouTube: YouTube Data API v3 + manual upload
Hosting: LOCAL (seu PC)
```

### **Para Escala (Depois do MVP)**:
```
IA Texto: Groq + Gemini (fallback)
Imagens: Google Imagen (créditos)
TTS: New TTS (voice cloning customizado)
Edição: n8n + Docker (AWS ou local)
Storage: Google Cloud Storage
YouTube: Upload automático (n8n)
Hosting: AWS (créditos) ou Google Cloud
```

---

**Status**: 🟡 AGUARDANDO CONFIRMAÇÕES DO USUÁRIO  
**Próximo**: Responder confirmações → Pesquisar preços → Definir stack final
