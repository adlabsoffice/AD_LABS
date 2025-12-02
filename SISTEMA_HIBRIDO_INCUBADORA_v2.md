# 🏭 INCUBADORA AD_LABS v2.0 - SISTEMA HÍBRIDO
## Fábrica Automatizada de Canais Dark YouTube

> **Objetivo**: Sistema 90% automatizado que cria e escala canais Dark em 2 horas  
> **Prazo**: 3 dias para MVP funcional  
> **Arquitetura**: Híbrida (Timestamps + Agentes + Deliverables + Maré)

---

## 🎯 PRINCÍPIO FUNDAMENTAL

### O Problema que Este Sistema Resolve
**MASTER v5.0 (2586 linhas)**: IA se perdia mesmo com tudo travado  
**Sistema Anterior**: Funcionou até certo ponto, mas travava em geração em massa

### A Solução Híbrida
```
Timestamps (T=0→N)     = Ordem linear clara (IA não pula etapas)
+ Agentes Independentes  = Contexto pequeno (IA não se perde)
+ Deliverables Salvos    = Checkpoints (IA não esquece)
+ Loops de 1 Item        = Sem batch gigante (IA não trava)
= INCUBADORA FUNCIONAL
```

---

## 📐 ARQUITETURA GERAL

### 8 Agentes Especialistas (Time Hollywood)

Cada agente:
- ✅ Recebe **1 input** claro (JSON)
- ✅ Executa **1 tarefa** específica
- ✅ Retorna **1 output** (JSON/CSV)
- ✅ **Máx 200 linhas** de contexto
- ✅ **Independente** de memória anterior

```
┌─────────────────────────────────────────────────┐
│  AGENTE 1: Inicializador                        │
│  Input: Nicho desejado                          │
│  Output: config.json                            │
└─────────────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────────────┐
│  AGENTE 2: Pesquisador                          │
│  Input: config.json                             │
│  Output: canais_referencias.csv (360 vídeos)    │
└─────────────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────────────┐
│  AGENTE 3: Analista                             │
│  Input: canais_referencias.csv                  │
│  Output: clusters.json (4-5 clusters)           │
└─────────────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────────────┐
│  AGENTE 4: Arquiteto de Eixos                   │
│  Input: clusters.json                           │
│  Output: eixo_01.json ... eixo_05.json          │
└─────────────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────────────┐
│  AGENTE 5: Gerador de Ideias                    │
│  Input: eixo_01.json                            │
│  Output: ideia_001.json (LOOP 150x)             │
└─────────────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────────────┐
│  AGENTE 6: Produtor de Vídeo                    │
│  Input: ideia_001.json                          │
│  Output: video_001/ (roteiro, SRT, prompts)     │
└─────────────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────────────┐
│  AGENTE 7: Editor                               │
│  Input: video_001/                              │
│  Output: video_001_final.mp4                    │
└─────────────────────────────────────────────────┘
              ↓
┌─────────────────────────────────────────────────┐
│  AGENTE 8: Analista de Maré                     │
│  Input: metricas_youtube.json                   │
│  Output: mare_report.json (qual eixo escalar)   │
└─────────────────────────────────────────────────┘
```

---

## ⏱️ FLUXO COM TIMESTAMPS

### Por Que Timestamps?
- ✅ **Ordem rigorosa** - IA não pode pular etapas
- ✅ **Recuperação fácil** - "Volte ao T=5"
- ✅ **Progresso visível** - Sabe onde está no processo

### Linha do Tempo Completa

