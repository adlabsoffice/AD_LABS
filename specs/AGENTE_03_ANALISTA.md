# AGENTE 03: ANALISTA
> **Timestamp**: T=2  
> **Responsabilidade**: Analisar vídeos coletados, fazer clustering e identificar padrões emocionais

---

## 🎯 OBJETIVO

Processar CSV bruto, limpar dados, fazer clustering semântico de títulos, e identificar 4-5 grupos emocionais para criar eixos.

---

## 📥 INPUT

### Arquivo: `outputs/T01_canais_referencias.csv`

Mínimo 200 vídeos com campos obrigatórios.

---

## 📤 OUTPUT

### Arquivo: `outputs/T02_clusters.json`

```json
{
  "timestamp": "T=2",
  "estatisticas": {
    "videos_brutos": 342,
    "videos_limpos": 215,
    "clusters_identificados": 4,
    "videos_descartados": 127
  },
  "clusters": [
    {
      "id": "cluster_0",
      "nome": "Emoção Identificada",
      "descricao": "Padrão emocional dominante",
      "tamanho": 55,
      "exemplos_titulos": [
        "título exemplo 1",
        "título exemplo 2",
        "título exemplo 3"
      ],
      "metricas": {
        "views_medias": 500000,
        "engajamento_medio": 0.08,
        "viral_score_medio": 1.5
      },
      "palavras_chave": ["palavra1", "palavra2", "palavra3"],
      "emocao_central": "injustiça + reparação",
      "saturacao": "média",
      "forca_viral": "alta"
    }
  ]
}
```

---

## 🔧 PROCESSO DE LIMPEZA

### Etapa 1: Remoção de Duplicatas
```python
# Por video_id
df_limpo = df.drop_duplicates(subset=['video_id'])
```

### Etapa 2: Filtros
```python
# Remover:
- Músicas/Clipes (buscar "official music", "lyric video")
- Shorts < 60s (muito curtos)
- Vídeos > 30min (muito longos para Dark)
- Views < 10.000 (sem tração)
- Canais com < 3 vídeos na amostra (inconsistentes)
```

### Etapa 3: Enriquecimento de Métricas
```python
# Criar novas colunas
df['VPH'] = views / horas_desde_publicacao
df['engajamento'] = (likes + comentarios) / views
df['viral_score'] = views_video / media_views_canal
```

---

## 🤖 CLUSTERING (HDBSCAN)

### Preparação
```python
from sentence_transformers import SentenceTransformer
import hdbscan

# 1. Vetorizar títulos
model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')
embeddings = model.encode(df['titulo'].tolist())

# 2. Clustering
clusterer = hdbscan.HDBSCAN(
    min_cluster_size=15,  # Mínimo 15 vídeos por cluster
    min_samples=5,
    metric='euclidean'
)

labels = clusterer.fit_predict(embeddings)
df['cluster'] = labels
```

### Análise de Clusters
```python
for cluster_id in set(labels):
    if cluster_id == -1:  # Ruído
        continue
    
    cluster_videos = df[df['cluster'] == cluster_id]
    
    # Extrair padrões
    top_palavras = extrair_keywords(cluster_videos['titulo'])
    emocao = identificar_emocao(top_palavras, cluster_videos)
    
    cluster_info = {
        "id": f"cluster_{cluster_id}",
        "tamanho": len(cluster_videos),
        "exemplos_titulos": cluster_videos['titulo'].head(5).tolist(),
        "palavras_chave": top_palavras[:10],
        "emocao_central": emocao,
        ...
    }
```

---

## 🎭 IDENTIFICAÇÃO DE EMOÇÕES

### Padrões Emocionais a Buscar
```python
PADROES_EMOCIONAIS = {
    "humilhação → revanche": [
        "zombar", "humilhar", "se arrepender", "vingança", "justiça"
    ],
    "segredo → revelação": [
        "segredo", "descobrir", "verdade", "revelar", "esconder"
    ],
    "medo → alívio": [
        "terror", "medo", "susto", "descobrir", "salvação"
    ],
    "injustiça → reparação": [
        "injusto", "cruel", "triste", "final feliz", "justiça"
    ],
    "curiosidade → recompensa": [
        "mistério", "incrível", "surpreendente", "impressionante"
    ]
}

def identificar_emocao(palavras_chave, videos):
    scores = {}
    
    for emocao, keywords in PADROES_EMOCIONAIS.items():
        score = sum(1 for palavra in palavras_chave if palavra in keywords)
        scores[emocao] = score
    
    return max(scores, key=scores.get)
```

