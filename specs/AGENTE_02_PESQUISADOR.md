# AGENTE 02: PESQUISADOR
> **Timestamp**: T=1  
> **Responsabilidade**: Buscar canais internacionais de referência e coletar dados para análise

---

## 🎯 OBJETIVO

Pesquisar YouTube em múltiplos idiomas, coletar 300-400 vídeos relevantes ao nicho, e salvar CSV estruturado para análise.

---

## 📥 INPUT

### Arquivo: `outputs/T00_config.json`

```json
{
  "projeto": {
    "nicho": "Mistérios Perturbadores"
  },
  "apis_disponiveis": {
    "youtube_data": true
  }
}
```

---

## 📤 OUTPUT

### Arquivo: `outputs/T01_canais_referencias.csv`

**Estrutura CSV**:
```csv
video_id,canal_id,canal_nome,titulo,views,likes,comentarios,duracao_segundos,data_publicacao,idioma,url
dQw4w9WgXcQ,UC123abc,Canal Exemplo,Título do Vídeo,1000000,50000,2000,480,2024-11-01,en,https://...
...
```

**Campos obrigatórios**:
- `video_id`: ID único do YouTube
- `canal_id`: ID do canal
- `canal_nome`: Nome do canal
- `titulo`: Título do vídeo
- `views`: Número de visualizações
- `likes`: Curtidas
- `comentarios`: Número de comentários
- `duracao_segundos`: Duração em segundos
- `data_publicacao`: Data ISO 8601
- `idioma`: Código (pt-br, en-us, es)
- `url`: URL completa

---

## 🔍 ESTRATÉGIA DE PESQUISA

### Termos de Busca por Nicho

**Sistema dinâmico**: Gerar termos baseado no nicho fornecido.

**Template de Geração**:
```python
nicho = config["projeto"]["nicho"]

# Usar Gemini para gerar termos
prompt = f"""
Nicho: {nicho}

Gere 9 termos de busca (3 por idioma) que encontrariam 
canais desse nicho no YouTube:

PT-BR (3 termos):
EN-US (3 termos):
ES (3 termos):

Formato: lista simples, sem numeração
"""

termos = gemini.generate(prompt)
```

**Exemplo para "Mistérios Perturbadores"**:
```
PT-BR:
- mistérios inexplicáveis
- casos perturbadores
- enigmas sem solução

EN-US:
- unsolved mysteries
- disturbing cases
- creepy facts

ES:
- misterios sin resolver
- casos perturbadores
- hechos extraños
```

### Lotes (Batches) de Pesquisa

Dividir em 4 lotes para controle:

```python
LOTES = [
    {"nome": "BR_Core", "termos": termos_pt[:3], "max_results": 100},
    {"nome": "US_Trends", "termos": termos_en[:3], "max_results": 120},
    {"nome": "US_Deep", "termos": termos_en[3:6], "max_results": 80},
    {"nome": "Latam", "termos": termos_es[:3], "max_results": 100}
]
```

### Sistema de Failover (4 API Keys)

```python
API_KEYS = [
    os.getenv("YOUTUBE_KEY_A"),
    os.getenv("YOUTUBE_KEY_B"),
    os.getenv("YOUTUBE_KEY_C"),
    os.getenv("YOUTUBE_KEY_D")
]

current_key_index = 0

def pesquisar_com_failover(termo, max_results):
    global current_key_index
    
    for tentativa in range(len(API_KEYS)):
        try:
            key = API_KEYS[current_key_index]
            resultados = youtube_search(termo, key, max_results)
            return resultados
            
        except QuotaExceededError:
            print(f"⚠️ Chave {current_key_index} excedeu quota")
            current_key_index = (current_key_index + 1) % len(API_KEYS)
            
        except TimeoutError:
            print(f"⏱️ Timeout - Retry...")
            time.sleep(5)
    
    raise ErroTodasChavesFalharam()
```

---

## ✅ VALIDAÇÕES

### Input Validation
- ✅ `T00_config.json` existe
- ✅ Campo `nicho` não vazio
- ✅ `youtube_data: true` nas APIs disponíveis
- ✅ Pelo menos 1 API key configurada

### Output Validation
- ✅ CSV gerado com > 200 vídeos
- ✅ Todos campos obrigatórios presentes
- ✅ Nenhuma duplicata (por `video_id`)
- ✅ Pelo menos 2 idiomas representados
- ✅ Vídeos de pelo menos 10 canais diferentes

---

## ⚠️ TRATAMENTO DE ERROS

| Erro | Ação |
|------|------|
| Quota Exceeded (403) | Trocar para próxima API key |
| Timeout | Retry com exponential backoff (5s, 10s, 20s) |
| Nenhum resultado | Tentar termo alternativo |
| Todas keys falharam | Abortar e reportar |
| CSV corrompido | Regenerar do raw data |

---

## 🔧 IMPLEMENTAÇÃO

