# 🎨 CONFIGURAÇÃO COMPLETA - TODOS OS CAMPOS DETALHADOS
## Guia Definitivo: Cada Opção, Cada Variação, Cada Possibilidade

---

## 📋 ÍNDICE DE CONFIGURAÇÕES

1. [Informações Básicas do Canal](#1-informações-básicas-do-canal)
2. [Definição de Nicho](#2-definição-de-nicho)
3. [Estilo Visual e Imagens](#3-estilo-visual-e-imagens)
4. [Configuração de Áudio](#4-configuração-de-áudio)
5. [Formato de Vídeo](#5-formato-de-vídeo)
6. [Legendas e Captions](#6-legendas-e-captions)
7. [Música e Efeitos Sonoros](#7-música-e-efeitos-sonoros)
8. [Estratégia de Produção](#8-estratégia-de-produção)
9. [Configurações de Upload](#9-configurações-de-upload)
10. [Análise e Métricas](#10-análise-e-métricas)
11. [Configurações Avançadas](#11-configurações-avançadas)

---

## 1. INFORMAÇÕES BÁSICAS DO CANAL

### **1.1 Nome do Canal**
```
Campo: canal.nome
Tipo: String (obrigatório)
Min: 3 caracteres
Max: 50 caracteres
Validação: Alfanumérico + espaços

Exemplo:
> Mistérios Proibidos
> Fatos Que Ninguém Conta
> Histórias de Vingança BR
```

### **1.2 Descrição do Canal**
```
Campo: canal.descricao
Tipo: String (opcional)
Max: 500 caracteres

Exemplo:
> Canal dedicado aos maiores mistérios não resolvidos do mundo. 
  Casos que a polícia não conseguiu decifrar, enigmas históricos 
  e teorias que vão fazer você questionar tudo.
```

### **1.3 Idioma Principal**
```
Campo: canal.idioma
Tipo: Select
Opções:
  [1] pt-BR (Português Brasil)
  [2] pt-PT (Português Portugal)
  [3] en-US (Inglês EUA)
  [4] es-ES (Espanhol)
  [5] Multi-idioma (define por vídeo)

Default: pt-BR
```

### **1.4 Público-Alvo**
```
Campo: canal.publico_alvo
Tipo: Multiple Select

Faixa Etária:
  [ ] 13-17 (Teens)
  [ ] 18-24 (Jovens Adultos)
  [x] 25-34 (Adultos)
  [x] 35-44 (Adultos Estabelecidos)
  [ ] 45+ (Maduros)

Gênero:
  [ ] Predominante Masculino
  [ ] Predominante Feminino
  [x] Todos os Gêneros

Interesses:
  [x] Mistérios
  [x] Ciência
  [ ] Entretenimento
  [ ] Educação
  [x] True Crime
```

---

## 2. DEFINIÇÃO DE NICHO

### **2.1 Modo de Definição**
```
Campo: nicho.modo
Tipo: Select

Opções:
  [1] Manual - Você sabe o que quer
  [2] IA Sugere - Pesquisa automática de oportunidades
  [3] Híbrido - IA sugere, você refina
```

#### **MODO 1: Manual**
```
Se escolher [1]:

Campo: nicho.manual.tema
Tipo: String
Prompt: "Digite o tema/nicho do canal:"
> Mistérios Não Resolvidos

Sistema executa:
  1. Valida tema (não pode ser genérico demais)
  2. Analisa competição (API YouTube)
  3. Calcula score (1-10)
  4. Mostra análise:
  
═══════════════════════════════════════════════════
  📊 ANÁLISE DO NICHO
═══════════════════════════════════════════════════
Tema: "Mistérios Não Resolvidos"

Demanda (Google Trends):
  ████████░░ 82/100 (Alta)

Competição (YouTube):
  Canais >100K subs: 284
  Canais >1M subs: 12
  Nível: ███████░░░ Médio-Alto

Potencial Viral:
  Média views top 100 vídeos: 450K
  Taxa engajamento: 4.2%
  Nível: █████████░ Alto

CPM Estimado:
  Nicho: $3-$6 (entretenimento/educação)
  
Score Final: 8.4/10 ⭐
Status: ✅ Viável (competitivo mas com potencial)

Recomendação IA:
  💡 Refine para: "Mistérios Brasileiros Não Resolvidos"
     Score projetado: 9.2/10 (menos competição)
  
Aceitar tema OU usar recomendação?
  [1] Usar "Mistérios Não Resolvidos"
  [2] Usar "Mistérios Brasileiros Não Resolvidos"
  [3] Cancelar e escolher outro
> _
```

#### **MODO 2: IA Sugere (Pesquisa Automática)**
```
Se escolher [2]:

Sistema executa:
  1. Google Trends: Top 100 termos crescentes
  2. YouTube API: Analisa 500+ nichos
  3. Groq IA: Cruza dados e ranqueia
  4. Apresenta Top 10

═══════════════════════════════════════════════════
  🔍 TOP 10 OPORTUNIDADES (Score 8.0+)
═══════════════════════════════════════════════════

1. Casos Paranormais Brasileiros (Score: 9.7/10) ⭐⭐⭐
   Demanda: ████████░░ Muito Alta
   Competição: ███░░░░░░░ Baixa
   Viral: █████████░ Muito Alto
   CPM: $4-$7
   
   Por quê é bom:
   - Termo crescendo 250% (último ano)
   - Apenas 8 canais >100K no Brasil
   - Média 600K views nos tops
   - Nicho "quente" mas pouco explorado localmente

2. Mistérios Históricos Explicados (Score: 9.5/10) ⭐⭐⭐
   Demanda: ████████░░ Alta
   Competição: ████░░░░░░ Baixa-Média
   Viral: ████████░░ Alto
   CPM: $5-$9 (educação)
   
   Por quê é bom:
   - Conteúdo evergreen (nunca envelhece)
   - Audiência engajada (comments 5%+)
   - Monetização premium

3. Teorias da Conspiração Desmascaradas (Score: 9.3/10) ⭐⭐⭐
   Demanda: █████████░ Muito Alta
   Competição: ██████░░░░ Média
   Viral: ██████████ Extremo
   CPM: $2-$5
   
   Por quê é bom:
   - Viralidade comprovada (8M+ views possíveis)
   - Público fiel e ativo
   - Fácil gerar ideias infinitas

[... 7-10 continuam ...]

Digite número (1-10) para selecionar:
> 2

✅ Selecionado: "Mistérios Históricos Explicados"

Quer customizar algo?
  [1] Usar como está
  [2] Ajustar foco (ex: "só Brasil", "só crimes")
> 2

Como quer focar?
> Mistérios Históricos do Brasil Colonial

✅ Refinado para: "Mistérios Históricos do Brasil Colonial"
   Novo Score: 9.8/10 (nicho ultra-específico!)
```

#### **MODO 3: Híbrido**
```
Se escolher [3]:

Você digita tema amplo:
> História

IA sugere 5 sub-nichos dentro de "História":
  1. Mistérios Históricos (Score: 9.5)
  2. História Alternativa "E Se?" (Score: 8.9)
  3. Fatos Ocultos da História (Score: 9.2)
  4. Batalhas e Guerras Explicadas (Score: 7.8)
  5. Personagens Históricos Polêmicos (Score: 8.5)

Você escolhe ou refina mais:
> 1

Confirma "Mistérios Históricos"
```

---

### **2.2 Palavras-Chave (Auto-Geradas)**
```
Campo: nicho.keywords
Tipo: Array (auto-gerado, editável)

Gerado automaticamente baseado no nicho.
Usado para:
  - Pesquisa YouTube
  - Títulos SEO
  - Tags

Exemplo (Mistérios Não Resolvidos):
[
  "mistérios não resolvidos",
  "casos sem solução",
  "enigmas",
  "teorias",
  "investigação",
  "true crime",
  "casos misteriosos",
  "sem explicação"
]

Quer editar? [S/n]
> n
```

---

## 3. ESTILO VISUAL E IMAGENS

### **3.1 Preset de Estilo**
```
Campo: visual.preset
Tipo: Select

PRESETS DISPONÍVEIS:

[1] REALISTA ESCURO (Mistérios/Terror/Crime)
────────────────────────────────────────────
Preview: https://pollinations.ai/p/dark-cinematic...
Base: "dark cinematic photography"
Mood: Dramático, sombrio, tenso
Cores: Preto, azul escuro, cinza
Lighting: Low-key, shadows
Exemplos: True crime, mistérios, teorias

[2] PIXAR 3D (Infantil/Educativo/Leve)
────────────────────────────────────────────
Preview: https://pollinations.ai/p/pixar-style...
Base: "pixar 3d animation style"
Mood: Alegre, colorido, convidativo
Cores: Vibrantes, saturadas
Lighting: Volumétrico, suave
Exemplos: Kids, motivação, educação leve

[3] ANIME/MANGA (Fantasia/Stories/Reviews)
────────────────────────────────────────────
Preview: https://pollinations.ai/p/anime-style...
Base: "anime illustration, manga art"
Mood: Expressivo, estilizado
Cores: Vibrantes, contornos fortes
Exemplos: Histórias, fantasia, reviews

[4] MINIMALISTA (Negócios/Tech/Finanças)
────────────────────────────────────────────
Preview: https://pollinations.ai/p/minimalist...
Base: "minimalist design, clean"
Mood: Profissional, elegante
Cores: Tons neutros, acentos
Exemplos: Produtividade, tech, negócios

[5] FOTOGRÁFICO COLORIDO (Lifestyle/Viagens)
────────────────────────────────────────────
Preview: https://pollinations.ai/p/vibrant-photo...
Base: "vibrant photography, colorful"
Mood: Energético, positivo
Cores: Saturadas, quentes
Exemplos: Viagens, comida, lifestyle

[6] CYBERPUNK/FUTURISTA (Tech/Sci-Fi)
────────────────────────────────────────────
Preview: https://pollinations.ai/p/cyberpunk...
Base: "cyberpunk, neon, futuristic"
Mood: High-tech, urbano
Cores: Neon (rosa, azul, roxo)
Exemplos: Tech, futuro, sci-fi

[7] VINTAGE/RETRÔ (Nostalgia/História)
────────────────────────────────────────────
Preview: https://pollinations.ai/p/vintage...
Base: "vintage photography, retro"
Mood: Nostálgico, antigo
Cores: Sépia, lavados
Exemplos: História, nostalgia

[8] CUSTOMIZADO
────────────────────────────────────────────
Você define todos os parâmetros manualmente

Escolha (1-8):
> 1

✅ Preset: REALISTA ESCURO
```

---

### **3.2 Customização de Estilo**
```
(Se escolheu preset 1-7, pode pular)
(Se escolheu [8] CUSTOMIZADO:)

══════════════════════════════════════════
  CUSTOMIZAÇÃO DE ESTILO VISUAL
══════════════════════════════════════════

[1/7] Tom Geral:
  [1] Escuro/Sombrio
  [2] Claro/Luminoso
  [3] Neutro/Equilibrado
> 1

[2/7] Mood/Atmosfera:
  [1] Dramático/Tenso
  [2] Alegre/Positivo
  [3] Misterioso/Intrigante
  [4] Sério/Profissional
  [5] Fantástico/Mágico
> 3

[3/7] Estilo Artístico:
  [1] Fotorealista
  [2] Ilustração/Arte
  [3] 3D Renderizado
  [4] Minimalista/Flat
> 1

[4/7] Paleta de Cores Dominante:
  [1] Monocromático (tons de uma cor)
  [2] Análogo (cores próximas)
  [3] Complementar (cores opostas)
  [4] Vibrante (saturado)
  [5] Dessaturado (tons lavados)
> 2

Escolha cores base (máx 3):
  Digite cores separadas por vírgula:
> azul escuro, roxo, preto

[5/7] Iluminação:
  [1] High-key (muita luz)
  [2] Low-key (sombras)
  [3] Natural (balanceada)
  [4] Neon/Artificial
> 2

[6/7] Nível de Detalhe:
  ████░░ <- arraste ou digite 1-10
> 8 (muito detalhado)

[7/7] Referência Visual (opcional):
  Cole URL de imagem exemplo OU deixe vazio:
> https://exemplo.com/imagem-ref.jpg

Processando referência...
✅ Estilo capturado!

══════════════════════════════════════════
  PREVIEW DO ESTILO
══════════════════════════════════════════

Prompt Gerado:
"mysterious dark blue and purple photography, low-key lighting,
highly detailed, atmospheric, cinematic, moody, 8k, ultra realistic"

Negative Prompt:
"bright, cheerful, cartoon, low quality, blurry"

Gerando imagem teste...
✅ [IMAGEM PREVIEW AQUI]

Satisfeito? [S/n]
> S

✅ Estilo customizado salvo!
```

---

### **3.3 Provider de Imagens**
```
Campo: imagens.provider
Tipo: Select

Opções:
  [1] Pollinations.AI (Grátis, ilimitado)
  [2] Google Imagen (Pago, créditos)
  [3] Stable Diffusion Local (Grátis, precisa GPU)
  [4] Mix (Pollinations + retry Imagen se falhar)

Recomendado: [1] Pollinations
> 1
```

---

### **3.4 Quantidade e Duração de Imagens**
```
Campo: imagens.quantidade_modo
Tipo: Select

Opções:
  [1] Auto (baseado em duração do vídeo)
  [2] Fixo (sempre X imagens)
  [3] Min-Max (varia entre X e Y)

> 1 (Auto)

Duração por imagem:
  Muito rápido: 2-3s
  Rápido: 3-4s
  Normal: 4-5s ← Recomendado
  Lento: 6-8s
  Muito lento: 8-10s+

> Normal (4-5s)

✅ Configurado: ~10-12 imagens para vídeo de 3min
```

---

### **3.5 Transições**
```
Campo: imagens.transicoes
Tipo: Select

Opções:
  [1] Fade (dissolve suave)
  [2] Crossfade (sobreposição)
  [3] Slide (desliza)
  [4] Zoom (aproxima/afasta)
  [5] Sem transição (corte direto)
  [6] Mix aleatório

> 1 (Fade)

Duração da transição:
  0.3s (rápida)
  0.5s (normal) ← Recomendado
  0.8s (suave)
  1.0s (lenta)

> 0.5s
```

---

### **3.6 Efeitos Visuais**
```
Campo: imagens.efeitos
Tipo: Multiple Select

[ ] Ken Burns (zoom+pan lento)
[x] Vinheta (escurecimento bordas)
[ ] Film Grain (textura de filme)
[ ] Color Grading automático
[x] Estabilização
[ ] Slow Motion

Intensidade dos efeitos selecionados:
  Vinheta: ████░░░░░░ 40%
  Estabilização: ██████░░░░ 60%
```

---

## 4. CONFIGURAÇÃO DE ÁUDIO

### **4.1 Provider TTS**
```
Campo: audio.tts.provider
Tipo: Select

Opções:
  [1] Google Cloud TTS (1M chars grátis/mês)
  [2] ElevenLabs (Pago, premium)
  [3] Azure TTS (Pago)
  [4] New TTS Local (Grátis, precisa setup)
  [5] Voice Clone Custom (fornece sample 10s)

Recomendado: [1] Google Cloud
> 1
```

---

### **4.2 Configuração de Voz (Google TTS)**
```
(Se escolheu Google Cloud TTS:)

══════════════════════════════════════════
  SELEÇÃO DE VOZ NARRATIVA
══════════════════════════════════════════

Idioma: pt-BR (Português Brasil)

VOZES DISPONÍVEIS:

MASCULINAS:
────────────────────────────────────────
[1] pt-BR-Wavenet-B (Neural, Grave)
    Tom: Profundo, sério
    Idade percebida: 35-45 anos
    Voice Sample: [▶️ Ouvir 5s]
    Use Cases: Mistérios, documentários, narração dramática

[2] pt-BR-Neural2-B (Standard, Média)
    Tom: Neutro, claro
    Idade percebida: 28-35 anos
    Voice Sample: [▶️ Ouvir 5s]
    Use Cases: Educativo, tecnologia, notícias

[3] pt-BR-Standard-A (Studio, Jovem)
    Tom: Energético, dinâmico
    Idade percebida: 20-28 anos
    Voice Sample: [▶️ Ouvir 5s]
    Use Cases: Gaming, entretenimento jovem

FEMININAS:
────────────────────────────────────────
[4] pt-BR-Wavenet-C (Neural, Grave)
    Tom: Profunda, madura
    Idade percebida: 35-45 anos
    Voice Sample: [▶️ Ouvir 5s]
    Use Cases: Narração dramática, histórias sérias

[5] pt-BR-Neural2-A (Standard, Clara)
    Tom: Jovem, amigável
    Idade percebida: 22-30 anos
    Voice Sample: [▶️ Ouvir 5s]
    Use Cases: Educativo, lifestyle, tutoriais

[6] pt-BR-Wavenet-A (Premium, Suave)
    Tom: Calma, reconfortante
    Idade percebida: 30-40 anos
    Voice Sample: [▶️ Ouvir 5s]
    Use Cases: Meditação, audiobooks, narração suave

Escolha voz (1-6):
> 4

✅ Selecionado: pt-BR-Wavenet-C (Feminina Grave)
```

---

### **4.3 Ajustes Finos de Voz**
```
══════════════════════════════════════════
  AJUSTES DE VOZ
══════════════════════════════════════════

Voz base: pt-BR-Wavenet-C

[1] Velocidade (Speaking Rate):
    0.5x (muito lento)
    0.75x (lento)
    1.0x (normal) ← Atual
    1.25x (rápido)
    1.5x (muito rápido)
    
    ████████████████████░░░░░░░░░░ 1.0x
    <- arraste ou digite valor
    
> 0.95 (levemente mais lento, mais dramático)

[2] Tom/Pitch:
    -20 (muito grave)
    -10 (grave) ← Sugerido para Wavenet-C
    0 (normal)
    +10 (agudo)
    +20 (muito agudo)
    
    ████████████░░░░░░░░░░░░░░░░░░ -10
    
> -8

[3] Volume Gain:
    -10dB (muito baixo)
    0dB (normal) ← Padrão
    +10dB (alto)
    +16dB (muito alto)
    
    ████████████████░░░░░░░░░░░░░░ 0dB
    
> +2dB (levemente mais alto)

[4] Pausa Entre Frases:
    Curta: 0.3s
    Normal: 0.5s ← Padrão
    Longa: 0.8s
    Muito longa: 1.2s
    
> 0.6s (respiro natural)

Preview com ajustes:
[▶️ Ouvir texto teste: "Este é um mistério que nunca foi resolvido..."]

Satisfeito? [S/n]
> S

✅ Ajustes salvos!
```

---

### **4.4 Voice Clone Custom (Opcional)**
```
(Se escolheu [5] Voice Clone Custom no 4.1:)

══════════════════════════════════════════
  CLONE DE VOZ PERSONALIZADO
══════════════════════════════════════════

Você precisa fornecer:
  ✅ Áudio sample: 10-30 segundos
  ✅ Transcrição exata do áudio
  ✅ Qualidade: Sem ruído de fundo

Provider: New TTS Local (grátis, ilimitado)

[1] Fazer upload de áudio:
    Arraste arquivo MP3/WAV OU
    Grave agora (microfone)
    
> upload: minha_voz.mp3

Analisando áudio...
  Duração: 15s ✅
  Qualidade: 89/100 ✅
  Ruído de fundo: Baixo ✅
  
[2] Digite transcrição EXATA do áudio:
> Era uma vez uma história que ninguém conseguia explicar.
  Os fatos estavam todos lá, mas nada fazia sentido.

Validando transcrição...
✅ Match: 98% (excelente)

Gerando clone de voz...
⏳ Processando no New TTS (30-60s)...
✅ Clone pronto!

Preview clone:
[▶️ Ouvir: "Este é um teste da sua voz clonada"]

Satisfeito? [S/n]
> S

✅ Voz clonada salva!
   Voice ID: custom_voice_001
```

---

## 5. FORMATO DE VÍDEO

### **5.1 Duração**
```
Campo: video.duracao
Tipo: Range

Opções:
  [1] Shorts (15-60s)
  [2] Curtos (60-120s / 1-2min)
  [3] Médios (120-300s / 2-5min) ← Recomendado
  [4] Longos (300-600s / 5-10min)
  [5] Muito Longos (600s+ / 10min+)
  [6] Customizado (você define min-max)

> 3 (Médios)

Definir range exato:
  Mínimo: 120s (2min)
  Target: 180s (3min) ← Média desejada
  Máximo: 240s (4min)
  
Ajustar? [S/n]
> S

Min: 150s (2.5min)
Target: 180s (3min)
Max: 210s (3.5min)

✅ Configurado: 2.5-3.5min (média 3min)
```

---

### **5.2 Resolução e Qualidade**
```
Campo: video.resolucao
Tipo: Select

Opções:
  [1] 720p (HD) - Menor arquivo
  [2] 1080p (Full HD) - Padrão ← Recomendado
  [3] 1440p (2K) - Alta qualidade
  [4] 2160p (4K) - Máxima qualidade

> 2 (1080p)

Aspect Ratio:
  [1] 16:9 (Horizontal - YouTube padrão)
  [2] 9:16 (Vertical - Shorts/TikTok)
  [3] 1:1 (Quadrado - Instagram)
  [4] 4:5 (Vertical moderado - Instagram Feed)

> 1 (16:9)

Frame Rate (FPS):
  [1] 24fps (cinema)
  [2] 30fps (padrão) ← Recomendado
  [3] 60fps (super fluido)

> 2 (30fps)

Bitrate de Vídeo:
  [1] Baixo (3-5 Mbps) - Arquivo pequeno
  [2] Médio (5-8 Mbps) - Balanceado ← Recomendado
  [3] Alto (8-12 Mbps) - Máxima qualidade

> 2 (Médio)

✅ Configurado: 1080p 16:9 30fps 5-8Mbps
   Tamanho estimado: 40-60MB por vídeo de 3min
```

---

### **5.3 Codec e Formato**
```
Campo: video.codec
Tipo: Select (Avançado)

Codec de Vídeo:
  [1] H.264 (AVC) - Compatibilidade máximo ← Recomendado
  [2] H.265 (HEVC) - Menor arquivo, menos compatível
  [3] VP9 - Google (YouTube nativo)

> 1 (H.264)

Formato Container:
  [1] MP4 - Universal ← Recomendado
  [2] MKV - Flexível
  [3] WEBM - Web

> 1 (MP4)

✅ Codec: H.264/MP4
```

---

## 6. LEGENDAS E CAPTIONS

### **6.1 Ativar Legendas**
```
Campo: legendas.ativas
Tipo: Boolean

Legendas hardcoded (gravadas no vídeo)?
  [S] Sim (YouTube + outros)
  [N] Não (só YouTube upload SRT separado)

Recomendado: SIM (melhor para algorit mo)
> S
```

---

### **6.2 Estilo de Legendas**
```
Campo: legendas.estilo
Tipo: Select

Opções:

[1] PADRÃO (Frase completa)
────────────────────────────────────────
┌──────────────────────────────────────┐
│                                       │
│        Este é um grande mistério     │
│        que nunca foi resolvido       │
│                                       │
└──────────────────────────────────────┘

[2] WORD-BY-WORD HIGHLIGHT (Palavra destacada)
────────────────────────────────────────
┌──────────────────────────────────────┐
│                                       │
│    Este é um grande >>MISTÉRIO<<     │
│      que nunca foi resolvido          │
│                                       │
└──────────────────────────────────────┘
^ Atual palavra em cor diferente

[3] KARAOKE STYLE (Preenche enquanto fala)
────────────────────────────────────────
┌──────────────────────────────────────┐
│                                       │
│    Este é um grande mistério         │
│    ████████████░░░░░░░░░░░░░░░░       │
│                                       │
└──────────────────────────────────────┘
^ Barra progride com a fala

[4] TOP + BOTTOM (Duas linhas opostas)
────────────────────────────────────────
┌──────────────────────────────────────┐
│          Este é um grande             │
│                                       │
│                                       │
│       mistério não resolvido          │
└──────────────────────────────────────┘

[5] BOLD WORDS (Palavras-chave em negrito)
────────────────────────────────────────
┌──────────────────────────────────────┐
│    Este é um grande **MISTÉRIO**     │
│       que **NUNCA** foi resolvido     │
└──────────────────────────────────────┘

[6] SEM LEGENDAS
────────────────────────────────────────

Escolha (1-6):
> 2 (Word-by-word Highlight)

✅ Estilo: Palavra destacada em tempo real
```

---

### **6.3 Customização Visual**
```
══════════════════════════════════════════
  CUSTOMIZAÇÃO DE LEGENDAS
══════════════════════════════════════════

[1] Fonte:
    [1] Montserrat (moderna, clean)
    [2] Roboto (tech, legível)
    [3] Bebas Neue (display, impacto)
    [4] Arial Black (clássica, forte)
    [5] Oswald (condensada)
    [6] Impact (muito forte)
    
> 1 (Montserrat)

  Peso:
    Light / Regular / Bold / ExtraBold
  > Bold

[2] Tamanho:
    32px (pequeno)
    42px (médio)
    52px (grande) ← Recomendado
    62px (muito grande)
    Customizado
    
> 52px

[3] Cores:
    Texto principal: #FFFFFF (branco)
    Palavra destacada: #FFD700 (dourado)
    
    Quer mudar? [S/n]
    > S
    
    Texto principal:
      Digite HEX OU escolha preset:
      [1] #FFFFFF (Branco)
      [2] #FFFF00 (Amarelo)
      [3] #00FFFF (Ciano)
      [4] Custom
    > 1
    
    Palavra destacada:
      [1] #FFD700 (Dourado)
      [2] #FF0000 (Vermelho)
      [3] #00FF00 (Verde)
      [4] #FF00FF (Magenta)
      [5] Custom
    > 2 (Vermelho - mais impacto)

[4] Contorno/Sombra:
    [ ] Contorno preto (thickness: 2px)
    [x] Sombra preta (blur: 4px)
    [ ] Background box (semi-transparente)
    
    Opacidade sombra:
    ████████░░░░░░░░░░░░░░░░░░░░ 80%
    
> 80%

[5] Posição:
    [1] Superior
    [2] Centro
    [3] Inferior ← Padrão YouTube
    [4] Customizada (% da tela)
    
> 3 (Inferior)

  Margem inferior: 10% da altura
  Ajustar? (5-20%)
  > 12%

[6] Animação de Entrada:
    [1] Fade (aparecer suave)
    [2] Slide Up (desliza de baixo)
    [3] Pop (cresce rápido)
    [4] Sem animação (aparece direto)
    
> 1 (Fade)

  Duração: 0.2s


PREVIEW LEGENDA:
╔════════════════════════════════════════╗
║                                         ║
║                                         ║
║       Este é um >>MISTÉRIO<< que nunca ║
║            foi resolvido                ║
╚════════════════════════════════════════╝

Satisfeito? [S/n]
> S

✅ Legendas customizadas salvas!
```

---

## 7. MÚSICA E EFEITOS SONOROS

### **7.1 Música de Fundo**
```
Campo: audio.musica.ativa
Tipo: Boolean + Config

Adicionar música de fundo?
  [S] Sim
  [N] Não (só narração)

> S

Tipo de Música:
  [1] Ambiente/Suave (fundo discreto)
  [2] Intensa/Dramática (presença marcante)
  [3] Upbeat/Energética (ritmo alto)
  [4] Cinematic/Épica (orquestral)
  [5] Mix (varia por vídeo/momento)

> 1 (Ambiente/Suave)

Fonte:
  [1] YouTube Audio Library (grátis, livre)
  [2] Epidemic Sound (pago, U$ 15/mês)
  [3] Upload próprio (você fornece MP3s)
  [4] IA Generative (Suno.ai, grátis)

> 1 (YouTube Audio Library)

Tags/Mood da música:
  (Sistema busca automaticamente)
  
  Tags mapeadas do seu nicho:
  - mysterious
  - dark
  - ambient
  - tension
  - investigation
  
  Adicionar/remover tags? [S/n]
  > n

Volume da música:
  ████░░░░░░░░░░░░░░░░░░░░░░░░ 15%
  (Narração sempre 100%, música background)
  
  Ajustar (5-40%):
  > 18%

Fade-in/out:
  Início: Fade-in 2s
  Final: Fade-out 3s
  
  OK? [S/n]
  > S

✅ Música configurada: Ambient 18% volume
```

---

### **7.2 Efeitos Sonoros**
```
Campo: audio.efeitos_sonoros
Tipo: Multiple Select

Adicionar efeitos sonoros?
  [S] Sim
  [N] Não

> S

Quando usar SFX:
  [ ] Intro (whoosh, impact)
  [x] Momentos-chave (revelações)
  [ ] Transições (swoosh entre cenas)
  [x] Outro (final dramático)

Biblioteca:
  [1] Freesound.org (grátis)
  [2] YouTube Audio Library SFX
  [3] Upload próprio

> 2 (YouTube Audio Library)

Intensidade:
  [1] Sutil (baixo volume)
  [2] Moderado ← Recomendado
  [3] Intenso (high impact)

> 2

✅ SFX em momentos-chave + outro
```

---

## 8. ESTRATÉGIA DE PRODUÇÃO

### **8.1 Quantidade de Vídeos Teste**
```
Campo: producao.videos_teste
Tipo: Integer

MVP: Testar 5 eixos com X vídeos cada

Vídeos por eixo:
  [1] 1 vídeo/eixo = 5 total (mínimo)
  [2] 2 vídeos/eixo = 10 total (padrão)
  [3] 3 vídeos/eixo = 15 total (agressivo)
  [4] Custom

> 2 (Padrão: 10 vídeos total)

✅ Produção inicial: 10 vídeos (2 por eixo)
```

---

### **8.2 Modelo de Ideias**
```
Campo: producao.gerador_ideias
Tipo: Config

Quantidade de ideias geradas:
  (Sistema gera 30 ideias/eixo = 150 total)
  
  Destas 150, quantas produzir agora?
  > 10 (as Top 10 por score)

Critério de seleção:
  [x] Score viral (IA predição)
  [x] Unicidade (não muito similar)
  [ ] Facilidade produção
  [x] Potencial SEO

✅ Produzir Top 10 ideias (score + único + SEO)
```

---

### **8.3 Frequência de Upload**
```
Campo: producao.frequencia_upload
Tipo: Select

Após produzir vídeos, upload no YouTube:
  [1] Todos de uma vez (batch)
  [2] Diário (1/dia)
  [3] Dia sim, dia não
  [4] 3x por semana
  [5] Manual (você decide)

> 2 (Diário)

Horário preferido:
  [1] Manhã (6-9h)
  [2] Almoço (11-14h)
  [3] Tarde (15-18h)
  [4] Noite (19-22h)
  [5] Madrugada (0-3h)

> 4 (Noite 19-22h)

  Horário exato:
  > 20:00 (8pm)

✅ Upload: 1 vídeo/dia às 20h
```

---

## 9. CONFIGURAÇÕES DE UPLOAD (YOUTUBE)

### **9.1 Metadados Padrão**
```
Campo: youtube.metadata
Tipo: Templates

[1] Descrição Template:
────────────────────────────────────────
{video_titulo}

{video_resumo}

🔔 INSCREVA-SE: {canal_url}

📱 REDES SOCIAIS:
Instagram: {instagram}
TikTok: {tiktok}

#MistériosNãoResolvidos #TrueCrime #Enigmas

──────────────────────────────────────

Editar template? [S/n]
> n

[2] Tags Padrão:
────────────────────────────────────────
Auto-geradas do nicho:
  - mistérios não resolvidos
  - casos sem solução
  - enigmas
  - teorias
  - true crime brasil
  
  + Tags específicas por vídeo (IA adiciona)

Máximo: 15 tags
Adicionar tags fixas? [S/n]
> S

Adicionar:
> investigação, crime, brasil

✅ Tags: Nicho (5) + Custom (3) + Por-vídeo (7)

[3] Categoria:
────────────────────────────────────────
  [1] Filme e Animação
  [ 2] Automóveis e Veículos
  [3] Música
  [4] Animais
  [5] Esportes
  [6] Viagem e Eventos
  [7] Jogos
  [8] Pessoas e Blogs
  [9] Comédia
  [10] Entretenimento ← Sugerido para Mistérios
  [11] Notícias e Política
  [12] Instrução e Estilo
  [13] Ciência e Tecnologia
  [14] Cinema e Entretenimento
  
> 10 (Entretenimento)

[4] Privacidade Padrão:
────────────────────────────────────────
  [1] Privado (você publica manual)
  [2] Não-listado (só com link)
  [3] Público (automático)
  [4] Agendado (seguir frequência config)

> 4 (Agendado - 20h diário)

✅ Upload automático agendado: 20h/dia
```

---

### **9.2 Thumbnail Automático**
```
Campo: youtube.thumbnail
Tipo: Config

Gerar thumbnail automaticamente?
  [S] Sim (IA cria)
  [N] Não (manual)

> S

Estilo de Thumbnail:
  [1] Frame do vídeo + título
  [2] Imagem customizada + título
  [3] Composição (múltiplas imagens)
  [4] Minimalista (só texto)

> 2 (Imagem + título)

Elementos:
  [x] Título do vídeo (grande)
  [x] Imagem de fundo
  [ ] Sua foto/avatar
  [x] Número do episódio (se série)
  [ ] Logo do canal

Fonte título:
  [1] Impact (clássico YouTube)
  [2] Bebas Neue (moderna)
  [3] Montserrat Bold
  
> 1 (Impact)

Cores título:
  Stroke (contorno): #FFFFFF (branco) ou #000000 (preto)?
  Fill (preenchimento): #FFFF00 (amarelo) ou custom?
  
  Usar amarelo + contorno preto (padrão)?
  > S

✅ Thumbnail: Auto-gerado, Impact, Amarelo/Preto
```

---

## 10. ANÁLISE E MÉTRICAS

### **10.1 Rastreamento de Performance**
```
Campo: analytics.tracking
Tipo: Boolean + Config

Ativar análise automática de métricas?
  [S] Sim (recomendado)
  [N] Não

> S

Frequência de coleta:
  [1] Tempo real (a cada hora)
  [2] Diária (1x/dia)
  [3] Semanal

> 2 (Diária)

Métricas rastreadas:
  [x] Views
  [x] Watch Time
  [x] CTR (Click-Through Rate)
  [x] AVD (Average View Duration)
  [x] Retention (%)
  [x] Likes/Dislikes
  [x] Comments
  [x] Shares
  [ ] Receita (AdSense)

✅ Analytics ativo: Coleta diária
```

---

### **10.2 Agente Maré (Identificação de Eixo Vencedor)**
```
Campo: mare.config
Tipo: Config

Quando executar Análise de Maré?
  [1] Após 5 vídeos postados
  [2] Após 7 dias
  [3] Após 10 vídeos
  [4] Manual

> 2 (Após 7 dias - 1 semana de dados)

Critério de "Eixo Vencedor":
  Peso das métricas:
  
  Views: ████████░░ 40%
  Retention: ██████░░░░ 30%
  CTR: ████░░░░░░ 20%
  Comments: ██░░░░░░░░ 10%
  
  Ajustar pesos? [S/n]
  > n

Ação após identificar vencedor:
  [x] Notificar você
  [ ] Auto-produzir 10 vídeos do eixo
  [x] Sugerir próximos passos

✅ Maré: Após 7 dias, notifica + sugere
```

---

## 11. CONFIGURAÇÕES AVANÇADAS

### **11.1 Modo Debug**
```
Campo: system.debug
Tipo: Boolean

Ativar logs detalhados?
  [S] Sim (recomendado para MVP)
  [N] Não

> S

Nível de log:
  [1] ERROR (só erros)
  [2] WARNING (avisos)
  [3] INFO (informativo) ← Recomendado
  [4] DEBUG (tudo)

> 3 (INFO)

Salvar logs em arquivo?
  [S] Sim (logs/producao.log)
  [N] Não

> S

✅ Debug ativo: INFO level, salvo em arquivo
```

---

### **11.2 Backup e Recovery**
```
Campo: system.backup
Tipo: Config

Backup automático:
  [x] Config do canal (config.json)
  [x] Todos os deliverables (CSVs, JSONs)
  [x] Vídeos finais (.mp4)
  [ ] Assets temporários

Frequência:
  [1] Após cada agente
  [2] Diariamente
  [3] Semanalmente

> 1 (Após cada agente - máxima segurança)

Local de backup:
  [1] Google Drive
  [2] Dropbox
  [3] Local (pasta no PC)
  [4] Supabase

> 3 (Local por enquanto)

  Pasta: D:\Backups\Incubadora
  
✅ Backup: Auto após cada etapa, local
```

---

### **11.3 Modo Batch vs Individual**
```
Campo: system.modo_producao
Tipo: Select

Como produzir vídeos:
  [1] Batch (gera todos de uma vez)
      Vantagem: Mais rápido
      Desvantagem: Trava se erro em 1
      
  [2] Individual (1 de cada vez, salva progresso)
      Vantagem: Recupera de erros
      Desvantagem: Um pouco mais lento
      
  [3] Hybrid (batch de 5, depois checkpoint)

Recomendado: [2] Individual (anti-travamento)
> 2

✅ Modo: Individual com checkpoints
```

---

## 📋 RESUMO FINAL DA CONFIGURAÇÃO

```
══════════════════════════════════════════════════════════
  📊 PERFIL COMPLETO DO CANAL
══════════════════════════════════════════════════════════

🎬 CANAL:
  Nome: Mistérios Proibidos
  Idioma: pt-BR
  Público: Adultos 25-44, Mistérios/True Crime

🎯 NICHO:
  Modo: IA Sugestão
  Tema: Mistérios Históricos do Brasil Colonial
  Score: 9.8/10 ⭐⭐⭐
  
🎨 VISUAL:
  Preset: Realista Escuro
  Provider: Pollinations.AI
  Imagens/vídeo: 10-12 (auto, 4-5s cada)
  Transições: Fade 0.5s
  Efeitos: Vinheta + Estabilização

🎙️ ÁUDIO:
  TTS: Google Cloud (pt-BR-Wavenet-C)
  Tom: Feminino Grave
  Ajustes: 0.95x velocidade, -8 pitch
  Música: Ambiente 18% volume (YouTube Library)
  SFX: Momentos-chave + Outro

📹 VÍDEO:
  Duração: 2.5-3.5min (target 3min)
  Resolução: 1080p 16:9 30fps
  Codec: H.264/MP4
  Qualidade: 5-8 Mbps

💬 LEGENDAS:
  Estilo: Word-by-Word Highlight
  Fonte: Montserrat Bold 52px
  Cores: Branco + Vermelho destaque
  Posição: Inferior 12%

📊 PRODUÇÃO:
  Vídeos teste: 10 (2 por eixo)
  Upload: Diário 20:00h
  Análise Maré: Após 7 dias

🔧 SISTEMA:
  Debug: INFO level
  Backup: Auto após cada etapa
  Modo: Individual (anti-travamento)

══════════════════════════════════════════════════════════

Salvar esta configuração? [S/n]
> S

Salvando em: canais/misterios_proibidos/config.json
✅ Configuração salva!

═══════════════════════════════════════════════════════════
  🚀 PRONTO PARA PRODUZIR!
  
  Próximo comando:
    python incubadora.py --canal misterios_proibidos --produzir
    
  Tempo estimado: 4-6 horas (10 vídeos)
═══════════════════════════════════════════════════════════
```

---

**Total de Campos Configuráveis**: **87 campos**  
**Tempo de Configuração**: 10-15 minutos (com leitura)  
**Salvamento**: Automático em `canais/{slug}/config.json`  
**Reutilização**: 100% (nunca pergunta de novo!)
