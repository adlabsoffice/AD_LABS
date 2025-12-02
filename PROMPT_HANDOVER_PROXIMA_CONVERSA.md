# 🔄 PROMPT DE HANDOVER - PRÓXIMA CONVERSA

## CONTEXTO COMPLETO

Você está continuando o desenvolvimento da **Incubadora AD_LABS v2.0** - sistema automatizado de criação de canais Dark YouTube.

### **Decisões Confirmadas:**
- ✅ Implementar **sistema completo** (Agentes 01-04) antes de produzir vídeos
- ✅ Canal piloto: "O Livro Caixa Divino" (Prosperidade Bíblica)
- ✅ Abordagem: **Opção C Híbrida** (25 cenas, personagem consistente, FFmpeg)
- ✅ Vídeos: 4-6 minutos (não shorts), ritmo 12s/cena

### **O Que Já Foi Feito:**
1. ✅ Workspace organizado (`old/` criada, docs consolidados)
2. ✅ Specs de todos agentes mapeadas (pasta `specs/`)
3. ✅ 9 agentes com código parcial (`incubadora/agentes/`)
4. ✅ Prompts para criar personagem "Jesus Moderno" (10 poses)
5. ✅ Pipeline técnico documentado (Opção C)
6. ✅ Guias criados: Git, Mapeamento Agentes, Estrutura

### **Agentes Faltantes (CRÍTICOS):**
- ❌ **Agente 01:** Inicializador (T=0) - Spec completa em `specs/AGENTE_01_INICIALIZADOR.md`
- ❌ **Agente 04:** Arquiteto de Eixos (T=3) - Spec em `specs/AGENTES_04-08_RESUMO.md`

### **Próxima Tarefa:**
**Implementar Agentes 01 e 04** para completar pipeline de setup do sistema.

---

## ARQUIVOS-CHAVE

📁 **Localização:** `d:\AD_LABS\`

### **Documentação Ativa:**
- `ESPECIFICACOES_TECNICAS_OPCAO_C.md` - Pipeline completo Opção C
- `PROMPTS_PERSONAGEM_JESUS_MODERNO.md` - 10 poses para criar
- `MAPEAMENTO_AGENTES.md` - Estado atual specs vs código
- `GUIA_GIT_BACKUP.md` - Setup Git (ainda não inicializado)

### **Specs dos Agentes:**
- `specs/AGENTE_01_INICIALIZADOR.md` - Implementar PRIMEIRO
- `specs/AGENTE_02_PESQUISADOR.md`
- `specs/AGENTE_03_ANALISTA.md`
- `specs/AGENTES_04-08_RESUMO.md` - Implementar Agente 04 daqui

### **Código Existente:**
- `incubadora/agentes/agente_02_pesquisador.py` - ✅ Pronto
- `incubadora/agentes/agente_03_narrador.py` - ✅ Pronto
- `incubadora/agentes/agente_05_roteirista.py` - ⚠️ Adaptar para 4-6min
- `incubadora/agentes/agente_06_visual.py` - ⚠️ Adaptar para 25 cenas
- `incubadora/agentes/agente_07_editor.py` - ⚠️ Implementar FFmpeg avançado
- (agentes 08-11 também existem)

### **Projeto Piloto:**
- `incubadora/canais/o_livro_caixa_divino/BIBLIA_DO_CANAL.md` - 149 ideias prontas
- `incubadora/canais/o_livro_caixa_divino/CONFIGURACAO_DETALHADA_LIVRO_CAIXA.md`

---

## PLANO DE IMPLEMENTAÇÃO

### **Fase Atual: 3 - Implementação Sistema Completo**

```markdown
### Fase 3: Implementação Sistema Completo
- [ ] Implementar Agente 01: Inicializador (T=0)
- [ ] Implementar Agente 04: Arquiteto Eixos (T=3)
- [ ] Adaptar Agentes 02-03 (validar funcionamento)
- [ ] Adaptar Agentes 05-11 para vídeos 4-6min (25 cenas)
- [ ] Testar pipeline completo (T=0 até T=13)
- [ ] Validar com canal Livro Caixa Divino
```

---

## DECISÕES TÉCNICAS

### **Stack Confirmado:**
- **Imagens:** Personagem manual (10 poses) + Pollinations para cenários
- **Pós-produção:** FFmpeg avançado (começar aqui, Remotion.js depois)
- **Narração:** Google TTS (grátis)
- **GPU:** Aguardando aprovação AWS/Google (usando alternativas por ora)

### **Adaptações Necessárias:**
1. **Agente 05 (Roteirista):** 1000-1500 palavras (não 600-800)
2. **Agente 06 (Visual):** 25 prompts (não 10-12)
3. **Agente 07 (Editor):** FFmpeg com transições dinâmicas

---

## CONTEXTO DO USUÁRIO

### **Situação:**
- Trabalha muito, pouco tempo disponível
- Situação financeira difícil (priorizar stack grátis)
- Alta crença no projeto
- Prefere fazer certo que rápido
- Histórico de criar projetos e abandonar (quer evitar isso)

### **Preferências:**
- Tranquilidade no sistema antes de produzir
- Qualidade > velocidade
- Documentação clara
- Não fazer "puxadinho"

### **Habilidades:**
- Conhece APIs e programação básica
- Familiarizado com metodologia "Puxadinho vs Mansão"
- Sabe usar ferramentas IA (Midjourney, Groq, etc)
- NÃO sabe fazer edição manual de vídeo

---

## PRÓXIMA AÇÃO IMEDIATA

**Quando retomar:**

1. Ler `specs/AGENTE_01_INICIALIZADOR.md`
2. Implementar `incubadora/agentes/agente_01_inicializador.py`
3. Testar com entrada mock
4. Validar que gera `T00_config.json` corretamente

**Código esperado:** ~200 linhas Python

---

## COMANDOS ÚTEIS

### **Ver estrutura:**
```powershell
cd d:\AD_LABS
tree /F incubadora
```

### **Verificar agentes:**
```powershell
ls incubadora\agentes\*.py
```

### **Testar agente:**
```powershell
python -m incubadora.agentes.agente_01_inicializador
```

---

## REGRAS IMPORTANTES

1. ⚠️ **Sempre avisar antes de modificar código** dos agentes existentes
2. ✅ Seguir metodologia "Mansão" (planejamento > execução)
3. ✅ Atualizar `task.md` após progresso
4. ✅ Commitar no Git após mudanças significativas
5. ✅ Testar isoladamente antes de integrar

---

## STATUS ATUAL

- **Janela de contexto:** ~50% usada
- **Workspace:** ✅ Organizado
- **Git:** ❌ Não inicializado (fazer se necessário)
- **Agentes implementados:** 9/11 (parcialmente)
- **Pipeline completo:** ❌ Aguardando Agentes 01 e 04

---

**RESUMO:** Continue a implementação dos Agentes 01 e 04. O usuário quer sistema robusto antes de produzir vídeos. Seja direto, objetivo e sempre confirme antes de modificar código existente.
