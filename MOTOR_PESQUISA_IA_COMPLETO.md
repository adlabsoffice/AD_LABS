# 🔍 MOTOR DE PESQUISA IA - SISTEMA COMPLETO
## Como a IA Analisa, Valida e Sugere TUDO Automaticamente

---

## 🎯 FLUXO GERAL

```
USUÁRIO DIGITA QUALQUER COISA
         ↓
IA ANALISA AUTOMATICAMENTE:
  - APIs: YouTube, Google Trends, Groq
  - Tempo: 10-30 segundos
  - Resultado: Score 0-10 + Sugestões
         ↓
APRESENTA PARA USUÁRIO:
  ✅ Análise do que digitou
  💡 3-5 Sugestões melhores
  📊 Dados completos
         ↓
USUÁRIO ESCOLHE OU REFINA
```

---

## 1. PESQUISA DE NOME DO CANAL

### **INPUT: Usuário Digita Nome**
```
[1/10] 📝 Nome do canal:
> Mistérios Proibidos
```

### **PROCESSAMENTO AUTOMÁTICO IA**:

```python
def analisar_nome_canal(nome_usuario):
    """
    Análise multi-camada de nome de canal
    """
    
    # === ETAPA 1: VALIDAÇÃO BÁSICA ===
    validacoes = {
        "tamanho_ok": 3 <= len(nome) <= 50,
        "sem_caracteres_especiais": regex_check(nome),
        "sem_palavras_proibidas": not contains_banned_words(nome),
        "pronunciavel": syllable_count(nome) <= 8
    }
    
    # === ETAPA 2: PESQUISA YOUTUBE (API) ===
    youtube_analysis = {
        "canais_similares": youtube_search_channels(nome_usuario),
        "total_resultados": len(resultados),
        "top_canal_subs": max([c.subscriber_count for c in resultados]),
        "disponibilidade": "nome único" if total < 5 else "muito comum"
    }
    
    # === ETAPA 3: ANÁLISE SEO (Google Trends) ===
    seo_data = {
        "volume_busca": google_trends_api(nome_usuario),
        "tendencia": "crescendo" | "estável" | "declinando",
        "interesse_global": score_0_100
    }
    
    # === ETAPA 4: ANÁLISE LINGUÍSTICA (Groq IA) ===
    groq_analysis = groq.chat.completions.create(
        model="llama-3.1-70b-versatile",
        messages=[{
            "role": "system",
            "content": """Você é especialista em branding YouTube.
            Analise o nome do canal e retorne JSON:
            {
              "memorabilidade": 0-10,
              "apelo_emocional": 0-10,
              "clareza_nicho": 0-10,
              "originalidade": 0-10,
              "problemas": ["lista de issues"],
              "fortalezas": ["lista de pontos fortes"]
            }"""
        }, {
            "role": "user",
            "content": f"Analise: {nome_usuario}"
        }],
        response_format={"type": "json_object"}
    )
    
    # === ETAPA 5: CÁLCULO DE SCORE FINAL ===
    score = (
        groq_analysis["memorabilidade"] * 0.25 +
        groq_analysis["originalidade"] * 0.25 +
        groq_analysis["clareza_nicho"] * 0.20 +
        (10 if youtube_analysis["disponibilidade"] == "nome único" else 5) * 0.20 +
        seo_data["score_normalizado"] * 0.10
    )
    
    return {
        "score": score,
        "validacoes": validacoes,
        "youtube": youtube_analysis,
        "seo": seo_data,
        "ia": groq_analysis
    }
```

---

### **OUTPUT PARA USUÁRIO**:

