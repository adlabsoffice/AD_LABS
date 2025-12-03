import os
import sys

# Adiciona o diretório incubadora ao path para importar o core
sys.path.append(os.path.join(os.getcwd(), "incubadora"))

from core.orchestrator import Orchestrator

# Configuração Hardcoded (Batch Mode)
config_livro_caixa = {
    "id": "proj_livro_caixa_001",
    "nome_canal": "O Livro Caixa Divino",
    "nicho": "Prosperidade Bíblica / Finanças",
    "estilo_visual": "Pixar 3D (Jesus Moderno)",
    "descricao": "Segredos milenares da prosperidade bíblica aplicados ao mundo moderno.",
    "voz": "pt-BR-Neural-Male (Tom Sábio e Jovem)",
    "provider_imagens": "imagen-4.0-fast", # Atualizado para padrão moderno
    "duracao_ideal": "4-6 minutos",
    "formato_video": "16:9",
    "pauta_inicial": [
        "Jesus Reage: O Primo Rico ensinou errado?",
        "Salomão vs Warren Buffett: Quem investe melhor?",
        "O dízimo é imposto ou investimento?"
    ]
}

def main():
    print("🚀 Iniciando Setup Batch: O Livro Caixa Divino...")
    
    orch = Orchestrator()
    
    # Inicia o projeto usando o Core Unificado
    # Isso vai criar pastas, salvar config.json e preparar para execução
    config_gerada = orch.iniciar_projeto(config_livro_caixa, modo="batch")
    
    print(f"✅ Setup concluído em: {config_gerada['paths']['root']}")
    print("Agora você pode rodar: python incubadora/run_agents.py --canal 'o_livro_caixa_divino'")

if __name__ == "__main__":
    main()
