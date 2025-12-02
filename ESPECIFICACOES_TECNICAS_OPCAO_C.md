# ⚙️ ESPECIFICAÇÕES TÉCNICAS - OPÇÃO C HÍBRIDA
## Sistema Automatizado para "O Livro Caixa Divino"

> **Abordagem:** Híbrida (qualidade profissional + custo baixo)  
> **Target:** Vídeos 4-6 minutos, 25 cenas, personagem consistente  
> **Prazo MVP:** 5-7 dias

---

## 🎬 PIPELINE COMPLETO

### **Fase 1: ROTEIRO (Automático - 3min)**

```python
# Agente: Roteirista
INPUT:
  - Título: "Jesus analisa: O método do Primo Rico"
  - Eixo: React/Viral
  - Duração target: 5 minutos

PROCESSAMENTO:
  1. Grok/Groq gera roteiro estruturado
  2. Valida densidade: 1000-1500 palavras
  3. Valida ritmo: 168-187 wpm
  4. Gera hook + desenvolvimento + CTA

OUTPUT:
  - roteiro.txt (1200 palavras)
  - roteiro_estruturado.json (com timecodes)
```

**Exemplo Output:**
```json
{
  "hook": {
    "texto": "Você já viu o Primo Rico ensinando...",
    "duracao_seg": 15,
    "emocao": "curiosidade"
  },
  "desenvolvimento": [...],
  "cta": {
    "texto": "Se inscreva para mais verdades...",
    "duracao_seg": 10
  }
}
```

---

### **Fase 2: STORYBOARD (Automático - 5min)**

```python
# Agente: Diretor de Arte
INPUT:
  - roteiro_estruturado.json
  - duracao_total: 300s (5min)
  - ritmo_visual: 12s/cena

PROCESSAMENTO:
  1. Divide roteiro em 25 cenas
  2. Para cada cena:
     - Identifica momento-chave
     - Define se usa personagem OU cena contextual
     - Gera prompt específico
  3. Aplica regra: 40% personagem + 60% contexto

OUTPUT:
  - storyboard.json (25 cenas descritas)
```

**Exemplo Cena:**
```json
{
  "cena_id": 3,
  "timestamp_inicio": 24,
  "timestamp_fim": 36,
  "tipo": "personagem",
  "pose_id": "jesus_pensativo_02",
  "prompt_contexto": "escritório moderno nas nuvens, luz dourada",
  "acao": "Jesus está pensativo analisando gráfico"
}
```

---

### **Fase 3: GERAÇÃO DE IMAGENS (Híbrido - 20min)**

#### **3A: Personagens (Manual 1x, Reutiliza Sempre)**

**Setup Inicial (Uma vez):**
```
1. Criar 10-15 poses do "Jesus Moderno"
   Ferramentas: Midjourney / Leonardo.AI
   
   Poses necessárias:
   - jesus_neutro.png (pose padrão)
   - jesus_pensativo.png (mão no queixo)
   - jesus_sorrindo.png (aprovação)
   - jesus_serio.png (julgamento)
   - jesus_chocado.png (reação viral)
   - jesus_explicando.png (mão aberta)
   - jesus_apontando.png (dedo indicador)
   - jesus_negando.png (mão em stop)
   - jesus_aprovando.png (thumbs up)
   - jesus_duvidando.png (sobrancelha levantada)
   
2. Padronizar:
   - Mesmo estilo visual (Pixar-like)
   - Mesma paleta de cores
   - Fundo transparente (PNG)
   - Resolução: 2048x2048

3. Salvar em biblioteca:
   assets/personagem/jesus_[pose].png
```

**Tempo:** 2-3 horas (fazer bem feito UMA VEZ)

**Custo:** 
- Midjourney: U$ 10/mês (cancela depois)
- OU Leonardo.AI: Grátis (150 imgs/mês)

---

#### **3B: Cenas Contextuais (Automático)**

```python
# Para 60% das cenas (15 de 25)
for cena in storyboard onde tipo == "contexto":
    prompt = gerar_prompt_pollinations(cena)
    
    # Exemplo prompt:
    # "modern office in the clouds, golden light,
    #  financial charts floating, 3D render, Pixar style,
    #  no people, wide shot, cinematic"
    
    imagem = pollinations_api.generate(
        prompt=prompt,
        width=1920,
        height=1080,
        model="turbo"
    )
    
    salvar(f"cena_{cena.id}.jpg")
```

**Tempo:** 15 imgs × 30s = ~8 minutos

**Custo:** R$ 0 (Pollinations grátis)

---

### **Fase 4: NARRAÇÃO (Automático - 2min)**

```python
# Agente: Sonoplasta
INPUT:
  - roteiro.txt
  - voz: "pt-BR-Neural-Male"
  - velocidade: 1.1x

PROCESSAMENTO:
  1. Google Cloud TTS gera áudio
  2. Converte para SRT (legendas sincronizadas)
  3. Aplica pausas estratégicas
  4. Adiciona ênfases

OUTPUT:
  - naracao.mp3 (5min de áudio)
  - legendas.srt (sincronizado)
```

**Custo:** R$ 0 (1M caracteres grátis/mês = ~500 vídeos)

---

### **Fase 5: MÚSICA (Automático - 3min)**

