# 💰 TABELA DE CUSTOS COMPLETA - TODAS AS APIs
## Comparação Detalhada para Decisão Inteligente

---

## 📊 RESUMO EXECUTIVO

| Categoria | Melhor Opção Grátis | Custo/Mês | Alternativa Paga | Custo/Mês |
|-----------|---------------------|-----------|------------------|-----------|
| **Texto (IA)** | Groq (Llama 3.1) | **R$ 0** | Grok 4 | U$ 25 grátis |
| **Imagens** | Pollinations.AI | **R$ 0** | Google Imagen | Créditos |
| **Narração (TTS)** | Google TTS | **R$ 0** (1M chars) | ElevenLabs | U$ 22 |
| **Servidor Vídeo** | AWS EC2 t2.micro | **R$ 0** (12 meses) | AWS t2.medium | U$ 35 |
| **Storage** | Supabase | **R$ 0** (500MB) | S3 | U$ 0.02/GB |

**TOTAL MENSAL (Configuração Grátis)**: **R$ 0,00**

---

## 🤖 CATEGORIA 1: GERAÇÃO DE TEXTO (IA)

### **OPÇÃO A: Groq** ⭐ **RECOMENDADO - GRÁTIS**

| Métrica | Valor | Observação |
|---------|-------|------------|
| **Custo** | **R$ 0** | Perpétuo |
| **Limite/Dia** | 14.400 requests | Llama 3.1 |
| **Limite/Request** | ~8.000 tokens | Suficiente para roteiro |
| **Latência** | ~1-2s | Muito rápido |
| **Qualidade** | ⭐⭐⭐⭐ | Excelente |

**Custo Real**:
```
150 roteiros/dia = 150 requests
Custo: R$ 0 (dentro do limite)

1 roteiro = ~1.500 tokens
150 roteiros = 225.000 tokens/dia
Limite: 14.400 requests (suficiente)
```

---

### **OPÇÃO B: Grok (xAI)** - **BACKUP**

| Métrica | Valor | Observação |
|---------|-------|------------|
| **Custo Free** | **U$ 25/mês grátis** | Até fim 2024 |
| **Depois Free** | U$ 0 | Continua? A verificar |
| **Grok-4** | U$ 3/M input, U$ 15/M output | Caro |
| **Grok-4-fast** | U$ 0.20/M input, U$ 0.50/M output | Razoável |
| **Qualidade** | ⭐⭐⭐⭐⭐ | Estado da arte |

**Custo Real** (Grok-4-fast):
```
1 roteiro = ~500 tokens input + 2.000 tokens output
150 roteiros/mês:
  Input: 75K tokens = U$ 0.015
  Output: 300K tokens = U$ 0.15
  Total: U$ 0.165/mês (~R$ 0.80)

Com U$ 25 grátis/mês: Cobre 150x mais!
```

---

### **OPÇÃO C: Gemini (Google)** - **SE TEM CRÉDITOS**

| Métrica | Valor | Observação |
|---------|-------|------------|
| **Free Tier** | U$ 300 créditos (90 dias) | Novos clientes |
| **Grátis Perpétuo** | 60 requests/min | Sim! |
| **Pro (Pago)** | U$ 0.25/M tokens input | Barato |
| **Qualidade** | ⭐⭐⭐⭐⭐ | Multimodal |

**Custo Real**:
```
Com free tier perpétuo (60 req/min):
150 roteiros/dia = OK (dentro do limite)
Custo: R$ 0

Se usar créditos:
150 roteiros × 2K tokens = 300K tokens
U$ 300 cobre: 1.2 BILHÃO de tokens
= 4.000 roteiros/dia por 90 dias!
```

---

## 🎨 CATEGORIA 2: GERAÇÃO DE IMAGENS

### **OPÇÃO A: Pollinations.AI** ⭐ **RECOMENDADO - GRÁTIS**

| Métrica | Valor | Observação |
|---------|-------|------------|
| **Custo** | **R$ 0** | Perpétuo, ilimitado |
| **Limite** | NENHUM | Sem rate limit |
| **Qualidade** | ⭐⭐⭐ | Boa (não premium) |
| **Watermark** | ❌ Não | Limpo |
| **Velocidade** | ~5-10s | Rápido |