### Pseudo-código
```python
def agente_pesquisador():
    # 1. Ler config
    config = ler_json("outputs/T00_config.json")
    nicho = config["projeto"]["nicho"]
    
    # 2. Gerar termos de busca
    termos = gerar_termos_busca(nicho)
    
    # 3. Inicializar
    todos_videos = []
    api_key_index = 0
    
    # 4. Para cada lote
    for lote in LOTES:
        print(f"📦 Processando: {lote['nome']}")
        
        for termo in lote["termos"]:
            try:
                # Buscar com failover
                videos = pesquisar_com_failover(
                    termo, 
                    lote["max_results"]
                )
                todos_videos.extend(videos)
                print(f"  ✅ {len(videos)} vídeos - {termo}")
                
            except Exception as e:
                print(f"  ❌ Erro: {e}")
                continue
    
    # 5. Remover duplicatas
    videos_unicos = remover_duplicatas(todos_videos, key="video_id")
    
    # 6. Validar mínimo
    if len(videos_unicos) < 200:
        print(f"⚠️ Apenas {len(videos_unicos)} vídeos. Mínimo: 200")
        # Tentar termos adicionais...
    
    # 7. Salvar CSV
    df = pd.DataFrame(videos_unicos)
    df.to_csv("outputs/T01_canais_referencias.csv", index=False)
    
    # 8. Atualizar progress
    atualizar_progress("T=1", "pesquisador")
    
    print(f"✅ {len(videos_unicos)} vídeos coletados")
    return videos_unicos
```

---

## 📋 EXEMPLO CONCRETO

### Input
```json
{
  "projeto": {"nicho": "Fatos Curiosos"},
  "apis_disponiveis": {"youtube_data": true}
}
```

### Execução (Log)
```
🔍 AGENTE 02: PESQUISADOR
==================================================
Nicho: Fatos Curiosos
Gerando termos de busca...

PT-BR: fatos curiosos, top 10 fatos, coisas estranhas
EN-US: interesting facts, top facts, weird facts
ES: datos curiosos, hechos extraños, top datos

📦 Lote 01: BR_Core
  ✅ 82 vídeos - fatos curiosos
  ✅ 78 vídeos - top 10 fatos
  ⚠️ Chave A excedeu quota → Failover para Chave B
  ✅ 65 vídeos - coisas estranhas

📦 Lote 02: US_Trends
  ✅ 105 vídeos - interesting facts
  ✅ 92 vídeos - top facts
  ⏱️ Timeout → Retry (sucesso)
  ✅ 88 vídeos - weird facts

📦 Lote 03: US_Deep
  [processando...]

📦 Lote 04: Latam
  [processando...]

📊 Resumo:
- Total bruto: 385 vídeos
- Após deduplicação: 342 vídeos
- Idiomas: PT-BR (110), EN-US (180), ES (52)
- Canais únicos: 45

✅ Arquivo salvo: outputs/T01_canais_referencias.csv
```

### Output (primeiras 3 linhas do CSV)
```csv
video_id,canal_id,canal_nome,titulo,views,likes,comentarios,duracao_segundos,data_publicacao,idioma,url
abc123,UC111,Fatos Insanos,10 Fatos que Vão Te Chocar,500000,25000,1200,420,2024-10-15,pt-br,https://youtube.com/watch?v=abc123
def456,UC222,Amazing Facts,Top 10 Weird Facts,1200000,60000,3500,380,2024-10-20,en-us,https://youtube.com/watch?v=def456
ghi789,UC333,Datos Locos,Hechos Increíbles,350000,18000,800,450,2024-10-10,es,https://youtube.com/watch?v=ghi789
```

---

## 🧪 TESTES

### Teste 1: Geração de Termos
```python
def test_gerar_termos():
    nicho = "Histórias de Terror"
    termos = gerar_termos_busca(nicho)
    
    assert len(termos) == 9  # 3 por idioma
    assert any("terror" in t.lower() or "horror" in t.lower() for t in termos)
```

### Teste 2: Failover de API Keys
```python
def test_failover_api_keys():
    # Simular quota exceeded na chave A
    with patch('youtube_search') as mock:
        mock.side_effect = [QuotaExceededError(), videos_validos]
        
        resultado = pesquisar_com_failover("teste", 50)
        
        # Deve ter usado chave B
        assert mock.call_count == 2
        assert len(resultado) > 0
```

### Teste 3: Validação Mínima
```python
def test_validacao_minima():
    # Simular poucos resultados
    videos = [{"video_id": f"v{i}"} for i in range(150)]
    
    with pytest.raises(ErroVideoInsuficientes):
        validar_output(videos)  # Mínimo: 200
```

---

## 📊 MÉTRICAS

- **Tempo esperado**: 10-20 minutos
- **Complexidade**: Média/Alta
- **Dependências**: YouTube Data API v3, pandas
- **Tamanho contexto**: ~150 linhas
- **API calls**: ~30-50 requests

---

## 🔐 SEGURANÇA

### Variáveis de Ambiente
```bash
# .env
YOUTUBE_KEY_A=AIza...
YOUTUBE_KEY_B=AIza...
YOUTUBE_KEY_C=AIza...
YOUTUBE_KEY_D=AIza...
```

### Rate Limiting
- Máx 100 resultados por request
- Delay de 1s entre requests
- Pool de 4 keys = 40.000 requests/dia

---

## ✅ CRITÉRIO DE SUCESSO

Agente completou com sucesso quando:
1. ✅ CSV gerado com 200-400 vídeos
2. ✅ Múltiplos idiomas representados
3. ✅ Nenhuma duplicata
4. ✅ Progress atualizado para T=1
5. ✅ Próxima etapa: T=2 (Analista)

---

**Status**: 📝 Spec Completa  
**Pronto para**: Implementação
