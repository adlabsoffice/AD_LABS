import os
import sys
# Adiciona o diretório atual ao path para importar os agentes
sys.path.append(os.getcwd())

from incubadora.agentes.agente_01_inicializador import Agente01Inicializador

config = {
    "nome_canal": "O Livro Caixa Divino",
    "nicho": "Prosperidade Bíblica / Finanças",
    "estilo_visual": "Pixar 3D (Jesus Moderno)",
    "descricao": "Segredos milenares da prosperidade bíblica aplicados ao mundo moderno. Estratégia de vida baseada na sabedoria do maior CEO que já existiu.",
    "voz": "pt-BR-Neural-Male (Tom Sábio e Jovem)",
    "provider_imagens": "AWS EC2 Spot (Flux.1 - LoRA Pixar)",
    "duracao_ideal": "4-6 minutos (React)",
    "formato_video": "LONGO (16:9)",
    "transicoes_ritmo": "Dinâmica (React)",
    "efeitos_visuais": "Pop-ups de Notícias/Gráficos + Reações 3D",
    "audio_musica": "AUTOMÁTICO (Trilha Suave -> Tensão -> Resolução)",
    "frequencia_upload": "2x Semana",
    "thumb_estrategia": "Jesus (Pixar) com expressão de dúvida/choque + Print do Primo Rico + Seta Vermelha",
    "pauta_inicial": [
        "Jesus Reage: O Primo Rico ensinou errado?",
        "Salomão vs Warren Buffett: Quem investe melhor?",
        "O dízimo é imposto ou investimento?"
    ]
}

agente = Agente01Inicializador()
agente.criar_estrutura_canal(config)