**Custo Real**:
```
10 imagens/vídeo × 150 vídeos/mês = 1.500 imagens
Custo: R$ 0,00
```

---

### **OPÇÃO B: Google Imagen (Vertex AI)** - **PREMIUM**

| Métrica | Valor | Observação |
|---------|-------|------------|
| **Free Tier** | U$ 300 créditos | 90 dias |
| **Imagen 2** | ~U$ 0.04/imagem | Estimativa |
| **Imagen 3** | ~U$ 0.08/imagem | Melhor qualidade |
| **Qualidade** | ⭐⭐⭐⭐⭐ | Estado da arte |

**Custo Real**:
```
1.500 imagens/mês × U$ 0.04 = U$ 60/mês (~R$ 300)

Com U$ 300 créditos:
U$ 300 ÷ U$ 60 = 5 meses grátis
Depois: R$ 300/mês (CARO!)

RECOMENDAÇÃO: Usar APENAS para testes/qualidade premium
```

---

### **OPÇÃO C: Stable Diffusion Local** - **CUSTO ZERO MAS PRECISA GPU**

| Métrica | Valor | Observação |
|---------|-------|------------|
| **Custo** | **R$ 0** | Se rodar local |
| **AWS GPU** | ~U$ 0.50-3/hora | p3.2xlarge |
| **Qualidade** | ⭐⭐⭐⭐ | Alta (customizável) |
| **Setup** | Complexo | ComfyUI, modelos, etc |

**Custo Real** (Local):
```
Energia PC: ~R$ 5/mês (desprezível)
Custo: R$ 0

AWS (se PC não aguentar):
1h geração/dia × U$ 1/hora × 30 dias = U$ 30/mês
```

---

## 🎙️ CATEGORIA 3: NARRAÇÃO (TTS)

### **OPÇÃO A: Google Cloud TTS** ⭐ **RECOMENDADO - GRÁTIS**

| Métrica | Valor | Observação |
|---------|-------|------------|
| **Free Tier** | **1 milhão caracteres/mês** | Perpétuo! |
| **Depois Free** | U$ 16/milhão | Barato |
| **WaveNet/Neural2** | Mesma pricing | Alta qualidade |
| **Latência** | ~2-5s | Rápido |
| **Qualidade** | ⭐⭐⭐⭐ | Natural |

**Custo Real**:
```
1 vídeo 3min = ~2.000 caracteres
1 milhão chars = 500 vídeos/mês GRÁTIS

Depois do free tier:
500 vídeos = U$ 16/mês (~R$ 80)
Por vídeo: R$ 0.16
```

---

### **OPÇÃO B: ElevenLabs** - **PREMIUM PAGO**

| Métrica | Valor | Observação |
|---------|-------|------------|
| **Free** | 10.000 chars/mês | Muito limitado |
| **Starter** | U$ 5/mês | 30.000 chars |
| **Creator** | U$ 22/mês | 100.000 chars |
| **Qualidade** | ⭐⭐⭐⭐⭐ | Melhor do mercado |
| **Voice Clone** | ✅ Sim | Premium feature |

**Custo Real**:
```
500 vídeos × 2K chars = 1M chars/mês
ElevenLabs Creator: U$ 22 (100K chars)
  = Precisa de 10× planos = U$ 220/mês! 💸

Google TTS: R$ 0 (mesmo 1M)
```

---

### **OPÇÃO C: New TTS Local** - **GRÁTIS MAS PC PESADO**

| Métrica | Valor | Observação |
|---------|-------|------------|
| **Custo** | **R$ 0** | 100% local |
| **Limite** | NENHUM | Ilimitado |
| **Qualidade** | ⭐⭐⭐⭐ | = ElevenLabs |
| **Requisitos** | 8GB RAM + tempo | CPU: lento |
| **Voice Clone** | ✅ 3s sample | Grátis! |

**Custo Real**:
```
PC ligado 24/7: ~R$ 50/mês (energia)
OU
Gerar em batch: ~R$ 5/mês

Problema: SEU PC NÃO AGUENTA
```

---

## 🎬 CATEGORIA 4: GERAÇÃO/EDIÇÃO DE VÍDEO

### **OPÇÃO A: AWS EC2 + Docker (narrated-story-creator)** ⭐ **RECOMENDADO**

