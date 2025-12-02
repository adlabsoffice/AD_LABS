# 📘 Manual de Instalação: New TTS (Clonagem de Voz Local)

Este guia foi extraído do seu arquivo de conhecimento: `11_Clone_Voice_Local_TTS_Tutorial_Gratuito.md`.

> [!IMPORTANT]
> **Sobre o Link de Download:** O arquivo original menciona que o link está na "descrição do vídeo original" do canal *The Oracle Guy*. Como não tenho acesso ao YouTube, você precisará localizar esse link no vídeo original ou usar o repositório oficial no GitHub (Newonic/New-TTS), embora o tutorial recomende a versão "One-Click" do Oracle Guy.

---

## 💻 Requisitos do Sistema

Antes de começar, verifique se seu PC aguenta:

*   **RAM:** Mínimo 8 GB (com 4 GB livres). Recomendado 32 GB para performance máxima.
*   **GPU (Placa de Vídeo):**
    *   **NVIDIA:** Funciona no modo rápido (GPU Version).
    *   **AMD / Intel / Sem Placa:** Funciona, mas deve usar a **CPU Version** (mais lento).
*   **Espaço em Disco:** ~5 GB livres.

---

## 🛠️ Passo a Passo de Instalação

### 1. Download
1.  Acesse o link do Google Drive (do vídeo do *The Oracle Guy*).
2.  Escolha a versão correta:
    *   Baixe **`GPU Version`** se tiver placa NVIDIA.
    *   Baixe **`CPU Version`** se tiver AMD ou não tiver placa de vídeo.
3.  **Nota:** O arquivo é grande (~1.5 GB a 3 GB).

### 2. Extração e Setup
1.  Você baixará um arquivo `.zip`. **Extraia** para uma pasta simples (ex: `C:\NewTTS`).
2.  Dentro da pasta, procure o arquivo **`ngspe.exe`**.
3.  Execute o `ngspe.exe` e instale (é um componente necessário de áudio, ~12 MB).

### 3. Primeira Execução
1.  Encontre o arquivo **`run_new_tts.bat`**.
2.  Clique duas vezes para rodar.
3.  Duas coisas vão acontecer:
    *   Uma janela preta (Terminal) vai abrir. **Não feche ela.**
    *   Seu navegador vai abrir automaticamente com a interface do programa.
4.  **Atenção:** Na primeira vez, ele vai baixar um "codec" extra de ~1.5 GB. Isso pode demorar um pouco. Tenha paciência.

---

## 🎙️ Como Usar (Básico)

### Gerar Fala Simples
1.  Vá na aba **"Generate Speech"**.
2.  Digite o texto.
3.  Escolha uma voz (ex: "Dave").
4.  Clique em **Generate**.

### Clonar uma Voz (O "Pulo do Gato")
1.  Vá na aba **"Instantly Clone New Voice"**.
2.  **Nome:** Dê um nome (ex: "Jesus Narrador").
3.  **Áudio de Referência:** Faça upload de um áudio limpo (3 a 10 segundos) da voz que quer clonar.
4.  **Texto de Referência:** Digite *exatamente* o que é dito no áudio de referência.
5.  Clique em **Clone Voice**.
6.  A nova voz aparecerá na lista da aba "Generate Speech".

---

## ⚠️ Dicas de Ouro (Do Arquivo 11)
*   **Samples:** Use áudios de alta qualidade e sem barulho de fundo. O site `101soundboards.com` é recomendado para achar vozes de famosos.
*   **Tom:** Se o áudio original for gritado, o clone vai gritar. Se for calmo, o clone será calmo. Para nosso canal, busque uma voz **calma, sábia e firme**.
