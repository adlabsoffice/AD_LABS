# 🏰 PROMPT HANDOVER: INCUBADORA AD_LABS v2.0 (Fase 1B -> Fase 2)

> **⚠️ REGRA DE OURO (50% CONTEXTO):** Estamos iniciando uma nova sessão pois atingimos o limite seguro de contexto. Mantenha o rigor da metodologia "Mansão" (Qualidade, Estrutura, Sem Puxadinhos).

## 1. Status do Projeto (Onde Estamos)
Finalizamos a **Fase 1B (Refatoração Core)**. O sistema deixou de ser um script simples e agora é uma **Orquestração de Agentes** robusta.

### ✅ O Que Foi Feito (Técnico)
1.  **APIManager (`incubadora/utils/api_manager.py`):**
    *   Sistema de Fallback implementado: `Gemini` (Principal) -> `Groq` (Secundário) -> `Claude` (Emergência).
    *   Gerencia múltiplas chaves e cotas.
2.  **SAPG (`incubadora/agentes/sapg.py`):**
    *   "Super Agente de Pesquisa Global" integrado.
    *   Capaz de pesquisar tendências (simulado/real) e gerar configs complexas.
3.  **Agentes Refatorados (T1-T4):**
    *   `Agente 02 (Pesquisador)`: Valida nichos com LLM.
    *   `Agente 03 (Analista)`: Clustera e analisa vídeos com LLM.
    *   `Agente 04 (Arquiteto)`: Cria eixos narrativos estruturados.
    *   `Agente 05 (Gerador Ideias)`: Gera 30 ideias por eixo.
4.  **Orquestrador (`incubadora/run_agents.py`):**
    *   **Menu T0 Inteligente:** Se não há config, oferece:
        *   [1] Pesquisa IA (SAPG)
        *   [2] Manual (Ideia Própria)

## 2. Metodologia "Mansão" (Regras de Conduta)
*   **Não quebre o que funciona:** Sempre faça backup (`agentes_backup/`) antes de tocar em agentes funcionais.
*   **Teste Unitário:** Nunca assuma que funcionou. Rode o script do agente isolado (`python agente_X.py`) para validar.
*   **Git:** Commits frequentes e descritivos.
*   **Estética:** O output do terminal deve ser lindo (Rich), organizado e inspirador.

## 3. Próximos Passos (Fase 2: Teste de Fluxo)
O objetivo imediato desta nova sessão é **VALIDAR O FLUXO COMPLETO (T0 -> T4)**.

**Sua Missão Agora:**
1.  Rodar o teste de integração usando o novo menu do SAPG.
2.  Verificar se os arquivos JSON são gerados corretamente em `outputs/`.
3.  Se tudo funcionar, preparar o terreno para a **Fase 3 (Produção de Vídeo - T5+)**.

## 4. Comando de Inicialização
Ao abrir o terminal na nova conversa, execute imediatamente:

```powershell
python incubadora/run_agents.py --canal teste_sapg_02 --modo incubacao
```

(Use `teste_sapg_02` para garantir um teste limpo).