| Métrica | Valor | Observação |
|---------|-------|------------|
| **t2.micro (Free)** | **R$ 0** | 12 meses, 750h/mês |
| **t2.small** | ~U$ 17/mês | 2GB RAM |
| **t2.medium** | ~U$ 35/mês | 4GB RAM |
| **Qualidade** | ⭐⭐⭐⭐ | Completo |
| **Features** | Tudo integrado | TTS, legendas, etc |

**Custo Real**:

**Cenário 1: t2.micro (GRÁTIS)**
```
750 horas/mês grátis
24/7 = 720h/mês
Custo: R$ 0 (dentro do free tier!)

Limitação: 1GB RAM = vídeos curtos
```

**Cenário 2: t2.medium (PAGO após 12 meses)**
```
U$ 35/mês × 12 = U$ 420/ano
Ou: U$ 0.05/hora on-demand

Produção em batch:
10 vídeos × 5min = 50min = U$ 0.04
500 vídeos/mês × 5min = 40h = U$ 2/mês

TRUQUE: Stop instance quando não usar!
```

---

### **OPÇÃO B: FFmpeg Local** - **GRÁTIS MAS PC PESADO**

| Métrica | Valor | Observação |
|---------|-------|------------|
| **Custo** | **R$ 0** | Open-source |
| **Complexidade** | Alta | Código Python |
| **Qualidade** | ⭐⭐⭐ | Básico |
| **Limitação** | PC precisa aguentar | Seu não aguenta |

---

### **OPÇÃO C: CapCut** - **MANUAL**

| Métrica | Valor | Observação |
|---------|-------|------------|
| **Custo** | **R$ 0** | Versão gratuita |
| **Automação** | ❌ Semi-manual | Templates |
| **Qualidade** | ⭐⭐⭐⭐⭐ | Profissional |
| **Tempo** | 10-20min/vídeo | Manual |

**Custo Real**:
```
Seu tempo: 500 vídeos × 15min = 125 horas
Se valorizar tempo em R$ 30/h = R$ 3.750/mês

Automação > Manual para escala!
```

---

## 💾 CATEGORIA 5: STORAGE (ASSETS)

### **OPÇÃO A: Supabase** ⭐ **RECOMENDADO - GRÁTIS**

| Métrica | Valor | Observação |
|---------|-------|------------|
| **Free Tier** | **500 MB** | Perpétuo |
| **Depois Free** | U$ 0.125/GB extra | Barato |
| **Bandwidth** | 2GB/mês | Suficiente |
| **Velocidade** | Rápida (CDN) | Global |

**Custo Real**:
```
3 assets fixos (backgrounds, avatars):
  - background.mp4: 50MB
  - 2× avatars.png: 2MB
  Total: 52MB

Espaço usado: 10% do free tier
Custo: R$ 0

Se precisar mais (vídeos finais):
500 vídeos × 20MB = 10GB
U$ 0.125 × 10GB = U$ 1.25/mês (~R$ 6)
```

---

### **OPÇÃO B: Google Cloud Storage** - **SE TEM CRÉDITOS**

| Métrica | Valor | Observação |
|---------|-------|------------|
| **Free Tier** | U$ 300 créditos | 90 dias |
| **Standard** | U$ 0.02/GB/mês | Depois créditos |
| **Bandwidth** | U$ 0.12/GB | Egress |

**Custo Real**:
```
10GB storage: U$ 0.20/mês
10GB downloads: U$ 1.20/mês
Total: U$ 1.40/mês (~R$ 7)

Com créditos: 200+ meses grátis
```

---

## 📱 CATEGORIA 6: YOUTUBE API

### **YouTube Data API v3** - **SEMPRE GRÁTIS**

| Métrica | Valor | Observação |
|---------|-------|------------|
| **Custo** | **R$ 0** | Perpétuo |
| **Quota/Dia** | 10.000 units | Suficiente |
| **Search** | 100 units/request | 100 buscas/dia |
| **Video Details** | 1-3 units | 3.000+/dia |

**Custo Real**:
```
Pesquisa inicial: 100 buscas × 100 units = 10.000 units
Custo: R$ 0 (máximo do dia, mas só faz 1x)

Análise diária: 500 vídeos × 3 units = 1.500 units
Custo: R$ 0
```

---

## 🎯 CONFIGURAÇÃO RECOMENDADA (CUSTO ZERO)

