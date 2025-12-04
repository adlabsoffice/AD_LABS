# Minhas Regras de Projeto

**Última atualização:** 2025-12-02  
**Versão:** 1.0.0

---

## 🚨 REGRA DE OURO: COMUNICAÇÃO ANTES DE AÇÃO

### ⚠️ SEMPRE Fazer:
1. **EXPLICAR PRIMEIRO:** Antes de qualquer comando ou mudança, explique o plano.
2. **AGUARDAR ACORDO:** Só execute se o usuário concordar explicitamente ("pode fazer", "ok", "vá em frente").
3. **Mostrar diff completo:** Antes de aplicar mudanças em arquivos.
4. **Nunca assumir permissão implícita:** O silêncio não é consentimento.

### ❌ NUNCA Fazer:
- ❌ Executar comandos ou ferramentas sem explicar o "porquê" antes.
- ❌ Modificar arquivos "automaticamente" sem avisar.
- ❌ Assumir que entendeu sem confirmar com o usuário.

> **Trauma anterior:** Agente destruiu arquivos e Git por executar sem confirmação. ISSO NÃO PODE SE REPETIR.

---

## 🎯 Filosofia de Trabalho

- **Mansão, não Puxadinho**: Planejamento estruturado antes de execução
- **Modularidade Total**: Agentes independentes, testáveis e documentados
- **Delta Only**: Mudanças cirúrgicas, nunca reescrever arquivos inteiros
- **Evidence-Based**: Toda decisão baseada em specs, docs ou código real

---

## 🐍 Stack Preferido

### Backend Principal
- **Linguagem:** Python 3.x
- **Package Manager:** pip + venv
- **Estrutura:** Agentes modulares (classes independentes)

### APIs Utilizadas no Sistema

> **✅ Auditoria realizada em:** 02/12/2025  
> **📊 Status:** Todas testadas e validadas  
> **📄 Relatório completo:** `incubadora/INVENTARIO_APIS_ATIVAS.md`

#### Google APIs (Múltiplas Keys Especializadas)

**GOOGLE_API_KEY_VIDEO** ✅ ATIVA  
- **Gemini 2.5 Pro** - `gemini-2.5-pro` (mais avançado disponível)
- **Gemini 2.5 Flash** - `gemini-2.5-flash` (rápido)
- **Gemini 2.0 Flash** - `gemini-2.0-flash` (produção)
- **Gemini 2.0 Flash Experimental** - `gemini-2.0-flash-exp`
- **Gemini 2.0 Image Gen** - `gemini-2.0-flash-exp-image-generation` 🎨
- Total: **40 modelos disponíveis**

**GOOGLE_API_KEY_AUDIO** ✅ ATIVA  
- Google Cloud Text-to-Speech (voz `pt-BR-Neural2-B`)
- Mesmos 40 modelos Gemini disponíveis

**GOOGLE_API_KEY_IMAGE** ✅ ATIVA  
- **Imagen 4.0 Standard** - `imagen-4.0-generate-preview-06-06`
- **Imagen 4.0 Ultra** - `imagen-4.0-ultra-generate-preview-06-06` 🚀
- **Gemini 3 Pro Image** - "Nano Banana Pro" (geração 4K profissional)
- Mesmos 40+ modelos Gemini disponíveis

---

### 🌐 Vertex AI Model Garden (Google Cloud - $300 Crédito)

> **Acesso via:** Google Cloud Console → Vertex AI → Model Garden  
> **Crédito Disponível:** $300 USD  
> **Status:** Conta ativa, modelos à disposição

#### 🎬 Geração de Vídeo (Veo)

**Veo 3** (Mais recente - Dezembro 2024)  
- 💰 **$0.75/segundo** (vídeo + áudio)  
- 💰 **$0.50/segundo** (só vídeo)  
- Exemplo: Vídeo 1min = **$45 USD** (com áudio)

**Veo 2**  
- 💰 **$0.50/segundo**  
- Exemplo: Vídeo 5min = **$150 USD**

⚠️ **CUSTO MUITO ALTO** - Usar com cautela!

#### 🎨 Geração de Imagem (Imagen - Vertex AI)

**Imagen 4 Ultra**  
- 💰 $0.06/imagem (R$ 0,36)  
- Mais alta qualidade

