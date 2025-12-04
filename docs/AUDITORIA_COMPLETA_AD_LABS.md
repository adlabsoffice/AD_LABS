# 🕵️ Relatório de Auditoria Completa: AD_LABS

**Data:** 03/12/2025
**Escopo:** Workspace `d:\AD_LABS` (excluindo `old` e `d:\PESQUISA\agentes`)
**Status:** ✅ Concluído

---

## 1. Visão Geral do Projeto

O **AD_LABS** é um sistema modular ("Incubadora") projetado para criar e gerenciar canais "Dark" no YouTube de forma automatizada. Ele opera em dois modos principais:
1.  **Incubação (T=0 a T=4):** Pesquisa de nicho, análise de concorrência e geração de ideias.
2.  **Produção (T=5 a T=11):** Geração de roteiro, áudio, visual e edição (atualmente em refatoração).

O sistema utiliza uma arquitetura de **Agentes Autônomos** orquestrados por scripts Python, com forte integração de LLMs (Gemini, Groq, Claude) via um gerenciador de APIs robusto.

---

## 2. Inventário e Estrutura

### 📂 Estrutura de Pastas Principal
```
d:\AD_LABS\incubadora\
├── agentes/                # Núcleo lógico (Agentes 01-11)
├── canais/                 # Configurações específicas por canal
├── config/                 # Configurações globais (api_priorities.json)
├── specs/                  # Documentação técnica (.md)
├── utils/                  # Bibliotecas compartilhadas (APIManager, ConfigParser)
├── outputs/                # Saídas geradas pelos agentes (T01, T02, etc.)
├── incubadora.py           # CLI / Frontend interativo
├── run_agents.py           # Orquestrador de pipeline
└── requirements.txt        # Dependências Python
```

### 📊 Status dos Arquivos Chave
| Arquivo | Tipo | Status | Obs |
|---------|------|--------|-----|
| `incubadora.py` | CLI | ⚠️ Alerta | Mistura UI com lógica |
| `run_agents.py` | Orquestrador | ⚠️ Alerta | Modo Produção pausado/híbrido |
| `agentes/sapg.py` | Agente | ✅ Real | **Zero Mocks**. Busca Trends via YouTube API (Hard Fail) |
| `agentes/agente_02...py` | Agente | ✅ Real | Busca Vídeos via YouTube API (Hard Fail) |
| `utils/api_manager.py` | Util | ✅ Ótimo | Sistema robusto de fallback e retry |
| `utils/config_parser.py` | Util | ✅ Bom | Parser de Markdown funcional |

---

## 3. Análise Crítica

### ✅ Pontos Fortes
1.  **Arquitetura Modular:** A separação em agentes (T=0, T=1...) é excelente e facilita manutenção.
2.  **APIManager Robusto:** O sistema de fallback entre Gemini, Groq e Claude (`utils/api_manager.py`) é profissional e garante continuidade.
3.  **Interface Rica:** Uso extensivo da biblioteca `rich` torna a operação via terminal clara e agradável.
4.  **Zero Mocks (Total):** SAPG e Agente 02 agora usam dados reais. Agentes de produção (`agente_06`, `agente_11`) usam serviços reais (S3, ComfyUI, Imagen).

### ❌ Pontos Críticos (Atenção Imediata)
1.  **Hardcoded Paths & IDs:**
    *   `run_agents.py`: Chat ID do Telegram fixo (`7757304726`).
    *   `agente_06_visual.py`: Caminho do `workflow_api.json` depende da estrutura exata.
    *   `agente_11_archivist.py`: Espera `output/video_final.mp4` fixo.
2.  **Mistura de Legado:** O `run_agents.py` importa agentes "Old" e "Novos", indicando uma migração incompleta.

---

## 4. Workflows Detalhados

### 🔄 Processo 1: Setup de Canal (T=0)
**Objetivo:** Definir nicho e criar configuração inicial.
1.  **Entrada:** Interação do usuário via `incubadora.py`.
2.  **Passo 1:** Usuário escolhe "Setup IA" ou "Manual".
3.  **Passo 2 (IA):** Chama `sapg.py` (REAL) para buscar tendências no YouTube.
4.  **Passo 3:** Gera `T00_config.json` com definições do canal.
5.  **Saída:** Arquivo `T00_config.json` e estrutura de pastas em `canais/`.

### 🔄 Processo 2: Incubação (T=1 a T=4)
**Objetivo:** Gerar banco de ideias validadas.
1.  **Entrada:** `T00_config.json`.
2.  **Passo 1 (Agente 02):** Busca vídeos reais no YouTube via API -> Gera `T01_canais_referencias.csv`.
3.  **Passo 2 (Agente 03):** Lê CSV, limpa e agrupa (Clustering) -> Gera `T02_clusters.json`.
4.  **Passo 3 (Agente 04):** Transforma clusters em 5 Eixos Narrativos -> Gera `T03_eixos/`.
5.  **Passo 4 (Agente 05):** Gera 150 ideias (30/eixo) via LLM -> Gera `outputs/T04_ideias/`.
6.  **Saída:** Banco de 150 ideias JSON prontas para produção.

### 🔄 Processo 3: Produção (T=5+) - *Em Refatoração*
**Objetivo:** Transformar ideia em vídeo final.
1.  **Entrada:** Uma ideia escolhida do T=4.
2.  **Passo 1 (Roteiro):** (Pendente de migração para novo formato).
3.  **Passo 2 (Visual - Agente 06):** Gera imagens via Google Imagen ou ComfyUI.
    *   *Falha:* Se não tiver API Key ou ComfyUI rodando, para.
4.  **Passo 3 (Arquivamento - Agente 11):** Upload para Drive e S3.
    *   *Dependência:* Requer `boto3` e credenciais configuradas.

---

## 5. Checklist de Melhorias Sugeridas

### 🔴 Prioridade Alta (Correções)
- [x] **Substituir SAPG:** Implementado pesquisa real via YouTube Data API (Hard Fail).
- [x] **Conectar YouTube API (Agente 02):** Implementado `YouTubeConnector` real.
- [ ] **Externalizar Configs:** Remover IDs hardcoded (Telegram, Paths) e mover tudo para `.env` ou `config.json`.

### 🟡 Prioridade Média (Estabilidade)
- [ ] **Unificar Pipeline:** Limpar `run_agents.py` removendo referências a agentes "Old" e finalizar a conexão da Produção com as novas Ideias (T=4).
- [ ] **Validar Dependências:** Criar um `check_env.py` que valida se todas as chaves do `api_priorities.json` estão carregadas antes de rodar.

### 🟢 Prioridade Baixa (Polimento)
- [ ] **Refatorar ConfigParser:** Tornar o regex mais flexível para variações no Markdown.
- [ ] **Logs Centralizados:** Mover prints do `console` para um arquivo de log rotativo para debug posterior.

---

**Conclusão:** O projeto tem uma base sólida e profissional ("Mansão"), mas algumas "paredes" (SAPG, Agente 02) são cenográficas ("Puxadinho"). A prioridade deve ser substituir essas simulações por dados reais para garantir que o conteúdo gerado seja baseado na realidade do mercado, não em alucinações da IA.
