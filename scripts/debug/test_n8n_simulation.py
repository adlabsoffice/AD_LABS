import os
import json
import subprocess
from rich.console import Console

console = Console()

def setup_test_channel():
    """
    Cria um canal de teste para simular o n8n.
    """
    base_path = "incubadora/canais"
    canal_nome = "canal_teste_n8n"
    canal_path = os.path.join(base_path, canal_nome)
    
    console.print(f"[bold cyan]SETUP: Criando canal de teste '{canal_nome}'...[/bold cyan]")
    
    os.makedirs(canal_path, exist_ok=True)
    
    # Configuração de Teste (ComfyUI CPU)
    config = {
        "nome_canal": "Canal Teste n8n",
        "nicho": "Curiosidades Tecnológicas",
        "estilo_visual": "Cyberpunk 2D",
        "descricao": "Canal de teste para validação de pipeline.",
        "voz": "pt-BR-Neural-Male",
        "provider_imagens": "ComfyUI (CPU Fallback)",
        "duracao_ideal": "1 minuto",
        "formato_video": "SHORT (9:16)",
        "pauta_inicial": ["O futuro da IA em 2025"]
    }
    
    with open(os.path.join(canal_path, "config.json"), "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4, ensure_ascii=False)
        
    # Credentials Template
    with open(os.path.join(canal_path, "credentials.template.json"), "w", encoding="utf-8") as f:
        f.write("{}")
        
    console.print("[green]Canal de teste configurado.[/green]")
    return canal_nome

def simulate_n8n_trigger(canal_nome):
    """
    Simula o disparo do n8n chamando o run_agents.py
    """
    console.print(f"[bold cyan]TRIGGER: Simulando execucao do n8n para '{canal_nome}'...[/bold cyan]")
    
    cmd = ["python", "run_agents.py", "--canal", canal_nome]
    
    try:
        result = subprocess.run(cmd, cwd="incubadora", capture_output=True, text=True)
        
        print(result.stdout)
        
        if result.returncode == 0:
            console.print("[bold green]SUCESSO: Pipeline executado sem erros![/bold green]")
            return True
        else:
            console.print("[bold red]FALHA: Erro na execucao do pipeline.[/bold red]")
            print(result.stderr)
            return False
            
    except Exception as e:
        console.print(f"[red]Erro ao executar subprocesso: {e}[/red]")
        return False

if __name__ == "__main__":
    canal = setup_test_channel()
    simulate_n8n_trigger(canal)
