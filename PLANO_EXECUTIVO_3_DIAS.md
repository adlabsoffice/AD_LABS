# 🎯 PLANO EXECUTIVO - PRÓXIMOS 3 DIAS
## O Que Vamos Fazer & Como Garantir Qualidade "Mansão"

---

## ✅ ONDE ESTAMOS AGORA (Feito até aqui)

### Documentação Criada
1. ✅ **Sistema Híbrido** completo (`SISTEMA_HIBRIDO_INCUBADORA_v2.md`)
2. ✅ **Specs técnicas** de todos 8 agentes (`specs/`)
3. ✅ **Índice** com roadmap (`specs/INDICE.md`)
4. ✅ **Análise comparativa** dos 3 sistemas anteriores

### O Que Temos de Concreto
- **Arquitetura anti-alucinação**: 8 agentes independentes (máx 200 linhas cada)
- **Timestamps lineares**: T=0 → T=15 (ordem rigorosa)
- **Deliverables salvos**: JSON/CSV em cada etapa (checkpoints)
- **Loop de 1 item**: Gera 1 ideia por vez (não 150 de uma vez)

### O Que NÃO Temos Ainda
- ❌ Código Python (zero linhas escritas)
- ❌ Ambiente configurado
- ❌ Testes rodando

**Status**: 100% planejamento, 0% implementação

---

## 🎯 O QUE VAMOS FAZER NOS 3 DIAS

### Objetivo Final
Código Python funcionando que:
- Input: "Mistérios Perturbadores" (nicho)
- Output: 5 vídeos prontos (roteiro + SRT + prompts + áudio)
- Tempo: <8 horas automatizadas
- Modo: 90% automático (humano só aprova)

---

## 📅 DIA 1 - HOJE (28/11) - FUNDAÇÃO

### Manhã (4h)

#### 1. Setup Ambiente (30min)
```bash
# Criar ambiente
cd d:\AD_LABS
python -m venv venv
venv\Scripts\activate

# Instalar dependências
pip install pandas hdbscan sentence-transformers google-generativeai python-dotenv rich click

# Criar .env
GEMINI_API_KEY=sua_chave
YOUTUBE_KEY_A=sua_chave
YOUTUBE_KEY_B=sua_chave
YOUTUBE_KEY_C=sua_chave
YOUTUBE_KEY_D=sua_chave
```

**Validação**: ✅ `pip list` mostra todas libs

---

#### 2. Agente 01: Inicializador (1h)
**O que faz**: Pergunta nicho, APIs, orçamento → gera `T00_config.json`

**Código**:
```python
# incubadora/agentes/01_inicializador.py
def executar():
    nicho = input("Qual nicho? ")
    # ... validações ...
    config = {...}
    salvar_json("outputs/T00_config.json", config)
    return config
```

**Teste**:
```bash
python -c "from agentes.01_inicializador import executar; executar()"
```

**Validação**: ✅ Arquivo `outputs/T00_config.json` criado e válido

---

#### 3. Agente 02: Pesquisador (2h)
**O que faz**: Busca YouTube → 300-400 vídeos → `T01_canais_referencias.csv`

**Código**:
```python
# incubadora/agentes/02_pesquisador.py
def executar():
    config = ler_json("outputs/T00_config.json")
    nicho = config["projeto"]["nicho"]
    
    # Gerar termos com Gemini
    termos = gerar_termos(nicho)
    
    # Buscar com failover
    videos = []
    for termo in termos:
        v = pesquisar_youtube(termo, api_keys)
        videos.extend(v)
    
    # Salvar CSV
    df = pd.DataFrame(videos)
    df.to_csv("outputs/T01_canais_referencias.csv")
```

**Teste**:
```bash
python -c "from agentes.02_pesquisador import executar; executar()"
```

**Validação**: 
- ✅ CSV com 200+ vídeos
- ✅ Múltiplos idiomas (PT, EN, ES)
- ✅ Failover funcionou (simular quota exceeded)

---

### Tarde (4h)

#### 4. Agente 03: Analista (2h)
**O que faz**: CSV → clustering → `T02_clusters.json`

