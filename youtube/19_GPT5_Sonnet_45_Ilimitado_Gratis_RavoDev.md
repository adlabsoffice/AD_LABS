# 19 - GPT-5 & Sonnet 4.5 Ilimitado GRÁTIS (RavoDev 2025)

**Fonte:** Transcrição YouTube (Tech Kevin)  
**Tema:** Como usar modelos premium IA (GPT-5, Claude Sonnet 4.5) ilimitado via RavoDev CLI

---

## 🎯 Visão Geral

**RavoDev CLI** permite usar todos modelos premium de IA completamente grátis através de trials ilimitados:
- ✅ GPT-5 (OpenAI)
- ✅ Claude Sonnet 4.5 (Anthropic)
- ✅ Outros modelos latest
- ✅ **20 milhões tokens grátis** por trial
- ✅ Renovação ilimitada

**Método:** Criar contas infinitas via email tricks

---

## 🛠️ Setup Completo (Passo a Passo)

### **PASSO 1: Criar Conta RavoDev**

**1. Acessar:**
- Google → "atlode dev" ou "bravo dev aentic"
- Link: `bravo.dev/aentic`

**2. Sign Up:**
```
Email: qualquer Gmail válido
Trick: adicionar pontos entre letras!
  exemplo@gmail.com
  e.xemplo@gmail.com  
  ex.emplo@gmail.com
→ Gmail trata como MESMO email, RavoDev trata como DIFERENTES
```

**3. Confirmação:**
- Código enviado ao email
- Copiar código → Colar na página
- Nome: qualquer
- Senha: qualquer
- Site name: escolher disponível → "Agree and Start"

**4. Dashboard:**
- Dismiss tutorial popup
- Pronto para instalar CLI

---

### **PASSO 2: Instalar RavoDev CLI**

**No RavoDev Dashboard:**
- Clicar "RavoDev CLI"
- Escolher OS (Mac/Windows/Linux)

#### **Para Mac:**

```bash
# 1. Install Homebrew CLI
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 2. Install ACLI
brew install acli

# 3. Verificar instalação
acli --version
# Output: acli version 1.3.4 (ou mais recente)
```

#### **Para Windows:**

```powershell
# Download installer do site
# Executar .exe
# Verificar:
acli --version
```

#### **Para Linux:**

```bash
# Seguir instruções específicas no site
acli --version
```

---

### **PASSO 3: Gerar API Token**

**1. No Dashboard:**
- Clicar link "Create API Token"
- Email verification enviado novamente

**2. Criar Token:**
```
Name: qualquer (ex: "Kevin")
Expiration: data futura qualquer
→ Token dura ~6 horas de uso pesado
→ Create
```

**3. Salvar Token:**
- ⚠️ Token mostrado **apenas uma vez**!
- Clicar "Copy" ou "Unhide" para ver
- Se fechar janela acidentalmente: criar novo token

---

### **PASSO 4: Login CLI**

**Terminal commands:**

```bash
# Se já usou antes, logout primeiro:
acli bravo off logout
# Output: "Logout was successful"

# Login com nova conta:
acli bravo off login

# Prompt: Email
→ Digite email usado no signup

# Prompt: API Token
→ Cole o token copiado

# Output: "Authentication successful"
```

**✅ Setup completo!**

---

## 💻 Usando RavoDev CLI

### **Workflow Básico:**

**1. Navegar para projeto:**
```bash
cd /path/to/your/project
```

**2. Iniciar RavoDev:**
```bash
acli ravo run
```

**Output:**
```
Working in directory: /path/to/your/project
Using model: gpt-5
```

**3. Interagir:**
- Digite prompts normalmente
- AI executa código generation/fixes
- Aceitar/rejeitar mudanças

---

### **Comandos Slash (/):**

#### **Trocar Modelos:**
```bash
/models
→ Lista todos modelos disponíveis
→ Selecionar: GPT-5, Claude Sonnet 4.5, etc.
```

**Modelos disponíveis:**
- GPT-5 (OpenAI latest)
- Claude Sonnet 4.5 (Anthropic)
- Outros modelos premium

#### **YOLO Mode:**
```bash
/yolo
→ Toggle ON: Skip confirmations
→ AI runs até task complete sem perguntar
```

**Útil para:** Deixar AI trabalhar sozinha

#### **Outros Comandos:**
```bash
/clear          # Limpa session history
/copy           # Copia última resposta
/directories    # Gerencia dirs
/feedback       # Enviar feedback
/help           # Lista todos comandos
/usage          # Verifica tokens usados
```

---

## 🎨 Exemplo Prático (Vídeo)

**Projeto:** Melhorar codebase existente

**Prompt:**
> "Suggest improvements for my codebase"

**Resultado:**
- AI analisa código
- Sugere refactorings
- Implementa mudanças automaticamente
- **Funcionando perfeitamente**