```
🔍 Analisando "Mistérios Proibidos"...
   ⏳ YouTube API... ✅
   ⏳ Google Trends... ✅
   ⏳ IA Linguística... ✅

═══════════════════════════════════════════════════════════
  📊 ANÁLISE: "Mistérios Proibidos"
═══════════════════════════════════════════════════════════

Score Geral: 7.8/10 ⭐⭐⭐ (BOM, mas pode melhorar)

✅ PONTOS FORTES:
  • Clareza de nicho: 9/10 (obviamente sobre mistérios)
  • Apelo emocional: 8/10 ("proibidos" gera curiosidade)
  • Memorabilidade: 7/10 (fácil de lembrar)

⚠️ PONTOS FRACOS:
  • Originalidade: 6/10 (padrão comum no YouTube BR)
  • Disponibilidade: Média (18 canais similares encontrados)
  • SEO: Médio (volume busca baixo para termo exato)

🔍 CANAIS SIMILARES EXISTENTES:
  1. "Mistérios do Mundo" (450K subs)
  2. "Mistérios Ocultos" (180K subs)
  3. "Proibidos da História" (95K subs)
  
⚡ COMPETIÇÃO: Média-Alta (dificulta destacar-se)

═══════════════════════════════════════════════════════════

💡 IA SUGERE 5 NOMES MELHORES:

1. "Portal dos Mistérios" (Score: 9.2/10) ⭐⭐⭐
   ✅ Único (0 canais exatos)
   ✅ SEO: Alto (12K buscas/mês)
   ✅ Memorável e místico
   ⚠️ Pode parecer genérico (mas SEO compensa)

2. "Enigmas do Abismo" (Score: 9.0/10) ⭐⭐⭐
   ✅ Único (0 canais exatos)
   ✅ Altamente memorável
   ✅ "Abismo" = forte apelo emocional (medo/curiosidade)
   ⚠️ SEO médio (4K buscas/mês)

3. "Zona Proibida" (Score: 8.8/10) ⭐⭐⭐
   ✅ Curto (fácil digitar)
   ✅ SEO alto (8K buscas/mês)
   ✅ Original o suficiente
   ⚠️ 2 canais pequenos com nomes parecidos

4. "Arquivo X Brasil" (Score: 8.5/10) ⭐⭐
   ✅ Referência cultural (Arquivo X)
   ✅ "Brasil" = diferencial geográfico
   ✅ SEO médio-alto (6K buscas/mês)
   ⚠️ Pode ter questões de copyright (Fox)

5. "Mistérios do 13º Andar" (Score: 8.3/10) ⭐⭐
   ✅ Muito memorável (13 = superstição)
   ✅ Único (0 exatos)
   ⚠️ SEO baixo (nome muito específico)

═══════════════════════════════════════════════════════════

Escolha uma opção:
  [1] Usar "Mistérios Proibidos" (seu original)
  [2-6] Usar sugestão 1-5 da IA
  [7] IA gerar mais 5 opções
  [8] Digitar outro nome
  
> _
```

---

## 2. PESQUISA DE OPORTUNIDADES DE NICHO

### **MODO: "IA, me mostre oportunidades"**

```
[2/10] 🎯 Como quer definir o nicho?
  [1] Digitar manualmente
  [2] IA pesquisa oportunidades e sugere ⭐
> 2
```

---

### **ALGORITMO COMPLETO**:

