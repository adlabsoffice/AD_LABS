# SPECS RESUMIDAS: AGENTES 04-08
> Specs condensadas dos agentes restantes para agilizar desenvolvimento

---

## AGENTE 04: ARQUITETO DE EIXOS
**Timestamp**: T=3  
**Input**: `T02_clusters.json`  
**Output**: `T03_eixos/eixo_01.json` ... `eixo_05.json`

### Responsabilidade
Transformar cada cluster em "eixo" (formato de conteúdo) estruturado.

### Schema Output
```json
{
  "id": "eixo_01",
  "nome": "Humilhação → Revanche",
  "cluster_origem": "cluster_0",
  "emocao_central": "humilhação + reparação",
  "personagem_tipo": "pessoa injustiçada",
  "formato_video": "1-3min",
  "padrão_dramatico": "conflito injusto → virada → justiça",
  "categorias_possiveis": ["escola", "trabalho", "família"],
  "saturacao": "média",
  "forca": "alta",
  "risco": "baixo",
  "rpm_esperado": "médio"
}
```

### Validação
- ✅ 5 eixos criados (1 por cluster top + combinações)
- ✅ Cada eixo com emoção distinta
- ✅ Padrão dramático definido

**Tempo**: 30min  
**Complexidade**: Média

---

## AGENTE 05: GERADOR DE IDEIAS
**Timestamp**: T=4  
**Input**: `T03_eixos/eixo_01.json`  
**Output**: `T04_ideias/ideia_001.json` ... `ideia_150.json`

### Responsabilidade
Gerar 30 ideias por eixo (total 150) em **loop de 1 item**.

### 🔑 MUDANÇA CRÍTICA
```python
# ❌ ANTES (travava):
ideias = gerar_30_ideias(eixo)  # Contexto explode

# ✅ AGORA (funciona):
for i in range(30):
    ideia = gerar_1_ideia(eixo, numero=i+1)
    salvar_json(f"ideia_{contador:03d}.json", ideia)
    contador += 1
```

### Schema Output
```json
{
  "id": "ideia_001",
  "eixo_id": "eixo_01",
  "numero": 1,
  "titulo": "Eles zombaram de mim na escola... mas hoje sou CEO",
  "conflito": "Garoto pobre humilhado por colegas ricos",
  "virada": "Vence olimpíada de matemática e ganha bolsa MIT",
  "emocao": "humilhação → revanche",
  "categoria": "escola"
}
```

### Prompt Template
```
Eixo: {eixo['nome']}
Emoção: {eixo['emocao_central']}
Padrão: {eixo['padrão_dramatico']}

Gere 1 ideia de vídeo seguindo:
- Título viral (choque/curiosidade)
- Conflito claro
- Virada emocional forte
- Categoria: {categoria_aleatoria}

JSON:
{
  "titulo": "",
  "conflito": "",
  "virada": ""
}
```

**Tempo**: 1-2h (150 iterações)  
**Complexidade**: Baixa (mas volume alto)

---

## AGENTE 06: PRODUTOR DE VÍDEO
**Timestamp**: T=5-T=9 (loop 5x)  
**Input**: `ideia_XXX.json` (selecionada)  
**Output**: `video_eixo_XX/` (pasta com roteiro, SRT, prompts, áudio)

### Responsabilidade
1. Roteiro (600-1300 caracteres para 1-3min)
2. SRT (legendas sincronizadas)
3. 10 Prompts de Imagem (MidJourney/SD)
4. Áudio TTS (Elevenlabs ou gratuito)

### Estrutura Output
```
video_eixo_01/
├── roteiro.txt
├── roteiro.srt
├── prompts_imagens.json
├── audio.mp3
└── metadata.json
```

### Roteiro Template
```
[CENA 1 - 0:00-0:10]
Hook forte iniciando conflito

[CENA 2 - 0:11-0:30]
Desenvolver tensão

[CENA 3 - 0:31-0:50]
Virada emocional

[CENA 4 - 0:51-1:00]
Resolução + lição
```

### SRT
```srt
1
00:00:00,000 --> 00:00:03,500
Eles zombaram de mim...

2
00:00:03,500 --> 00:00:07,000
Mas não sabiam o que estava por vir.
```

### Prompts de Imagem
```json
{
  "prompts": [
    {
      "cena": 1,
      "prompt": "Pixar style, school hallway, sad teenager being laughed at, dramatic lighting, 8k --ar 16:9",
      "timing": "0:00-0:10"
    }
  ]
}
```

**Tempo**: 45min por vídeo  
**Complexidade**: Média/Alta

---

## AGENTE 07: EDITOR
**Timestamp**: T=10  
**Input**: `video_eixo_XX/`  
**Output**: Projeto CapCut ou vídeo final

### Responsabilidade
**MVP**: Gerar template CapCut semi-automático  
**Futuro**: Edição 100% automatizada (Remotion.js)

