# 15 - Groq: APIs de IA Gratuitas (Sem Cartão de Crédito)

**Fonte:** Transcrição YouTube  
**Tema:** Como usar APIs gratuitas do Groq para desenvolvimento de apps AI

---

## 🎯 Visão Geral

**Groq** oferece uma das ofertas mais generosas de **API gratuita** para IA, perfeita para desenvolvedores que querem construir apps AI sem custos iniciais.

**Website:** `groq.com`

---

## 📊 Rate Limits (Limites de Uso)

### **Como Entender Rate Limits:**

**Métricas:**
- **RPM** = Requests Per Minute (Requisições por minuto)
- **RPD** = Requests Per Day (Requisições por dia)
- **TPM** = Tokens Per Minute (Tokens por minuto)
- **TPD** = Tokens Per Day (Tokens por dia)

---

## 🔥 APIs Disponíveis (GRÁTIS)

### **1. DeepSeek API**
- **RPD:** 1.000 requests/dia
- **RPM:** 30 requests/minuto

### **2. Llama Family APIs**
- **RPD:** **14.400 requests/dia** 🔥
- **RPM:** Varia por modelo
**💡 Enorme para plano gratuito!**

### **3. OpenAI GPT-4o API**
- **RPD:** 1.000 requests/dia
- **RPM:** 30 requests/minuto

### **4. Qwen 3 API**
- **RPD:** 1.000 requests/dia
- **RPM:** **60 requests/minuto** (2x mais rápido!)

### **5. Whisper API (Speech-to-Text)**
- **RPD:** 2.000 requests/dia
**💡 Construa apps de voz AI!**

---

## 🎨 Tipos de Modelos

**Groq fornece:**
1. **Text generation** - Geração de texto
2. **Speech-to-text** - Transcrição de áudio
3. **Text-to-speech** - Síntese de voz
4. **Vision models** - Análise de imagens
5. **Reasoning models** - Raciocínio avançado

**Resultado:** Tudo que você precisa para apps AI em um lugar.

---

## 🛠️ Playground (Teste Grátis)

### **Como usar:**

1. Acessar `groq.com`
2. Ir para Playground
3. Testar modelos diretamente no browser

### **Exemplo testado no vídeo:**

**Input:**
> "Give me a Next.js 15 app router API code sample"

**Output:**
- ✅ API routes examples
- ✅ Project layouts
- ✅ Basic GET method
- ✅ CRUD operations
- ✅ Dynamic API routes
- ✅ **Baseado na versão mais recente!**

**💡 Resposta completa e atualizada**

---

## 🔑 Criando API Key

### **Passo a passo:**

1. Clicar em "Create API Key"
2. Dar nome para a key
3. Submitar
4. **Copiar key** (mostrada apenas uma vez!)

**⚠️ Importante:** Salve a key em local seguro

---

## 🧪 Testando com Postman

### **Setup:**

**1. URL:**
```
https://api.groq.com/openai/v1/chat/completions
```

**2. Authorization:**
- Type: **Bearer Token**
- Token: [sua API key]

**3. Body (JSON):**
```json
{
  "model": "llama-3.1-70b-versatile",
  "messages": [
    {
      "role": "user",
      "content": "Explain quantum computing"
    }
  ]
}
```

**4. Headers:**
- `Content-Type: application/json`

**5. Remover:**
- `"stream": true` (para resposta completa, não streaming)

### **Resultado:**
- ✅ Resposta AI completa
- ✅ 1 request usado (999 restantes!)

---

## 💻 Integração em Apps

### **Método 1: Fetch JavaScript**

**Postman → Code:**
1. Clicar no botão "Code"
2. Selecionar linguagem (JavaScript fetch, Axios, Python, etc.)
3. Copiar código
4. Colar no projeto

**Exemplo (JavaScript):**
```javascript
const response = await fetch('https://api.groq.com/openai/v1/chat/completions', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${process.env.GROQ_API_KEY}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    model: 'llama-3.1-70b-versatile',
    messages: [{
      role: 'user',
      content: 'Hello!'
    }]
  })
});

const data = await response.json();
console.log(data.choices[0].message.content);
```

### **Método 2: Groq Package**

**JavaScript:**
```bash
npm install groq-sdk
```

**Python:**
```bash
pip install groq
```

**Uso:**
```javascript
import Groq from 'groq-sdk';

const groq = new Groq({
  apiKey: process.env.GROQ_API_KEY
});

const completion = await groq.chat.completions.create({
  messages: [{
    role: 'user',
    content: 'Explain AI'
  }],
  model: 'llama-3.1-70b-versatile'
});

console.log(completion.choices[0].message.content);
```

---

## ⚙️ Settings e Customização

**Parâmetros disponíveis:**

### **1. Temperature**
- Controla criatividade/randomness
- **Baixo:** Focado, consistente
- **Alto:** Criativo, imprevisível

### **2. Max Tokens**
- Limite de tokens na resposta
- Controla tamanho do output

### **3. Stream Mode**
- **ON:** Resposta em tempo real (como ChatGPT typing)
- **OFF:** Resposta completa de uma vez

### **4. JSON Mode**
- **ON:** Força resposta em formato JSON
- **Super útil para desenvolvedores!**

