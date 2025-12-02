# ✅ Prompt: Quality Assurance (Validação Final do Briefing)

> **Objetivo**: Validar se o briefing está completo e pronto para detalhamento

---

## Quando Usar

Após criar seu briefing estruturado, mas ANTES de aprovar e avançar para detalhamento.

---

## 📋 Prompt de Validação

```
Você é um consultor sênior especializado em análise de requisitos e quality assurance de projetos.

Recebi o briefing abaixo para um projeto e preciso que você faça uma análise crítica ANTES de aprovar para desenvolvimento.

---
BRIEFING:
[COLE SEU BRIEFING COMPLETO AQUI]
---

Por favor, avalie o briefing segundo os critérios abaixo e dê uma nota de 0-10 para cada:

## 1. CLAREZA DO PROBLEMA (0-10)
- O problema está bem definido?
- É específico o suficiente?
- Fica claro POR QUE resolver isso?

**Nota**: __/10
**Feedback**: [comentários e sugestões]

## 2. DEFINIÇÃO DE USUÁRIOS (0-10)
- Os usuários estão bem caracterizados?
- Fica claro o contexto de uso?
- As motivações/objeções foram consideradas?

**Nota**: __/10
**Feedback**: [comentários e sugestões]

## 3. ESCOPO E PRIORIZAÇÃO (0-10)
- A separação Must/Should/Could/Won't faz sentido?
- O MVP é viável?
- Há features demais ou de menos?

**Nota**: __/10
**Feedback**: [comentários e sugestões]

## 4. INPUT/OUTPUT (0-10)
- Está claro o que entra no sistema?
- Está claro o que sai do sistema?
- O fluxo principal é compreensível?

**Nota**: __/10
**Feedback**: [comentários e sugestões]

## 5. VIABILIDADE TÉCNICA (0-10)
- Os requisitos técnicos são realistas?
- As integrações são factíveis?
- Há restrições técnicas claras?

**Nota**: __/10
**Feedback**: [comentários e sugestões]

## 6. RISCOS E MITIGAÇÕES (0-10)
- Os riscos principais foram identificados?
- Há planos de mitigação?
- Algo crítico foi esquecido?

**Nota**: __/10
**Feedback**: [comentários e sugestões]

## 7. CRITÉRIOS DE SUCESSO (0-10)
- É possível medir se o projeto deu certo?
- As métricas são realistas?
- Há validação com usuários planejada?

**Nota**: __/10
**Feedback**: [comentários e sugestões]

## 8. COMPLETUDE (0-10)
- Há gaps críticos de informação?
- Algo essencial ficou de fora?
- O briefing permite avançar para detalhamento?

**Nota**: __/10
**Feedback**: [comentários e sugestões]

---

## NOTA FINAL
**Média**: __/10

## STATUS
- [ ] ✅ APROVADO - Pode avançar para detalhamento
- [ ] ⚠️ APROVADO COM RESSALVAS - Corrigir [listar itens] antes
- [ ] ❌ REPROVADO - Precisa refazer [listar seções]

## GAPS CRÍTICOS IDENTIFICADOS
[Liste informações essenciais que estão faltando]

## RECOMENDAÇÕES PARA PRÓXIMA FASE
[Sugestões para o detalhamento]

## PERGUNTAS PARA O USUÁRIO RESPONDER
[Questões que precisam ser esclarecidas antes de continuar]

---

Seja rigoroso na avaliação. É melhor identificar problemas AGORA do que durante desenvolvimento.
```

---

## Como Interpretar o Resultado

### ✅ Se Nota ≥ 8.0
**Briefing aprovado!** Pequenos ajustes podem ser feitos, mas pode avançar.

### ⚠️ Se Nota 6.0 - 7.9
**Aprovado com ressalvas.** Corrija os gaps apontados antes de prosseguir.

### ❌ Se Nota < 6.0
**Reprovado.** Refaça as seções problemáticas. Não adiante sem corrigir.

---

## ⚙️ Ciclo de Refinamento

```
Briefing Inicial
    ↓
Quality Assurance (IA)
    ↓
Nota < 8.0? → Corrigir gaps → Quality Assurance novamente
    ↓
Nota ≥ 8.0? → Aprovação HUMANA
    ↓
Aprovado? → Avançar para Detalhamento
    ↓
Não aprovado? → Mais pesquisas/refinamento
```

---

## 💡 Dica

**Use clones diferentes para segunda opinião**:
- Primeira validação: Claude Opus
- Segunda validação: Elon Musk (clone)
- Terceira validação: Steve Jobs (clone - foco UX)

Se todos derem ≥ 8.0, você tem um briefing sólido.

---

## Exemplo de Resposta da IA

```
## 1. CLAREZA DO PROBLEMA (0-10)
Nota: 7/10

Feedback: O problema está relativamente claro (gestão de leads para 
dentistas), mas falta especificar:
- Qual é o problema ATUAL que eles enfrentam? (planilhas? papel?)
- Quantos leads por dia/semana eles recebem?
- Qual o custo desse problema? (leads perdidos = quanto em R$?)

Sugestão: Adicione 1-2 parágrafos sobre "situação atual vs situação 
desejada" com números concretos.

[...]

NOTA FINAL: 7.2/10

STATUS: ⚠️ APROVADO COM RESSALVAS

GAPS CRÍTICOS:
1. Não especifica volume de dados esperado
2. Não menciona LGPD/compliance
3. Critérios de sucesso são vagos

RECOMENDAÇÕES:
- Adicione seção sobre proteção de dados
- Defina métricas numéricas (ex: "reduzir perda de leads de 30% para 5%")
```

**Ação**: Corrija os 3 gaps e rode QA novamente.

---

**Esforço**: 5% Humano | 95% IA  
**Tempo estimado**: 20-40 minutos (incluindo correções)  
**Próximo passo**: Aprovação Final Humana