```
T=0  │ Setup Inicial
     │ └─ Agente: Inicializador
     │ └─ Input: Nicho (ex: "Histórias Dramáticas")
     │ └─ Output: config.json
     │
T=1  │ Pesquisa de Canais
     │ └─ Agente: Pesquisador
     │ └─ Ação: Buscar canais internacionais
     │ └─ Output: canais_referencias.csv (360 vídeos)
     │
T=2  │ Análise e Clustering
     │ └─ Agente: Analista
     │ └─ Ação: HDBSCAN clustering
     │ └─ Output: clusters.json (4-5 grupos)
     │
T=3  │ Criação dos 5 Eixos
     │ └─ Agente: Arquiteto de Eixos
     │ └─ Ação: Transformar clusters em formatos
     │ └─ Output: eixo_01.json ... eixo_05.json
     │
T=4  │ Geração de Ideias (LOOP)
     │ ├─ Agente: Gerador de Ideias
     │ ├─ Para cada eixo (5x):
     │ │   └─ Para cada ideia (30x):
     │ │       └─ Gerar 1 ideia por vez
     │ └─ Output: ideia_001.json ... ideia_150.json
     │
T=5  │ Produção: Vídeo Eixo 1
     │ └─ Agente: Produtor
     │ └─ Input: ideia_001.json (selecionada)
     │ └─ Output: video_eixo_01/ (roteiro + SRT + prompts)
     │
T=6  │ Produção: Vídeo Eixo 2
     │ └─ [Repetir T=5]
     │
T=7  │ Produção: Vídeo Eixo 3
T=8  │ Produção: Vídeo Eixo 4
T=9  │ Produção: Vídeo Eixo 5
     │
T=10 │ Edição: 5 Vídeos (Semi-Automático)
     │ └─ Agente: Editor
     │ └─ Para cada vídeo:
     │     └─ Gerar projeto CapCut
     │
T=11 │ Postagem Manual
     │ └─ Usuário: 1 vídeo/dia por 5 dias
     │
T=12 │ Coleta de Métricas (48-72h depois)
     │ └─ Usuário: Input manual de views/CTR/retenção
     │
T=13 │ Detecção de Maré
     │ └─ Agente: Analista de Maré
     │ └─ Input: metricas.json
     │ └─ Output: mare_report.json
     │
T=14 │ Escala: 10-20 Vídeos do Eixo Vencedor
     │ └─ Loop T=4→T=10 focado em 1 eixo
     │
T=15+│ Escala Massiva: 100 Vídeos
     │ └─ Repetir ciclo
```

---

## 📦 DELIVERABLES (Checkpoints Salvos)

### Estrutura de Arquivos

```
AD_LABS/
├── incubadora/
│   ├── agentes/
│   │   ├── 01_inicializador.py
│   │   ├── 02_pesquisador.py
│   │   ├── 03_analista.py
│   │   ├── 04_arquiteto_eixos.py
│   │   ├── 05_gerador_ideias.py
│   │   ├── 06_produtor_video.py
│   │   ├── 07_editor.py
│   │   └── 08_analista_mare.py
│   │
│   ├── outputs/
│   │   ├── T00_config.json
│   │   ├── T01_canais_referencias.csv
│   │   ├── T02_clusters.json
│   │   ├── T03_eixos/
│   │   │   ├── eixo_01.json
│   │   │   ├── eixo_02.json
│   │   │   ├── eixo_03.json
│   │   │   ├── eixo_04.json
│   │   │   └── eixo_05.json
│   │   ├── T04_ideias/
│   │   │   ├── ideia_001.json
│   │   │   ├── ideia_002.json
│   │   │   └── ... (150 arquivos)
│   │   ├── T05-09_videos/
│   │   │   ├── video_eixo_01/
│   │   │   │   ├── roteiro.txt
│   │   │   │   ├── roteiro.srt
│   │   │   │   ├── prompts_imagens.json
│   │   │   │   └── audio.mp3
│   │   │   └── ... (5 pastas)
│   │   ├── T13_mare_report.json
│   │   └── progress.json (estado atual)
│   │
│   ├── templates/
│   │   ├── config_template.json
│   │   ├── eixo_template.json
│   │   └── ideia_template.json
│   │
│   └── orquestrador.py (MAESTRO)
│
└── README.md
```

### Formato dos Deliverables