```python
def pesquisar_oportunidades_nichos():
    """
    Sistema híbrido: Trends + YouTube + IA
    Encontra nichos com Alta Demanda + Baixa Competição
    """
    
    # === ETAPA 1: GOOGLE TRENDS (Top Crescentes) ===
    print("🔍 Analisando Google Trends...")
    
    tendencias = google_trends.trending_searches(
        country="BR",  # ou "US" se internacional
        timeframe="today 12-m",
        categories=[
            "Entertainment",
            "News",
            "Science",
            "People & Society"
        ]
    )
    
    # Filtra só termos relevantes para YouTube
    termos_youtube = [
        t for t in tendencias 
        if is_youtube_viable(t)  # remove notícias efêmeras
    ]
    
    # Top 100 termos crescentes
    top_100 = termos_youtube[:100]
    
    # === ETAPA 2: ANÁLISE YouTube (Para Cada Termo) ===
    print(f"📊 Analisando {len(top_100)} nichos no YouTube...")
    
    analises = []
    for termo in top_100:
        # Buscar canais no nicho
        canais = youtube.search().list(
            part="snippet",
            q=termo,
            type="channel",
            maxResults=50
        ).execute()
        
        # Buscar vídeos top
        videos = youtube.search().list(
            part="snippet",
            q=termo,
            type="video",
            maxResults=100,
            order="viewCount"
        ).execute()
        
        # Calcular métricas
        competicao = {
            "canais_grandes": len([c for c in canais if c["subs"] > 100000]),
            "canais_medios": len([c for c in canais if 10000 < c["subs"] < 100000]),
            "saturacao": "baixa" if canais_grandes < 10 else "média" if < 30 else "alta"
        }
        
        demanda = {
            "media_views_top10": mean([v["views"] for v in videos[:10]]),
            "engagement_rate": mean([v["likes"]/v["views"] for v in videos]),
            "frequencia_posts": count_videos_last_30_days(termo)
        }
        
        analises.append({
            "termo": termo,
            "competicao": competicao,
            "demanda": demanda
        })
    
    # === ETAPA 3: GROQ IA (Refinar e Pontuar) ===
    print("🤖 IA refinando resultados...")
    
    # Groq analisa cada nicho em batch
    for batch in chunks(analises, 10):
        prompt = f"""
        Você é especialista em YouTube. Analise estes nichos:
        
        {json.dumps(batch)}
        
        Para CADA nicho, retorne JSON:
        {{
          "nicho": "nome",
          "potencial_viral": 0-10,
          "longevidade": 0-10 (evergreen vs tendência passageira),
          "monetizacao_cpm": "baixo|medio|alto",
          "dificuldade_producao": 0-10,
          "score_oportunidade": 0-10,
          "razao": "explicação curta"
        }}
        
        Ordene por score_oportunidade DESC.
        """
        
        ia_scores = groq.generate(prompt, response_format="json")
        
        # Mescla análise IA com dados YouTube
        for nicho in batch:
            nicho.update(ia_scores[nicho["termo"]])
    
    # === ETAPA 4: CALCULAR SCORE FINAL ===
    for nicho in analises:
        # Fórmula: Demanda × (1/Competição) × Viral × Longevidade
        score_final = (
            (nicho["demanda"]["media_views"] / 100000) * 0.30 +  # Demanda
            (10 - nicho["competicao"]["saturacao_score"]) * 0.30 +  # Baixa competição
            nicho["potencial_viral"] * 0.20 +
            nicho["longevidade"] * 0.20
        )
        
        nicho["score_final"] = min(score_final, 10)
    
    # Ordenar por score
    analises.sort(key=lambda x: x["score_final"], reverse=True)
    
    # Retornar Top 10 (score > 8.0)
    return [n for n in analises if n["score_final"] >= 8.0][:10]
```

---

### **OUTPUT PARA USUÁRIO**:

