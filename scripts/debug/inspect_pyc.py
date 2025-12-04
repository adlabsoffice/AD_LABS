import marshal
import os
import sys

def extract_strings_from_code(code_obj):
    strings = []
    for const in code_obj.co_consts:
        if isinstance(const, str):
            strings.append(const)
        elif hasattr(const, 'co_consts'):
            strings.extend(extract_strings_from_code(const))
    
    for name in code_obj.co_names:
        strings.append(f"NAME: {name}")
        
    return strings

def inspect_file(path):
    print(f"\n{'='*20}\nINSPECIONANDO: {os.path.basename(path)}\n{'='*20}")
    try:
        with open(path, 'rb') as f:
            f.seek(16) # Skip header
            code_obj = marshal.load(f)
            strings = extract_strings_from_code(code_obj)
            for s in strings:
                print(s)
    except Exception as e:
        print(f"Erro ao ler {path}: {e}")

if __name__ == "__main__":
    # Lista de arquivos que o usuário pediu
    targets = [
        r"d:\AD_LABS\incubadora\tests\__pycache__\test_agente_04.cpython-314.pyc",
        r"d:\AD_LABS\incubadora\tests\__pycache__\test_manual_canal_piloto.cpython-314.pyc",
        r"d:\AD_LABS\incubadora\tests\__pycache__\test_pipeline_t00_t03.cpython-314.pyc"
    ]
    
    for target in targets:
        if os.path.exists(target):
            inspect_file(target)
        else:
            # Tenta achar se o find_by_name retornou caminho diferente
            print(f"Arquivo não encontrado no caminho padrão: {target}")