**Código**:
```python
# incubadora/agentes/03_analista.py
def executar():
    df = pd.read_csv("outputs/T01_canais_referencias.csv")
    
    # Limpar
    df_limpo = limpar_dados(df)
    
    # Clustering
    embeddings = model.encode(df_limpo['titulo'])
    labels = clusterer.fit_predict(embeddings)
    
    # Identificar emoções
    clusters = analisar_clusters(df_limpo, labels)
    
    salvar_json("outputs/T02_clusters.json", clusters)
```

**Validação**:
- ✅ 3-6 clusters identificados
- ✅ Cada cluster com emoção definida
- ✅ Ruído < 30%

---

#### 5. Agente 04: Arquiteto de Eixos (1h)
**O que faz**: Clusters → 5 eixos → `eixo_01.json` ... `eixo_05.json`

**Código**:
```python
# incubadora/agentes/04_arquiteto_eixos.py
def executar():
    clusters = ler_json("outputs/T02_clusters.json")
    
    eixos = []
    for i, cluster in enumerate(clusters[:5]):
        eixo = {
            "id": f"eixo_{i+1:02d}",
            "nome": cluster["nome"],
            "emocao_central": cluster["emocao_central"],
            ...
        }
        salvar_json(f"outputs/T03_eixos/eixo_{i+1:02d}.json", eixo)
        eixos.append(eixo)
```

**Validação**:
- ✅ 5 arquivos JSON criados
- ✅ Cada um com emoção diferente
- ✅ Todos campos obrigatórios preenchidos

---

#### 6. Teste End-to-End T=0→T=3 (1h)
```bash
python orquestrador.py --etapas 0-3
```

**Validação**:
- ✅ Roda sem erros
- ✅ 5 eixos prontos
- ✅ Progress.json correto

---

## 📅 DIA 2 (29/11) - PRODUÇÃO

### Manhã (4h)

#### 7. Agente 05: Gerador de Ideias (2h)
**CRÍTICO**: Loop de 1 item

**Código**:
```python
# incubadora/agentes/05_gerador_ideias.py
def executar():
    eixos = listar_eixos()
    
    contador = 1
    for eixo in eixos:
        for i in range(30):  # 30 por eixo
            # ✅ GERAR 1 IDEIA POR VEZ
            ideia = gerar_1_ideia(eixo, numero=i+1)
            
            salvar_json(
                f"outputs/T04_ideias/ideia_{contador:03d}.json", 
                ideia
            )
            contador += 1
            
            print(f"✅ Ideia {contador-1}/150")
```

**Teste Inicial**: Só 10 ideias (debug)
```bash
python agentes/05_gerador_ideias.py --debug --max 10
```

**Validação**:
- ✅ 10 ideias geradas sem travar
- ✅ Cada uma em arquivo separado
- ✅ Seguem padrão emocional do eixo

**Teste Full**: 150 ideias
```bash
python agentes/05_gerador_ideias.py
```

**Validação**:
- ✅ 150 arquivos JSON
- ✅ Nenhuma alucinação/erro
- ✅ Tempo < 2h

---

#### 8. Agente 06: Produtor de Vídeo - Parte 1 (2h)
**O que faz**: Ideia → roteiro + SRT

**Código**:
```python
# incubadora/agentes/06_produtor_video.py
def executar(ideia_path):
    ideia = ler_json(ideia_path)
    
    # 1. Roteiro
    roteiro = gerar_roteiro(ideia)
    
    # 2. SRT
    srt = converter_para_srt(roteiro)
    
    # 3. Salvar
    pasta = criar_pasta_video(ideia["id"])
    salvar(f"{pasta}/roteiro.txt", roteiro)
    salvar(f"{pasta}/roteiro.srt", srt)
```

**Teste**: 1 vídeo só
```bash
python agentes/06_produtor_video.py --ideia outputs/T04_ideias/ideia_001.json
```

**Validação**:
- ✅ Roteiro com 600-1300 caracteres
- ✅ SRT validamente formatado
- ✅ Tempo < 10min

---

### Tarde (4h)

#### 9. Agente 06: Produtor - Parte 2 (2h)
**Adicionar**: Prompts de imagem + TTS