**Imagen 4** (Padrão)  
- 💰 $0.04/imagem (R$ 0,24)

**Imagen 4 Fast**  
- 💰 $0.02/imagem (R$ 0,12)  
- Rápido e econômico

**Imagen 3 / 3 Fast**  
- Também disponíveis com preços similares

**Serviços Adicionais:**
- Edição/Inpainting: $0.02/imagem
- Upscaling (aumentar resolução): $0.003/imagem

#### 🎵 Geração de Música (Lyria 2)

**Lyria 2** - IA de música do Google DeepMind  
- 💰 **$0.06 por 30 segundos** de música  
- Exemplo: 3 min de música = **$0.36 USD**  
- Gera música original baseada em prompts

#### 🧠 LLMs via Vertex AI Model Garden

**Claude 3.5 (Anthropic via Vertex)**  
- `claude-3-5-sonnet`: $3.00 input / $15.00 output (por 1M tokens)  
- `claude-3-5-haiku`: $0.80 input / $4.00 output (mais barato)

**Llama (Meta via Vertex)**  
- `llama-3.1-405b`: $5.00 input / $16.00 output  
- `llama-3.3-70b`: $0.72 input / $0.72 output (econômico!)

**Mistral (via Vertex)**  
- `mistral-large`: $2.00 input / $6.00 output

#### 🎤 Text-to-Speech (Cloud TTS)

**Cloud TTS Neural2** (Voz pt-BR-Neural2-B)  
- 💰 $16.00 por 1 milhão de caracteres  
- ~500 palavras = 3.000 caracteres = **$0.048 USD**  
- Já configurado e em uso no `agente_03_narrador.py`

#### LLM APIs

**GROQ_API_KEY** ✅ ATIVA (20 modelos)  
- `llama-3.1-8b-instant` - LLM rápido
- `llama-3.3-70b-versatile` - Llama 3.3 mais capaz
- `llama-4-scout-17b` & `llama-4-maverick-17b` - Llama 4 (experimental)
- `groq/compound` & `compound-mini` - Modelos Groq
- `whisper-large-v3-turbo` - Transcrição de áudio
- `playai-tts-arabic` - TTS multilíngue
- `qwen/qwen3-32b` - LLM chinês
- `moonshotai/kimi-k2-instruct-0905` - LLM chinês

**ANTHROPIC_API_KEY (Claude)** ✅ ATIVA  
- `claude-sonnet-4-20250514` - Claude Sonnet 4 (mais recente)
- `claude-3-5-sonnet-20241022` - Claude 3.5 Sonnet
- `claude-3-opus-latest` - Claude 3 Opus

**Claude via AWS Bedrock** ✅ CÓDIGO EXISTE  
- Arquivo: `automate_aws_tasks.py` tem integração Bedrock
- Modelos disponíveis: Claude via AWS (precisa ativar no console)
- Usado para: Tarefas automatizadas AWS

**Claude via Google Vertex AI** ⚠️ A VERIFICAR  
- Possível via Vertex AI Model Garden
- Necessário habilitar no Google Cloud Console

~~**XAI_API_KEY**~~ ❌ INATIVA  
Key retornou erro 404 - desativada ou expirada

#### Social Media APIs

**TELEGRAM_BOT_TOKEN** ✅ ATIVA  
- Token: `8023515576:AAGxblQlQUcm7QG8MA2ebVN1MbDKimNgTco`
- Bot: `@adlabs_boss_bot`
- Chat ID salvo em: `telegram_id.txt`
- Usado para: Notificações automáticas da fábrica de vídeos
- Scripts: `get_telegram_id.py`, `send_telegram_help.py`

**INSTAGRAM_USER / INSTAGRAM_PASSWORD** ⚠️ NO .ENV  
- Usado em: `agente_08_instagram.py`
- Biblioteca: `instagrapi`
- Função: Postagem automática de vídeos no Instagram
- Status: Credenciais no `.env` (não exportadas aqui por segurança)

**TikTok API** ❌ NÃO CONFIGURADA  
- Mencionado em: `sapg.py` (exemplo de tema)
- Sem credenciais ou agente específico implementado

#### Outras APIs

