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
    print(f"\n{'='*40}\nARQUIVO: {os.path.basename(path)}\n{'='*40}")
    try:
        with open(path, 'rb') as f:
            f.seek(16)
            code_obj = marshal.load(f)
            strings = extract_strings_from_code(code_obj)
            for s in strings:
                print(s)
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    base = r"d:\AD_LABS\incubadora\tests\__pycache__"
    targets = [
        "test_agente_04.cpython-314.pyc",
        "test_manual_canal_piloto.cpython-314.pyc",
        "test_pipeline_t00_t03.cpython-314.pyc",
        "test_agente_01.cpython-314.pyc"
    ]
    
    for t in targets:
        full_path = os.path.join(base, t)
        if os.path.exists(full_path):
            inspect_file(full_path)
        else:
            print(f"ARQUIVO NÃO ENCONTRADO: {t}")
