# 💰# Simulação de Custo: Google Full Stack (Estimativa)

## 1. Componentes
- **Roteiro (Texto):** Google Gemini 2.0 Flash (via `generativelanguage.googleapis.com`).
- **Narração (Áudio):** Google Cloud Text-to-Speech (`Neural2`).
- **Visual (Imagem):** **PLACEHOLDER** (Imagen 4.0 desativado por custo).

## 2. Tabela Oficial de Preços (Vertex AI) - Detalhada

### 🧠 Modelos de Linguagem (Gemini)
| Modelo | Input (1M tokens) | Output (1M tokens) | Áudio Input (1M) | Vídeo Input (1M) |
| :--- | :--- | :--- | :--- | :--- |
| **Gemini 2.0 Flash** | **$0.15** | **$0.60** | $1.00 | $3.00 |
| **Gemini 2.0 Flash Lite** | **$0.075** | **$0.30** | $0.075 | - |
| **Gemini 1.5 Flash** | $0.075 | $0.30 | $1.00 | $1.00 |
| **Gemini 1.5 Pro** | $1.25 | $5.00 | $10.00 | $10.00 |

### 🎨 Geração de Imagem (Imagen)
| Modelo | Preço por Imagem | Obs |
| :--- | :--- | :--- |
| **Imagen 4 Ultra** | **$0.06** | Qualidade Máxima |
| **Imagen 4** | **$0.04** | Padrão |
| **Imagen 4 Fast** | **$0.02** | Rápido/Econômico |
| **Imagen 3** | **$0.04** | Versão Anterior |
| **Imagen 3 Fast** | **$0.02** | Versão Anterior Rápida |

### 🎥 Geração de Vídeo (Veo) - 🚨 ALTO CUSTO
| Modelo | Preço por Segundo | Preço por Minuto |
| :--- | :--- | :--- |
| **Veo 3 (Vídeo + Áudio)** | **$0.75** | **$45.00** (~R$ 270,00) |
| **Veo 3 (Só Vídeo)** | **$0.50** | **$30.00** (~R$ 180,00) |
| **Veo 2** | **$0.50** | **$30.00** (~R$ 180,00) |

### 🎵 Geração de Música (Lyria)
| Modelo | Preço |
| :--- | :--- |
| **Lyria 2** | **$0.06** por 30 segundos |

---

## 3. Análise do Gasto de "2000"
Com base na tabela oficial que você forneceu:

1.  **Cenário Veo (Vídeo):**
    *   3 vídeos de 5 min = 15 min totais.
    *   15 min = 900 segundos.
    *   Custo (Veo 3 c/ Áudio): 900 * $0.75 = **$675.00 USD** (~R$ 4.050,00).
    *   *Isso bate com seu relato de gasto alto.*

2.  **Cenário Imagen 4 Ultra (Imagem):**
    *   3 vídeos * 75 imagens/vídeo = 225 imagens.
    *   Custo: 225 * $0.06 = **$13.50 USD** (~R$ 80,00).
    *   *Muito mais barato que vídeo.*

## 4. Custo Real do Projeto (Recomendado)
Utilizando a stack otimizada:

| Componente | Modelo | Qtd (1 Vídeo 5min) | Custo (USD) | Custo (BRL) |
| :--- | :--- | :--- | :--- | :--- |
| **Roteiro** | Gemini 2.0 Flash | 1 Roteiro | < $0.01 | R$ 0,05 |
| **Áudio** | Neural2 | 4.5k chars | $0.07 | R$ 0,42 |
| **Visual** | **Imagen 4 Fast** | 75 imagens | 75 * $0.02 = $1.50 | R$ 9,00 |
| **TOTAL** | | | **~$1.58** | **~R$ 9,50** |

**Conclusão:**
Para viabilizar o canal, use **Imagen 4 Fast ($0.02)** ou **Imagen 4 ($0.04)**.
**JAMAIS use o Veo** para vídeos inteiros, a menos que tenha orçamento de TV.