- **YouTube Data API** - Pesquisa de vídeos e métricas (quota a verificar)
- **Elevenlabs** - TTS premium (opcional, não testado)

---

### 🌐 Vertex AI Model Garden (Google Cloud)

> **Arsenal Completo via $300 crédito GCP**  
> Acesso a modelos de múltiplos fornecedores via API unificada

#### 🎬 Geração de Vídeo

**Veo 3** ✅ DISPONÍVEL (🚨 Alto custo)
- **Veo 3 + Audio:** $0.75/segundo (R$ 4,50/seg)
- **Veo 3 só vídeo:** $0.50/segundo (R$ 3,00/seg)
- **Veo 2:** $0.50/segundo
- **Uso recomendado:** Thumbnails animados (5-10s) = 40-60 com $300
- **Evitar:** Vídeos longos (1 min = $45 USD)

#### 🎵 Geração de Música

**Lyria 2** ✅ DISPONÍVEL
- **Preço:** $0.06 por 30 segundos (R$ 0,36)
- **Uso:** Background music para vídeos
- **$300 gera:** ~500 faixas de 30s

#### 🤖 LLMs via Model Garden

**Claude 3.5 (via Google)**
- **Sonnet:** $3/1M input, $15/1M output
- **Haiku:** $0.80/1M input, $4/1M output (mais barato que Anthropic direta!)

**Llama (Meta)**
- **Llama 3.1 405B:** $5/1M input, $16/1M output (modelo gigante)
- **Llama 3.3 70B:** $0.72/1M (input/output) - 🏆 **MELHOR CUSTO-BENEFÍCIO**

**Mistral**
- **Mistral Large:** $2/1M input, $6/1M output

#### 📊 Análise de Custo-Benefício ($300 crédito)

**Para Roteiros/Texto:**
1. 🥇 Gemini 2.0 Flash: $0.15/1M (mais barato)
2. 🥈 Llama 3.3 70B: $0.72/1M (excelente)
3. 🥉 Claude Haiku: $0.80/1M

**Para Imagens:**
1. 🥇 Imagen 4 Fast: $0.02/img = 15.000 imagens
2. 🥈 Imagen 4: $0.04/img = 7.500 imagens
3. 🥉 Imagen 4 Ultra: $0.06/img = 5.000 imagens

**Para Áudio TTS:**
- Cloud TTS Neural2: $16/1M caracteres = 18.7M chars com $300

### Bibliotecas Core
```python
# Essenciais (sempre presente)
rich                    # Interface CLI elegante
python-dotenv          # Variáveis de ambiente
requests               # HTTP requests

# Processamento
pandas                 # Análise de dados
moviepy                # Edição de vídeo
paramiko               # SSH/Deploy

# IA/ML (quando necessário)
groq                   # API Groq
google-api-python-client  # APIs Google
instagrapi             # Instagram automation

# Cloud
boto3                  # AWS SDK
```

### Frontend (quando necessário)
- **Preferência:** HTML + Vanilla CSS + JavaScript
- **Framework:** Evitar por padrão, usar Vite se necessário
- **Styling:** CSS Vanilla (máxima flexibilidade)

---

## 📂 Estrutura de Pastas Padrão

### Projeto Principal (AD_LABS)
```
projeto/
├── incubadora/              # Sistema principal
│   ├── agentes/            # Agentes numerados (01-11)
│   │   ├── agente_01_*.py
│   │   ├── agente_02_*.py
│   │   └── ...
│   ├── canais/             # Configurações por canal
│   │   └── nome_canal/
│   │       ├── config.json
│   │       └── outputs/
│   ├── n8n_workflows/      # Workflows de automação
│   ├── utils/              # Funções compartilhadas
│   ├── .env                # Variáveis de ambiente (NUNCA commitar)
│   ├── requirements.txt    # Dependências
│   └── incubadora.py       # Orquestrador principal
├── specs/                   # Especificações técnicas (.md)
├── outputs/                 # Outputs temporários
├── old/                     # Código deprecated (NUNCA deletar)
└── README.md
```

