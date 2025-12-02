# 🎨 SISTEMA DE CONFIGURAÇÃO AUTOMÁTICA - PERFIL DO CANAL
## Setup Único + Consistência Total

---

## 🎯 COMO FUNCIONA

### **Setup Inicial (1x, 10 minutos)**:

Você roda:
```bash
python incubadora.py --setup-canal
```

Sistema PERGUNTA TUDO uma vez:
```
═══════════════════════════════════════════════════════
  🎬 INCUBADORA AD_LABS - SETUP DE CANAL
═══════════════════════════════════════════════════════

[1/10] 📝 Nome do canal:
> Mistérios Proibidos

[2/10] 🎯 Como quer definir o nicho?
  [1] Digitar manualmente
  [2] IA pesquisa oportunidades e sugere
> 2

  🔍 IA Pesquisando tendências...
  ✅ 5 oportunidades encontradas:
  
  1. "Teorias da Conspiração" (Score: 9.2/10)
     - Demanda: Alta (50K buscas/mês)
     - Competição: Média
     - Potencial viral: Alto
     
  2. "Casos Paranormais" (Score: 8.8/10)
     - Demanda: Muito Alta
     - Competição: Alta
     - Potencial viral: Médio
     
  3. "Mistérios Não Resolvidos" (Score: 9.5/10)
     - Demanda: Alta
     - Competição: Baixa ⭐
     - Potencial viral: Muito Alto
     
  [Digite número 1-5 OU escreva nicho customizado]
> 3

✅ Nicho selecionado: "Mistérios Não Resolvidos"

[3/10] 🎨 Estilo Visual (imagens):
  [1] Realista/Fotográfico (escuro, dramático)
  [2] Pixar 3D (colorido, animado)
  [3] Anime/Ilustração (estilizado)
  [4] Minimalista (simples, elegante)
  [5] Customizado (você define prompt)
> 1

  ✅ Configurado: Realista Escuro
  Preview prompt: "dark cinematic photography, dramatic lighting, 
                   mysterious atmosphere, high quality, 8k"

[4/10] 🎙️ Tipo de Voz:
  [1] Masculina - Grave (Joe Rogan style)
  [2] Masculina - Média (narrador neutro)
  [3] Feminina - Grave (madura, séria)
  [4] Feminina - Média (jovem, clara)
  [5] Customizada (voice clone - você fornece sample)
> 3

  ✅ Configurado: Feminina Grave
  Preview: pt-BR-Wavenet-C (Google TTS)

[5/10] 🎬 Duração dos Vídeos:
  [1] Curtos (1-2min) - Shorts
  [2] Médios (2-4min) - Feed + Shorts
  [3] Longos (5-8min) - Aprofundados
  [4] Mix (varia por eixo)
> 2

  ✅ Configurado: 2-4min (média: 3min)

[6/10] 📊 Quantidade de Vídeos Teste:
  [1] Mínimo (5 vídeos - 1 por eixo)
  [2] Padrão (10 vídeos - 2 por eixo)
  [3] Agressivo (15 vídeos - 3 por eixo)
> 2

  ✅ Configurado: 10 vídeos teste

[7/10] 🎵 Música de Fundo:
  [1] Sem música (só narração)
  [2] Música suave (fundo discreto)
  [3] Música intensa (dramática)
  [4] Customizada (você fornece arquivo)
> 2

  ✅ Configurado: Música suave de fundo
  Biblioteca: YouTube Audio Library (livre de copyright)

[8/10] 📝 Legendas:
  [1] Sim - Estilo padrão (branco com sombra)
  [2] Sim - Estilo highlight (palavra por palavra)
  [3] Não
> 2

  ✅ Configurado: Legendas word-by-word highlight

[9/10] 🖼️ Quantidade de Imagens por Vídeo:
  Vídeo de 3min recomenda 8-12 imagens
  [Digite número ou ENTER para auto (baseado em duração)]
> [ENTER]

  ✅ Auto-configurado: 3-4 seg por imagem
  (~10 imagens para vídeo de 3min)

[10/10] 🎯 Frequência de Upload:
  [1] Diária (1 vídeo/dia)
  [2] Dia sim, dia não (3-4/semana)
  [3] Semanal (2-3/semana)
  [4] Manual (você decide)
> 1

  ✅ Configurado: Upload diário

═══════════════════════════════════════════════════════
  📋 RESUMO DA CONFIGURAÇÃO
═══════════════════════════════════════════════════════

Canal: Mistérios Proibidos
Nicho: Mistérios Não Resolvidos (AI-sugerido, Score 9.5/10)
Estilo: Realista Escuro
Voz: Feminina Grave (pt-BR-Wavenet-C)
Duração: 2-4min (média 3min)
Vídeos Teste: 10 (2 por eixo)
Música: Suave (fundo)
Legendas: Word-by-word highlight
Imagens: Auto (~10 por vídeo)
Upload: Diário

═══════════════════════════════════════════════════════

Confirma configuração? [S/n]
> S

✅ Configuração salva em: canais/misterios_proibidos/config.json

🚀 Pronto para começar!

Próximo comando:
  python incubadora.py --produzir
```

