# 📱 CREDENCIAIS DE REDES SOCIAIS - AD_LABS

**Última Atualização:** 02/12/2025 12:22  
**Status:** Catalogadas e Documentadas

---

## ✅ TELEGRAM - COMPLETAMENTE CONFIGURADO

### Bot Ativo
- **Token:** `8023515576:AAGxblQlQUcm7QG8MA2ebVN1MbDKimNgTco`
- **Nome do Bot:** `@adlabs_boss_bot`
- **Chat ID:** Salvo em `telegram_id.txt`

### Funcionalidade
✅ **Notificações Automáticas Ativas**

O sistema envia notificações Telegram em todas as etapas:
1. 🏭 Fábrica iniciada
2. 📝 Roteiro criado
3. 🎙️ Áudio gerado (envia amostra do Hook)
4. 🎨 Imagens geradas (envia exemplos de cenas)
5. 🖼️ Thumbnail criada
6. ✅ Vídeo final concluído
7. 🚨 Erros críticos

### Arquivos Relacionados
- `get_telegram_id.py` - Obtém Chat ID do usuário
- `send_telegram_help.py` - Envia mensagem de ajuda
- `run_agents.py` - Integração completa (funções `enviar_telegram` e `enviar_telegram_arquivo`)
- `telegram_id.txt` - Armazena Chat ID

### Variável de Ambiente
```bash
TELEGRAM_BOT_TOKEN=8023515576:AAGxblQlQUcm7QG8MA2ebVN1MbDKimNgTco
TELEGRAM_CHAT_ID=[seu_chat_id]  # Salvo em telegram_id.txt
```

---

## ⚠️ INSTAGRAM - CONFIGURADO MAS CREDENCIAIS PRIVADAS

### Status
**Credenciais existem** no `.env` mas não são exibidas por segurança

### Implementação
- **Agente:** `agente_08_instagram.py`
- **Biblioteca:** `instagrapi`
- **Classe:** `Agente08Instagram`

### Funcionalidade
✅ **Postagem Automática de Vídeos**

Recursos implementados:
- Login automático via `instagrapi`
- Postagem de vídeos
- Upload de thumbnails
- Suporte a legendas
- Validação de credenciais

### Variáveis de Ambiente
```bash
INSTAGRAM_USER=seu_usuario
INSTAGRAM_PASSWORD=sua_senha
```

### Como Usar
```python
from agentes.agente_08_instagram import Agente08Instagram

agente = Agente08Instagram()
agente.postar_video(
    caminho_video="path/to/video.mp4",
    legenda="Sua legenda aqui",
    caminho_thumbnail="path/to/thumb.jpg"  # opcional
)
```

### Observações
- ⚠️ Instagram pode bloquear automação - usar com cautela
- ✅ Agente tem validação de credenciais antes de postar
- 📱 Suporta posts no feed (não Stories/Reels ainda)

---

## ❌ TIKTOK - NÃO CONFIGURADO

### Status
**Sem implementação ou credenciais**

### Evidências
- Mencionado apenas em `sapg.py` como exemplo de tema
- Sem agente específico
- Sem credenciais no `.env`
- Sem bibliotecas de automação instaladas

### Para Implementar (Futuro)
1. Biblioteca sugerida: `TikTokApi` (unofficial)
2. Criar `agente_XX_tiktok.py`
3. Adicionar credenciais ao `.env`:
   ```bash
   TIKTOK_SESSION_ID=...
   TIKTOK_MS_TOKEN=...
   ```

---

## 🔐 RESUMO DE SEGURANÇA

### Credenciais Expostas (Podem ser regeneradas)
- ✅ **Telegram Bot Token** - Exposto neste documento (pode ser revogado no BotFather)

### Credenciais Protegidas (No .env)
- 🔒 **Instagram User/Password** - No `.env`, ignorado pelo Git
- 🔒 **Telegram Chat ID** - Em `telegram_id.txt`, ignorado pelo Git

### Recomendações
1. 🔄 **Rotacionar Telegram Token** se necessário via [@BotFather](https://t.me/botfather)
2. 🔐 **Nunca commitar `.env`** (já está no `.gitignore`)
3. 📝 **Usar `.env.example`** para template sem credenciais

---

## 📊 COMPARAÇÃO DE PLATAFORMAS

| Plataforma | Status | Automação | Agente | Observações |
|------------|--------|-----------|--------|-------------|
| **Telegram** | ✅ Ativo | Notificações | - | Bot próprio funcionando |
| **Instagram** | ⚠️ Configurado | Postagem | agente_08 | Credenciais no .env |
| **TikTok** | ❌ Não configurado | - | - | Mencionado mas não implementado |
| **YouTube** | ⚠️ API faltante | - | - | YouTube Data API não encontrada |

---

## 🎯 PRÓXIMAS AÇÕES SUGERIDAS

### Curto Prazo
1. ✅ **Testar Instagram** - Fazer um post de teste via `agente_08_instagram.py`
2. ✅ **Validar Telegram** - Enviar mensagem de teste
3. ⚠️ **Adicionar YouTube API** - Para upload automático de vídeos

### Médio Prazo
1. 📱 **Implementar TikTok** - Se houver demanda
2. 🎬 **Instagram Reels** - Adicionar suporte a Reels (diferente de posts de vídeo)
3. 📊 **Analytics** - Coletar métricas de cada plataforma

---

**Gerado por:** Antigravity (Prompt Coringa v1.0.0)  
**Data:** 02/12/2025 12:22