### Agentes (Prompts)
```
agentes/
├── Meta_Prompts/           # 37 prompts de meta-engenharia
├── Marketing_Vendas/       # 28 prompts de marketing
├── Copywriting_Conteudo/   # 25 prompts de copy
├── Desenvolvimento/        # 16 prompts dev
├── [outras categorias]
├── CATALOGO_AGENTES.md     # Índice completo
└── CATALOGO_AGENTES.csv    # Para análise

### 🗺️ Mapa da Mansão (Estrutura de Pastas)

**Raiz (`/`):**
- `docs/`: Documentação geral, handovers, manuais.
- `scripts/`: Scripts de manutenção, setup e debug que não são do core.
- `logs/`: Arquivos de log (gitignored).
- `outputs/`: Saídas gerais (gitignored).
- `incubadora/`: O sistema principal.

**Incubadora (`/incubadora`):**
- `agentes/`: Apenas os agentes numéricos (01-11).
- `core/`: Lógica central (Orquestrador, Classes Base).
- `services/`: Serviços reutilizáveis (ImageGen, TTS, VideoRender).
- `utils/`: Utilitários puros (não de negócio).
- `scripts/`: Scripts operacionais da incubadora.
  - `deploy/`: Scripts de deploy (AWS, GCP).
  - `ops/`: Scripts de verificação, fix e manutenção.
  - `tests/`: Scripts de teste pontuais.
- `docs/`: Documentação técnica específica da incubadora.

---

---

## 🏗️ Padrões de Arquitetura e Organização

### Contexto de Execução
- **Regra:** Scripts devem ser executados como módulos a partir da raiz do projeto.
- **Motivo:** Evita "hacks" de `sys.path.append` e garante resolução correta de imports.
- **Padrão:** `python -m incubadora.run_agents` em vez de `python incubadora/run_agents.py`.
- **Obs:** *Refatoração pendente para adotar este padrão em todo o sistema.*

### Organização de Arquivos
- **Regra:** A raiz do projeto deve conter apenas arquivos essenciais de configuração e documentação de entrada.
- **Anti-Padrão:** Scripts soltos (`teste.py`, `debug.py`) na raiz.
- **Destinos Corretos:**
  - Scripts de teste/debug -> `tests/` ou `scripts/debug/`
  - Scripts de setup -> `scripts/setup/`
  - Documentação -> `docs/` ou `specs/`
  - Logs e Outputs -> `logs/` e `outputs/` (gitignored)

---

## 🔧 Convenções de Código

### Nomenclatura Python

**Arquivos:**
```python
# Agentes numerados com prefixo
agente_01_inicializador.py
agente_02_pesquisador.py

# Utilitários descritivos
json_utils.py
progress_utils.py
```

**Classes:**
```python
# PascalCase, descritivo
class Agente01Inicializador:
class ErroNichoInvalido(Exception):
```

**Funções/Métodos:**
```python
# snake_case, verbos quando ações
def gerar_id_unico(self) -> str:
def validar_nicho(self, nicho: str) -> bool:
def coletar_apis_disponiveis(self) -> Dict[str, bool]:
```

**Variáveis:**
```python
# snake_case, descritivo
config_file = "T00_config.json"
orcamento_maximo_mensal = 0
apis_disponiveis = {}
```

### Nomenclatura de Arquivos de Output

**Padrão Timestamp:**
```
T00_config.json          # T=0 (Inicializador)
T01_canais_referencias.csv   # T=1 (Pesquisador)
T02_clusters.json        # T=2 (Analista)
T03_eixos/
  ├── eixo_01.json       # Numeração com zero à esquerda
  ├── eixo_02.json
  └── ...
```

### Estrutura de Classes (Agentes)

```python
"""
AGENTE XX: NOME
Timestamp: T=X
Responsabilidade: [Descrição clara]
"""

import os
import json
from typing import Dict, Optional
from rich.console import Console

console = Console()


class ErroCustomizado(Exception):
    """Exceções específicas do agente."""
    pass


