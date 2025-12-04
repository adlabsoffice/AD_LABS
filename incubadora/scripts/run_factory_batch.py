import sys
import os
import time
from typing import List

# Adiciona diretório raiz
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agentes.agente_factory_process import FactoryProcessAgent
from rich.console import Console
from rich.progress import track

console = Console()

from concurrent.futures import ThreadPoolExecutor, as_completed

def process_product(agent, product):
    try:
        output_file = agent.run(product)
        if output_file:
            return (product, "Sucesso", output_file)
        else:
            return (product, "Falha", "Sem output")
    except Exception as e:
        return (product, "Erro", str(e))

def run_batch(products: List[str], max_workers: int = 5):
    agent = FactoryProcessAgent()
    
    console.print(f"[bold green]🚀 Iniciando Lote de Fábrica: {len(products)} produtos[/bold green]")
    console.print(f"[dim]Processamento Paralelo: {max_workers} threads[/dim]")
    
    results = []
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_product = {executor.submit(process_product, agent, p): p for p in products}
        
        for future in track(as_completed(future_to_product), total=len(products), description="Processando em paralelo..."):
            product = future_to_product[future]
            try:
                result = future.result()
                results.append(result)
                # Log imediato para feedback visual
                status_color = "green" if result[1] == "Sucesso" else "red"
                console.print(f"   ↳ {product}: [{status_color}]{result[1]}[/{status_color}]")
            except Exception as e:
                results.append((product, "Erro Fatal", str(e)))
                
    console.print("\n[bold]📊 Relatório Final:[/bold]")
    for prod, status, detail in results:
        color = "green" if status == "Sucesso" else "red"
        console.print(f"[{color}]{prod}: {status} - {detail}[/{color}]")

if __name__ == "__main__":
    # Se passar argumentos, usa eles
    if len(sys.argv) > 1:
        lista_produtos = sys.argv[1:]
    else:
        # Lista padrão de exemplo (Tendências "How It's Made")
        lista_produtos = [
            "Glass Bottles",
            "Pencils",
            "Toilet Paper",
            "Aluminum Cans"
        ]
        
    run_batch(lista_produtos)
