# 📚 ÍNDICE DAS SPECS - INCUBADORA AD_LABS v2.0

Todas as especificações técnicas para implementação dos 8 agentes.

---

## 📁 Estrutura de Specs

```
specs/
├── AGENTE_01_INICIALIZADOR.md        ✅ Completa (detalhada)
├── AGENTE_02_PESQUISADOR.md          ✅ Completa (detalhada)  
├── AGENTE_03_ANALISTA.md             ✅ Completa (detalhada)
├── AGENTES_04-08_RESUMO.md           ✅ Completa (resumida)
└── INDICE.md                          ✅ Este arquivo
```

---

## 🎯 Quick Reference por Agente

### AGENTE 01: Inicializador
- **T**: T=0
- **Input**: CLI (usuário)
- **Output**: `T00_config.json`, `progress.json`
- **Tempo**: 2min
- **Complexidade**: ⭐ Baixa
- **Dependências**: Nenhuma
- **Crítico**: ✅ Sim

### AGENTE 02: Pesquisador
- **T**: T=1
- **Input**: `T00_config.json`
- **Output**: `T01_canais_referencias.csv` (300-400 vídeos)
- **Tempo**: 15min
- **Complexidade**: ⭐⭐⭐ Alta
- **Dependências**: YouTube Data API, pandas
- **Features**: Sistema de failover (4 keys), retry exponencial
- **Crítico**: ✅ Sim

### AGENTE 03: Analista
- **T**: T=2
- **Input**: `T01_canais_referencias.csv`
- **Output**: `T02_clusters.json` (4-5 clusters)
- **Tempo**: 8min
- **Complexidade**: ⭐⭐⭐ Alta
- **Dependências**: HDBSCAN, sentence-transformers
- **Features**: Clustering semântico, identificação de emoções
- **Crítico**: ✅ Sim

### AGENTE 04: Arquiteto de Eixos
- **T**: T=3
- **Input**: `T02_clusters.json`
- **Output**: `eixo_01.json` ... `eixo_05.json`
- **Tempo**: 30min
- **Complexidade**: ⭐⭐ Média
- **Dependências**: Gemini API
- **Crítico**: ✅ Sim

### AGENTE 05: Gerador de Ideias
- **T**: T=4
- **Input**: `eixo_XX.json`
- **Output**: `ideia_001.json` ... `ideia_150.json`
- **Tempo**: 90min
- **Complexidade**: ⭐ Baixa (mas volume alto)
- **Dependências**: Gemini API
- **Features**: **Loop de 1 item** (crítico anti-travamento)
- **Crítico**: ⚠️ Volume

### AGENTE 06: Produtor de Vídeo
- **T**: T=5-9 (loop 5x)
- **Input**: `ideia_XXX.json`
- **Output**: `video_eixo_XX/` (roteiro, SRT, prompts, áudio)
- **Tempo**: 45min por vídeo
- **Complexidade**: ⭐⭐⭐ Alta
- **Dependências**: Gemini, TTS (Elevenlabs ou gratuito)
- **Features**: Geração de roteiro, SRT, prompts imagem, áudio
- **Crítico**: ✅ Sim

### AGENTE 07: Editor
- **T**: T=10
- **Input**: `video_eixo_XX/`
- **Output**: Projeto CapCut ou vídeo final
- **Tempo**: 30min (semi-manual MVP)
- **Complexidade**: ⭐ Baixa (MVP)
- **Dependências**: Nenhuma (manual)
- **Features**: Template + instruções (MVP), Remotion.js (futuro)
- **Crítico**: Manual OK no MVP

### AGENTE 08: Analista de Maré
- **T**: T=13
- **Input**: `metricas_youtube.json` (input manual)
- **Output**: `T13_mare_report.json`
- **Tempo**: 5min
- **Complexidade**: ⭐ Baixa
- **Dependências**: Nenhuma
- **Features**: Algoritmo de detecção de maré
- **Crítico**: ✅ Sim

---

## ⏱️ Timeline Estimado (T=0 → T=13)

```
T=0  │ Inicializador        │ 2min   │ ████
T=1  │ Pesquisador          │ 15min  │ ███████████████
T=2  │ Analista             │ 8min   │ ████████
T=3  │ Arquiteto 5 Eixos    │ 30min  │ ██████████████████████████████
T=4  │ Gerar 150 Ideias     │ 90min  │ ██████████████████████████████████████████████████████████████
T=5-9│ Produzir 5 Vídeos    │ 4h     │ ████████████████████████████████████████████████████████████████████████████████████████
T=10 │ Edição (semi-manual) │ 30min  │ ██████████████████████████████
T=11 │ Postagem manual      │ 5 dias │ (usuário)
T=12 │ Input métricas       │ 5min   │ ████
T=13 │ Detecção Maré        │ 5min   │ ████

TOTAL AUTOMATIZADO: ~7-8 horas
```

---