**Código**:
```python
def executar(ideia_path):
    # ... roteiro + SRT (já feito)
    
    # 4. Prompts de imagem
    prompts = gerar_10_prompts_imagem(roteiro)
    salvar_json(f"{pasta}/prompts_imagens.json", prompts)
    
    # 5. Áudio TTS
    audio = gerar_audio_tts(roteiro)
    salvar(f"{pasta}/audio.mp3", audio)
```

**Validação**:
- ✅ 10 prompts MidJourney/SD válidos
- ✅ Arquivo MP3 gerado
- ✅ Duração áudio = duração esperada do vídeo

---

#### 10. Loop: Produzir 5 Vídeos (2h)
**1 vídeo por eixo**

```bash
python orquestrador.py --etapas 5-9
```

**Validação**:
- ✅ 5 pastas `video_eixo_XX/`
- ✅ Cada uma com 4 arquivos (roteiro, SRT, prompts, áudio)
- ✅ Nenhum erro/travamento

---

## 📅 DIA 3 (30/11) - INTEGRAÇÃO & ENTREGA

### Manhã (3h)

#### 11. Agente 07: Editor MVP (2h)
**MVP**: Template + instruções (CapCut manual é OK)

**Código**:
```python
# incubadora/agentes/07_editor.py
def executar(video_path):
    # Organizar arquivos
    preparar_pasta_capcut(video_path)
    
    # Gerar instruções
    instrucoes = """
    IMPORTAR PARA CAPCUT:
    1. Adicionar áudio: audio/narration.mp3
    2. Adicionar imagens 01-10
    3. Importar SRT
    4. Ajustar zoom/pan
    5. Exportar 1080p
    """
    
    salvar(f"{video_path}/INSTRUCOES_CAPCUT.txt", instrucoes)
```

**Validação**:
- ✅ Arquivos organizados
- ✅ Instruções claras
- ✅ Testável em CapCut

---

#### 12. Agente 08: Analista de Maré (1h)
**O que faz**: Métricas → detecta eixo vencedor

**Código**:
```python
# incubadora/agentes/08_analista_mare.py
def executar():
    metricas = input_metricas_manual()
    
    # Calcular scores
    for video in metricas:
        score = calcular_mare_score(video)
    
    # Identificar vencedor
    vencedor = max(metricas, key=lambda v: v['mare_score'])
    
    relatorio = {...}
    salvar_json("outputs/T13_mare_report.json", relatorio)
```

**Teste**: Métricas simuladas

**Validação**:
- ✅ Identifica corretamente o melhor
- ✅ Recomendação clara

---

### Tarde (3h)

#### 13. Orquestrador Master (2h)
**CLI único rodando tudo**

**Código**:
```python
# orquestrador.py
import click

@click.command()
@click.option('--start', is_flag=True)
@click.option('--etapas', default='all')
def main(start, etapas):
    if start or etapas == 'all':
        executar_t0_inicializador()
        executar_t1_pesquisador()
        executar_t2_analista()
        executar_t3_arquiteto()
        executar_t4_gerador_ideias()
        executar_t5_9_produtor()
        executar_t10_editor()
        # T11-T12: manual
        executar_t13_analista_mare()
    
    print("✅ INCUBADORA COMPLETA!")
```

**Validação**:
- ✅ `python orquestrador.py --start` roda T=0→T=10
- ✅ Progress bar visual (Rich)
- ✅ Logs claros

---

#### 14. Teste Completo End-to-End (1h)
```bash
# Limpar outputs
rm -rf outputs/*

# Rodar do zero
python orquestrador.py --start

# Input
Nicho: "Fatos Curiosos"
APIs: Gemini + YouTube
Orçamento: R$ 0
Prazo: 3 dias
```

**Validação**:
- ✅ 5 vídeos completos produzidos
- ✅ Tempo total < 8h
- ✅ Nenhum erro/travamento
- ✅ Deliverables salvos em cada T

---

#### 15. Documentação Final (30min)
```
README.md:
- Setup (como instalar)
- Uso (como rodar)
- Troubleshooting

video_walkthrough.mp4:
- 10min mostrando sistema rodando
```

---

## 🛡️ COMO GARANTIR "MANSÃO" (NÃO PUXADINHO)

### Regras de Ouro

#### 1. ✅ Cada Agente = 1 Arquivo
```
❌ ERRADO: Tudo em orquestrador.py (monolítico)
✅ CERTO: 8 arquivos separados em agentes/
```

