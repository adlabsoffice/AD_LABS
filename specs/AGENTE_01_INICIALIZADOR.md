# AGENTE 01: INICIALIZADOR
> **Timestamp**: T=0  
> **Responsabilidade**: Capturar informações iniciais e criar configuração base do projeto

---

## 🎯 OBJETIVO

Transformar input do usuário (nicho desejado) em configuração estruturada que será usada por todos os outros agentes.

---

## 📥 INPUT

### Fonte: CLI/Terminal (Interação com usuário)

**Perguntas a fazer**:
```
1. Qual nicho/tema você quer testar? 
   (ex: "Histórias Dramáticas", "Mistérios Perturbadores", "Fatos Curiosos")

2. Quais APIs você tem disponível?
   [ ] Gemini (gratuita)
   [ ] Claude
   [ ] OpenAI
   [ ] YouTube Data API
   [ ] Elevenlabs
   [ ] Outras: ___________

3. Qual seu orçamento máximo mensal por canal?
   (ex: R$ 0, R$ 100, R$ 500)

4. Prazo desejado?
   (ex: 3 dias, 1 semana, 1 mês)
```

---

## 📤 OUTPUT

### Arquivo: `outputs/T00_config.json`

**JSON Schema**:
```json
{
  "timestamp": "T=0",
  "data_criacao": "2025-11-28T15:20:00",
  "projeto": {
    "id": "canal_001",
    "nicho": "string",
    "status": "inicializado"
  },
  "apis_disponiveis": {
    "gemini": true/false,
    "claude": true/false,
    "openai": true/false,
    "youtube_data": true/false,
    "elevenlabs": true/false,
    "outras": []
  },
  "restricoes": {
    "orcamento_maximo_mensal": 500,
    "prazo_dias": 3,
    "modo": "mvp"
  },
  "proxima_etapa": "T=1"
}
```

### Arquivo: `outputs/progress.json`

```json
{
  "timestamp_atual": "T=0",
  "ultimo_agente": "inicializador",
  "status": "aguardando_pesquisa",
  "proxima_acao": "Executar Agente 02: Pesquisador",
  "checkpoint": {
    "eixos_criados": 0,
    "ideias_geradas": 0,
    "videos_produzidos": 0,
    "mare_identificada": false
  }
}
```

---

## ✅ VALIDAÇÕES

### Input Validation
- ✅ Nicho não pode ser vazio
- ✅ Nicho deve ter entre 3-50 caracteres
- ✅ Pelo menos 1 API deve estar disponível
- ✅ Orçamento >= 0
- ✅ Prazo >= 1 dia

### Output Validation
- ✅ Arquivo `T00_config.json` foi criado
- ✅ Todas propriedades obrigatórias presentes
- ✅ Arquivo `progress.json` existe
- ✅ JSON é válido (parseable)

---

## ⚠️ TRATAMENTO DE ERROS

| Erro | Ação |
|------|------|
| Usuário não responde | Usar valores default |
| Nicho inválido | Pedir novamente (max 3x) |
| Nenhuma API disponível | Erro crítico - abortar |
| Pasta `outputs/` não existe | Criar automaticamente |
| Arquivo já existe | Perguntar se sobrescreve |

---

## 🔧 IMPLEMENTAÇÃO

### Pseudo-código
```python
def agente_inicializador():
    print("🚀 INCUBADORA AD_LABS v2.0")
    print("=" * 50)
    
    # 1. Coletar informações
    nicho = input("Qual nicho você quer testar? ")
    
    # 2. Validar
    if not validar_nicho(nicho):
        raise ErroNichoInvalido()
    
    # 3. Perguntar APIs (checklist interativo)
    apis = coletar_apis_disponiveis()
    
    # 4. Coletar restrições
    orcamento = input("Orçamento máximo/mês (R$): ") or 0
    prazo = input("Prazo em dias: ") or 3
    
    # 5. Criar config
    config = {
        "timestamp": "T=0",
        "data_criacao": datetime.now().isoformat(),
        "projeto": {
            "id": gerar_id_unico(),
            "nicho": nicho,
            "status": "inicializado"
        },
        "apis_disponiveis": apis,
        "restricoes": {
            "orcamento_maximo_mensal": int(orcamento),
            "prazo_dias": int(prazo),
            "modo": "mvp" if prazo <= 3 else "completo"
        },
        "proxima_etapa": "T=1"
    }
    
    # 6. Salvar
    salvar_json("outputs/T00_config.json", config)
    atualizar_progress("T=0", "inicializador")
    
    # 7. Confirmar
    print("✅ Configuração salva!")
    print(f"📁 Arquivo: outputs/T00_config.json")
    
    return config
```

---

## 📋 EXEMPLO CONCRETO

### Input do Usuário
```
Nicho: Mistérios Perturbadores
APIs: [x] Gemini, [x] YouTube Data API, [ ] Outras
Orçamento: R$ 0 (grátis)
Prazo: 3 dias
```

### Output Gerado
**`outputs/T00_config.json`**:
```json
{
  "timestamp": "T=0",
  "data_criacao": "2025-11-28T15:20:00",
  "projeto": {
    "id": "canal_9f3a2b1c",
    "nicho": "Mistérios Perturbadores",
    "status": "inicializado"
  },
  "apis_disponiveis": {
    "gemini": true,
    "claude": false,
    "openai": false,
    "youtube_data": true,
    "elevenlabs": false,
    "outras": []
  },
  "restricoes": {
    "orcamento_maximo_mensal": 0,
    "prazo_dias": 3,
    "modo": "mvp"
  },
  "proxima_etapa": "T=1"
}
```

---

## 🧪 TESTES

### Teste 1: Happy Path
```python
def test_inicializador_happy_path():
    # Simular input
    mock_input = {
        "nicho": "Histórias Dramáticas",
        "apis": {"gemini": True, "youtube_data": True},
        "orcamento": 100,
        "prazo": 3
    }
    
    # Executar
    resultado = agente_inicializador(mock_input)
    
    # Validar
    assert resultado["projeto"]["nicho"] == "Histórias Dramáticas"
    assert resultado["apis_disponiveis"]["gemini"] == True
    assert os.path.exists("outputs/T00_config.json")
```

### Teste 2: Erro - Nicho Vazio
```python
def test_inicializador_nicho_vazio():
    mock_input = {"nicho": "", ...}
    
    with pytest.raises(ErroNichoInvalido):
        agente_inicializador(mock_input)
```

### Teste 3: Defaults
```python
def test_inicializador_defaults():
    mock_input = {"nicho": "Teste", "apis": {}, "orcamento": "", "prazo": ""}
    
    resultado = agente_inicializador(mock_input)
    
    assert resultado["restricoes"]["orcamento_maximo_mensal"] == 0
    assert resultado["restricoes"]["prazo_dias"] == 3
```

---

## 📊 MÉTRICAS

- **Tempo esperado**: 1-2 minutos (interação com usuário)
- **Complexidade**: Baixa
- **Dependências**: Nenhuma
- **Tamanho contexto**: ~50 linhas

---

## ✅ CRITÉRIO DE SUCESSO

Agente completou com sucesso quando:
1. ✅ Arquivo `T00_config.json` criado e válido
2. ✅ Arquivo `progress.json` atualizado
3. ✅ Todas validações passaram
4. ✅ Próxima etapa definida (T=1)

---

**Status**: 📝 Spec Completa  
**Pronto para**: Implementação