class AgenteXXNome:
    """
    Agente XX: Nome
    [Descrição detalhada]
    """
    
    def __init__(self):
        self.output_path = "outputs"
        self.config_file = "TXX_nome_output.json"
    
    def executar(self, input_data: Optional[Dict] = None) -> Dict:
        """
        Método principal de execução.
        
        Args:
            input_data: Dados de entrada (geralmente JSON do agente anterior)
        
        Returns:
            Dict com resultado do processamento
        """
        console.print(Panel.fit(
            f"[bold cyan]Agente {XX}: {Nome}[/bold cyan]",
            title="T={X}"
        ))
        
        try:
            # Lógica principal aqui
            resultado = self._processar(input_data)
            self._salvar_output(resultado)
            return resultado
            
        except ErroCustomizado as e:
            console.print(f"[bold red]❌ Erro: {e}[/bold red]")
            raise


def main():
    """Teste standalone do agente."""
    agente = AgenteXXNome()
    resultado = agente.executar()


if __name__ == "__main__":
    main()
```

---

## 📝 Documentação Obrigatória

### Por Agente
```markdown
# AGENTE_XX_NOME.md

## Visão Geral
- **Timestamp:** T=X
- **Input:** [arquivo ou dado]
- **Output:** [arquivo gerado]
- **Tempo estimado:** Xmin
- **Dependências:** [APIs/libs]

## Responsabilidade
[Descrição clara do que faz]

## Fluxo de Execução
1. Passo 1
2. Passo 2
...

## Tratamento de Erros
- Erro X: Comportamento Y
- Retry policy: [se aplicável]

## Exemplos
```python
# Código de exemplo
```
```

### README.md Mínimo
```markdown
# Nome do Projeto

## Setup Rápido
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env  # Editar com suas keys
```

## Uso
```bash
python incubadora.py --start
```

## Estrutura
[Breve descrição da arquitetura]
```

---

## 🚫 Anti-Padrões (NUNCA FAZER)

### Código
- ❌ **Emojis em código Python** (causa `UnicodeEncodeError` no Windows)
- ❌ **Hardcoded API keys** (sempre usar `.env`)
- ❌ **Deletar código funcional** (mover para `/old` se deprecado)
- ❌ **Sobrescrever arquivos inteiros** (usar `multi_replace_file_content`)
- ❌ **Gerar 150 itens de uma vez** (sempre loop de 1 item por vez)

### Arquitetura
- ❌ **Monólitos >500 linhas** (quebrar em agentes/módulos)
- ❌ **Agentes que dependem de memória de contexto** (deliverables salvos)
- ❌ **Ordem implícita de execução** (usar timestamps T=0→T=X)

### Processos
- ❌ **Executar sem brief aprovado**
- ❌ **Modificar arquivos sem mostrar diff**
- ❌ **Assumir que "melhorias" são desejadas**
- ❌ **Pular validação de inputs**

---

## 🛠️ Ferramentas Obrigatórias

### Desenvolvimento
- **Editor:** VS Code
- **Python:** 3.8+ (preferencialmente 3.11+)
- **Git:** Sempre fazer checkpoints antes de mudanças críticas

### Deploy/Cloud
- **Preferência:** Google Cloud Platform (GCP)
- **Alternativa:** AWS (quando necessário)
- **Automação:** n8n workflows

### CLI
- **Interface:** `rich` (painéis, cores, spinners)
- **Prompts:** `rich.prompt` (validações inline)
- **Progress:** Arquivos JSON (não prints temporários)

---

## 🔐 Segurança & Ambiente

### .env Template
```bash
# LLM APIs
GEMINI_API_KEY=your_key_here
GROQ_API_KEY=your_key_here

# Social APIs
YOUTUBE_DATA_API_KEY=your_key_here
INSTAGRAM_USERNAME=your_username
INSTAGRAM_PASSWORD=your_password

# Cloud
GCP_PROJECT_ID=your_project_id
AWS_ACCESS_KEY_ID=your_key_id
AWS_SECRET_ACCESS_KEY=your_secret_key

# Telegram (notificações)
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
```

### .gitignore Essencial
```
# Ambiente
.env
.env.*
venv/
__pycache__/

# API Keys
*.pem
*_secret.json
gcp-credentials.json

# Outputs temporários
outputs/
*.mp4
*.mp3

# IDE
.vscode/
.idea/
```

---

## 📊 Tracking & Progress

