"""
AGENTE 01: INICIALIZADOR
Timestamp: T=0
Responsabilidade: Capturar informações iniciais e criar configuração base do projeto
"""

import os
import json
import uuid
from datetime import datetime
from typing import Dict, Optional
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm

console = Console()


class ErroNichoInvalido(Exception):
    """Exceção para nicho inválido."""
    pass


class ErroAPIInvalida(Exception):
    """Exceção para APIs inválidas."""
    pass


class Agente01Inicializador:
    """
    Agente 01: Inicializador
    Transforma input do usuário em configuração estruturada (T00_config.json)
    """
    
    def __init__(self):
        self.output_path = "outputs"
        self.config_file = "T00_config.json"
        self.progress_file = "progress.json"
    
    def gerar_id_unico(self) -> str:
        """Gera ID único para o projeto."""
        return f"canal_{uuid.uuid4().hex[:8]}"
    
    def validar_nicho(self, nicho: str) -> bool:
        """
        Valida se o nicho é aceitável.
        Regras:
        - Não pode ser vazio
        - Deve ter entre 3-50 caracteres
        """
        if not nicho or len(nicho.strip()) < 3:
            raise ErroNichoInvalido("Nicho deve ter pelo menos 3 caracteres")
        
        if len(nicho) > 50:
            raise ErroNichoInvalido("Nicho deve ter no máximo 50 caracteres")
        
        return True
    
    def coletar_apis_disponiveis(self) -> Dict[str, bool]:
        """
        Coleta quais APIs o usuário tem disponível via checklist interativo.
        """
        console.print("\n[bold yellow]Quais APIs você tem disponível?[/bold yellow]")
        
        apis = {
            "gemini": Confirm.ask("Gemini (gratuita)?", default=True),
            "claude": Confirm.ask("Claude?", default=False),
            "openai": Confirm.ask("OpenAI?", default=False),
            "youtube_data": Confirm.ask("YouTube Data API?", default=True),
            "elevenlabs": Confirm.ask("Elevenlabs (TTS)?", default=False)
        }
        
        # Pergunta se tem outras
        outras = Prompt.ask("Outras APIs (separadas por vírgula, ou Enter para pular)", default="")
        apis["outras"] = [x.strip() for x in outras.split(",") if x.strip()]
        
        # Validação: pelo menos 1 API deve estar disponível
        if not any([v for k, v in apis.items() if k != "outras"]):
            raise ErroAPIInvalida("Pelo menos uma API deve estar disponível")
        
        return apis
    
    def coletar_restricoes(self) -> Dict:
        """Coleta orçamento e prazo do usuário."""
        orcamento = Prompt.ask(
            "Orçamento máximo mensal por canal (R$)", 
            default="0"
        )
        
        prazo = Prompt.ask(
            "Prazo desejado em dias", 
            default="3"
        )
        
        try:
            orcamento_int = int(orcamento)
            prazo_int = int(prazo)
        except ValueError:
            console.print("[red]Valores devem ser numéricos. Usando defaults.[/red]")
            orcamento_int = 0
            prazo_int = 3
        
        # Validações
        if orcamento_int < 0:
            console.print("[yellow]Orçamento negativo ajustado para R$ 0[/yellow]")
            orcamento_int = 0
        
        if prazo_int < 1:
            console.print("[yellow]Prazo mínimo é 1 dia[/yellow]")
            prazo_int = 1
        
        # Define modo baseado no prazo
        modo = "mvp" if prazo_int <= 3 else "completo"
        
        return {
            "orcamento_maximo_mensal": orcamento_int,
            "prazo_dias": prazo_int,
            "modo": modo
        }
    
    def criar_estrutura_outputs(self):
        """Cria pasta outputs/ se não existir."""
        os.makedirs(self.output_path, exist_ok=True)
        console.print(f"[dim]Pasta {self.output_path}/ verificada[/dim]")
    
    def salvar_json(self, dados: Dict, filename: str):
        """Salva dados em arquivo JSON."""
        filepath = os.path.join(self.output_path, filename)
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(dados, f, indent=2, ensure_ascii=False)
            console.print(f"[green]✅ Arquivo salvo: {filepath}[/green]")
        except Exception as e:
            console.print(f"[red]Erro ao salvar {filename}: {e}[/red]")
            raise
    
    def atualizar_progress(self, timestamp: str, ultimo_agente: str, status: str = "completo"):
        """Atualiza arquivo de progresso global."""
        progress = {
            "timestamp_atual": timestamp,
            "ultimo_agente": ultimo_agente,
            "status": status,
            "proxima_acao": "Executar Agente 02: Pesquisador",
            "ultimo_update": datetime.now().isoformat(),
            "checkpoint": {
                "eixos_criados": 0,
                "ideias_geradas": 0,
                "videos_produzidos": 0,
                "mare_identificada": False
            }
        }
        self.salvar_json(progress, self.progress_file)
    
    def executar(self, nicho: Optional[str] = None) -> Dict:
        """
        Método principal - executa o agente inicializador.
        
        Args:
            nicho: Nicho desejado (opcional, se None pergunta ao usuário)
        
        Returns:
            Dict com configuração gerada
        """
        console.print(Panel.fit(
            "[bold cyan]🚀 INCUBADORA AD_LABS v2.0[/bold cyan]\n"
            "[dim]Agente 01: Inicializador (T=0)[/dim]",
            title="Inicialização"
        ))
        
        try:
            # 1. Coletar Nicho
            if nicho is None:
                console.print("\n[bold]Passo 1: Definir Nicho[/bold]")
                nicho = Prompt.ask(
                    "Qual nicho/tema você quer testar?",
                    default="Histórias Dramáticas"
                )
            
            # 2. Validar Nicho
            self.validar_nicho(nicho)
            console.print(f"[green]✓ Nicho válido: {nicho}[/green]")
            
            # 3. Coletar APIs
            console.print("\n[bold]Passo 2: APIs Disponíveis[/bold]")
            apis = self.coletar_apis_disponiveis()
            
            # 4. Coletar Restrições
            console.print("\n[bold]Passo 3: Restrições[/bold]")
            restricoes = self.coletar_restricoes()
            
            # 5. Criar Config
            config = {
                "timestamp": "T=0",
                "data_criacao": datetime.now().isoformat(),
                "projeto": {
                    "id": self.gerar_id_unico(),
                    "nicho": nicho,
                    "status": "inicializado"
                },
                "apis_disponiveis": apis,
                "restricoes": restricoes,
                "proxima_etapa": "T=1"
            }
            
            # 6. Criar estrutura e salvar
            self.criar_estrutura_outputs()
            self.salvar_json(config, self.config_file)
            self.atualizar_progress("T=0", "inicializador", "aguardando_pesquisa")
            
            # 7. Confirmação
            console.print("\n" + "="*60)
            console.print("[bold green]✅ INICIALIZAÇÃO CONCLUÍDA COM SUCESSO![/bold green]")
            console.print(f"[dim]Projeto ID: {config['projeto']['id']}[/dim]")
            console.print(f"[dim]Modo: {restricoes['modo'].upper()}[/dim]")
            console.print(f"[dim]Próxima etapa: T=1 (Agente 02: Pesquisador)[/dim]")
            console.print("="*60 + "\n")
            
            return config
            
        except ErroNichoInvalido as e:
            console.print(f"[bold red]❌ Erro de Nicho: {e}[/bold red]")
            raise
        except ErroAPIInvalida as e:
            console.print(f"[bold red]❌ Erro de API: {e}[/bold red]")
            raise
        except Exception as e:
            console.print(f"[bold red]❌ Erro inesperado: {e}[/bold red]")
            raise


def main():
    """Função para teste standalone do agente."""
    agente = Agente01Inicializador()
    config = agente.executar()
    
    console.print("\n[bold cyan]Configuração Gerada:[/bold cyan]")
    console.print(json.dumps(config, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
