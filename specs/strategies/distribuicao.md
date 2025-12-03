# Estratégia de Distribuição e Publicação (Agente Publisher)

**Objetivo:** Automatizar o "Last Mile" da produção: do arquivo MP4 até o vídeo publicado no canal, com SEO otimizado e Thumbnails de alta conversão.

---

## 1. Quem faz o quê?

### A. Thumbnails (A Vitrine)
*   **Responsável:** `Agente 07 (Visual)` + `Agente 12 (Publisher)`
*   **Fluxo:**
    1.  **Geração Base (Agente 07):** Cria 4 variações de imagem baseada no Blueprint (Rosto expressivo, fundo escuro, contraste alto).
    2.  **Seleção & Texto (Agente 12):**
        *   Escolhe a melhor imagem (via LLM Vision).
        *   Adiciona texto (0-3 palavras) usando `Pillow` (Python Image Library).
        *   Aplica filtros de correção de cor (Vibrance/Contrast) para "popar" na tela.
    3.  **Formato:** JPG, 1280x720, <2MB.

### B. Upload e Metadados (O SEO)
*   **Responsável:** `Agente 12 (Publisher)`
*   **Fluxo:**
    1.  **Título:** Otimizado pelo Blueprint (6-8 palavras, Title Case).
    2.  **Descrição:**
        *   Primeira linha: Hook de SEO (palavras-chave).
        *   Links: Afiliados, Redes Sociais.
        *   Hashtags: #Shorts + 2 do nicho.
    3.  **Tags:** Geradas via análise de tendências.
    4.  **Upload:** Via YouTube Data API.
    5.  **Status Inicial:** `Privado` ou `Não Listado`.

### C. Aprovação (O Controle)
*   **Responsável:** Você (via Telegram).
*   **Fluxo:**
    1.  O Agente 12 sobe o vídeo como `Não Listado`.
    2.  Envia no Telegram:
        *   Link do Vídeo.
        *   Thumbnail gerada.
        *   Título e Descrição.
    3.  **Botões:** `[APROVAR PÚBLICO]` | `[REFAZER THUMB]` | `[AJUSTAR TÍTULO]`.

---

## 2. Estratégia Multi-Canal (O Polvo)

### Instagram (Reels) & TikTok
*   **Problema:** O YouTube Shorts aceita até 60s, mas formatos variam.
*   **Solução:** O mesmo vídeo MP4 (9:16) serve para os três.
*   **Agente Publisher:**
    *   Usa API não-oficial (ou oficial se disponível) para Instagram/TikTok.
    *   Agenda postagem para horários de pico (ex: 18h).
    *   **Regra de Ouro:** Remove marca d'água se houver.

---

## 3. Plano de Implementação (Próximos 140 min)

1.  **Criar `Agente 12 (Publisher)`:**
    *   Script Python que autentica no YouTube.
    *   Função `upload_video(file, title, description, thumb)`.
2.  **Integrar no Pipeline:**
    *   Adicionar passo 11 no `run_agents.py`.
3.  **Teste de Upload:**
    *   Subir o vídeo piloto (que está renderizando) como `Privado` no canal de teste.

---

## 4. Checklist de Segurança
- [ ] Token do YouTube válido (`client_secrets.json`).
- [ ] Cota de API monitorada (Upload gasta 1600 unidades).
- [ ] Fallback: Se falhar upload, salvar metadados em JSON para upload manual.
