# 🧠 CONTEXTO MESTRE: PROJETO INCUBADORA (Fonte Única da Verdade)
> **ATENÇÃO IA:** Este arquivo é a autoridade máxima sobre o projeto. Leia-o ANTES de qualquer ação. Se houver conflito com outras fontes, este arquivo prevalece.

---

## 1. 📍 ONDE ESTAMOS (Status Imediato)
*   **Data da Última Atualização:** 30/11/2025 08:12
*   **Fase:** Refatoração Sistêmica (Tornando Incubadora Universal).
*   **Objetivo Atual:** Implementar sistema de configuração baseado em MD para todos os agentes.
*   **Status:** 🔧 EM PROGRESSO. 
    *   ✅ `utils/config_parser.py` criado e testado
    *   ✅ Agente 10 (Diretor) refatorado para ler MD
    *   ⏳ Agentes 03, 05, 06 ainda usam valores hardcoded
*   **Bloqueio Atual:** Nenhum. Continuando refatoração.

---

## 2. 🏭 A FÁBRICA (Infraestrutura)
A "Incubadora" é uma pipeline de automação de vídeo híbrida e **PARAMETRIZÁVEL POR CANAL**.

### Componentes Ativos:
*   **Orquestrador:** `run_agents.py` (Maestro local Python)
*   **Config Parser:** `utils/config_parser.py` - **NOVO**
    *   Lê arquivos `CONFIGURACAO_DETALHADA_*.md`
    *   Extrai regras por seção (audio, visual, producao, etc)
    *   Permite que agentes sejam 100% dinâmicos
*   **Agentes de Produção:**
    *   Agente 02: Pesquisador (Green Dot)
    *   Agente 05: Roteirista (Gemini)
    *   Agente 03: Narrador (Google TTS)
    *   Agente 06: Visual (Flux.1/Pollinations)
    *   Agente 09: Sound Designer (Mixagem)
    *   **Agente 10: Diretor (QA/Gatekeeper)** - ✅ Refatorado (usa MD)
    *   Agente 11: Arquivista

### Arquitetura de Configuração (NOVO):
```
Canal/
├── CONFIGURACAO_DETALHADA_*.md  ← FONTE DA VERDADE (1500+ linhas, todos os campos)
├── BIBLIA_DO_CANAL.md           ← Identidade (Tom, Persona, Estilo)
└── config.json                  ← Cache/Resumo (compatibilidade legada)
```

**Filosofia:** 
- Arquivo MD = Template preenchido (igual formulário completo)
- Agentes leem APENAS sua seção do MD
- Se criar canal de Shorts, basta mudar valores no MD (não mexe em código)

---

## 3. 🎬 CANAL PILOTO: O LIVRO CAIXA DIVINO
*   **Status:** REAL (não é mock).
*   **Config MD:** `d:\AD_LABS\incubadora\canais\o_livro_caixa_divino\CONFIGURACAO_DETALHADA_LIVRO_CAIXA.md`
*   **Nicho:** Prosperidade Bíblica / Finanças
*   **Formato:** React (Jesus vs Gurus)
*   **Duração Alvo:** 4-6 minutos
*   **Regras Críticas (extraídas do MD):**
    *   Ritmo Visual: Máx 8s/cena
    *   Densidade: Mín 1000 palavras
    *   Velocidade Fala: 1.1x
    *   WPM: 168-187

---

## 4. 🔄 SISTEMA DE QUALIDADE (Gatekeeper)
**Agente 10 (Diretor):**
- ✅ Implementa Hard Veto (bloqueio total se < 1000 palavras ou ritmo > 8s)
- ✅ Lê regras do MD automaticamente
- ✅ Loop de correção automática (até 3 tentativas)
- ✅ Feedback estruturado para Agente 05 re-gerar

**Flow de Reprovação:**
```
Agente 05 gera roteiro
    ↓
Agente 10 audita
    ↓
Se REPROVAR → Feedback para Agente 05 → Refaz (até 3x)
    ↓
Se APROVAR → Segue para Agente 03 (Narração)
```

---

## 5. 📝 PRÓXIMOS PASSOS (Roadmap Imediato)
1. ✅ Criar `config_parser.py`
2. ✅ Refatorar Agente 10 para usar MD
3. ⏳ Refatorar Agente 03 (Narrador) para ler velocidade do MD
4. ⏳ Refatorar Agente 05 (Roteirista) para ler densidade/WPM do MD
5. ⏳ Refatorar Agente 06 (Visual) para ler preset/provider do MD
6. ⏳ Testar produção completa com sistema MD
7. ⏳ Criar walkthrough.md documentando sistema

---

## 6. 🚫 NÃO MEXER (Dependências Externas)
*   n8n: `http://44.221.49.174:5678` (AWS)
*   ComfyUI: `http://136.119.237.19:8188` (Google Cloud)

---

## 7. 📚 DOCUMENTOS DE REFERÊNCIA
*   **Template Mestre:** `d:\AD_LABS\CONFIGURACAO_DETALHADA_TODOS_CAMPOS.md` (1523 linhas)
*   **Bíblia do Canal:** `d:\AD_LABS\incubadora\canais\o_livro_caixa_divino\BIBLIA_DO_CANAL.md`
*   **Regras Top 100:** `d:\AD_LABS\incubadora\REGRAS_OURO_100_MAIORES.md`
