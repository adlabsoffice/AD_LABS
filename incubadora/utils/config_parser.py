"""
Config Parser - Lê e parseia arquivos MD de configuração detalhada
Permite que cada agente extraia apenas as seções relevantes para sua função.
"""

import re
import os
from typing import Dict, Any, List, Optional

def ler_config_md(caminho_md: str) -> Dict[str, Any]:
    """
    Lê o arquivo MD de configuração e retorna um dicionário estruturado.
    
    Args:
        caminho_md: Caminho absoluto para o arquivo CONFIGURACAO_DETALHADA_*.md
        
    Returns:
        Dict com todas as configurações parseadas por seção
    """
    if not os.path.exists(caminho_md):
        raise FileNotFoundError(f"Arquivo de configuração não encontrado: {caminho_md}")
    
    with open(caminho_md, 'r', encoding='utf-8') as f:
        conteudo = f.read()
    
    config = {
        "canal": {},
        "nicho": {},
        "visual": {},
        "audio": {},
        "video": {},
        "estrategia": {},
        "regras_producao": {}
    }
    
    # Parsear Informações Básicas
    config["canal"]["nome"] = _extrair_valor(conteudo, r'### \*\*1\.1 Nome do Canal\*\*.*?Valor: "([^"]+)"')
    config["canal"]["descricao"] = _extrair_valor(conteudo, r'### \*\*1\.2 Descrição do Canal\*\*.*?Valor: "([^"]+)"')
    config["canal"]["idioma"] = _extrair_valor(conteudo, r'### \*\*1\.3 Idioma Principal\*\*.*?Valor: ([^\r\n]+)')
    
    # Parsear Nicho
    config["nicho"]["principal"] = _extrair_valor(conteudo, r'### \*\*2\.1 Nicho Principal\*\*.*?Valor: "([^"]+)"')
    
    # Parsear Visual
    config["visual"]["preset"] = _extrair_valor(conteudo, r'### \*\*3\.1 Preset de Estilo\*\*.*?Valor: ([^\r\n]+)')
    config["visual"]["provider"] = _extrair_valor(conteudo, r'### \*\*3\.2 Provider de Imagens\*\*.*?Valor: ([^\r\n]+)')
    
    # Parsear Ritmo Visual (CRÍTICO)
    ritmo_match = re.search(r'Ritmo Visual:\s*Troca de cena a cada\s*(\d+)\s*segundos', conteudo, re.IGNORECASE)
    if ritmo_match:
        config["regras_producao"]["ritmo_visual_max_seg"] = int(ritmo_match.group(1))
    
    # Parsear Áudio
    config["audio"]["provider"] = _extrair_valor(conteudo, r'### \*\*4\.1 Voz Narrativa\*\*.*?Provider: ([^\r\n]+)')
    config["audio"]["voz"] = _extrair_valor(conteudo, r'Voz: ([^\r\n]+)')
    
    # Parsear Velocidade (CRÍTICO)
    velocidade_match = re.search(r'Velocidade:\s*([\d.]+)x', conteudo)
    if velocidade_match:
        config["regras_producao"]["velocidade_fala"] = float(velocidade_match.group(1))
    
    # Parsear Duração (CRÍTICO)
    duracao_match = re.search(r'### \*\*5\.1 Duração\*\*.*?Alvo:\s*(\d+)-(\d+)\s*minutos', conteudo, re.DOTALL)
    if duracao_match:
        config["regras_producao"]["min_minutos"] = int(duracao_match.group(1))
        config["regras_producao"]["max_minutos"] = int(duracao_match.group(2))
    
    # Parsear Resolução
    config["video"]["resolucao"] = _extrair_valor(conteudo, r'### \*\*5\.2 Resolução\*\*.*?Valor: ([^\r\n]+)')
    
    # Parsear Regras de Produção (Top 100)
    regras_section = re.search(r'### \*\*6\.2 Regras de Produção.*?\*   \*\*Roteiro\*\*: (.+?)(?=###|\Z)', conteudo, re.DOTALL)
    if regras_section:
        # Extrair densidade de palavras (WPM)
        wpm_match = re.search(r'Ritmo\s+([\d-]+)\s*wpm', regras_section.group(1), re.IGNORECASE)
        if wpm_match:
            wpm_range = wpm_match.group(1).split('-')
            config["regras_producao"]["wpm_min"] = int(wpm_range[0])
            config["regras_producao"]["wpm_max"] = int(wpm_range[1]) if len(wpm_range) > 1 else int(wpm_range[0])
    
    # Estimar densidade de palavras baseada em duração e WPM (DEFAULT)
    if "min_minutos" in config["regras_producao"] and "wpm_min" in config["regras_producao"]:
        min_palavras = config["regras_producao"]["min_minutos"] * config["regras_producao"]["wpm_min"]
        config["regras_producao"]["densidade_palavras_min"] = min_palavras

    # --- SOBRESCREVER COM VALORES EXPLÍCITOS DA SEÇÃO 7 (HARD VETO) ---
    secao_veto = re.search(r'## 7\. REGRAS DE PRODUÇÃO \(HARD VETO\)(.+?)(?=##|\Z)', conteudo, re.DOTALL)
    if secao_veto:
        texto_veto = secao_veto.group(1)
        
        # Extrair pares chave: valor
        for linha in texto_veto.split('\n'):
            match = re.search(r'\*\s*\*\*(\w+)\*\*:\s*([\d.]+)', linha)
            if match:
                chave = match.group(1)
                valor = match.group(2)
                
                # Converter para int ou float
                if '.' in valor:
                    config["regras_producao"][chave] = float(valor)
                else:
                    config["regras_producao"][chave] = int(valor)

    
    return config


def _extrair_valor(texto: str, pattern: str) -> Optional[str]:
    """Helper: Extrai valor via regex e retorna limpo."""
    match = re.search(pattern, texto, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip().strip('"')
    return None


def get_config_secao(config: Dict[str, Any], secao: str) -> Dict[str, Any]:
    """
    Retorna apenas uma seção específica da config.
    
    Args:
        config: Dict completo parseado
        secao: Nome da seção (ex: 'audio', 'visual', 'regras_producao')
        
    Returns:
        Dict com apenas a seção solicitada
    """
    return config.get(secao, {})


if __name__ == "__main__":
    # Teste rápido
    caminho_teste = r"d:\AD_LABS\incubadora\canais\o_livro_caixa_divino\CONFIGURACAO_DETALHADA_LIVRO_CAIXA.md"
    
    if os.path.exists(caminho_teste):
        config = ler_config_md(caminho_teste)
        print("[OK] Config parseado com sucesso!")
        print(f"\n[REGRAS DE PRODUCAO]:")
        for k, v in config["regras_producao"].items():
            print(f"   {k}: {v}")
    else:
        print(f"[ERRO] Arquivo nao encontrado: {caminho_teste}")
