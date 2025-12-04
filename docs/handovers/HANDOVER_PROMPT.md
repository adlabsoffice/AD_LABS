# 🚀 Prompt de Continuidade (Handover)

**Copie e cole o texto abaixo no novo chat para continuarmos exatamente de onde paramos:**

---

Estou continuando o desenvolvimento do **AD_LABS**. Aqui está o estado atual do projeto:

**1. Status Atual:**
- Acabamos de realizar uma **Auditoria Completa** (Relatório em: `d:\AD_LABS\AUDITORIA_COMPLETA_AD_LABS.md`).
- Mapeamos **Todas as Credenciais** (Relatório em: `d:\AD_LABS\TODAS_AS_CREDENCIAIS_E_APIS.md`).
- **MODO REAL ATIVADO:** Removemos os mocks do `sapg.py` e `agente_02_pesquisador.py`. Eles agora usam a API do YouTube real.
- **Configuração Crítica:** Como não tínhamos a `YOUTUBE_DATA_API_KEY` padrão, configuramos o sistema para usar a `GOOGLE_API_KEY_VIDEO` (que está no `.env`) como fallback. O sistema está configurado para **Hard Fail** (travar) se a API der erro, sem simulações.

**2. Próximos Passos Imediatos:**
- Precisamos **testar na prática** se a busca real no YouTube está funcionando com a chave configurada.
- Executar o `sapg.py` para gerar um nicho real.
- Executar o `agente_02` para buscar vídeos reais.

**3. Contexto Técnico:**
- Stack: Python + Rich + Google/Groq APIs.
- Filosofia: "Mansão" (Código robusto, sem puxadinhos).
- Regras: `d:\AD_LABS\MINHAS_REGRAS.md`.

Por favor, assuma a persona de **Arquiteto de Projetos Robusto** e vamos iniciar os testes do Modo Real.