### MVP Approach
```python
def editor_mvp():
    # 1. Criar pasta organizada
    projeto_capcut/
    ├── images/
    │   ├── 01.png ... 10.png
    ├── audio/
    │   └── narration.mp3
    ├── subtitles/
    │   └── legendas.srt
    └── INSTRUCOES.txt
    
    # 2. Gerar instruções
    """
    IMPORTAR PARA CAPCUT:
    1. Adicionar áudio: audio/narration.mp3
    2. Adicionar imagens na ordem (01-10)
    3. Importar SRT: subtitles/legendas.srt
    4. Ajustar zoom/pan leve
    5. Exportar 1080p
    """
```

**Tempo**: 5-10min por vídeo (semi-manual)  
**Complexidade**: Baixa (MVP)

---

## AGENTE 08: ANALISTA DE MARÉ
**Timestamp**: T=13  
**Input**: `metricas_youtube.json` (manual do usuário)  
**Output**: `T13_mare_report.json`

### Responsabilidade
Identificar qual dos 5 eixos "pegou" (viralizou).

### Input Manual
```json
{
  "videos": [
    {"eixo": "eixo_01", "views_48h": 500, "ctr": 0.02, "retencao": 0.25},
    {"eixo": "eixo_02", "views_48h": 5000, "ctr": 0.08, "retencao": 0.65},
    {"eixo": "eixo_03", "views_48h": 800, "ctr": 0.03, "retencao": 0.30}
  ]
}
```

### Algoritmo de Detecção
```python
def detectar_mare(videos):
    for video in videos:
        # Score ponderado
        score = (
            video['views_48h'] * 0.4 +
            video['ctr'] * 1000 * 0.3 +
            video['retencao'] * 100 * 0.3
        )
        video['mare_score'] = score
    
    vencedor = max(videos, key=lambda v: v['mare_score'])
    
    if vencedor['mare_score'] > 2x media:
        return {"mare_identificada": True, "eixo_vencedor": vencedor['eixo']}
    else:
        return {"mare_identificada": False, "acao": "testar_mais"}
```

### Output
```json
{
  "timestamp": "T=13",
  "mare_identificada": true,
  "eixo_vencedor": "eixo_02",
  "metricas_vencedor": {
    "views_48h": 5000,
    "ctr": 0.08,
    "retencao": 0.65,
    "mare_score": 285
  },
  "recomendacao": "Escalar: produzir 10-20 vídeos do eixo_02",
  "eixos_descartar": ["eixo_01", "eixo_03", "eixo_04", "eixo_05"]
}
```

**Tempo**: 5min  
**Complexidade**: Baixa

---

## ORQUESTRADOR MASTER

### Responsabilidade
Executar todos agentes em sequência (T=0 → T=13).

### CLI
```bash
$ python incubadora.py --start
```

### Flow
```python
def orquestrador():
    print("🏭 INCUBADORA AD_LABS v2.0")
    
    # T=0
    with progress_bar("Inicializando"):
        agente_01_inicializador()
    
    # T=1
    with progress_bar("Pesquisando canais"):
        agente_02_pesquisador()
    
    # T=2
    with progress_bar("Analisando clusters"):
        agente_03_analista()
    
    # T=3
    with progress_bar("Criando 5 eixos"):
        agente_04_arquiteto()
    
    # T=4 (LOOP)
    with progress_bar("Gerando 150 ideias"):
        for eixo in eixos:
            for i in range(30):
                agente_05_gerador_ideias(eixo, i)
    
    # T=5-9 (LOOP)
    with progress_bar("Produzindo 5 vídeos"):
        for eixo in eixos:
            ideia = selecionar_melhor_ideia(eixo)
            agente_06_produtor(ideia)
    
    # T=10
    print("⚠️ Edição semi-manual - Siga instruções em cada pasta")
    
    # T=11
    print("📤 Poste 1 vídeo/dia. Aguarde 48-72h")
    input("Pressione ENTER após postar e coletar métricas...")
    
    # T=12
    metricas = input_metricas_manual()
    
    # T=13
    with progress_bar("Detectando maré"):
        mare = agente_08_analista_mare(metricas)
    
    print(f"✅ CONCLUÍDO!")
    if mare['mare_identificada']:
        print(f"🎯 Eixo vencedor: {mare['eixo_vencedor']}")
        print(f"📈 Próximo: Escalar para 10-20 vídeos")
    else:
        print("⚠️ Nenhuma maré clara. Teste mais 5 vídeos.")
```

---

## 📊 RESUMO DE COMPLEXIDADE

| Agente | Tempo | Complexidade | Crítico? |
|--------|-------|--------------|----------|
| 01. Inicializador | 2min | Baixa | ✅ |
| 02. Pesquisador | 15min | Alta | ✅ |
| 03. Analista | 8min | Alta | ✅ |
| 04. Arquiteto | 30min | Média | ✅ |
| 05. Gerador Ideias | 90min | Baixa | ⚠️ Volume |
| 06. Produtor | 4h | Alta | ✅ |
| 07. Editor | 30min | Baixa | Manual OK |
| 08. Analista Maré | 5min | Baixa | ✅ |

**Total**: ~7-8 horas fim-a-fim (T=0 → T=13)

---

**Status**: 📝 Todas Specs Completas  
**Pronto para**: Começar Desenvolvimento Dia 1