#### T00_config.json
```json
{
  "timestamp": "T=0",
  "nicho": "Histórias Dramáticas",
  "apis_disponiveis": ["gemini", "youtube_data"],
  "orcamento_maximo": 500,
  "prazo_dias": 3,
  "status": "completo"
}
```

#### T03_eixos/eixo_01.json
```json
{
  "timestamp": "T=3",
  "id": "eixo_01",
  "nome": "Humilhação → Revanche",
  "emocao_central": "humilhação + reparação",
  "personagem": "estudante injustiçado",
  "formato": "1-3min",
  "saturacao": "média",
  "forca": "alta",
  "risco": "baixo",
  "status": "validado"
}
```

#### T04_ideias/ideia_001.json
```json
{
  "timestamp": "T=4",
  "id": "ideia_001",
  "eixo_id": "eixo_01",
  "titulo": "Eles zombaram de mim... mas se arrependeram",
  "conflito": "Garoto pobre humilhado na escola",
  "virada": "Vence olimpíada de matemática",
  "status": "pronto_para_producao"
}
```

#### progress.json (Estado Atual)
```json
{
  "timestamp_atual": "T=5",
  "ultimo_agente": "produtor_video",
  "proxima_acao": "Produzir vídeo eixo 2",
  "eixos_criados": 5,
  "ideias_geradas": 150,
  "videos_produzidos": 1,
  "mare_identificada": false
}
```

---

## 🔑 MUDANÇA-CHAVE: Loop de 1 Item

### ANTES (Sistema Travava)
```python
# ❌ Gerar 30 ideias de uma vez
prompt = f"Gere 30 ideias para o eixo {eixo}"
ideias = gemini.generate(prompt)  # IA se perde aqui
```

### AGORA (Sistema Funciona)
```python
# ✅ Loop de 1 ideia por vez
for i in range(30):
    prompt = f"Gere 1 ideia para {eixo}. Número: {i+1}"
    ideia = gemini.generate(prompt)
    salvar_json(f"ideia_{i:03d}.json", ideia)
    # IA nunca perde contexto
```

---

## 🚀 ROADMAP DE 3 DIAS (DETALHADO)

### 🔴 DIA 1 - Fundação (28/11 - HOJE)

#### Manhã (4h)
- [ ] **T=0**: Criar estrutura de pastas
- [ ] **Agente 1**: Inicializador (1h)
  - Input: CLI pergunta nicho
  - Output: `T00_config.json`
- [ ] **Agente 2**: Pesquisador (2h)
  - YouTube Data API
  - Sistema de failover (4 keys)
  - Output: `T01_canais_referencias.csv`
- [ ] **Teste**: Pesquisar "Histórias Dramáticas" → 360 vídeos

#### Tarde (4h)
- [ ] **Agente 3**: Analista (3h)
  - HDBSCAN clustering
  - Limpeza de dados
  - Output: `T02_clusters.json`
- [ ] **Agente 4**: Arquiteto de Eixos (1h)
  - Input: clusters
  - Output: 5× `eixo_XX.json`
- [ ] **Teste End-to-End**: T=0 → T=3 funcionando

---

### 🟡 DIA 2 - Produção (29/11)

#### Manhã (4h)
- [ ] **Agente 5**: Gerador de Ideias (2h)
  - **CRÍTICO**: Loop de 1 ideia
  - Para debug: gerar só 10 ideias primeiro
  - Output: `ideia_001.json` ... `ideia_150.json`
- [ ] **Agente 6**: Produtor de Vídeo (2h)
  - Roteirista: gera roteiro
  - SRT: converte para legendas
  - Diretor de Arte: 10 prompts de imagem
  - Output: pasta `video_eixo_01/`

#### Tarde (4h)
- [ ] **Loop T=5→T=9**: Produzir 5 vídeos
  - 1 por eixo
  - ~45min cada
- [ ] **Teste**: 1 vídeo completo (roteiro + SRT + prompts)

---

### 🟢 DIA 3 - Integração (30/11 - DEADLINE)

#### Manhã (3h)
- [ ] **Agente 7**: Editor (2h)
  - Gerar template CapCut
  - Script de importação
  - **MVP**: Semi-automático (manual aceitável)
