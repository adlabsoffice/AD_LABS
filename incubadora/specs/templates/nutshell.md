# Template: Bible in a Nutshell (Fast-Paced Epic)

## Estrutura do Roteiro

### 1. Hook Visual (00:00 - 00:05)
- **Objetivo:** Prender a atenção IMEDIATAMENTE.
- **Visual:** Algo chocante, grandioso ou curioso. Sem "Olá galera".
- **Áudio:** Efeito sonoro impactante (Boom, Whoosh) + Frase curta do narrador.

### 2. Desenvolvimento Acelerado (Corpo)
- **Ritmo:** Cenas de 3 a 5 segundos MÁXIMO.
- **Estilo:** "Show, don't tell". O narrador complementa a imagem, não descreve o óbvio.
- **Transições:** Cortes secos. Ação puxa ação.

### 3. Clímax & Resolução
- **Clímax:** Aumentar a intensidade da música e da narração.
- **Resolução:** Rápida e reflexiva.

---

## Instruções para o Roteirista (LLM)

1. **Densidade de Cenas:** Gere MUITAS cenas curtas. Para 1 minuto de vídeo, precisamos de ~15-20 cenas.
2. **Descrições Visuais:** Use termos cinematográficos: "Wide shot", "Close-up", "Low angle", "Slow motion".
3. **Narrativa:** Use a voz ativa. Frases curtas e potentes.
4. **Emoção:** Indique a emoção dominante de cada bloco.

## Exemplo de Bloco JSON

```json
{
  "speaker": "Narrador",
  "dialogue": "Mas Davi não via um gigante. Ele via um alvo.",
  "visual_prompt": "Extreme close-up nos olhos de Davi, foco intenso, pupilas dilatadas, suor na testa, fundo desfocado, cinematic lighting, 8k",
  "duration_seconds": 3.5,
  "emotion": "determinação"
}
```