## 🔑 Mudanças-Chave vs MASTER v5.0

| Aspecto | MASTER v5.0 | AD_LABS v2.0 |
|---------|-------------|--------------|
| **Contexto** | 2586 linhas monolíticas | Máx 200 linhas/agente |
| **Ordem** | Implícita | Timestamps T=0→T=15 |
| **Memória** | IA precisa lembrar tudo | Deliverables salvos (JSON/CSV) |
| **Ideias** | 150 de uma vez (trava) | 1 por vez em loop |
| **Recuperação** | "Prompt Bunker" (falha) | Ler último deliverable |
| **Modularidade** | Monolítico | 8 agentes testáveis |

---

## 📊 Priorização para MVP (3 dias)

### Dia 1 - Fundação (CRÍTICO)
- ✅ Agente 01: Inicializador
- ✅ Agente 02: Pesquisador
- ✅ Agente 03: Analista
- ✅ Agente 04: Arquiteto

**Output**: 5 eixos validados

### Dia 2 - Produção (CRÍTICO)
- ✅ Agente 05: Gerador Ideias (só 10 ideias para debug)
- ✅ Agente 06: Produtor (só 1 vídeo completo para validar)

**Output**: 1 vídeo completo end-to-end

### Dia 3 - Integração (CRÍTICO)
- ✅ Agente 07: Editor (MVP semi-manual)
- ✅ Agente 08: Analista Maré
- ✅ Orquestrador Master CLI

**Output**: Sistema funcionando T=0→T=13

---

## 🚀 Próximos Passos Imediatos

### Agora (15min)
- [x] Specs concluídas
- [ ] Setup ambiente Python
  ```bash
  python -m venv venv
  pip install pandas hdbscan sentence-transformers google-generativeai
  ```

### Dia 1 - Manhã (4h)
- [ ] Criar estrutura de pastas
  ```bash
  mkdir -p incubadora/{agentes,outputs,templates,specs}
  ```
- [ ] Implementar Agente 01 (1h)
- [ ] Implementar Agente 02 (2h)
- [ ] Testar T=0→T=1 (30min)

### Dia 1 - Tarde (4h)
- [ ] Implementar Agente 03 (2h)
- [ ] Implementar Agente 04 (1h)
- [ ] Testar T=0→T=3 completo (1h)

---

## 📋 Checklist de Implementação

### Por Agente
- [ ] Criar arquivo `agentes/XX_nome.py`
- [ ] Implementar função principal
- [ ] Adicionar validações input/output
- [ ] Tratamento de erros
- [ ] Logging com timestamp
- [ ] Teste unitário
- [ ] Teste end-to-end

### Geral
- [ ] `orquestrador.py` (CLI master)
- [ ] `utils/` (funções compartilhadas)
- [ ] `.env.example` (template de API keys)
- [ ] `README.md` (instruções mínimas)
- [ ] `requirements.txt`
- [ ] Video walkthrough (10min)

---

## ✅ Critérios de Aceitação (Definition of Done)

**MVP está completo quando**:
1. ✅ Comando `python incubadora.py --start` executa T=0→T=10
2. ✅ Gera 5 eixos validados
3. ✅ Gera pelo menos 1 vídeo completo (roteiro + SRT + prompts)
4. ✅ Sistema de failover funciona (testa com quota exceeded)
5. ✅ Progress salvo em cada etapa (recuperável)
6. ✅ Documentação mínima presente
7. ✅ Outra pessoa consegue rodar seguindo README

---

## 📦 Deliverables Finais (Dia 3 EOD)

```
incubadora/
├── agentes/
│   ├── 01_inicializador.py      ✅
│   ├── 02_pesquisador.py        ✅
│   ├── 03_analista.py           ✅
│   ├── 04_arquiteto_eixos.py    ✅
│   ├── 05_gerador_ideias.py     ✅
│   ├── 06_produtor_video.py     ✅
│   ├── 07_editor.py             ✅ (MVP)
│   └── 08_analista_mare.py      ✅
├── outputs/
│   └── (gerados em runtime)
├── templates/
│   ├── config_template.json
│   ├── eixo_template.json
│   └── ideia_template.json
├── utils/
│   ├── json_utils.py
│   ├── progress_utils.py
│   └── validators.py
├── orquestrador.py              ✅
├── requirements.txt             ✅
├── .env.example                 ✅
├── README.md                    ✅
└── video_walkthrough.mp4        ✅
```

---

## 🎯 Meta de Sucesso

**Sistema permite**:
- ✅ Qualquer nicho como input → 5 vídeos prontos em <8h
- ✅ 90%+ automatizado (humano só aprova)
- ✅ Replicável para 10+ canais
- ✅ Zero alucinações (deliverables salvos)

---

**Status**: 🟢 SPECS COMPLETAS - PRONTO PARA DESENVOLVIMENTO  
**Próximo**: Setup ambiente + Implementação Dia 1
