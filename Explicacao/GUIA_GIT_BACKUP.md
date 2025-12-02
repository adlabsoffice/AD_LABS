# 🔄 GUIA: BACKUP GIT DO PROJETO

## Por Que Git AGORA?

✅ **Proteção contra perda** - Sistema complexo com muitas partes  
✅ **Histórico de mudanças** - Ver o que funcionou/quebrou  
✅ **Colaboração futura** - Compartilhar com outros ou você mesmo em outro PC  
✅ **Rollback fácil** - Voltar se algo der errado  

---

## 📋 SETUP GIT (Rápido)

### **Passo 1: Verificar se Git está instalado**
```powershell
git --version
```

Se não estiver: Baixar em [git-scm.com](https://git-scm.com)

---

### **Passo 2: Inicializar repositório**
```powershell
cd d:\AD_LABS
git init
```

---

### **Passo 3: Criar .gitignore**
Criar arquivo `d:\AD_LABS\.gitignore`:
```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
.venv/

# Outputs temporários
outputs/
*.mp4
*.wav
*.mp3
*.jpg
*.png
*.webp

# Credenciais
.env
*.key
*.pem
*_secret*.json
api_keys.json

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
desktop.ini

# Logs
*.log
logs/

# Backups antigos
old/
backup/
```

---

### **Passo 4: Fazer primeiro commit**
```powershell
# Adicionar tudo
git add .

# Ver o que será commitado
git status

# Commitar
git commit -m "🎬 Projeto Incubadora AD_LABS v2.0 - Setup Inicial

- Metodologia Puxadinho vs Mansão
- Canal piloto: O Livro Caixa Divino
- 9 agentes (specs + código parcial)
- Especificações Opção C Híbrida
- Prompts personagem Jesus Moderno
"
```

---

### **Passo 5: Criar branches (Opcional mas Recomendado)**
```powershell
# Branch atual = main (produção estável)
# Criar branch de desenvolvimento
git checkout -b desenvolvimento

# Trabalhar sempre em 'desenvolvimento'
# Só mesclar em 'main' quando funcionar
```

---

## 🔄 WORKFLOW DIÁRIO

### **Ao Começar o Dia:**
```powershell
git status  # Ver o que mudou
```

### **Após Mudanças Importantes:**
```powershell
git add .
git commit -m "feat: implementar agente roteirista"
```

### **Antes de Testes Arriscados:**
```powershell
# Criar branch de backup
git checkout -b backup-antes-teste-ffmpeg
# Fazer testes
# Se der ruim: git checkout desenvolvimento
```

---

## 📤 BACKUP REMOTO (Recomendado)

### **Opção A: GitHub (Privado Grátis)**
```powershell
# 1. Criar repo no GitHub (privado)
# 2. Conectar
git remote add origin https://github.com/SEU_USER/incubadora-ad-labs.git
git branch -M main
git push -u origin main
```

### **Opção B: GitLab (Privado Grátis)**
Similar ao GitHub

### **Opção C: Só Local (Rápido)**
```powershell
# Backup manual em outra pasta
xcopy d:\AD_LABS d:\BACKUP_AD_LABS\ /E /I /Y
```

---

## ⚡ COMANDOS ÚTEIS

### **Ver histórico:**
```powershell
git log --oneline --graph --all
```

### **Reverter mudanças:**
```powershell
# Desfazer arquivo específico
git checkout -- arquivo.py

# Voltar commit inteiro
git revert HEAD
```

### **Ver diferenças:**
```powershell
git diff  # Ver mudanças não commitadas
```

---

## 🎯 ESTRUTURA DE COMMITS

Use prefixos semânticos:

```
feat: nova funcionalidade
fix: correção de bug
docs: documentação
refactor: refatoração
test: testes
chore: tarefas gerais

Exemplos:
git commit -m "feat: adicionar agente 01 inicializador"
git commit -m "fix: corrigir transições FFmpeg"
git commit -m "docs: atualizar README com setup"
```

---

## ✅ CHECKLIST PRIMEIRA VEZ

- [ ] `git --version` funciona?
- [ ] `.gitignore` criado?
- [ ] `git init` executado?
- [ ] Primeiro commit feito?
- [ ] (Opcional) Remoto configurado?

---

## 🚨 O QUE **NÃO** COMMITAR

❌ Senhas e API keys (.env)  
❌ Vídeos finais (.mp4, .mov)  
❌ Assets grandes (usar Git LFS se necessário)  
❌ Arquivos temporários (__pycache__)  

**SEMPRE** verificar com `git status` antes de `git commit`!

---

**Recomendação:** Commite **AGORA** antes de fazer qualquer mudança grande! 🎯
