# 22 - Cursor Ilimitado GRÁTIS + Full Deploy (Melhor que Claude Code)

**Fonte:** Transcrição YouTube (Tech Kevin)  
**Tema:** Tutorial completo RavoDev CLI para criar + hospedar websites com todas features do Cursor

---

## 🎯 O Que Este Tutorial Cobre

**Stack completo:**
- ✅ Vibe coding ilimitado (RavoDev CLI)
- ✅ Cursor features equivalentes
- ✅ Website creation
- ✅ GitHub version control
- ✅ Vercel deployment (CDN global)
- ✅ **$0 custo total**

**Quote:**
> "This is going to be the best video of AI you've ever seen... and it's completely for free."

---

## 💻 Setup RavoDev CLI (Detalhado)

### **PASSO 1: Criar Conta**

```
1. Google → "ravoev"
2. First link: bravo.dev
3. Click "Try Now" (yellow button)
4. Email: Gmail trick!
   - Use pontos para criar "novos" emails
   - exemplo@gmail.com → e.xemplo@gmail.com
5. Sign up
6. Verification code → Email
7. Nome: qualquer
8. Senha: qualquer
9. Site name: escolher disponível (green check)
10. "Agree and Start"
11. Load screen → Dismiss popup
```

---

### **PASSO 2: Install RavoDev CLI**

**No Dashboard:**
- Click "RavoDev CLI"

#### **Mac:**
```bash
# 1. Click "Mac" tab
# 2. Copy first command (Homebrew)
/bin/bash -c "$(curl -fsSL ...)"

# 3. Open Terminal → Paste → Enter
# 4. Copy second command
brew install acli

# 5. Terminal → Paste → Enter
# 6. Verificar:
acli --version
# Output: "ACLI version 1.3.4" (ou newer)
```

#### **Windows:**
```powershell
# 1. Click "Windows" tab
# 2. Download .exe installer
# 3. Run as administrator
# 4. Verify:
acli --version
```

#### **Linux:**
```bash
# Follow Linux tab instructions
acli --version
```

---

### **PASSO 3: API Token Generation**

```
1. Close CLI window
2. Click "Atlin account" link
3. Email verification code → Check email
4. Paste code
5. "Create API token"
6. Name: qualquer ("Kevin")
7. Expiration: escolher data futura
   → Trial dura ~6h uso intenso
8. Click "Create"
9. ⚠️ KEEP WINDOW OPEN!
10. View token: Click eye icon (opcional)
11. Click "Copy" (clipboard confirmation)
```

---

### **PASSO 4: Login CLI**

**Terminal commands:**

```bash
# Se já usou antes, LOGOUT primeiro:
acli bravo off logout
# Output: "Logout was successful"

# Login com nova conta:
acli bravo off login

# Prompt 1: Email
→ DIGITE manualmente (copy/paste pode ter caracteres invisíveis)
→ Email que usou no signup

# Prompt 2: API Token
→ Paste o token copiado

# Output: "Authentication successful"
```

**✅ RavoDev CLI configurado!**

---

## 🎨 Criando Website

### **PASSO 1: Setup Diretório**

#### **Mac/Linux:**
```bash
# Desktop or qualquer pasta
mkdir Kevin_Cursor_Website
cd Kevin_Cursor_Website
```

#### **Windows:**
```
1. Right-click Desktop
2. New → Folder
3. Name: "Kevin_Cursor_Website"
4. Terminal:
cd [drag and drop folder]
```

**Confirmar:**
```bash
# Pasta vazia
ls  # (Mac/Linux)
dir # (Windows)
```

---

### **PASSO 2: Iniciar RavoDev**

```bash
acli ravo dev run

# Output:
# "Working in directory: .../Kevin_Cursor_Website"
# "Using model: gpt-5" (ou outro)
```

**Interface CLI ativa!**

---

### **PASSO 3: Configurar CLI**

**Slash commands:**

#### **1. Trocar Modelo (opcional):**
```bash
/models
→ Arrow keys para escolher:
  - GPT-5
  - Claude Sonnet 4.5
  - Outros
→ Enter
```

**Recomendação:** Claude Sonnet 4.5 para websites

#### **2. Ativar YOLO Mode:**
```bash
/yolo
→ "YOLO mode engaged"
```

**O que faz:** Skip ALL confirmations → AI roda até concluir task

#### **3. Outros Comandos Úteis:**
```bash
/clear    # Limpa context window
/usage    # Ver tokens usados
/help     # Lista todos comandos
/memory   # Gerenciar memória
```

