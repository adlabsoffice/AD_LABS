# 🏗️ Arquitetura "Fábrica de Conteúdo" na AWS

Esta é a estrutura ideal para usar seus **$100 de crédito** de forma inteligente, automatizando YouTube, TikTok e Instagram.

## O Conceito: "Cérebro & Músculo"

Não vamos deixar uma máquina cara ligada 24h. Vamos usar duas:

1.  **🧠 O Cérebro (n8n):** Uma máquina fraquinha, **GRÁTIS** (Free Tier), ligada 24/7. Ela pensa, agenda e manda ordens.
2.  **💪 O Músculo (ComfyUI):** Uma máquina potente (GPU), **PAGA** (com os créditos), que só liga quando precisa trabalhar.

---

## 1. O Cérebro: Servidor de Automação (Always On)
*   **Serviço:** EC2 `t2.micro` ou `t3.micro` (Elegível ao Nível Gratuito).
*   **Custo:** $0,00 (12 meses grátis).
*   **O que roda aqui?**
    *   **n8n:** O maestro das automações.
    *   **Postador de Redes Sociais:** Scripts leves que postam no Insta/TikTok.
    *   **Vigia:** Um script que liga/desliga o "Músculo".

## 2. O Músculo: Servidor de Geração (On-Demand)
*   **Serviço:** EC2 `g4dn.xlarge` (Placa de Vídeo Tesla T4).
*   **Custo:** ~$0.52/hora (R$ 3,00/hora).
*   **O que roda aqui?**
    *   **ComfyUI:** Gera imagens e vídeos insanos sem custo por imagem.
    *   **Renderização:** Monta o vídeo final (MoviePy) muito rápido.

---

## 🔄 O Fluxo Detalhado (Quem faz o quê?)

```mermaid
graph TD
    subgraph "🧠 CÉREBRO (AWS t3.micro - Grátis)"
        N8N[n8n (Maestro)]
        AgenteInsta[Agente 08 (Instagram)]
        AgenteRoteiro[Agente 05 (Roteiro)]
    end

    subgraph "💪 MÚSCULO (AWS g4dn - GPU)"
        ComfyUI[ComfyUI (Gera Imagens)]
        Editor[Agente 07 (Monta Vídeo)]
    end

    subgraph "📱 REDES SOCIAIS"
        IG[Instagram API]
        TT[TikTok API]
    end

    %% Fluxo
    N8N -- "1. Acorda (08:00)" --> AgenteRoteiro
    AgenteRoteiro -- "2. Cria Texto" --> N8N
    N8N -- "3. Liga Servidor GPU" --> ComfyUI
    ComfyUI -- "4. Gera Imagens" --> Editor
    Editor -- "5. Renderiza Vídeo" --> N8N
    N8N -- "6. Desliga Servidor GPU" --> N8N
    N8N -- "7. Manda Vídeo + Legenda" --> AgenteInsta
    AgenteInsta -- "8. Posta (Login via Senha)" --> IG
```

### Respostas para suas dúvidas:

1.  **Quem faz tudo?**
    *   O **n8n** é o chefe. Ele manda os outros trabalharem.
    *   O **ComfyUI** é o artista. Ele só desenha.
    *   Os **Agentes Python** (que criamos) são os operários.

2.  **Como eu acesso o Insta sem navegador?**
    *   O `agente_08_instagram.py` usa uma biblioteca chamada `instagrapi`.
    *   Ela "finge" ser um celular Android.
    *   Ela usa o seu **Login e Senha** (que colocamos no arquivo `.env`) para conectar direto no servidor do Instagram. Não precisa de Chrome.

3.  **Onde estamos agora?**
    *   Temos os Agentes (Operários). ✅
    *   Temos o Servidor n8n (Chefe). ✅
    *   **Falta:** Conectar os fios (Criar o desenho acima dentro do n8n).

---

## ✅ Vantagens dessa Estrutura
1.  **Economia Extrema:** Você só gasta créditos quando está gerando vídeo. O resto do tempo é grátis.
2.  **Poder Ilimitado:** Com o ComfyUI na sua própria GPU, você não paga por imagem gerada. Pode testar à vontade.
3.  **Automação Total:** O n8n cuida de tudo. Você só aprova se quiser.

## Próximos Passos
1.  **Garantir os Créditos:** Terminar as 5 tarefas do `AWS_CREDITS_GUIDE.md`.
2.  **Instalar o Cérebro:** Subir o n8n na máquina grátis (Fácil).
3.  **Configurar o Músculo:** Criar a máquina com GPU e instalar ComfyUI (Médio).