### **Stack Grátis Completo**:
```
Texto: Groq (Llama 3.1)
  → 14.4K/dia = ilimitado prático
  → R$ 0/mês

Imagens: Pollinations.AI
  → Ilimitado
  → R$ 0/mês

Narração: Google Cloud TTS
  → 1M chars/mês = 500 vídeos
  → R$ 0/mês

Vídeo: AWS EC2 t2.micro
  → 750h/mês free tier
  → R$ 0/mês (12 meses)

Storage: Supabase
  → 500MB
  → R$ 0/mês

YouTube: Data API v3
  → 10K units/dia
  → R$ 0/mês

TOTAL: R$ 0,00/mês
```

**Capacidade**:
- 500 vídeos/mês (limite TTS)
- Qualidade: ⭐⭐⭐⭐ (muito boa)
- Escalabilidade: Média (free tiers)

---

## 💸 CONFIGURAÇÃO PREMIUM (SE QUISER PAGAR)

### **Stack Pago (Qualidade Máxima)**:
```
Texto: Grok 4-fast
  → U$ 0.20/M tokens
  → ~U$ 5/mês para 500 vídeos

Imagens: Google Imagen 3
  → U$ 0.08/imagem
  → U$ 60/mês (1.500 imagens)

Narração: ElevenLabs Creator
  → U$ 22/mês
  → 100K chars = 50 vídeos
  → Precisa 10x = U$ 220/mês

Vídeo: AWS t2.medium on-demand
  → U$ 0.05/hora
  → U$ 2-5/mês (batch)

Storage: Google Cloud
  → U$ 1.40/mês

YouTube: API v3
  → R$ 0

TOTAL: ~U$ 290/mês (~R$ 1.450)
```

**Diferença vs Grátis**:
- Qualidade: +10-15%
- Custo: +infinito%
- **NÃO VALE A PENA para MVP!**

---

## 📋 CUSTOS POR VÍDEO

| Configuração | Custo/Vídeo | Custo 500 Vídeos/Mês |
|--------------|-------------|----------------------|
| **100% Grátis** | R$ 0,00 | R$ 0,00 |
| **Híbrida (TTS Google + resto grátis)** | R$ 0,00 | R$ 0,00 (1M chars) |
| **Premium (tudo pago)** | R$ 2,90 | R$ 1.450 |

---

## 🎯 RECOMENDAÇÃO FINAL

### **Para MVP (Primeiros 6 Meses)**:
✅ **Stack 100% Grátis**
- Custo: **R$ 0,00/mês**
- Limite: 500 vídeos/mês
- Qualidade: ⭐⭐⭐⭐

### **Para Escala (Depois 6 Meses)**:
✅ **Híbrido**:
```
Texto: Groq (continua grátis)
Imagens: Pollinations (continua grátis)
TTS: Google TTS (continua grátis até 1M)
Vídeo: AWS t2.micro (stop/start) = U$ 2-5/mês
Storage: Supabase + extra = U$ 1-2/mês

TOTAL: U$ 3-7/mês (~R$ 15-35)
```

---

## 📍 ONDE ESTÃO OS MANUAIS

**Todos os manuais estão em**: `d:\AD_LABS\`

| Arquivo | O Que É |
|---------|---------|
| **`GUIA_SETUP_COMPLETO_ZERO_CUSTO.md`** | 🏆 Tutorial passo a passo COMPLETO |
| `ESTRATEGIA_FERRAMENTAS_GRATIS.md` | Estratégia e comparação |
| `ESTRATEGIA_CLOUD_PC_FRACO.md` | Setup cloud (AWS) |
| `ARSENAL_FERRAMENTAS_APIS.md` | Arsenal completo |
| `REGRAS_OURO_100_MAIORES.md` | Padrões YouTube |
| `youtube/11_Clone_Voice_Local_TTS_Tutorial_Gratuito.md` | New TTS local |
| `youtube/15_Groq_Free_AI_APIs_Tutorial.md` | Groq setup |
| `youtube/18_Videos_Longos_Virais_IA_N8N_Gratis.md` | n8n + Docker |

---

**Custo Total Configuração Grátis**: **R$ 0,00/mês**  
**Capacidade**: 500 vídeos/mês  
**Período**: 6-12 meses grátis, depois R$ 15-35/mês