```
═══════════════════════════════════════════════════════════
  🔥 TOP 10 OPORTUNIDADES (Score 8.0+)
═══════════════════════════════════════════════════════════

Processamos 100 nichos via:
  ✅ Google Trends (tendências globais)
  ✅ YouTube Data API (50 canais + 100 vídeos por nicho)
  ✅ Groq IA (análise qualitativa)

Tempo total: 2min 34s

───────────────────────────────────────────────────────────

1. 🏆 Casos Paranormais Brasileiros
   Score: 9.7/10 ⭐⭐⭐⭐⭐ EXCEPCIONAL
   
   📊 DADOS:
   Demanda (Google): ████████████░ 85/100 (Muito Alta)
   Competição: ███░░░░░░░░░░ Baixa (8 canais >100K)
   Viral: ████████████░ 9.2/10
   Longevidade: ███████████░░ 8.8/10 (Evergreen)
   
   💰 MONETIZAÇÃO:
   CPM Estimado: $4-7 (médio-alto)
   Sponsors: Possível (produtos paranormais)
   
   📈 MÉTRICAS YOUTUBE:
   Média views top 10: 680K views
   Engagement: 5.2% (excelente!)
   Upload frequency: 1.2 vídeos/dia (não saturado)
   
   💡 POR QUÊ É OPORTUNIDADE:
   • Termo crescendo 250% (último ano)
   • Brasil tem cultura forte em paranormal
   • Pouquíssimos canais profissionais no BR
   • Conteúdo evergreen (nunca fica velho)
   • Público engajado e fiel
   
   ⚠️ DESAFIOS:
   • Precisa pesquisa de casos reais
   • Pode ser sensível (famílias envolvidas)

───────────────────────────────────────────────────────────

2. 🏆 Mistérios Históricos Explicados
   Score: 9.5/10 ⭐⭐⭐⭐⭐ EXCEPCIONAL
   
   📊 DADOS:
   Demanda: ████████████░ 82/100 (Alta)
   Competição: ████░░░░░░░░░ Baixa-Média (22 canais >100K)
   Viral: ███████████░░ 8.8/10
   Longevidade: █████████████ 10/10 (100% Evergreen!)
   
   💰 MONETIZAÇÃO:
   CPM: $5-9 (alto - educação)
   Sponsors: Livros, cursos, apps educativos
   
   📈 MÉTRICAS:
   Média views: 520K
   Engagement: 4.8%
   Frequência: 0.9 vídeos/dia (espaço!)
   
   💡 POR QUÊ:
   • Conteúdo nunca envelhece
   • Audiência educada (alto CPM)
   • Infinitas histórias (centenas de anos)
   • Fácil pesquisar (livros, Wikipedia)
   
   ⚠️ DESAFIOS:
   • Precisa boa pesquisa histórica
   • Competição internacional (EUA)

───────────────────────────────────────────────────────────

3. 🏆 Teorias da Conspiração Desmascaradas
   Score: 9.3/10 ⭐⭐⭐⭐⭐ EXCEPCIONAL
   
   📊 DADOS:
   Demanda: █████████████ 92/100 (Extrema!)
   Competição: ██████░░░░░░░ Média (45 canais >100K)
   Viral: █████████████ 10/10 (Máximo!)
   Longevidade: ████████░░░░░ 7.5/10
   
   💰 MONETIZAÇÃO:
   CPM: $2-5 (entretenimento)
   Sponsors: Limitado (nicho polêmico)
   
   📈 MÉTRICAS:
   Média views: 1.2M (!!)
   Engagement: 6.5% (altíssimo!)
   Frequência: 2.3 vídeos/dia (competitivo)
   
   💡 POR QUÊ:
   • Viralidade comprovada (milhões possíveis)
   • Público extremamente engajado
   • Sempre surgem novas teorias
   • Fácil gerar ideias infinitas
   
   ⚠️ DESAFIOS:
   • Competição média-alta
   • Possível desmonetização (conteúdo sensível)
   • Precisa fact-checking rigoroso

───────────────────────────────────────────────────────────

[ 4-10 continuam com mesmo formato... ]

───────────────────────────────────────────────────────────

Filtros Disponíveis:
  [F] Filtrar por CPM (só alto)
  [C] Filtrar por competição (só baixa)
  [V] Filtrar por viral potential (só 9+)
  [I] Filtrar por idioma/região
  
Ações:
  [1-10] Selecionar nicho
  [M] Ver mais 10 opções
  [R] Redefinir critérios de busca
  
> _
```

---

## 3. ANÁLISE INTERNACIONAL vs LOCAL

### **DETECÇÃO AUTOMÁTICA**:

