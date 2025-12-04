# 🤖 HANDOVER GENERATOR PROMPT

**Objetivo:** Criar um documento de handover PERFEITO para que o próximo agente (ou você mesmo no futuro) possa retomar o trabalho instantaneamente, sem perda de contexto.

---

## 📝 Instruções para a IA

Você deve analisar TODO o contexto atual (arquivos abertos, histórico de chat, `task.md`, `implementation_plan.md`) e gerar um arquivo Markdown chamado `HANDOVER_FINAL.md` (ou atualizar o existente) seguindo estritamente a estrutura abaixo.

### Estrutura do Handover

```markdown
# 🚀 HANDOVER: [Nome do Projeto/Tarefa]
**Data:** [Data Atual]
**Status:** [✅ Estável / 🚧 Em Progresso / 🛑 Bloqueado]
**Próximo Passo Imediato:** [Ação clara e direta para começar]

---

## 🧠 Contexto & Decisões (O "Porquê")
*Explique as decisões tomadas para que o próximo não tente "consertar" o que foi proposital.*
- **Decisão X:** Fizemos assim porque...
- **Mudança Y:** Alteramos a estrutura para...
- **Ponto de Atenção:** Cuidado com o arquivo Z...

## 🏗️ Estado Atual (O "Onde")
*Liste os arquivos críticos e seu estado.*
- `caminho/arquivo.ext`: [O que foi feito nele]
- `caminho/arquivo2.ext`: [O que falta fazer]

## 📋 Checklist de Retomada
- [ ] Ler este Handover
- [ ] Carregar regras (`MINHAS_REGRAS.md`)
- [ ] [Próxima tarefa do task.md]
- [ ] [Tarefa subsequente]

## 🚨 Alertas & Riscos
- [ ] [Algo que pode quebrar]
- [ ] [Dependência faltando]

---

> **Comando de Retomada Sugerido:**
> "Olá! Li o HANDOVER. Vamos continuar com [Próximo Passo Imediato]."
```

---

## 🚀 Como Executar

1.  **Analise** o estado atual do projeto.
2.  **Preencha** o template acima com informações REAIS e ESPECÍFICAS.
3.  **Salve** o arquivo em `d:\AD_LABS\incubadora\docs\HANDOVER_FINAL.md`.
4.  **Avise** o usuário que o handover está pronto.
