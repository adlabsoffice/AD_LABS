# 26 - Como Fazer TIMELAPSE com IA (Método Completo Grátis)

**Fonte:** Transcrição YouTube  
**Tema:** Criar timelapses cinematográficos impossíveis usando apenas IA (Gemini + Kling/Veo3)

---

## 🎯 O Que Vamos Criar

**Timelapse IA:**
- ✅ Sem câmera
- ✅ Sem drone
- ✅ Sem dias de gravação
- ✅ **Cenários impossíveis**
- ✅ Dia → Noite smooth transitions

**Método:** Gemini (images) + Kling AI (animation)

---

## 🛠️ Stack Tecnológica

| Etapa | Ferramenta | Função |
|-------|------------|--------|
| 1 | **Gemini (Nano Banana)** | Gerar frames (manhã/tarde/noite) |
| 2 | **Kling AI** ou **Veo 3** | Animar transições |
| 3 | **Premiere/CapCut** | Juntar clips finais |

---

## 📋 Workflow Completo

### **ETAPA 1: Criar Frames Base (Gemini)**

**Passo 1: Frame Inicial**
```
Prompt:
"Create drone shot of [scene]. Morning light."

Exemplo:
Pessoa no topo de montanha, mãos abertas, 
vista drone frontal
```

**Passo 2: Frame Pôr do Sol**
```
1. Upload frame inicial
2. Prompt:
"Same scene, same angle. Golden hour, sunset lighting."
```

**Passo 3: Frame Noite**
```
1. Upload frame pôr do sol
2. Prompt:
"Same scene, rotate camera 45° horizontal. 
Night time, stars visible."
```

**Resultado:** 3 imagens consistentes (manhã/tarde/noite)

---

### **ETAPA 2: Animar Transições**

#### **Opção A: Kling AI (Recomendado)**

**Por quê:** Transições mais suaves

**Processo:**
```
1. Kling AI → Image to Video
2. Frame 1: Manhã
3. Frame 2: Pôr do Sol
4. Prompt: "timelapse"
5. Duration: 5 segundos
6. Generate
```

**Resultado:** Smooth transition manhã → tarde

**Repetir:**
```
Frame 1: Tarde
Frame 2: Noite
→ Transition tarde → noite
```

---

#### **Opção B: Google Flow (Veo 3)**

**Processo:**
```
1. Flow → Frames to Video
2. Upload 2 frames
3. Prompt: "Create timelapse with fixed camera"
4. Generate
```

**Limitação:** Às vezes transição "grosseira" (menos suave)

---

### **ETAPA 3: Edição Final**

**Premiere Pro / CapCut:**
```
1. Import ambos clips:
   - Manhã → Tarde (5s)
   - Tarde → Noite (5s)
2. Arrastar sequencialmente na timeline
3. (Opcional) Add color grading
4. Export
```

**Resultado:** Timelapse completo 10 segundos

---

## 🎨 Exemplos de Prompts

**Urbano:**
```
Frame 1: "Drone wide shot, New York cityscape, sunrise"
Frame 2: "Same angle, golden hour"
Frame 3: "Same angle, night, city lights glowing"
```

**Natureza:**
```
Frame 1: "Forest clearing, morning mist, sun rays"
Frame 2: "Same scene, afternoon bright sunlight"
Frame 3: "Same scene, twilight, fireflies appearing"
```

**Futurista:**
```
Frame 1: "Futuristic city, drone view, morning"
Frame 2: "Same angle, flying cars active, sunset"
Frame 3: "Same angle, neon lights, night sky"
```

---

## ✅ Tips Para Sucesso

**Consistência:**
- ✅ Sempre mencionar "same angle/same camera"
- ✅ Upload frame anterior como referência
- ✅ Especificar mudança apenas de lighting/tempo

**Kling vs Veo 3:**
- **Kling:** Mais suave, transitions melhores
- **Veo 3:** Mais rápido, mas pode ter "jumps"

**Créditos Kling:**
- Começam com 166 créditos free
- 5s video = ~10-20 créditos
- Renovável com novas contas

---

## 🎓 Criatividade Infinita

**Não se limite aos exemplos:**
- Catedral mudando através dos séculos
- Árvore crescendo em seconds
- Cidade construindo-se sozinha
- Planeta visto do espaço (rotação)

**Receita:** Frames consistentes + animação IA = Magic

---

## 🔗 Links

**Tools:**
- Gemini: `gemini.google.com`
- Kling AI: `klingai.com`
- Google Flow: `flow.google.com`

**Editing:**
- CapCut: Grátis
- Premiere Pro: Pago
