# Coqui XTTS v2 - Deployment Guide for GCP

## 📋 O Que É Isso?

Este é um servidor de **Text-to-Speech com Clonagem de Voz** usando o modelo open-source **Coqui XTTS v2**.

**Funcionalidades:**
- Gera áudio de alta qualidade em 17 idiomas (incluindo português).
- **Clonagem de Voz:** Com apenas 6 segundos de áudio de referência, replica qualquer voz.
- API REST simples para integração.

---

## 🚀 Deploy no Google Cloud Run

### Pré-requisitos
- Google Cloud CLI instalado ([Download](https://cloud.google.com/sdk/docs/install))
- Projeto GCP ativo
- Billing habilitado

### Passo 1: Autenticar

```bash
gcloud auth login
gcloud config set project SEU_PROJETO_ID
```

### Passo 2: Fazer Build da Imagem

```bash
cd d:\AD_LABS\deploy\coqui_xtts

gcloud builds submit --tag gcr.io/SEU_PROJETO_ID/coqui-xtts
```

### Passo 3: Deploy no Cloud Run

```bash
gcloud run deploy coqui-xtts \
  --image gcr.io/SEU_PROJETO_ID/coqui-xtts \
  --platform managed \
  --region us-central1 \
  --memory 4Gi \
  --cpu 2 \
  --timeout 300 \
  --allow-unauthenticated
```

**Resultado:** Você receberá uma URL pública (ex: `https://coqui-xtts-abc123-uc.a.run.app`).

---

## 🎤 Como Usar a API

### 1. Gerar Áudio Simples (Sem Clonagem)

```bash
curl -X POST "https://sua-url.run.app/tts" \
  -F "text=No princípio, Deus criou os céus e a terra." \
  -F "language=pt" \
  --output audio.wav
```

### 2. Clonar Voz de um Narrador

#### Passo 1: Preparar Áudio de Referência
- Baixe um vídeo do YouTube (ex: narrador do "Bible in a Nutshell").
- Extraia um trecho de **6-30 segundos** onde só a voz dele está audível (sem música).
- Converta para WAV: `ffmpeg -i video.mp4 -ar 22050 -ac 1 referencia.wav`

#### Passo 2: Fazer Upload da Voz

```bash
curl -X POST "https://sua-url.run.app/upload_reference_voice" \
  -F "voice_name=epic_narrator" \
  -F "voice_file=@referencia.wav"
```

#### Passo 3: Gerar Áudio com a Voz Clonada

```bash
curl -X POST "https://sua-url.run.app/tts" \
  -F "text=E Davi venceu Golias, não com espada, mas com fé." \
  -F "language=pt" \
  -F "speaker_wav_file=@referencia.wav" \
  --output audio_clonado.wav
```

---

## 🔗 Integração com o Agente 08

Após o deploy, você receberá uma URL. Passe essa URL para o Agente Antigravity configurar o `agente_08_narrador.py`.

Exemplo:
```
URL do Coqui XTTS: https://coqui-xtts-abc123-uc.a.run.app
```

---

## 💰 Estimativa de Custo (GCP Cloud Run)

- **Requisições:** Grátis até 2M/mês.
- **Compute:** ~$0.10/hora (só paga quando está em uso).
- **Exemplo:** 100 vídeos/mês (~300 áudios) = **$2-5 USD/mês**.

---

## 🐛 Troubleshooting

### Erro: "Model not found"
- O modelo baixou corretamente no build? Veja os logs: `gcloud builds log LAST_BUILD_ID`

### Timeout na primeira requisição
- O modelo é grande (~2GB). A primeira chamada pode demorar 30-60s. Depois fica rápido.

### Qualidade de áudio ruim
- Verifique se o áudio de referência está limpo (sem eco, sem música de fundo).
- Use um arquivo WAV com 22.050 Hz, mono.

---

## 📚 Documentação da API

Após o deploy, acesse: `https://sua-url.run.app/docs`

Você verá a interface Swagger com todos os endpoints disponíveis.
