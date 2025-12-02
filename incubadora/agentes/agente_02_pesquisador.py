import os
import json
import time
from rich.console import Console
from groq import Groq

console = Console()

class Agente02Pesquisador:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        self.client = Groq(api_key=self.api_key) if self.api_key else None
        
        # Knowledge Base: Carrega estratégias dos arquivos locais (01-10)
        self.knowledge_base = self._carregar_knowledge_base()

    def _carregar_knowledge_base(self):
        """Lê os arquivos markdown da pasta youtube para extrair conceitos."""
        kb = {}
        base_dir = r"d:\AD_LABS\youtube"
        # Arquivos chave mencionados pelo usuário
        files = [
            "01_Como_Crescer_um_Canal_do_Zero_em_2025.md",
            "02_Iniciando_Canal_YouTube_2025_Faca_Isso.md",
            "08_Framework_1246_Videos_YouTube_Sucesso.md"
        ]
        
        for f in files:
            path = os.path.join(base_dir, f)
            if os.path.exists(path):
                try:
                    with open(path, "r", encoding="utf-8") as file:
                        # Lê os primeiros 2k caracteres para dar contexto ao LLM sem estourar tokens
                        kb[f] = file.read()[:2000] 
                except Exception as e:
                    console.print(f"[red]Erro ao ler {f}: {e}[/red]")
        return kb

    def pesquisar_conteudo_base(self, tema, alvo):
        """
        Pesquisa o conteúdo original para o React.
        Ex: Pesquisa vídeos do 'Primo Rico' sobre 'Dívidas' ou 'Investimentos'.
        """
        console.print(f"[bold yellow]AGENTE 02: Pesquisando '{alvo}' sobre '{tema}'...[/bold yellow]")
        
        # Simulação de busca no YouTube (API real viria aqui)
        resultado_simulado = {
            "titulo_original": "3 ERROS QUE TE DEIXAM POBRE (Primo Rico)",
            "pontos_chave": [
                "Erro 1: Gastar mais do que ganha.",
                "Erro 2: Não investir o dinheiro.",
                "Erro 3: Comprar passivos achando que são ativos."
            ],
            "tom_original": "Educativo, Pragmático, Focado em Matemática Financeira.",
            "oportunidade_react": "Jesus concorda com a prudência (Provérbios), mas adiciona a dimensão espiritual (Generosidade/Propósito) que o Primo Rico não aborda."
        }
        
        time.sleep(2) # Simula tempo de pesquisa
        console.print(f"[green]Video Encontrado:[/green] {resultado_simulado['titulo_original']}")
        
        return resultado_simulado

    def analisar_viabilidade_viral(self, ideia):
        """
        Analisa se a ideia segue os principios dos arquivos 01-10 (Green Dot, Packaging).
        """
        console.print(f"[bold yellow]AGENTE 02: Validando 'Green Dot' para '{ideia}'...[/bold yellow]")
        
        # 1. Teste das 3 Perguntas (Simulado)
        perguntas = {
            "perpetual": True, # Dá para fazer 100 videos?
            "searchable": True, # Tem demanda?
            "sustainable": True # Dá dinheiro?
        }
        
        if not all(perguntas.values()):
            console.print("[red]Ideia rejeitada pelo Green Dot Test.[/red]")
            return {"score": 0, "analise": "Falha no Green Dot."}

        # 2. Packaging First (Titulo + Thumb)
        # O Agente 02 agora define isso ANTES do roteiro
        packaging = {
            "titulo_hook": "JESUS vs PRIMO RICO: Quem está certo?",
            "thumbnail_concept": "Jesus (lado esquerdo, humilde) vs Primo Rico (lado direito, terno). Texto: 'DINHEIRO OU ALMA?'"
        }
        
        # APLICAR REGRAS TOP 100 (Arquivo 11)
        packaging = self._aplicar_regras_top100(packaging)
        
        console.print(f"[green]Green Dot Validado![/green]")
        console.print(f"   [cyan]Titulo:[/cyan] {packaging['titulo_hook']}")
        console.print(f"   [cyan]Thumb:[/cyan] {packaging['thumbnail_concept']}")

        return {
            "score": 95,
            "analise": "Alta demanda. Packaging forte definido.",
            "packaging": packaging
        }

    def _aplicar_regras_top100(self, packaging):
        """
        Refina o packaging para seguir estritamente o Blueprint do Top 100.
        """
        titulo = packaging['titulo_hook']
        thumb_desc = packaging['thumbnail_concept']
        
        # REGRA 1: Título (6-8 palavras, Title Case, Sem Emojis)
        # Mock de refinamento (em produção seria via LLM)
        palavras = titulo.split()
        if len(palavras) < 6 or len(palavras) > 8:
            # Força ajuste para exemplo (simulado)
            titulo = "Jesus Contra Primo Rico: A Verdade Financeira" # 7 palavras
        
        # Title Case
        titulo = titulo.title()
        
        # REGRA 2: Thumbnail (Max 3 palavras, Cores)
        # Adiciona instrução de cores se não tiver
        if "Cores:" not in thumb_desc:
            thumb_desc += " Cores: Fundo Preto/Cinza Escuro, Contraste Vermelho/Branco."
            
        return {
            "titulo_hook": titulo,
            "thumbnail_concept": thumb_desc
        }