- [ ] **Agente 8**: Analista de Maré (1h)
  - Input: métricas (simuladas para teste)
  - Output: `mare_report.json`

#### Tarde (3h)
- [ ] **Orquestrador Master** (2h)
  - CLI: `python incubadora.py --start`
  - Executa T=0 → T=13 automaticamente
  - Progress bar visual (Rich)
- [ ] **Teste Completo** (1h)
  - Rodar sistema do zero
  - Nicho: "Mistérios Perturbadores"
  - Validar: 5 vídeos prontos

#### Final (2h)
- [ ] **Documentação Mínima**
  - README.md
  - Video walkthrough (10min)
- [ ] **Deploy/Entrega**

---

## 🛡️ SISTEMA ANTI-ALUCINAÇÃO

### Regras Rigorosas para Cada Agente

```python
class AgenteBase:
    def __init__(self):
        self.max_context_lines = 200  # NUNCA mais que isso
        self.max_retries = 3
        self.timeout = 30
    
    def executar(self, input_path, output_path):
        # 1. LER input (JSON/CSV)
        data = self.ler_deliverable(input_path)
        
        # 2. VALIDAR input
        if not self.validar_input(data):
            raise ErroInputInvalido()
        
        # 3. EXECUTAR tarefa (1 coisa só)
        resultado = self.processar(data)
        
        # 4. VALIDAR output
        if not self.validar_output(resultado):
            raise ErroOutputInvalido()
        
        # 5. SALVAR deliverable
        self.salvar_deliverable(output_path, resultado)
        
        # 6. ATUALIZAR progress.json
        self.atualizar_progresso()
        
        return resultado
```

### Recuperação de Erros

```python
# Se agente falhar no T=5
if erro_detectado:
    # 1. Ler progress.json
    estado = ler_json("progress.json")
    
    # 2. Identificar último timestamp OK
    ultimo_ok = estado["timestamp_atual"]  # Ex: T=4
    
    # 3. Recarregar deliverable
    ultimo_deliverable = ler_json(f"T04_ideias/ideia_150.json")
    
    # 4. Recomeçar do ponto certo
    executar_timestamp(T=5, input=ultimo_deliverable)
```

---

## 📊 MÉTRICAS DE SUCESSO

### Critérios para MVP (3 dias)

| Métrica | Meta | Como Medir |
|---------|------|------------|
| **Automação** | 90%+ | Humano só aprova/posta |
| **Velocidade** | <2h | T=0 → T=9 completo |
| **Confiabilidade** | 0 alucinações | IA não apaga/muda nada |
| **Replicabilidade** | 100% | Roda em qualquer máquina |
| **Qualidade** | 5/5 vídeos OK | Padrão consistente |

---

## 🎯 DIFERENÇAS vs MASTER v5.0

| Aspecto | MASTER v5.0 | AD_LABS v2.0 |
|---------|-------------|--------------|
| **Tamanho Contexto** | 2586 linhas | Máx 200/agente |
| **Ordem** | Implícita | Timestamps explícitos |
| **Memória** | IA precisa lembrar | Deliverables salvos |
| **Geração em Massa** | 150 ideias de uma vez | 1 por vez (loop) |
| **Recuperação** | Prompt Bunker (falha) | Ler último deliverable |
| **Modularidade** | Monolítico | 8 agentes independentes |
| **Testabilidade** | Difícil | Cada agente testável |

---

## ✅ APROVAÇÃO PARA DESENVOLVIMENTO

**Status**: 🟢 **PRONTO PARA EXECUÇÃO**

### Próximos Passos Imediatos

1. **Confirmar entendimento** ✅ (feito)
2. **Criar specs detalhadas** de cada agente (próximo)
3. **Começar Dia 1** - Agentes 1-4

---

**Versão**: AD_LABS Incubadora v2.0  
**Data**: 28/11/2025  
**Prazo**: 3 dias (até 30/11)
