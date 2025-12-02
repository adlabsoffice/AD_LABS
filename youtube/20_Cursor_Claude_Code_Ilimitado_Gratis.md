# 20 - Cursor + Claude Code Ilimitado GRÁTIS (Melhor que Trial)

**Fonte:** Transcrição YouTube (Tech Kevin)  
**Tema:** Usar vibe coding ilimitado com RavoDev CLI + website deployment completo

---

## 🎯 O Que Este Tutorial Ensina

**Resultado final:**
- ✅ Vibe coding ilimitado (Claude Sonnet 4.5, GPT-5)
- ✅ Criar website do zero
- ✅ Deploy live (grátis)
- ✅ **Sem cartão de crédito**
- ✅ **Sem conhecimento técnico**

**Método:** RavoDev CLI trial infinito

---

## 🛠️ Setup RavoDev (Resumido)

### **PASSO 1: Criar Conta**

```
1. Google → "ravoev"
2. Click "Try Now"
3. Email: usar Gmail trick (pontos!)
   - exemplo@gmail.com
   - e.xemplo@gmail.com (nova conta, mesmo inbox)
4. Verification code → Email
5. Nome + senha: qualquer
6. Site name: escolher disponível
7. "Agree and Start"
```

---

### **PASSO 2: Install CLI**

#### **Mac:**
```bash
# Terminal
brew install acli
acli --version
```

#### **Windows:**
```powershell
# Download .exe do site
# Install
acli --version
```

---

### **PASSO 3: API Token**

```
1. Dashboard → "Create API Token"
2. Email verification code
3. Name: qualquer
4. Expiration: 6h+ na frente
5. Create → COPY token
```

---

### **PASSO 4: Login**

```bash
# Se usou antes, logout:
acli bravo off logout

# Login:
acli bravo off login
# Email: o que usou no signup
# API Token: colar o copiado

# Output: "Authentication successful"
```

---

## 🎨 Criando Website do Zero

### **Setup Projeto:**

**1. Criar diretório:**
```bash
# Mac:
cd Desktop/
mkdir tech_kevin_website
cd tech_kevin_website/

# Windows:
# Criar pasta manualmente → Right click "New Folder"
# Terminal: cd [drag & drop pasta]
```

**2. Iniciar RavoDev:**
```bash
acli ravo run
# Aguardar "Working in directory..."
```

---

### **Configurar CLI:**

**Slash commands iniciais:**

```bash
# 1. Ativar YOLO mode (skip confirmations)
/yolo
→ "YOLO mode engaged"

# 2. Trocar modelo (opcional)
/models
→ Escolher: GPT-5 ou Claude Sonnet 4.5
```

---

### **Prompt de Criação:**

**Método demonstrado no vídeo:**

**1. Encontrar inspiração:**
- Google → "awwards" (website awards)
- Escolher design bonito
- Copiar URL

**2. Prompt:**
```
Create me a React website similar to [PASTE URL]

Exemplo real:
"Create me a React website. I added a image folder with a template screenshot. I want you to create me a website exactly similar to the UX of that."
```

**3. Executar:**
- RavoDev analisa
- Vibe codes automaticamente
- Cria estrutura completa

**Tempo:** ~2-5 minutos

---

### **Resultado (Exemplo vídeo):**

**AI criou:**
- ✅ React project completo
- ✅ Images folder estruturado
- ✅ Components organizados
- ✅ Routing funcional
- ✅ **Localhost rodando**

**Instrução final AI:**
```
Your React website is ready!
Run: npm install
Then: npm run dev
Open: http://localhost:3000
```

---

## 💻 Testando Localmente

**Terminal commands:**

```bash
# Install dependencies
npm install

# Run dev server
npm run dev

# Output:
# Local: http://localhost:3000
```

**No browser:**
```
http://localhost:3000
```

**Resultado (vídeo):**
> "Wow. This is what we just created right now. Literally from one prompt... I'm actually pretty amazed by this."

**Features testadas:**
- ✅ Layout responsivo
- ✅ Navegação funcional
- ✅ Imagens carregando
- ✅ Design fiel à inspiração

---

## 🚀 Deploy no GitHub + Vercel

### **PARTE 1: GitHub**

**1. Criar repo:**
```
1. github.com → Login/Signup
2. Click "New" (botão verde)
3. Repository name: "tech_kevin_website"
4. Description: (opcional)
5. "Create repository"
```

**2. Upload files:**
```
1. Click "uploading an existing file"
2. Abrir pasta do projeto
3. Drag & drop TUDO... **EXCETO node_modules**
4. Commit message: "Create website"
5. "Commit changes"
```

**⚠️ IMPORTANTE:** NÃO fazer upload de `node_modules` (pasta gigante)

---

### **PARTE 2: Vercel**

**1. Criar conta:**
```
1. vercel.com
2. "Sign Up"
3. Choose: Hobby (FREE)
4. Name: qualquer
5. "Continue with GitHub" (conecta contas)
```

**2. Deploy:**
```
1. Dashboard → "Add New" → "Project"
2. Buscar: "tech_kevin_website"
3. Click "Import"
4. Framework preset: Auto-detected (React)
5. NÃO mudar nada
6. Click "Deploy"
```