### Arquivos de Estado
```json
// progress.json
{
  "timestamp_atual": "T=3",
  "ultimo_agente": "arquiteto_eixos",
  "status": "completo",
  "proxima_acao": "Executar Agente 04",
  "checkpoint": {
    "eixos_criados": 5,
    "ideias_geradas": 10,
    "videos_produzidos": 0
  }
}
```

### Logging
```python
# Sempre usar rich.console
console.print("[green]✅ Sucesso[/green]")
console.print("[yellow]⚠️ Aviso[/yellow]")
console.print("[red]❌ Erro[/red]")
console.print("[dim]Informação secundária[/dim]")
```

---

## 🧪 Testing

### Teste Standalone (cada agente)
```python
if __name__ == "__main__":
    # Sempre ter um main() testável
    agente = AgenteXXNome()
    resultado = agente.executar()
    console.print(json.dumps(resultado, indent=2))
```

### Validação de Output
```python
def validar_output(self, dados: Dict) -> bool:
    """Sempre validar antes de salvar."""
    campos_obrigatorios = ["timestamp", "status", "dados"]
    
    for campo in campos_obrigatorios:
        if campo not in dados:
            raise ValueError(f"Campo obrigatório ausente: {campo}")
    
    return True
```

---

## 🎨 Preferências de Interface

### CLI
- **Painéis:** Para separar seções visualmente
- **Spinners:** Para processos longos
- **Confirmações:** Para ações destrutivas
- **Cores consistentes:**
  - Verde: Sucesso
  - Amarelo: Aviso
  - Vermelho: Erro
  - Cyan: Títulos/Headers
  - Dim: Info secundária

### Web (quando necessário)
- **Design:** Moderno, dark mode por padrão
- **Cores:** Paletas harmônicas (evitar RGB básico)
- **Tipografia:** Google Fonts (Inter, Roboto, Outfit)
- **Animações:** Micro-interações suaves

---

## 📌 Ordem de Prioridades

1. **Funcionalidade** > Estética
2. **Modularidade** > Performance (até ter problemas reais)
3. **Documentação clara** > Código "esperto"
4. **Failover/Retry** > Assumir sucesso
5. **Salvar estado** > Confiar em memória

---

## 🔄 Workflow Git

### Checkpoints Críticos
```bash
# Antes de implementar novo agente
git add .
git commit -m "Checkpoint: Antes de implementar Agente XX"

# Após completar agente funcional
git add .
git commit -m "feat: Agente XX - [Nome] implementado e testado"

# Antes de mudanças arquiteturais
git add .
git commit -m "Checkpoint: Antes de refatoração [descrição]"
```

---

## 💡 Filosofia de Erros

### Sempre Implementar
```python
# 1. Exceptions customizadas
class ErroNichoInvalido(Exception):
    pass

# 2. Try-except com mensagens claras
try:
    resultado = processar()
except ErroEspecifico as e:
    console.print(f"[red]❌ Erro: {e}[/red]")
    raise  # Re-raise para não esconder

# 3. Validações na entrada
def executar(self, input_data: Dict):
    if not input_data:
        raise ValueError("Input não pode ser vazio")
```

### Retry Policy (quando aplicável)
```python
import time

MAX_RETRIES = 3
RETRY_DELAY = 2  # segundos

for tentativa in range(MAX_RETRIES):
    try:
        resultado = api.call()
        break
    except APIError as e:
        if tentativa < MAX_RETRIES - 1:
            console.print(f"[yellow]Retry {tentativa+1}/{MAX_RETRIES}[/yellow]")
            time.sleep(RETRY_DELAY * (tentativa + 1))  # Exponential backoff
        else:
            raise
```

---

## 🎯 Critérios de "Pronto"

### Para Agente
- ✅ Função `executar()` implementada
- ✅ Validação de input/output
- ✅ Tratamento de erros específicos
- ✅ Logging com `rich.console`
- ✅ Teste standalone (`main()`)
- ✅ Spec atualizada em `/specs`

### Para Projeto
- ✅ Todos agentes testados isoladamente
- ✅ Fluxo end-to-end T=0→T=X funcional
- ✅ README.md com instruções claras
- ✅ `.env.example` documentado
- ✅ Failover testado (quota exceeded)
- ✅ Outra pessoa consegue rodar seguindo README

---

**🃏 Estas regras são a fundação. Mansão, não puxadinho.**