---

## 📁 ARQUIVO GERADO: `config.json`

```json
{
  "canal": {
    "nome": "Mistérios Proibidos",
    "slug": "misterios_proibidos",
    "created_at": "2024-11-28T16:23:00"
  },
  
  "nicho": {
    "tipo": "pesquisa_ia",
    "valor": "Mistérios Não Resolvidos",
    "score_oportunidade": 9.5,
    "demanda": "alta",
    "competicao": "baixa",
    "potencial_viral": "muito_alto",
    "palavras_chave": [
      "mistérios não resolvidos",
      "casos sem solução",
      "enigmas",
      "investigações"
    ]
  },
  
  "estilo_visual": {
    "preset": "realista_escuro",
    "base_prompt": "dark cinematic photography, dramatic lighting, mysterious atmosphere, high quality, 8k, realistic",
    "negative_prompt": "cartoon, anime, colorful, bright, cheerful",
    "aspectos": {
      "tom": "escuro",
      "mood": "misterioso",
      "qualidade": "premium"
    }
  },
  
  "audio": {
    "tts": {
      "provider": "google_cloud",
      "genero": "feminino",
      "tom": "grave",
      "voice_name": "pt-BR-Wavenet-C",
      "speaking_rate": 1.0,
      "pitch": -2.0
    },
    "musica": {
      "ativa": true,
      "tipo": "suave",
      "volume": 0.15,
      "fonte": "youtube_audio_library",
      "tags": ["mysterious", "ambient", "dark"]
    }
  },
  
  "video": {
    "duracao": {
      "min": 120,
      "max": 240,
      "target": 180
    },
    "fps": 30,
    "resolucao": "1080p",
    "aspect_ratio": "16:9",
    "formato_saida": "mp4"
  },
  
  "legendas": {
    "ativas": true,
    "estilo": "word_by_word_highlight",
    "fonte": "Montserrat Bold",
    "tamanho": 48,
    "cor_principal": "#FFFFFF",
    "cor_highlight": "#FFD700",
    "sombra": true,
    "posicao": "centro"
  },
  
  "imagens": {
    "provider": "pollinations",
    "quantidade": "auto",
    "duracao_por_imagem": 3.5,
    "transicoes": "fade",
    "duracao_transicao": 0.5
  },
  
  "producao": {
    "videos_teste": 10,
    "videos_por_eixo": 2,
    "frequencia_upload": "diaria"
  },
  
  "regras_consistencia": {
    "sempre_mesmo_estilo_visual": true,
    "sempre_mesma_voz": true,
    "sempre_mesma_duracao_range": true,
    "sempre_mesmo_formato": true,
    "permitir_variacoes_criativas": "apenas_conteudo"
  }
}
```

---

## 🔧 MODO 1: PESQUISA AUTOMÁTICA DE OPORTUNIDADES