**Comparação com Cursor:**
> "This is pretty much even better than Cursor VIP"

---

## ♻️ Renovando Trials (Ilimitado)

**Quando trial acabar (20M tokens):**

```bash
# 1. Logout
acli bravo off logout

# 2. Criar nova conta RavoDev
→ Usar email trick (adicionar pontos)
→ exemplo@gmail.com → e.xemplo@gmail.com

# 3. Gerar novo API token

# 4. Login novamente
acli bravo off login
→ Email novo
→ Token novo

# ✅ Mais 20M tokens!
```

**Tempo para usar 20M tokens:** ~6 horas uso intensivo

---

## 📊 Comparação: RavoDev vs Cursor

| Feature | Cursor | RavoDev CLI |
|---------|--------|-------------|
| Free tier | 2 weeks trial | **Ilimitado** (email trick) |
| Modelos | Limited | **Todos latest** |
| IDE | Próprio | **Any** (VSCode, terminal) |
| Confirmations | Automático | Customizável (/yolo) |
| Vibe coding | ✅ | ✅ |
| Voice commands | ❌ | ❌ |
| Price after trial | $20/mês | **$0 forever** |

**Vantagens RavoDev:**
- ✅ Trials infinitos
- ✅ Modelos sempre atualizados
- ✅ Funciona em qualquer IDE/terminal
- ✅ YOLO mode (hands-off)

---

## ✅ Checklist de Uso

### **Primeira Vez:**
- [ ] Criar conta RavoDev (email trick pronto)
- [ ] Install CLI (Homebrew ou Windows installer)
- [ ] Verificar instalação (`acli --version`)
- [ ] Gerar API token
- [ ] Login CLI
- [ ] Testar comando básico

### **Uso Diário:**
- [ ] `cd project/`
- [ ] `acli ravo run`
- [ ] `/models` → escolher modelo
- [ ] `/yolo` → ativar
- [ ] Prompt → AI trabalha
- [ ] Accept changes

### **Quando Trial Acabar:**
- [ ] `acli bravo off logout`
- [ ] Nova conta (email com ponto diferente)
- [ ] Novo token
- [ ] Login novamente
- [ ] Continue coding

---

## 🎓 Dicas e Tricks

### **Email Trick (Gmail):**
```
Original: johndoe@gmail.com

Variations (TODAS recebem emails em MESMA caixa):
j.ohndoe@gmail.com
jo.hndoe@gmail.com
joh.ndoe@gmail.com
john.doe@gmail.com
j.o.h.n.d.o.e@gmail.com
```

**Resultado:** ~100+ contas RavoDev com 1 Gmail!

### **Otimizar Workflow:**
1. Sempre ativar `/yolo` no início
2. Escolher modelo antes de prompt longo
3. Use `/clear` se context window ficar grande
4. Monitor `/usage` periodicamente

### **Melhor Modelo para Cada Task:**
- **Code generation:** GPT-5
- **Code review:** Claude Sonnet 4.5
- **Debugging:** GPT-5
- **Refactoring:** Claude Sonnet 4.5

---

## ⚠️ Limitações e Avisos

**Técnicas:**
- ⚠️ 20M tokens não é infinito (mas renova fácil)
- ⚠️ 6h uso intensivo = trial acabado
- ⚠️ CLI não tem GUI (terminal only)

**Éticas:**
- ⚠️ Email trick pode violar ToS (use por sua conta)
- ⚠️ RavoDev pode bloquear padrões suspeitos
- ⚠️ Não abuse (cria contas só quando precisar)

**Práticas:**
- Use para projetos legítimos
- Não revenda acesso
- Suporte desenvolvedores se puder ($)

---

## 🔗 Links e Recursos

**Principais:**
- RavoDev: `bravo.dev`
- Dashboard: `bravo.dev/aentic`
- Docs: (verificar site)

**Instalação:**
- Homebrew (Mac): `brew.sh`
- Windows installer: (download do site)

---

## 💡 Por Que Funciona?

**RavoDev Business Model:**
- Oferece trials generosos para adoção
- Espera converter para paid tiers
- Email trick explora sistema de trials

**Sustentabilidade:**
- Pode mudar políticas qualquer momento
- Aproveite enquanto disponível
- Considere paid se usar profissionalmente

---

## 🎬 Conclusão

RavoDev CLI = **Melhor forma de usar modelos premium grátis** (GPT-5, Sonnet 4.5):
- Setup: 10 minutos
- Custo: $0
- Limite: Ilimitado (email trick)
- Qualidade: Mesma dos pagos

**Próximos passos:** 
1. Criar primeira conta
2. Testar em projeto real
3. Comparar com Cursor
4. Renovar quando necessário

**Quote do vídeo:**
> "This is pretty much the best way out there to vibe code completely for free... even better than Cursor VIP."
