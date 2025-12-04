# Configuração de Canal - AD_LABS

## Como criar arquivo de configuração

O arquivo `canal_config.json` deve ser criado em:
```
d:\AD_LABS\incubadora\config\<nome_do_canal>\canal_config.json
```

**Nota:** Este arquivo está no `.gitignore` por conter configurações sensíveis/específicas de cada ambiente.

## Template para "O Livro Caixa Divino"

Crie o arquivo `d:\AD_LABS\incubadora\config\o_livro_caixa_divino\canal_config.json` com o seguinte conteúdo:

```json
{
  "canal_id": "o_livro_caixa_divino",
  "nome_canal": "O Livro Caixa Divino",
  "descricao": "Canal onde Jesus reage a temas modernos usando parábolas e ensinamentos bíblicos",
  
  "configuracoes_video": {
    "duracao_alvo_segundos": 60,
    "duracao_maxima_segundos": 70,
    "aspect_ratio": "16:9",
    "resolucao": "1920x1080",
    "fps": 30
  },
  
  "configuracoes_imagem": {
    "provider": "imagen",
    "model": "imagen-4-standard",
    "quality": "hd",
    "use_character_reference": true,
    "visual_style": "cinematic lighting, 4k quality, dramatic composition, realistic style, warm color grading"
  },
  
  "configuracoes_audio": {
    "provider": "google_cloud",
    "fallback": ["google_cloud"],
    "voice_id": "pt-BR-Neural2-B",
    "speed": 1.15,
    "pitch": 0.0,
    "target_wpm_min": 168,
    "target_wpm_max": 187
  },
  
  "personagens": {
    "jesus": {
      "name": "Jesus",
      "description": "Homem de 30 anos, pele morena clara, cabelos castanhos ondulados até os ombros, barba castanha bem cuidada, olhos castanhos profundos e expressivos, túnica branca simples com cinto de corda, sandálias de couro, expressão serena e compassiva, postura confiante mas acessível",
      "style_keywords": [
        "cinematic lighting",
        "4k quality",
        "dramatic composition",
        "realistic style",
        "warm color grading",
        "soft bokeh background"
      ],
      "reference_image": null,
      "appearance_count": 0
    },
    "narrador": {
      "name": "Narrador",
      "description": "Voz neutra e confiável, sem representação visual. Usado para contexto narrativo e transições.",
      "style_keywords": [],
      "reference_image": null,
      "appearance_count": 0
    }
  },
  
  "templates": {
    "padrao": "react",
    "disponiveis": ["react", "news", "drama", "pixar"]
  },
  
  "telegram": {
    "checkpoints_habilitados": true,
    "timeout_minutos": 10,
    "enviar_previews": true
  },
  
  "metadados": {
    "criado_em": "2024-12-04",
    "versao": "2.0",
    "status": "ativo"
  }
}
```

## Estrutura dos Campos

### configuracoes_imagem
- `provider`: "imagen" ou "midjourney"
- `model`: "imagen-4-standard" ou "imagen-4-ultra"
- `use_character_reference`: true para consistência de personagens

### configuracoes_audio
- `provider`: "google_cloud", "chirp" ou "elevenlabs"
- `fallback`: array de providers alternativos
- `voice_id`: ID da voz (veja lista em `services/tts_strategy.py`)

### personagens
Cada personagem deve ter:
- `name`: Nome único
- `description`: Descrição física detalhada (50-500 chars)
- `style_keywords`: Array de keywords de estilo
- `reference_image`: Path da primeira imagem (preenchido automaticamente)
- `appearance_count`: Contador de aparições (preenchido automaticamente)

## Como os Agentes Usam Este Config

### Agente Visual (07)
```python
visual = Agente07Visual(
    canal_id="o_livro_caixa_divino",
    config=canal_config["configuracoes_imagem"]
)
```

### Agente Narrador (08)
```python
narrador = Agente08Narrador(
    canal_id="o_livro_caixa_divino",
    config=canal_config["configuracoes_audio"]
)
```

### Character Manager
Carrega automaticamente `personagens` do config.

## Comandos Úteis

**Criar diretório do canal:**
```bash
mkdir -p d:\AD_LABS\incubadora\config\o_livro_caixa_divino
```

**Validar JSON:**
```bash
python -c "import json; json.load(open('d:/AD_LABS/incubadora/config/o_livro_caixa_divino/canal_config.json'))"
```

**Testar pipeline com config:**
```bash
python run_agents.py --canal o_livro_caixa_divino --fase producao
```