### **Como Funciona**:

```python
def pesquisar_oportunidades():
    """
    1. Google Trends: Top 100 nichos em alta
    2. YouTube API: Analisa competição
    3. Groq IA: Avalia potencial viral
    4. Score: Demanda × (1/Competição) × Viral
    """
    
    # Exemplo de resultado
    oportunidades = [
        {
            "nicho": "Mistérios Não Resolvidos",
            "score": 9.5,
            "demanda": "alta",
            "competicao": "baixa",
            "viral_potencial": "muito_alto",
            "razao": "Alto interesse + Pouca saturação = Oportunidade!"
        },
        # ... mais 4
    ]
    
    return oportunidades
```

### **Critérios de Avaliação**:

| Fator | Peso | Como Mede |
|-------|------|-----------|
| **Demanda** | 40% | Google Trends + YouTube searches |
| **Competição** | 30% | Nº canais grandes no nicho |
| **Viral** | 20% | Média de views de vídeos top |
| **Monetização** | 10% | CPM médio do nicho |

**Score Final**: 0-10 (recomenda só 8+)

---

## 🔧 MODO 2: NICHO MANUAL

### **Se Escolher "Digitar Manualmente"**:

```
[2/10] 🎯 Como quer definir o nicho?
  [1] Digitar manualmente
  [2] IA pesquisa oportunidades e sugere
> 1

Digite o nicho do canal:
> Fatos Curiosos sobre Espaço

🔍 Analisando nicho "Fatos Curiosos sobre Espaço"...

✅ Análise Completa:
  - Demanda: Média-Alta (Google Trends: 68/100)
  - Competição: Média (152 canais >100K subs)
  - CPM Estimado: U$ 3-5 (ciência)
  - Potencial Viral: Médio-Alto
  - Score: 7.8/10 ⚠️ (OK, mas competitivo)

Recomendações IA:
  💡 Sugestão: "Mistérios do Espaço Não Explicados"
     (Score: 9.1/10 - menos competição, mais viral)
  
Quer usar nicho original OU sugestão IA?
  [1] Usar "Fatos Curiosos sobre Espaço"
  [2] Usar "Mistérios do Espaço Não Explicados"
  [3] Pesquisar mais opções
> 1

✅ Confirmado: "Fatos Curiosos sobre Espaço"
```

---

## 🎨 PRESETS DE ESTILO VISUAL

### **Opção 1: Realista Escuro**
```
Base Prompt:
"dark cinematic photography, dramatic lighting, mysterious 
atmosphere, noir style, high contrast, moody, 8k, ultra realistic"

Negative:
"cartoon, anime, bright colors, cheerful, illustration"

Use Cases: Mistérios, Terror, Crimes, Teorias
```

### **Opção 2: Pixar 3D**
```
Base Prompt:
"pixar style, 3D render, disney animation, volumetric lighting,
vibrant colors, cute characters, professional 3D modeling, 8k"

Negative:
"realistic, photo, dark, scary, 2D"

Use Cases: Infantil, Educativo Leve, Motivacional
```

### **Opção 3: Anime/Ilustração**
```
Base Prompt:
"anime style, manga illustration, vibrant colors, detailed artwork,
studio ghibli inspired, beautiful anime art, HD"

Negative:
"realistic, 3D, photo, ugly, western cartoon"

Use Cases: Histórias, Fantasia, Review de Anime
```

### **Opção 4: Minimalista**
```
Base Prompt:
"minimalist design, clean aesthetic, simple shapes, elegant,
modern, flat design, professional infographic style"

Negative:
"complex, cluttered, realistic, photo, messy"

Use Cases: Negócios, Tech, Finanças, Educativo
```

### **Opção 5: Customizado**
```
Sistema pergunta:
  - Tom (escuro/claro/neutro)
  - Mood (dramático/alegre/sério)
  - Referência (URL de imagem exemplo)
  
Groq IA gera prompt personalizado baseado nas respostas
```

---

## 🎙️ PRESETS DE VOZ

