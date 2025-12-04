# 🚀 HANDOVER: High-Quality Video Pipeline

**Data:** 04/12/2024  
**Status:** ✅ Nutshell Style Implementado | ❌ Coqui XTTS Deploy Failed  
**Próximo Passo:** Escolher solução alternativa para TTS (opções no final)

---

## 🎯 O Que Foi Feito

### 1. Template Nutshell (Ritmo Acelerado)
- ✅ Criado `specs/templates/nutshell.md`
- ✅ Configurado para cenas de 3-5 segundos
- ✅ Auto-seleção quando `canal_id = bible_in_a_nutshell`

### 2. Stack Real Configurado
- ✅ **Roteiro:** Claude 3.5 Sonnet (via Anthropic API)
- ✅ **Imagens:** Google Imagen 4 (via Vertex AI)
- ✅ **Áudio:** Coqui XTTS v2 (em deploy)

### 3. Style Mapper (Visual)
- ✅ Intercepta provider "MagicLight.ai"
- ✅ Redireciona para Imagen com keywords Pixar/3D

### 4. Pacote de Deploy Coqui XTTS
- ✅ Dockerfile (lazy loading do modelo)
- ✅ API FastAPI (`api.py`)
- ✅ Script PowerShell (`deploy_gcp.ps1`)
- ✅ README completo
- ⏳ **Build em andamento** no GCP projeto `fast-circle-479719-h8`

---

## 📋 Estado Atual do Deploy (FALHOU)

**Build:** ✅ Concluído (imagem `gcr.io/fast-circle-479719-h8/coqui-xtts`)
**Deploy:** ❌ Falhou - Health check timeout

**Problema:**
- Cloud Run exige que o container inicie em <60s
- Modelo XTTS (2GB) demora ~3-5min para baixar na primeira execução
- Health check falha antes do modelo terminar de baixar

**Tentativas:**
1. Timeout 300s: Falhou
2. Timeout 600s + no-cpu-throttling: Falhou

**Log de Erro:**
```
The user-provided container failed to start and listen on the port
defined provided by the PORT=8080 environment variable within the
allocated timeout.
```

---

## 🔧 Soluções Alternativas

### Opção 1: Compute Engine (VM) - RECOMENDADO
**Prós:**
- Modelo baixa uma vez e fica em disco
- Sem limite de startup timeout
- Mesma API (só muda a URL)

**Contras:**
- Precisa ficar ligado (custo fixo ~$20/mês)
- Mais complexo de gerenciar

**Como fazer:**
1. Criar VM: `gcloud compute instances create coqui-xtts --machine-type=e2-medium`
2. SSH na VM: `gcloud compute ssh coqui-xtts`
3. Instalar Docker e rodar o container
4. Criar IP estático

### Opção 2: Usar ElevenLabs (Pago)
**Prós:**
- API pronta, sem deploy
- Qualidade excelente
- Startup instantâneo

**Contras:**
- $5/mês (30k caracteres)

**Como fazer:**
1. Criar conta: https://elevenlabs.io
2. Pegar API key
3. Configurar no `.env`: `ELEVENLABS_API_KEY=...`
4. Agente já suporta (está no código)

### Opção 3: Usar Google Cloud TTS (Atual)
**Prós:**
- Já funciona
- Grátis/barato

**Contras:**
- Voz robótica (sem emoção)

---

## ❓ Decisão Necessária (Próxima Conversa)

Escolha uma opção:
1. **VM** para Coqui XTTS (grátis, mas mais trabalho)
2. **ElevenLabs** (pago $5/mês, zero config)
3. **Manter Google TTS** (funcional, mas voz fraca)

---

## 🔧 Arquivos Modificados

### Configuração
- `canais/bible_in_a_nutshell/CONFIGURACAO_DETALHADA_BIBLE_NUTSHELL.md`
  - Provider de imagens: Google Imagen 4
  - Provider de áudio: Google Cloud TTS → Coqui XTTS (pendente URL)
  - Prompts visuais: Claude 3.5 Sonnet

### Agentes
- `agentes/agente_06_roteirista.py`
  - Seleção automática de template Nutshell
  - Configurado para usar Claude 3.5 Sonnet (com fallback para Gemini)
  - Corrigido path do `templates_dir`

- `agentes/agente_07_visual.py`
  - Style Mapper ativo (MagicLight → Imagen + Pixar keywords)

### Serviços
- `services/tts_strategy.py`
  - Adicionado suporte a `coqui_xtts` no factory

- `services/coqui_tts_strategy.py` (NOVO)
  - Cliente para chamar API do Coqui XTTS remoto

### Templates
- `specs/templates/nutshell.md` (NOVO)
  - Template para vídeos rápidos (3-5s/cena)

### Deploy
- `deploy/coqui_xtts/Dockerfile`
- `deploy/coqui_xtts/api.py`
- `deploy/coqui_xtts/deploy_gcp.ps1`
- `deploy/coqui_xtts/README.md`

---

## 🚨 Pendências para Próxima Sessão

### Imediato
- [ ] Aguardar build do Coqui XTTS terminar (comando rodando)
- [ ] Fazer deploy no Cloud Run
- [ ] Configurar URL no sistema

### Médio Prazo
- [ ] Atualizar Agente 06 para usar Claude Opus 4.5 via Vertex AI (em vez de API direta)
- [ ] Testar clonagem de voz com referência do YouTube
- [ ] Implementar Agente 09 (Sound Designer) para SFX

### Longo Prazo
- [ ] Configurar ComfyUI na GPU Tesla P4 (GCP)
- [ ] Integrar geração de vídeo (movimento real em vez de slideshow)

---

## 🔑 Variáveis de Ambiente Necessárias

```bash
# APIs Google
GOOGLE_API_KEY_IMAGE=...
GOOGLE_API_KEY_AUDIO=...
GOOGLE_API_KEY_VIDEO=...

# Claude
ANTHROPIC_API_KEY=...

# Coqui XTTS (após deploy)
COQUI_XTTS_URL=https://coqui-xtts-XXX.run.app

# Telegram
TELEGRAM_BOT_TOKEN=...
```

---

## 💡 Comandos Úteis

**Ver progresso do build:**
```powershell
gcloud builds list --ongoing
```

**Logs do build:**
```powershell
gcloud builds log BUILD_ID
```

**Deploy manual (após build):**
```powershell
gcloud run deploy coqui-xtts `
  --image gcr.io/fast-circle-479719-h8/coqui-xtts `
  --platform managed `
  --region us-central1 `
  --memory 4Gi `
  --cpu 2 `
  --timeout 300 `
  --allow-unauthenticated
```

---

**🃏 Continua de onde parou. Mansão, não puxadinho.**