### **5. Built-in Tools**
- **Browser Search:** AI busca na web antes de responder
- Dá respostas mais atualizadas/precisas

### **6. Advanced:**
- **Top P** - Controla range de escolha do modelo
- **Seed** - Torna outputs consistentes/reproduzíveis

---

## 🔌 MCP Servers

**Feature extra:**
- Adicionar MCP servers
- Extend setup com integrações customizadas

**💡 Para workflows avançados**

---

## 🎙️ Whisper AI (Speech-to-Text)

### **Como usar:**

**1. No Playground:**
- Upload arquivo de áudio OU
- Gravar voz diretamente

**2. Teste demonstrado:**
- Upload `test.mp3`
- **Resultado:** Transcrição exata, perfeita

### **3. Ver código:**
- Clicar "View Code"
- Copiar sample code
- Integrar em app

**Casos de uso:**
- Chat app com áudio
- Voice assistants
- Transcrição automática
- Acessibilidade

---

## 📚 Documentação

**Groq fornece:**
- ✅ Docs claras e bem explicadas
- ✅ Exemplos de código
- ✅ API reference completa
- ✅ Guias de integração

**Acessível em:** `groq.com/docs`

---

## 💰 Pricing Comparison

| Provider | Free Tier | Limits |
|----------|-----------|--------|
| **Groq** | ✅ Sim | 14.4K RPD (Llama) |
| OpenAI | ❌ $5 mínimo | Rate limits baixos |
| Anthropic | ❌ Pago | N/A |
| Google AI | ✅ Sim | Limits menores |

**Vencedor:** Groq (para experimentação e protótipos)

---

## 🚀 Casos de Uso

### **1. Chatbots**
```javascript
// Exemplo: Customer support chatbot
const response = await groq.chat.completions.create({
  model: 'llama-3.1-70b-versatile',
  messages: conversationHistory
});
```

### **2. Voice AI Apps**
```javascript
// Transcrição + Resposta
const transcription = await groq.audio.transcriptions.create({
  file: audioFile,
  model: 'whisper-large-v3'
});

const response = await groq.chat.completions.create({
  messages: [{ role: 'user', content: transcription.text }],
  model: 'llama-3.1-70b-versatile'
});
```

### **3. Code Generation**
```javascript
// Generate Next.js API route
const code = await groq.chat.completions.create({
  messages: [{
    role: 'user',
    content: 'Create Next.js 15 API route for user authentication'
  }],
  model: 'llama-3.1-70b-versatile',
  response_format: { type: 'json_object' } // JSON mode
});
```

### **4. Research Automation**
```javascript
// Com browser search enabled
const answer = await groq.chat.completions.create({
  messages: [{
    role: 'user',
    content: 'Latest AI news from this week'
  }],
  model: 'llama-3.1-70b-versatile',
  tools: ['browser_search'] // Built-in tool
});
```

---

## ✅ Checklist de Ação

### **Hoje:**
- [ ] Criar conta em `groq.com`
- [ ] Gerar API key
- [ ] Testar no Playground
- [ ] Fazer requisição teste no Postman

### **Esta Semana:**
- [ ] Integrar em projeto pequeno
- [ ] Testar Whisper API
- [ ] Comparar performance vs OpenAI
- [ ] Explorar JSON mode

### **Este Mês:**
- [ ] Construir chatbot funcional
- [ ] Implementar voice feature
- [ ] Deploy app usando Groq API
- [ ] Monitorar usage limits

---

## 🎓 Lições-Chave

1. **Free ≠ Fraco** - Groq oferece modelos de qualidade gratuitamente
2. **Llama >>> Outros** - 14.4K requests/dia é generoso demais
3. **Whisper incluído** - Voice AI sem pagar extra
4. **JSON mode = Vida fácil** - Parsing automático
5. **Browser search = Atualizado** - AI com contexto web

---

## ⚠️ Limitações

**Rate limits:**
- ⚠️ 14.4K/dia é muito, mas não infinito
- ⚠️ Apps production precisarão upgrade eventualmente

**Modelos:**
- ⚠️ Não tem todos os modelos (ex: GPT-4 Turbo, Claude 3 Opus)
- ⚠️ Foco em open-source (Llama, DeepSeek, Qwen)

**Suporte:**
- ⚠️ Free tier = suporte limitado

---

## 🔗 Links e Recursos

**Principais:**
- Website: `groq.com`
- Docs: `groq.com/docs`
- Playground: `groq.com/playground`
- API Reference: `groq.com/api-reference`

**Ferramentas:**
- Postman: `postman.com`
- Groq SDK (npm): `groq-sdk`
- Groq SDK (pip): `groq`

---

## 🎬 Conclusão

Groq democratiza acesso a APIs de IA, oferecendo:
- ✅ **14.4K requests/dia** (Llama)
- ✅ **Sem cartão de crédito**
- ✅ **Whisper incluído**
- ✅ **JSON mode nativo**
- ✅ **Documentação excelente**

**Ideal para:** Desenvolvedores experimentando, MVPs, aprendizado, protótipos.

**Próximos passos:** Criar conta, pegar API key, começar a construir!

---

**💡 Dica final:** Se o vídeo ajudou, like + subscribe + compartilhe. Mais tutoriais de AI local e ferramentas gratuitas no canal!
