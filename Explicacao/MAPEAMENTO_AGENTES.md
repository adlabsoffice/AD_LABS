# 🤖 MAPEAMENTO COMPLETO DOS AGENTES

## Situação Atual: Specs vs Código

### **📋 SPECS (Especificações - Pasta `specs/`)**

Aqui estão as **DEFINIÇÕES** de como cada agente deve funcionar:

✅ **AGENTE_01_INICIALIZADOR.md** - Setup inicial do projeto  
✅ **AGENTE_02_PESQUISADOR.md** - Pesquisa YouTube/tendências  
✅ **AGENTE_03_ANALISTA.md** - Análise de competidores  
✅ **AGENTES_04-08_RESUMO.md** - Specs dos agentes 04 a 08  

---

### **💻 CÓDIGO (Implementações - Pasta `incubadora/agentes/`)**

Aqui estão os **CÓDIGOS PYTHON** já prontos:

✅ agente_02_pesquisador.py ← Implementado  
✅ agente_03_narrador.py ← Implementado  
✅ agente_05_roteirista.py ← Implementado  
✅ agente_06_visual.py ← Implementado  
✅ agente_07_editor.py ← Implementado  
✅ agente_08_instagram.py ← Implementado  
✅ agente_09_sound_designer.py ← Implementado  
✅ agente_10_director.py ← Implementado  
✅ agente_11_archivist.py ← Implementado  

---

## 🔍 OS AGENTES "FALTANTES"

### **AGENTE 01: Inicializador**
**Status:** ⚠️ Spec existe, código compilado existe (.pyc), **código-fonte (.py) NÃO existe**

**Por que importa:**
- É o PRIMEIRO agente da cadeia (T=0)
- Captura input do usuário
- Cria arquivo `T00_config.json`
- SEM ELE, pipeline não inicia

**Solução:**
Ver AGENTE_01_INICIALIZADOR.md e implementar

---

### **AGENTE 04: ???**
**Status:** ❌ NÃO EXISTE como arquivo separado

**Onde está:**
Dentro de `AGENTES_04-08_RESUMO.md` (especificação coletiva)

**O que faz:**
Precisa verificar o arquivo `AGENTES_04-08_RESUMO.md` para saber

---

## 📊 NUMERAÇÃO DOS AGENTES

| ID | Nome | Spec | Código | Status |
|----|------|------|--------|--------|
| 01 | Inicializador | ✅ | ⚠️ (.pyc only) | **CRÍTICO** |
| 02 | Pesquisador | ✅ | ✅ | OK |
| 03 | Narrador/Analista | ✅ | ✅ | OK |
| 04 | (Ver specs) | 📦 | ❓ | **INVESTIGAR** |
| 05 | Roteirista | ❓ | ✅ | OK |
| 06 | Visual | ❓ | ✅ | OK |
| 07 | Editor | ❓ | ✅ | OK |
| 08 | Instagram | 📦 | ✅ | OK |
| 09 | Sound Designer | ❓ | ✅ | OK |
| 10 | Director | ❓ | ✅ | OK |
| 11 | Archivist | ❓ | ✅ | OK |

**Legenda:**
- ✅ Existe
- ⚠️ Parcial
- ❌ Não existe
- ❓ Não localizado ainda
- 📦 Agrupado em arquivo coletivo

---

## 🎯 PRÓXIMOS PASSOS

### **1. Ler AGENTES_04-08_RESUMO.md**
Descobrir o que é o agente 04 e se faz sentido para o projeto Livro Caixa Divino

### **2. Implementar Agente 01**
Baseado na spec `AGENTE_01_INICIALIZADOR.md`

### **3. Adaptar Agentes Existentes**
Verificar se agentes 05-11 estão alinhados com:
- Vídeos 4-6min (não shorts)
- 25 cenas por vídeo
- Personagem consistente
- FFmpeg transições

---

## 📁 ESTRUTURA DE PASTAS

```
AD_LABS/
├── specs/              ← ESPECIFICAÇÕES (como deve ser)
│   ├── AGENTE_01_INICIALIZADOR.md
│   ├── AGENTE_02_PESQUISADOR.md
│   ├── AGENTE_03_ANALISTA.md
│   └── AGENTES_04-08_RESUMO.md
│
├── incubadora/
│   └── agentes/        ← CÓDIGO REAL (o que está pronto)
│       ├── agente_02_pesquisador.py
│       ├── agente_03_narrador.py
│       ├── agente_05_roteirista.py
│       └── ...
│
└── (documentação projeto)
```

---

## ⚠️ IMPORTANTE

**Specs ≠ Código**

- `specs/` = **PLANO** (como deve funcionar)
- `agentes/` = **REALIDADE** (o que está implementado)

Nem sempre estão sincronizados!

**Próxima tarefa:** Sincronizar specs com código e adaptar para Opção C.
