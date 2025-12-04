"""
Script de teste de TODAS as APIs disponíveis + estimativa de custos
"""
import os
import json
from datetime import datetime

# Resultados
results = {
    "data_teste": datetime.now().isoformat(),
    "apis_testadas": {},
    "custos_estimados": {},
    "recomendacoes": []
}

print("🧪 TESTANDO TODAS AS APIS...")
print("=" * 60)

# 1. GOOGLE GEMINI 2.0 FLASH
print("\n1️⃣ Testando Gemini 2.0 Flash Experimental...")
try:
    import google.generativeai as genai
    
    # Tenta com KEY_VIDEO
    api_key = os.getenv("GOOGLE_API_KEY_VIDEO")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY_VIDEO não encontrada")
    
    genai.configure(api_key=api_key)
    
    # Lista modelos disponíveis
    models = genai.list_models()
    gemini_2_models = [m.name for m in models if "2.0" in m.name or "2.5" in m.name]
    
    # Testa Gemini 2.0 Flash
    if "models/gemini-2.0-flash-exp" in [m.name for m in models]:
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        response = model.generate_content("Diga apenas: OK")
        
        results["apis_testadas"]["Gemini 2.0 Flash"] = {
            "status": "✅ ATIVO",
            "modelo": "gemini-2.0-flash-exp",
            "resposta_teste": response.text,
            "modelos_2x_disponiveis": gemini_2_models
        }
        print(f"   ✅ Gemini 2.0 Flash: FUNCIONANDO")
        print(f"   📊 Modelos 2.x disponíveis: {len(gemini_2_models)}")
    else:
        results["apis_testadas"]["Gemini 2.0 Flash"] = {
            "status": "❌ NÃO DISPONÍVEL",
            "modelos_disponiveis": gemini_2_models
        }
        print(f"   ❌ Gemini 2.0 Flash: NÃO ENCONTRADO")
        
except Exception as e:
    results["apis_testadas"]["Gemini 2.0 Flash"] = {
        "status": "❌ ERRO",
        "erro": str(e)
    }
    print(f"   ❌ Erro: {e}")

# 2. GOOGLE IMAGEN 3
print("\n2️⃣ Testando Imagen 3 (2K)...")
try:
    from google.cloud import aiplatform
    
    # Lista modelos Imagen disponíveis
    # Nota: Imagen 3 pode não estar disponível via API pública ainda
    
    results["apis_testadas"]["Imagen 3"] = {
        "status": "⏳ VERIFICAÇÃO MANUAL NECESSÁRIA",
        "nota": "Imagen 3 pode estar disponível apenas via Vertex AI Studio",
        "alternativa": "Usar Imagen 4 Ultra (Nano Banana) que já funciona"
    }
    print(f"   ⏳ Imagen 3: Verificação manual necessária")
    print(f"   💡 Use Imagen 4 Ultra enquanto isso")
    
except Exception as e:
    results["apis_testadas"]["Imagen 3"] = {
        "status": "❌ ERRO",
        "erro": str(e)
    }
    print(f"   ❌ Erro: {e}")

# 3. VEO 2 (Geração de Vídeo)
print("\n3️⃣ Testando Veo 2 (Geração de Vídeo)...")
try:
    # Veo 2 está disponível via Vertex AI
    # Precisa de projeto GCP configurado
    
    results["apis_testadas"]["Veo 2"] = {
        "status": "⏳ REQUER VERTEX AI",
        "nota": "Disponível via Vertex AI Model Garden",
        "projeto": "fast-circle-479719-h8",
        "custo": "$0.75/segundo de vídeo (CARO!)"
    }
    print(f"   ⏳ Veo 2: Disponível via Vertex AI")
    print(f"   💰 CUSTO: $0.75/segundo (60s = $45!)")
    
except Exception as e:
    results["apis_testadas"]["Veo 2"] = {
        "status": "❌ ERRO",
        "erro": str(e)
    }
    print(f"   ❌ Erro: {e}")

# 4. GROQ LLAMA 4
print("\n4️⃣ Testando Groq Llama 4...")
try:
    from groq import Groq
    
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY não encontrada")
    
    client = Groq(api_key=api_key)
    
    # Testa Llama 4 Scout
    response = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[{"role": "user", "content": "Diga apenas: OK"}],
        max_tokens=10
    )
    
    results["apis_testadas"]["Llama 4 Scout"] = {
        "status": "✅ ATIVO",
        "modelo": "llama-4-scout-17b-16e-instruct",
        "resposta_teste": response.choices[0].message.content
    }
    print(f"   ✅ Llama 4 Scout: FUNCIONANDO")
    
except Exception as e:
    results["apis_testadas"]["Llama 4 Scout"] = {
        "status": "❌ ERRO",
        "erro": str(e)
    }
    print(f"   ❌ Erro: {e}")