### **Google Cloud TTS (Grátis 1M chars)**:

| Preset | Voice Name | Gênero | Tom | Use Case |
|--------|------------|--------|-----|----------|
| **Masc. Grave** | pt-BR-Wavenet-B | M | Grave | Mistérios, Crimes |
| **Masc. Média** | pt-BR-Neural2-B | M | Neutro | Educativo, News |
| **Fem. Grave** | pt-BR-Wavenet-C | F | Grave | Narração Dramática |
| **Fem. Média** | pt-BR-Neural2-A | F | Claro | Educativo, Kids |

### **Customização Adicional**:
```json
{
  "speaking_rate": 1.0,   // 0.5-2.0 (velocidade)
  "pitch": 0.0,          // -20 a +20 (tom)
  "volume_gain_db": 0.0  // -96 a +16 (volume)
}
```

---

## 🔒 CONSISTÊNCIA TRAVADA

### **O Que NUNCA Muda** (travado após setup):

✅ Estilo visual (prompt base)
✅ Tipo de voz (mesma sempre)
✅ Duração range (sempre 2-4min)
✅ Formato de legendas
✅ Música de fundo (tipo)
✅ Aspect ratio (16:9)
✅ Resolução (1080p)

### **O Que Pode Variar** (criatividade):

🎨 Conteúdo específico das imagens
🎨 Texto do roteiro
🎨 Ideias de vídeos
🎨 Músicas específicas (dentro do tipo)

---

## 📋 COMANDOS COMPLETOS

### **Setup Canal** (1x):
```bash
python incubadora.py --setup-canal

# OU modo rápido (tudo default):
python incubadora.py --setup-canal --preset "misterios_escuros"
```

### **Produzir Vídeos** (usa config salvo):
```bash
# Produção inicial (10 vídeos teste)
python incubadora.py --produzir

# Escalar eixo vencedor
python incubadora.py --escalar eixo_02 --quantidade 20

# Novo lote (mantém config)
python incubadora.py --produzir --quantidade 5
```

### **Ver Configuração**:
```bash
python incubadora.py --ver-config
```

### **Editar Configuração**:
```bash
# Mudar só a voz
python incubadora.py --config voz --valor "pt-BR-Wavenet-B"

# Mudar duração
python incubadora.py --config duracao --min 180 --max 300

# Reconfigurar tudo
python incubadora.py --reconfigurar
```

---

## 🎯 MÚLTIPLOS CANAIS

### **Estrutura de Pastas**:
```
incubadora/
├── canais/
│   ├── misterios_proibidos/
│   │   ├── config.json
│   │   ├── outputs/
│   │   └── analytics/
│   │
│   ├── fatos_curiosos/
│   │   ├── config.json
│   │   └── outputs/
│   │
│   └── historias_vinganca/
│       ├── config.json
│       └── outputs/
```

### **Trocar Entre Canais**:
```bash
# Listar canais
python incubadora.py --list-canais

# Selecionar canal
python incubadora.py --canal misterios_proibidos --produzir

# Produzir em todos
python incubadora.py --todos-canais --produzir
```

---

## ✅ RESUMO FINAL

### **Você Faz 1x** (10min):
```
1. python incubadora.py --setup-canal
2. Responde 10 perguntas
3. Confirma
```

### **Sistema Salva**:
```
✅ Nicho (manual ou AI-sugerido)
✅ Estilo visual (travado)
✅ Tipo de voz (travado)
✅ Duração padrão (travado)
✅ Formato legendas (travado)
✅ Música (travado)
✅ Tudo configurado!
```

### **Próximas Produções**:
```
python incubadora.py --produzir

Sistema USA automaticamente:
  ✅ Mesmo estilo
  ✅ Mesma voz
  ✅ Mesma duração
  ✅ Zero perguntas!
```

---

**Status**: 🟢 Sistema de Configuração Completo Definido  
**Próximo**: Codificar CLI interativa + salvamento config  
**Quando**: Assim que você aprovar este setup!