---

### **PASSO 4: Criar Website (Prompt)**

**Estratégia (demonstrada):**

**1. Encontrar Inspiração:**
- Google → "awwards" (website awards)
- Escolher design award-winning
- Copiar URL

**2. Prompt:**
```
Create me a React website similar to [PASTE URL DO AWWARDS]
```

**Exemplo real (vídeo):**
```
Create me a React website similar to [awwards design URL]
```

**3. AI Executa:**
- Analisa URL de inspiração
- Cria project structure
- Installs dependencies
- Generates components
- **Faz tudo automaticamente** (YOLO mode)

**4. Aguardar Conclusão:**
- Terminal mostra progresso
- "Success message" ao final
- Instrução para rodar: `localhost:3000`

---

### **RESULTADO (Demonstrado):**

**AI gerou:**
- ✅ React app completo
- ✅ Routing funcional
- ✅ Components organizados
- ✅ Imagens de casas (real estate theme)
- ✅ Páginas: Home, Properties, About, Contact
- ✅ **Mobile responsive**

**Qualidade (quote):**
> "This is actually pretty nice... for one prompt. For 1-2 prompts, this is the result that we got."

**Funcionalidades testadas:**
- ✅ Links funcionam
- ✅ Mobile-friendly (testado no vídeo)
- ✅ Todas páginas navegáveis
- ✅ Layout profissional

---

## 🖥️ Rodar Localmente

**Terminal (na pasta do projeto):**

```bash
# Install dependencies (se necessário)
npm install

# Run dev server
npm run dev

# Output:
# "Local: http://localhost:3000"
```

**Browser:**
```
http://localhost:3000
```

**Preview:** Website totalmente funcional!

---

## 🚀 Deploy (GitHub + Vercel)

### **PARTE 1: GitHub**

**1. Criar Conta:**
```
1. github.com
2. "Sign Up" (ou Login se já tem)
3. Opções:
   - Email
   - Gmail account (recomendado)
   - Apple account
```

**2. Criar Repositório:**
```
1. Dashboard → Green "New" button
2. Repository name: "kevin-cursor-website"
3. Description: (opcional)
4. Public (default)
5. "Create repository"
```

**3. Upload Código:**
```
1. "Uploading an existing file" link
2. Abrir pasta do projeto
3. **Drag & drop TUDO EXCETO:**
   - ❌ node_modules (muito grande!)
4. Commit message: "Create website"
5. "Commit changes"
```

**Aguardar upload:** Pode demorar alguns minutos

---

### **PARTE 2: Vercel**

**1. Criar Conta:**
```
1. vercel.com
2. "Sign Up"
3. Choose: "Hobby" (FREE plan)
4. Name: qualquer
5. "Continue with GitHub"
   → Conecta contas automaticamente
```

**2. Import Project:**
```
1. Dashboard → "Add New" → "Project"
2. Search: "kevin-cursor-website"
3. Aparece na lista → Click "Import"
```

**3. Configure (Auto-detected):**
```
Framework Preset: Create React App (auto)
Root Directory: ./
Build Command: npm run build (auto)
Output Directory: build (auto)

→ NÃO MUDAR NADA
```

**4. Deploy:**
```
Click "Deploy"
→ Aguardar build (1-2 minutos)
→ Confetti animation = Sucesso!
```

**5. Obter Link:**
```
Dashboard → Project → Visit
URL: https://kevin-cursor-website.vercel.app
```

---

### **RESULTADO FINAL:**

**Website LIVE:**
- ✅ HTTPS grátis
- ✅ CDN global (Vercel edge network)
- ✅ Custom domain support (opcional)
- ✅ **$0 custo**

**Testar:**
- Abrir URL em qualquer device
- Compartilhar com amigos
- **100% funcional worldwide!**

---

## 🔄 Atualizando Website

**Workflow:**

```bash
# 1. Modificar código (via RavoDev)
cd kevin-cursor-website/
acli ravo dev run
→ "/yolo"
→ "Add dark mode toggle to navigation"

# AI implementa mudança

# 2. Upload para GitHub
→ Drag & drop files atualizados (exceto node_modules)
→ Commit

# 3. Vercel auto-deploys!
→ Webhook detecta push
→ Rebuild automático (~1 min)
→ Site atualizado!
```

**Continuous deployment:** GitHub → Vercel pipeline automático

---

## 📊 Comparação: RavoDev vs Cursor