#### 2. ✅ Validação em CADA Etapa
```python
def executar():
    # 1. Validar input
    if not validar_input(data):
        raise ErroInputInvalido()
    
    # 2. Processar
    resultado = processar(data)
    
    # 3. Validar output
    if not validar_output(resultado):
        raise ErroOutputInvalido()
    
    # 4. Salvar
    salvar_deliverable(resultado)
```

#### 3. ✅ Progress Salvo SEMPRE
```python
# Depois de CADA agente
atualizar_progress(timestamp="T=X", agente="nome")
```

#### 4. ✅ Logs Claros
```python
import logging

logger.info(f"[T={timestamp}] Iniciando {agente}")
logger.info(f"[T={timestamp}] ✅ Concluído - {output_path}")
logger.error(f"[T={timestamp}] ❌ Erro: {erro}")
```

#### 5. ✅ Testes Antes de Avançar
```
Dia 1:
- Teste T=0 → OK? Avança para T=1
- Teste T=1 → OK? Avança para T=2
- ...

NÃO avançar se etapa anterior falhar!
```

---

## ✋ CHECKPOINTS DE VALIDAÇÃO

### Checkpoint Dia 1 (EOD)
- [ ] Ambiente instalado sem erros
- [ ] T=0→T=3 roda end-to-end
- [ ] 5 eixos validados
- [ ] CSV com 200+ vídeos
- [ ] Clusters identificados

**SE FALHAR**: Não começar Dia 2

---

### Checkpoint Dia 2 (EOD)
- [ ] Loop de ideias funciona (10 ideias teste)
- [ ] 150 ideias sem travar
- [ ] 1 vídeo completo produzido (roteiro+SRT+prompts+áudio)
- [ ] TTS funcionando

**SE FALHAR**: Não começar Dia 3

---

### Checkpoint Dia 3 (EOD - FINAL)
- [ ] 5 vídeos completos
- [ ] Orquestrador roda T=0→T=10 sem erros
- [ ] Documentação presente
- [ ] Outra pessoa consegue rodar (README claro)

**SE FALHAR**: Não entregar

---

## ❌ SINAIS DE PUXADINHO (RED FLAGS)

Se QUALQUER coisa abaixo acontecer → PARAR e REFATORAR:

1. ❌ Código com >200 linhas em 1 arquivo
2. ❌ IA alucinando/apagando coisas
3. ❌ Erros não tratados (crashes)
4. ❌ Deliverables não salvos
5. ❌ Código duplicado em vários lugares
6. ❌ Variáveis hard-coded (sem .env)
7. ❌ Sem testes/validação
8. ❌ Logs ausentes ou confusos

---

## ✅ CRITÉRIOS DE "PRONTO"

### MVP está pronto quando:
1. ✅ Comando `python orquestrador.py --start` roda do início ao fim
2. ✅ Input: nicho → Output: 5 vídeos completos
3. ✅ Tempo < 8h automatizadas
4. ✅ 90%+ automático (humano só aprova etapas)
5. ✅ Nenhuma alucinação (deliverables salvos)
6. ✅ README permite outra pessoa rodar
7. ✅ Código organizado (8 agentes + orquestrador)
8. ✅ Logs claros em cada etapa

---

## 🎯 PRÓXIMA AÇÃO (Aguardando Sua Aprovação)

### Opção A: Começar Dia 1 AGORA 🚀
Eu te guio passo a passo:
1. Setup ambiente
2. Agente 01
3. Testa
4. Agente 02
5. Testa
6. ...

### Opção B: Revisar Plano Primeiro 📋
Você lê este documento, faz perguntas, ajustamos o que for necessário.

### Opção C: Criar Template de Código Base 🏗️
Antes de codificar, crio estrutura básica:
```
incubadora/
├── agentes/
│   ├── __init__.py
│   ├── base.py (classe AgenteBase)
│   └── ...
├── utils/
│   ├── json_utils.py
│   ├── validators.py
│   └── ...
├── orquestrador.py
├── requirements.txt
└── .env.example
```

---

## 💬 Sua Decisão

**O plano está claro?**  
**Alguma dúvida/ajuste antes de começar?**  
**Qual opção (A, B ou C)?**