```python
# Sistema musical adaptativo
ESTRUTURA:
  - 0-15s: Música curiosa/tension (hook)
  - 15-270s: Lo-fi suave (desenvolvimento)  
  - 270-300s: Épica/resolução (CTA)

IMPLEMENTAÇÃO:
  1. Biblioteca pré-curada (YouTube Audio Library)
     - 10 músicas "hook"
     - 20 músicas "background"
     - 10 músicas "CTA"
  
  2. IA escolhe baseado em:
     - Emoção do roteiro
     - Tom do vídeo
  
  3. FFmpeg faz crossfade entre camadas

OUTPUT:
  - trilha_completa.mp3 (5min, 3 camadas mixadas)
```

---

### **Fase 6: PÓS-PRODUÇÃO (Automático - 30min)**

#### **6A: Composição Visual (FFmpeg Avançado)**

```python
# Para cada cena:
def processar_cena(cena, anterior):
    # 1. Carregar imagem base
    if cena.tipo == "personagem":
        img = compositar_personagem(
            pose=cena.pose_id,
            fundo=gerar_fundo_contextual(cena.prompt_contexto)
        )
    else:
        img = carregar(f"cena_{cena.id}.jpg")
    
    # 2. Aplicar Ken Burns (zoom + pan)
    img_animada = ken_burns_effect(
        img,
        duracao=12,
        zoom_inicio=1.0,
        zoom_fim=1.2,
        pan_x=random(-50, 50),
        pan_y=random(-30, 30)
    )
    
    # 3. Adicionar legendas word-by-word
    com_legendas = adicionar_legendas_animadas(
        img_animada,
        legendas_srt,
        timestamp=cena.timestamp
    )
    
    # 4. Transição para próxima cena
    if anterior:
        transicao = escolher_transicao_aleatoria()
        resultado = aplicar_transicao(
            anterior,
            com_legendas,
            tipo=transicao,
            duracao=0.5
        )
    
    return resultado
```

**Transições Disponíveis (FFmpeg xfade):**
1. `fade` - Dissolve clássico
2. `wipeleft` - Varrer esquerda
3. `slideleft` - Deslizar esquerda
4. `circleopen` - Círculo abrindo
5. `zoomin` - Zoom dramático
6. `dissolve` - Dissolver pixels

---

#### **6B: Efeitos Especiais Simples**

```python
# Pop-ups de texto (sem After Effects)
def adicionar_popup_texto(frame, texto, posicao):
    # FFmpeg drawtext com animação
    return drawtext(
        text=texto,
        fontsize=48,
        fontcolor="yellow",
        borderw=3,
        bordercolor="black",
        x=f"if(lt(t,{posicao}),W,W-300*(t-{posicao})/0.5)",
        y=100,
        enable=f"between(t,{posicao},{posicao+2})"
    )

# Exemplo: Quando falar "Primo Rico"
# Pop-up: 📊 "40 MILHÕES DE VIEWS"
```

---

#### **6C: Composição Final**

```python
# Combinar tudo
ffmpeg -i video_visual.mp4 \
       -i naracao.mp3 \
       -i trilha_completa.mp3 \
       -filter_complex "\
         [1:a]volume=1.0[narr];\
         [2:a]volume=0.18[mus];\
         [narr][mus]amix=inputs=2[audio]\
       " \
       -map 0:v -map [audio] \
       -c:v libx264 -preset medium \
       -crf 23 -pix_fmt yuv420p \
       output_final.mp4
```

**Tempo total:** ~30 minutos render (25 cenas)

---

## 📊 RESUMO TÉCNICO

| Etapa | Ferramenta | Tempo | Custo | Automação |
|-------|-----------|-------|-------|-----------|
| Roteiro | Groq/Grok | 3min | R$ 0 | 100% |
| Storyboard | Python | 5min | R$ 0 | 100% |
| Personagem (setup) | Midjourney | 2-3h | U$ 10 | 0% (1x only) |
| Cenas contextuais | Pollinations | 8min | R$ 0 | 100% |
| Narração | Google TTS | 2min | R$ 0 | 100% |
| Música | YouTube Library | 3min | R$ 0 | 100% |
| Pós-produção | FFmpeg | 30min | R$ 0 | 100% |
| **TOTAL/VÍDEO** | - | **~60min** | **~R$ 0** | **95%** |

**Setup inicial:** 2-3 horas (criar biblioteca de poses)  
**Depois disso:** Totalmente automatizado

---

## 🎯 QUALIDADE ESPERADA

### **Visual:**
- Personagem: 9/10 (consistente, profissional)
- Cenas: 7/10 (boas, não cinematográficas)
- **Média:** 8/10

### **Ritmo:**
- Troca visual: 12s (mantém atenção)
- Transições: Suaves e variadas
- **Engajamento:** ALTO

### **Diferencial:**
✅ Personagem reconhecível  
✅ Qualidade acima da média  
✅ Não genérico  
✅ Replicável

---

## 🚀 EVOLUÇÃO FUTURA

**Quando GPU AWS/Google liberar:**

### **Upgrade 1: Personagem Totalmente Automatizado**
```
Treinar LoRA "Jesus Moderno":
- 200 imagens das poses criadas
- Flux.1 Dev + LoRA training
- Resultado: Gera poses infinitas automaticamente
- Qualidade: 9.5/10
```

### **Upgrade 2: Efeitos After Effects → Remotion.js**
```
- Animações de gráficos 3D
- Partículas, física
- Transições cinematográficas
- Qualidade: 9.5/10
```

**Opção C (agora) → Opção A (depois)** = Caminho natural de evolução!