---

## ✅ VALIDAÇÕES

### Input Validation
- ✅ CSV existe e é válido
- ✅ Mínimo 200 vídeos
- ✅ Todos campos obrigatórios presentes

### Output Validation
- ✅ Entre 3-6 clusters identificados
- ✅ Cada cluster tem mínimo 15 vídeos
- ✅ Ruído (cluster -1) < 30% dos vídeos
- ✅ Emoções identificadas para todos clusters

---

## ⚠️ TRATAMENTO DE ERROS

| Erro | Ação |
|------|------|
| Poucos vídeos após limpeza | Relaxar filtros (ex: aceitar 5.000 views) |
| Clustering gera 1 cluster só | Ajustar min_cluster_size |
| Muito ruído (>40%) | Ajustar min_samples |
| Erro de encoding | Remover caracteres especiais |

---

## 📋 EXEMPLO CONCRETO

### Input (primeiras 5 linhas do CSV)
```csv
video_id,titulo,views,likes,comentarios,duracao_segundos
abc123,Eles me humilharam... mas se arrependeram,500000,25000,1200,240
def456,10 Mistérios que Nunca Foram Resolvidos,800000,40000,2000,480
ghi789,A Verdade Sobre Salomão e o Ouro,350000,15000,800,360
...
```

### Output (clusters.json - resumido)  
```json
{
  "timestamp": "T=2",
  "estatisticas": {
    "videos_brutos": 342,
    "videos_limpos": 215,
    "clusters_identificados": 4
  },
  "clusters": [
    {
      "id": "cluster_0",
      "nome": "Humilhação e Revanche",
      "tamanho": 55,
      "exemplos_titulos": [
        "Eles me humilharam... mas se arrependeram",
        "Zombaram de mim na escola. Hoje sou CEO",
        "Me chamaram de pobre. Se arrependeram"
      ],
      "palavras_chave": ["humilhar", "zombar", "arrepender", "vingança"],
      "emocao_central": "humilhação → revanche",
      "metricas": {
        "views_medias": 450000,
        "engajamento_medio": 0.09,
        "viral_score_medio": 1.8
      },
      "saturacao": "média",
      "forca_viral": "alta"
    },
    {
      "id": "cluster_1",
      "nome": "Mistérios Não Resolvidos",
      "tamanho": 48,
      "emocao_central": "curiosidade → recompensa",
      "saturacao": "alta",
      "forca_viral": "média"
    }
  ]
}
```

---

## 🧪 TESTES

```python
def test_limpeza_dados():
    df_raw = pd.read_csv("test_data.csv")
    df_clean = limpar_dados(df_raw)
    
    # Nenhum short < 60s
    assert all(df_clean['duracao_segundos'] >= 60)
    
    # Nenhuma duplicata
    assert len(df_clean) == df_clean['video_id'].nunique()

def test_clustering():
    df = carregar_dados_teste()
    clusters = fazer_clustering(df)
    
    assert len(clusters) >= 3
    assert len(clusters) <= 6
    assert sum(c['tamanho'] for c in clusters) >= 150
```

---

## 📊 MÉTRICAS

- **Tempo esperado**: 5-10 minutos
- **Complexidade**: Alta
- **Dependências**: pandas, hdbscan, sentence-transformers
- **Tamanho contexto**: ~180 linhas

---

## ✅ CRITÉRIO DE SUCESSO

1. ✅ 3-6 clusters identificados
2. ✅ Cada cluster com emoção clara
3. ✅ JSON válido gerado
4. ✅ Progress atualizado para T=2

---

**Status**: 📝 Spec Completa  
**Pronto para**: Implementação