# 5. CLAUDE SONNET 4
print("\n5️⃣ Testando Claude Sonnet 4...")
try:
    import anthropic
    
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY não encontrada")
    
    client = anthropic.Anthropic(api_key=api_key)
    
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=10,
        messages=[{"role": "user", "content": "Diga apenas: OK"}]
    )
    
    results["apis_testadas"]["Claude Sonnet 4"] = {
        "status": "✅ ATIVO",
        "modelo": "claude-sonnet-4-20250514",
        "resposta_teste": message.content[0].text
    }
    print(f"   ✅ Claude Sonnet 4: FUNCIONANDO")
    
except Exception as e:
    results["apis_testadas"]["Claude Sonnet 4"] = {
        "status": "❌ ERRO",
        "erro": str(e)
    }
    print(f"   ❌ Erro: {e}")

# 6. WHISPER TURBO (Groq)
print("\n6️⃣ Testando Whisper Large V3 Turbo...")
try:
    # Whisper precisa de arquivo de áudio para testar
    results["apis_testadas"]["Whisper V3 Turbo"] = {
        "status": "⏳ REQUER ARQUIVO DE ÁUDIO",
        "nota": "Disponível via Groq, precisa de MP3/WAV para testar"
    }
    print(f"   ⏳ Whisper: Requer áudio para teste")
    
except Exception as e:
    results["apis_testadas"]["Whisper V3 Turbo"] = {
        "status": "❌ ERRO",
        "erro": str(e)
    }
    print(f"   ❌ Erro: {e}")

# ESTIMATIVA DE CUSTOS
print("\n\n💰 ESTIMATIVA DE CUSTOS (por vídeo de 1min)")
print("=" * 60)

costs = {
    "Gemini 2.0 Flash": {
        "input": "$0.00 (grátis até 1M tokens/dia)",
        "output": "$0.00 (grátis até 1M tokens/dia)",
        "total_por_video": "$0.00"
    },
    "Gemini 2.5 Pro": {
        "input": "$1.25 / 1M tokens",
        "output": "$5.00 / 1M tokens",
        "total_por_video": "~$0.01 (roteiro típico)"
    },
    "Imagen 4 Ultra (Nano Banana)": {
        "por_imagem": "$0.06",
        "total_por_video": "$0.36 (6 imagens)"
    },
    "Veo 2 (Vídeo Direto)": {
        "por_segundo": "$0.75",
        "total_por_video": "$45.00 (60s) 🔴 CARO!"
    },
    "Claude Sonnet 4": {
        "input": "$3.00 / 1M tokens",
        "output": "$15.00 / 1M tokens",
        "total_por_video": "~$0.02"
    },
    "Llama 4 (Groq)": {
        "input": "$0.00 (grátis)",
        "output": "$0.00 (grátis)",
        "total_por_video": "$0.00"
    },
    "Cloud TTS": {
        "por_caractere": "$0.000016",
        "total_por_video": "$0.02 (1200 caracteres)"
    }
}

results["custos_estimados"] = costs

for api, cost in costs.items():
    print(f"\n{api}:")
    for k, v in cost.items():
        print(f"   {k}: {v}")

# CUSTO TOTAL POR VÍDEO (pipeline otimizado)
print("\n\n📊 CUSTO TOTAL POR VÍDEO (Pipeline Otimizado)")
print("=" * 60)

pipeline_otimizado = {
    "Roteiro": "Gemini 2.0 Flash (grátis)",
    "Imagens": "Imagen 4 Ultra ($0.36)",
    "Áudio": "Cloud TTS ($0.02)",
    "TOTAL": "$0.38/vídeo"
}

print("\nPipeline Recomendado:")
for step, cost in pipeline_otimizado.items():
    print(f"   {step}: {cost}")

print(f"\n💡 Com $300 GCP: ~789 vídeos possíveis!")

# RECOMENDAÇÕES
print("\n\n🎯 RECOMENDAÇÕES")
print("=" * 60)

recomendacoes = [
    "✅ Migrar para Gemini 2.0 Flash (grátis + 2x mais rápido)",
    "✅ Usar Imagen 4 Ultra com Character Reference",
    "❌ EVITAR Veo 2 (muito caro: $45/vídeo)",
    "✅ Claude Sonnet 4 apenas para validação de roteiro",
    "✅ Llama 4 (Groq) para ideias rápidas (grátis)",
    "⚠️ Chirp TTS: verificar se disponível (melhor qualidade)"
]

results["recomendacoes"] = recomendacoes

for rec in recomendacoes:
    print(f"   {rec}")

# Salvar resultados
output_file = "outputs/teste_apis_completo.json"
os.makedirs("outputs", exist_ok=True)
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print(f"\n\n✅ Resultados salvos em: {output_file}")
print("=" * 60)