**3. Aguardar:**
- Build automático
- Deploy completo
- **Vercel link gerado**

---

### **RESULTADO FINAL:**

**Vercel fornece:**
```
https://tech-kevin-website.vercel.app
```

**Website LIVE:**
- ✅ Acessível worldwide
- ✅ HTTPS grátis
- ✅ CDN global
- ✅ $0 custo

**Testar:**
- Abrir link
- Website idêntico ao localhost
- **100% funcional**

---

## ♻️ Atualizando Website

**Workflow:**

```bash
# 1. Modificar código localmente (via RavoDev)
acli ravo run
→ "/yolo"
→ "Add dark mode toggle"

# 2. Upload mudanças no GitHub
→ Drag & drop files atualizados
→ Commit

# 3. Vercel auto-deploys!
→ Webhook detecta mudança
→ Rebuild automático
→ Site atualizado
```

**Tempo de atualização:** ~1-2 minutos

---

## 📊 Comparação: RavoDev vs Cursor

| Feature | Cursor | RavoDev CLI |
|---------|--------|-------------|
| **Trial** | 2 semanas | Infinito (email trick) |
| **Modelos** | Limited free | Todos latest |
| **Interface** | IDE próprio | Terminal |
| **YOLO mode** | ❌ | ✅ |
| **Multi-project** | ✅ | ✅ |
| **Price pós-trial** | $20/mês | $0 |
| **Facilidade** | Mais fácil | Requer CLI |

**Quando usar cada:**
- **Cursor:** Preferência por GUI, teste rápido
- **RavoDev:** Uso prolongado, $0 budget, power users

---

## ✅ Checklist Completo (Start to Finish)

### **Setup (one-time):**
- [ ] Criar conta RavoDev (email trick)
- [ ] Install CLI (`brew install acli` ou .exe)
- [ ] Gerar API token
- [ ] Login CLI

### **Criar Website:**
- [ ] `mkdir project && cd project`
- [ ] `acli ravo run`
- [ ] `/yolo` + `/models` (escolher)
- [ ] Prompt: "Create React website..."
- [ ] Aguardar conclusão
- [ ] `npm install && npm run dev`
- [ ] Testar `localhost:3000`

### **Deploy:**
- [ ] Criar conta GitHub
- [ ] Novo repo
- [ ] Upload files (sem node_modules)
- [ ] Criar conta Vercel (Hobby)
- [ ] Import project
- [ ] Deploy
- [ ] Testar link live

### **Manutenção:**
- [ ] Modificações via RavoDev
- [ ] Upload no GitHub
- [ ] Vercel auto-deploys

---

## 🎓 Dicas Avançadas

### **Otimizar Prompts:**
```
❌ Ruim: "Make website"
✅ Bom: "Create React website similar to [URL]"
✅ Melhor: "Create React website. Tech stack: React 18, Tailwind CSS. Features: dark mode, responsive, SEO optimized. Style: modern, minimal, inspired by [URL]"
```

### **Debugging:**
```bash
# Se build falhar:
/clear  # Limpa context
→ "Fix build errors"

# Ver o que AI fez:
/copy  # Copia última response
```

### **Multi-page Sites:**
```
Prompt inicial: "Create React website with routing"
Follow-up: "Add about page, contact page, blog section"
```

---

## ⚠️ Troubleshooting

**Problema:** Node modules error  
**Fix:** Delete `node_modules`, run `npm install` novamente

**Problema:** Vercel build fail  
**Fix:** Verificar package.json scripts, ensure `"build": "react-scripts build"`

**Problema:** RavoDev trial acabou  
**Fix:** $ Logout → Nova conta (email com ponto diferente) → Login

---

## 💡 Casos de Uso

**O que você pode criar:**
1. **Portfolio pessoal** - React + Vercel = grátis
2. **Landing pages** - Para produtos/serviços
3. **Blogs** - Com Markdown support
4. **Dashboards** - Admin panels
5. **E-commerce** - Frontend (backend separado)

**Limitações:**
- ❌ Backend complexo (use Supabase/Firebase separado)
- ❌ Databases (integrar externamente)
- ✅ Frontend = 100% coberto

---

## 🔗 Links Úteis

**Ferramentas:**
- RavoDev: `bravo.dev`
- GitHub: `github.com`
- Vercel: `vercel.com`
- Awwards (inspiração): `awwwards.com`

**Docs:**
- React: `react.dev`
- Vercel docs: `vercel.com/docs`
- RavoDev CLI: (verificar site)

---

## 🎬 Conclusão (Quote do Vídeo)

> "This is literally perfect. If I saw this website in real life, I would think a real company made this... From one single prompt, it literally created everything."

**Stack completo $0:**
- RavoDev CLI (vibe coding)
- GitHub (version control)
- Vercel (hosting + CDN)

**Tempo total:** Setup 30min → Sites infinitos depois

**Próximos passos:**
1. Criar primeira conta
2. Deploy primeiro site
3. Compartilhar link
4. Iterar e melhorar