| Feature | Cursor IDE | RavoDev CLI |
|---------|------------|-------------|
| **Interface** | GUI (próprio IDE) | Terminal |
| **Free Trials** | 2 semanas | **Ilimitado** (email trick) |
| **Modelos** | Limited | **Todos latest** |
| **YOLO mode** | ❌ | ✅ |
| **Context window** | Limited | Similar |
| **Usage tracking** | Built-in | `/usage` command |
| **Ease of use** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Cost pós-trial** | $20/mês | **$0** |
| **Flexibility** | Medium | High |

**Quando usar cada:**
- **Cursor:** Prefere GUI, teste rápido, primeira vez
- **RavoDev:** Uso prolongado, CLI confortável, $0 budget

---

## ✅ Checklist Full Stack (Start to Finish)

### **Setup (one-time):**
- [ ] Criar conta RavoDev
- [ ] Install CLI (`brew install acli` ou .exe)
- [ ] Gerar API token
- [ ] Login CLI (`acli bravo off login`)

### **Website Creation:**
- [ ] `mkdir project && cd project`
- [ ] `acli ravo dev run`
- [ ] `/models` → escolher Claude 4.5
- [ ] `/yolo` → ativar
- [ ] Prompt: "Create React website similar to [URL]"
- [ ] Aguardar AI concluir
- [ ] `npm install && npm run dev`
- [ ] Test `localhost:3000`

### **GitHub:**
- [ ] Criar conta github.com
- [ ] Novo repositório
- [ ] Upload files (sem node_modules!)

### **Vercel:**
- [ ] Criar conta vercel.com (Hobby tier)
- [ ] Import GitHub repo
- [ ] Deploy
- [ ] Test live URL

### **Manutenção:**
- [ ] Modificações via RavoDev
- [ ] Push para GitHub
- [ ] Vercel auto-rebuild

---

## 🎓 Dicas Avançadas

### **Melhorar Prompts:**
```
❌ Básico: "Make a website"
✅ Bom: "Create React website similar to [URL]"
✅ Melhor: "Create React 18 website. Tech: Tailwind CSS, React Router. Features: dark mode, blog, contact form. Design inspiration: [URL]"
```

### **Debug Fast:**
```bash
# Se algo deu errado:
/clear  # Reset context
→ "Fix all errors in the codebase"

# Ver todas mudanças:
/copy  # Copia última response
```

### **Multi-Feature Requests:**
```
Prompt inicial: "Create website with..."
Follow-ups:
- "Add authentication"
- "Add blog section with Markdown support"
- "Integrate Stripe checkout"
```

---

## 💡 Casos de Uso Reais

**O que criar:**
1. **Portfolio** - Mostrar trabalhos (designers, devs)
2. **Landing pages** - Produtos/serviços (conversão)
3. **Blogs** - Content creation platforms
4. **Dashboards** - Admin panels, analytics
5. **E-commerce** -Frontend (backend separado)
6. **Apps SaaS** - MVPs rápidos

**Limitações:**
- ❌ Backend complexo (adicione Firebase/Supabase)
- ❌ Databases built-in (integre externalmente)
- ✅ Frontend = 100% coberto por RavoDev

---

## ⚠️ Troubleshooting

**Problema:** `npm install` errors  
**Fix:** Delete `package-lock.json` + `node_modules` → retry

**Problema:** Vercel build failed  
**Fix:** Check `package.json` scripts → ensure `"build": "react-scripts build"`

**Problema:** GitHub upload stuck  
**Fix:** Verifique tamanho files (node_modules SEMPRE excluir!)

**Problema:** RavoDev trial ended  
**Fix:** Logout → Nova conta (email com ponto diferente) → Login

---

## 🔗 Stack de Links

**Ferramentas:**
- RavoDev: `bravo.dev`
- GitHub: `github.com`
- Vercel: `vercel.com`
- Awwards (design): `awwwards.com`

**Docs:**
- React: `react.dev`
- Vercel docs: `vercel.com/docs`
- GitHub guides: `docs.github.com`

---

## 🎬 Conclusão (Quote Vídeo)

> " We literally didn't do any coding. We just typed in prompts. This is the best vibe coding video you've ever watched."

**Full stack gratuito:**
- RavoDev CLI: Código
- GitHub: Version control
- Vercel: Hosting + CDN

**Tempo total:** 30min setup → Sites infinitos depois

**Custo total:** $0

**Resultado:** Websites production-ready compartilháveis worldwide

**Próximos passos:**
1. Setup hoje
2. Criar primeiro site
3. Deploy e compartilhar
4. Iterar features
5. Build portfolio de projetos!