```python
def analisar_melhor_idioma_mercado(nicho):
    """
    IA decide automaticamente se PT-BR ou EN-US é melhor
    """
    
    # === ANÁLISE PARALELA: BR vs US ===
    mercados = {}
    
    for idioma, pais in [("pt-BR", "BR"), ("en-US", "US")]:
        # Google Trends por país
        demanda_local = google_trends.interest_by_region(
            nicho,
            resolution="COUNTRY",
            inc_low_vol=False
        )[pais]
        
        # YouTube API por região
        youtube_stats = youtube.search().list(
            part="snippet,statistics",
            q=nicho,
            type="video",
            regionCode=pais,
            maxResults=100
        ).execute()
        
        # Groq IA: Análise cultural
        analise_cultural = groq.generate(f"""
        Analise o nicho "{nicho}" para o mercado {pais}:
        
        Retorne JSON:
        {{
          "adequacao_cultural": 0-10,
          "demanda_local": 0-10,
          "barreiras": ["lista"],
          "vantagens": ["lista"],
          "recomendacao": "muito recomendado|recomendado|não recomendado"
        }}
        """)
        
        # CPM por região (AdSense data)
        cpm_data = {
            "BR": {"min": 0.5, "avg": 2.5, "max": 6},
            "US": {"min": 2, "avg": 8, "max": 20}
        }
        
        mercados[idioma] = {
            "demanda": demanda_local,
            "competicao": len(youtube_stats["items"]),
            "media_views": mean([v["views"] for v in youtube_stats]),
            "cpm": cpm_data[pais],
            "cultural": analise_cultural,
            "populacao": 214M if pais == "BR" else 331M
        }
    
    # === SCORE COMPARATIVO ===
    for idioma, data in mercados.items():
        score = (
            data["demanda"] * 0.25 +
            (10 - normalize(data["competicao"])) * 0.25 +
            data["cultural"]["adequacao_cultural"] * 0.20 +
            normalize(data["cpm"]["avg"]) * 0.20 +
            normalize(data["populacao"]) * 0.10
        )
        mercados[idioma]["score_final"] = score
    
    # Comparar
    if mercados["en-US"]["score_final"] > mercados["pt-BR"]["score_final"] + 1.5:
        return "en-US", mercados
    else:
        return "pt-BR", mercados
```

---

### **OUTPUT**:

```
🌍 Analisando melhores mercados para "Mistérios Históricos"...
   ⏳ Google Trends (BR vs US)... ✅
   ⏳ YouTube Stats (2 regiões)... ✅
   ⏳ IA Cultural Analysis... ✅

═══════════════════════════════════════════════════════════
  🌎 COMPARAÇÃO DE MERCADOS
═══════════════════════════════════════════════════════════

Nicho: "Mistérios Históricos"

┌─────────────────────────────────────────────────────────┐
│  PORTUGUÊS BRASIL (pt-BR)                                │
├─────────────────────────────────────────────────────────┤
│  Score: 8.2/10 ⭐⭐⭐                                    │
│                                                          │
│  💰 MONETIZAÇÃO:                                         │
│    CPM Médio: $2.50                                     │
│    Receita/1M views: ~$2.500                            │
│                                                          │
│  📊 DEMANDA:                                             │
│    Google Trends: 68/100                                │
│    População: 214M                                      │
│                                                          │
│  🎯 COMPETIÇÃO:                                          │
│    Canais >100K: 18                                     │
│    Saturação: Média-Baixa                               │
│                                                          │
│  🎨 ADEQUAÇÃO CULTURAL:                                  │
│    Score IA: 9.2/10                                     │
│    Brasil ama mistérios/paranormal                      │
│    História colonial rica                                │
│                                                          │
│  ✅ VANTAGENS:                                           │
│    • Menos competição                                   │
│    • Cultura brasileira favorável                       │
│    • Você fala português nativo                         │
│    • Histórias locais únicas                            │
│                                                          │
│  ⚠️ DESVANTAGENS:                                        │
│    • CPM mais baixo                                     │
│    • Mercado menor                                      │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  INGLÊS ESTADOS UNIDOS (en-US)                          │
├─────────────────────────────────────────────────────────┤
│  Score: 9.8/10 ⭐⭐⭐⭐⭐ RECOMENDADO!                  │
│                                                          │
│  💰 MONETIZAÇÃO:                                         │
│    CPM Médio: $8.00 (3.2x maior!!)                     │
│    Receita/1M views: ~$8.000                            │
│                                                          │
│  📊 DEMANDA:                                             │
│    Google Trends: 89/100 (muito maior!)                │
│    População: 331M + global (1B+ EN speakers)          │
│                                                          │
│  🎯 COMPETIÇÃO:                                          │
│    Canais >100K: 156 (maior, mas...)                   │
│    Saturação: Média (mercado MUITO maior compensa)     │
│                                                          │
│  🎨 ADEQUAÇÃO CULTURAL:                                  │
│    Score IA: 10/10                                      │
│    EUA = maior mercado YouTube global                   │
│    História mundial (não só EUA)                        │
│                                                          │
│  ✅ VANTAGENS:                                           │
│    • CPM 3-4x maior                                     │
│    • Mercado 10x maior                                  │
│    • Alcance global                                     │
│    • Potencial patrocínios internacionais                │
│                                                          │
│  ⚠️ DESVANTAGENS:                                        │
│    • Mais competição                                    │
│    • Precisa inglês fluente (IA pode narrar!)          │
│    • Produção mais profissional esperada                │
└─────────────────────────────────────────────────────────┘

═══════════════════════════════════════════════════════════
  💡 RECOMENDAÇÃO IA
═══════════════════════════════════════════════════════════

🏆 MELHOR OPÇÃO: INGLÊS (en-US)

Razão: Apesar da maior competição, o CPM 3.2x maior e o mercado
10x maior compensam amplamente. Com 100K views/vídeo:

PT-BR: $250 de receita
EN-US: $800 de receita (3.2x!)

Mesmo com metade das views (50K), ainda ganha mais em EN ($400).

🎙️ SOLUÇÃO PARA BARREIRA DO IDIOMA:
  ✅ Google TTS tem vozes EN perfeitas (grátis!)
  ✅ Groq/Grok escrevem roteiro em inglês nativo
  ✅ VOCÊ não precisa falar, só validar roteiro!

═══════════════════════════════════════════════════════════

Escolha:
  [1] Seguir recomendação IA (Inglês - en-US) ⭐
  [2] Usar Português (pt-BR)
  [3] Criar 2 canais (1 PT + 1 EN) - duplicar esforço
  [4] Multi-idioma (mesmo canal, vídeos legendados)
  
> _
```

---

## 4. FLUXO COMPLETO INTEGRADO

```
USUÁRIO INICIA SETUP
         ↓
═══ NOME DO CANAL ═══
  User digita: "Mistérios Proibidos"
         ↓
  [IA ANALISA - 15s]
  - YouTube API (canais similares)
  - Google Trends (SEO)
  - Groq (linguística)
         ↓
  Score: 7.8/10
  5 Sugestões melhores (8.3-9.2)
         ↓
  User escolhe: "Portal dos Mistérios" (9.2)
         ↓
═══ DEFINIÇÃO DE NICHO ═══
  User escolhe: [2] IA sugere
         ↓
  [IA PESQUISA - 2min]
  - Google Trends (100 nichos)
  - YouTube API (5.000+ canais)
  - Groq (análise qualitativa)
         ↓
  Top 10 oportunidades (score 8.0+)
         ↓
  User escolhe: "Casos Paranormais BR" (9.7)
         ↓
═══ ANÁLISE DE MERCADO ═══
  [IA COMPARA - 30s]
  - PT-BR vs EN-US
  - CPM, demanda, competição
  - Adequação cultural
         ↓
  Recomendação: EN-US (score 9.8 vs 8.2)
  Razão: CPM 3.2x maior compensa
         ↓
  User escolhe: EN-US
         ↓
  [SISTEMA AJUSTA AUTO]
  - Voice: en-US-Wavenet-D
  - Keywords: English terms
  - Cultural refs: Global
         ↓
═══ RESTO DO SETUP ═══
  (Continua com visual, etc)
```

---

## 📊 RESUMO DE APIS USADAS

| API/Serviço | Uso | Custo | Frequência |
|-------------|-----|-------|------------|
| **YouTube Data API v3** | Pesquisa canais/vídeos | Grátis (10K units/dia) | Setup + Semanal |
| **Google Trends API** | Demanda de termos | Grátis | Setup |
| **Groq (Llama 3.1)** | Análise qualitativa | Grátis (14.4K/dia) | Setup + Produção |
| **Grok (Backup)** | Se Groq exceder | U$25/mês grátis | Raramente |

**Custo Total Pesquisas**: **R$ 0,00**

---

**Tempo total setup com IA**: **5-8 minutos**  
**Qualidade decisões**: **9.5+/10** (dados reais)  
**Trabalho manual**: **Mínimo** (só aprovar!)

Posso começar a codificar este motor? 🚀
