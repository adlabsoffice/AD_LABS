"""
AGENTE 05: GERADOR DE IDEIAS
Timestamp: T=4
Responsabilidade: Gerar 30 ideias de vídeo por eixo (150 total) - 1 POR VEZ!
"""

import os
import json
import random
import time
from typing import Dict, List
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress

console = Console()


class ErroEixoInvalido(Exception):
    """Exceção para eixo inválido."""
    pass


class Agente05GeradorIdeias:
    """
    Agente 05: Gerador de Ideias
    
    O QUE FAZ (em linguagem simples):
    1. Pega os 5 eixos emocionais do Agente 04
    2. Para cada eixo, cria 30 ideias diferentes de vídeo
    3. IMPORTANTE: Gera 1 ideia por vez (não 30 de uma vez!)
    4. Salva cada ideia como arquivo JSON separado
    5. Total: 150 ideias (5 eixos × 30 ideias)
    
    POR QUE 1 POR VEZ?
    Porque gerar 30 de uma vez trava o sistema (contexto explode).
    É como pedir 1 café por vez ao invés de 30 juntos!
    """
    
    def __init__(self):
        self.input_path = "outputs/T03_eixos"
        self.output_path = "outputs/T04_ideias"
        self.ideias_por_eixo = 30
        self.contador_global = 1
        
        # Categorias possíveis para variar os vídeos
        self.categorias = [
            "escola", "trabalho", "família", "relacionamentos",
            "amizade", "vizinhança", "internet", "faculdade"
        ]
    
    def criar_estrutura_outputs(self):
        """Cria pasta de output para ideias."""
        os.makedirs(self.output_path, exist_ok=True)
        console.print(f"[dim]Pasta {self.output_path}/ verificada[/dim]")
    
    def carregar_eixos(self) -> List[Dict]:
        """
        Carrega todos os eixos criados pelo Agente 04.
        
        SIMPLES: Abre os 5 arquivos de eixos (eixo_01.json até eixo_05.json)
        """
        if not os.path.exists(self.input_path):
            raise FileNotFoundError(
                f"Pasta {self.input_path} não encontrada. "
                "Execute Agente 04 (Arquiteto de Eixos) primeiro."
            )
        
        eixos = []
        arquivos_eixo = sorted([f for f in os.listdir(self.input_path) if f.endswith('.json')])
        
        if len(arquivos_eixo) == 0:
            raise ErroEixoInvalido("Nenhum arquivo de eixo encontrado")
        
        for arquivo in arquivos_eixo:
            filepath = os.path.join(self.input_path, arquivo)
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    eixo = json.load(f)
                    eixos.append(eixo)
            except Exception as e:
                console.print(f"[yellow]⚠ Erro ao ler {arquivo}: {e}[/yellow]")
                continue
        
        console.print(f"[green]✓ {len(eixos)} eixos carregados[/green]")
        return eixos
    
    def gerar_1_ideia(self, eixo: Dict, numero: int) -> Dict:
        """
        Gera UMA ÚNICA ideia de vídeo baseada no eixo.
        
        SIMPLES:
        - Pega a emoção do eixo (ex: "humilhação → revanche")
        - Escolhe uma categoria aleatória (escola, trabalho, etc.)
        - Cria título viral + conflito + virada emocional
        
        IMPORTANTE: Esta função gera APENAS 1 ideia, não 30!
        """
        # Pega informações do eixo
        emocao = eixo.get('emocao_central', 'emoção genérica')
        padrao = eixo.get('padrao_dramatico', 'conflito → resolução')
        categorias_eixo = eixo.get('categorias_possiveis', self.categorias)
        
        # Escolhe categoria aleatória
        categoria = random.choice(categorias_eixo if categorias_eixo else self.categorias)
        
        # Gera componentes da ideia baseado na emoção
        titulo, conflito, virada = self._criar_historia_por_emocao(emocao, categoria, numero)
        
        # Monta ideia estruturada
        ideia = {
            "id": f"ideia_{self.contador_global:03d}",
            "eixo_id": eixo.get('id', 'eixo_desconhecido'),
            "numero": numero,
            "titulo": titulo,
            "conflito": conflito,
            "virada": virada,
            "emocao": emocao,
            "categoria": categoria,
            "padrao_dramatico": padrao,
            "timestamp": "T=4",
            "status": "gerada"
        }
        
        return ideia
    
    def _criar_historia_por_emocao(self, emocao: str, categoria: str, numero: int) -> tuple:
        """
        Cria título, conflito e virada baseados na emoção e categoria.
        
        SIMPLES: Tem templates para cada tipo de emoção
        """
        emocao_lower = emocao.lower()
        
        # Templates por tipo de emoção (simplificado - versão real usaria LLM)
        if "humilh" in emocao_lower or "revanc" in emocao_lower:
            titulos = [
                f"Eles zombaram de mim na {categoria}... mas se arrependeram #{numero}",
                f"Me chamaram de fracassado na {categoria}. Hoje sou CEO #{numero}",
                f"Fui humilhado na {categoria}. A vingança veio #{numero}",
                f"Riram da minha cara na {categoria}. Olha quem ri agora #{numero}"
            ]
            conflitos = [
                f"Pessoa humilhada publicamente na {categoria}",
                f"Sofrendo bullying constante na {categoria}",
                f"Sendo menosprezado por todos na {categoria}"
            ]
            viradas = [
                f"Alcança grande sucesso e todos pedem desculpas",
                f"Vence competição importante e ganha reconhecimento",
                f"Torna-se referência mundial na área"
            ]
        
        elif "segredo" in emocao_lower or "revela" in emocao_lower:
            titulos = [
                f"Descobri um segredo na {categoria} que mudou tudo #{numero}",
                f"O que escondem na {categoria}... você não vai acreditar #{numero}",
                f"Revelação chocante na {categoria} #{numero}",
                f"Ninguém sabia a verdade sobre a {categoria} #{numero}"
            ]
            conflitos = [
                f"Segredo guardado há anos sendo descoberto",
                f"Verdade oculta vindo à tona",
                f"Mistério finalmente sendo revelado"
            ]
            viradas = [
                f"Revelação muda completamente a situação",
                f"Verdade liberta todos os envolvidos",
                f"Segredo era mais chocante que imaginavam"
            ]
        
        elif "medo" in emocao_lower or "terror" in emocao_lower:
            titulos = [
                f"O dia mais assustador na {categoria} #{numero}",
                f"Nunca mais volto naquela {categoria} #{numero}",
                f"Experiência aterrorizante na {categoria} #{numero}",
                f"Sobrevivi ao pior da {categoria} #{numero}"
            ]
            conflitos = [
                f"Situação perigosa/assustadora na {categoria}",
                f"Ameaça real enfrentada",
                f"Momento de pânico absoluto"
            ]
            viradas = [
                f"Consegue escapar por pouco",
                f"Descobre que não era tão perigoso quanto parecia",
                f"Supera o medo e sai mais forte"
            ]
        
        elif "injust" in emocao_lower or "repara" in emocao_lower:
            titulos = [
                f"Fui injustiçado na {categoria}, mas a justiça chegou #{numero}",
                f"O dia que consertaram o erro na {categoria} #{numero}",
                f"Finalmente fizeram justiça na {categoria} #{numero}",
                f"Acusado injustamente na {categoria}. Final feliz #{numero}"
            ]
            conflitos = [
                f"Acusação injusta na {categoria}",
                f"Sofrendo consequências por algo que não fez",
                f"Sistema falhou com a pessoa"
            ]
            viradas = [
                f"Verdade finalmente provada",
                f"Justiça é feita após longa luta",
                f"Inocência comprovada publicamente"
            ]
        
        else:  # Emoção genérica ou curiosidade
            titulos = [
                f"História incrível que aconteceu na {categoria} #{numero}",
                f"Descoberta surpreendente na {categoria} #{numero}",
                f"Você não vai acreditar no que rolou na {categoria} #{numero}",
                f"O mistério da {categoria} finalmente resolvido #{numero}"
            ]
            conflitos = [
                f"Situação misteriosa na {categoria}",
                f"Algo inexplicável acontecendo",
                f"Descoberta intrigante"
            ]
            viradas = [
                f"Explicação surpreendente encontrada",
                f"Mistério resolvido de forma inesperada",
                f"Descoberta muda tudo"
            ]
        
        # Escolhe aleatoriamente dos templates
        titulo = random.choice(titulos)
        conflito = random.choice(conflitos)
        virada = random.choice(viradas)
        
        return titulo, conflito, virada
    
    def salvar_ideia(self, ideia: Dict):
        """Salva ideia em arquivo JSON individual."""
        filename = f"{ideia['id']}.json"
        filepath = os.path.join(self.output_path, filename)
        
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(ideia, f, indent=2, ensure_ascii=False)
        except Exception as e:
            console.print(f"[red]Erro ao salvar {filename}: {e}[/red]")
            raise
    
    def atualizar_progress(self, total_ideias: int):
        """Atualiza arquivo progress.json."""
        progress_file = "outputs/progress.json"
        
        try:
            if os.path.exists(progress_file):
                with open(progress_file, "r", encoding="utf-8") as f:
                    progress = json.load(f)
            else:
                progress = {}
            
            progress.update({
                "timestamp_atual": "T=4",
                "ultimo_agente": "gerador_ideias",
                "status": "ideias_geradas",
                "proxima_acao": "Selecionar melhores ideias e produzir vídeos (T=5-9)",
                "checkpoint": {
                    "clusters_identificados": progress.get("checkpoint", {}).get("clusters_identificados", 0),
                    "eixos_criados": progress.get("checkpoint", {}).get("eixos_criados", 5),
                    "ideias_geradas": total_ideias,
                    "videos_produzidos": 0
                }
            })
            
            with open(progress_file, "w", encoding="utf-8") as f:
                json.dump(progress, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            console.print(f"[yellow]Aviso: Não foi possível atualizar progress.json: {e}[/yellow]")
    
    def executar(self) -> Dict:
        """
        Método principal - gera todas as ideias.
        
        SIMPLES:
        1. Carrega 5 eixos
        2. Para cada eixo, gera 30 ideias (1 por vez!)
        3. Salva cada ideia imediatamente
        4. Total: 150 ideias
        
        IMPORTANTE: Loop de 1 item! Nunca gera 30 de uma vez!
        """
        console.print(Panel.fit(
            "[bold cyan]💡 AGENTE 05: GERADOR DE IDEIAS[/bold cyan]\n"
            "[dim]Gera 30 ideias por eixo - 1 POR VEZ! (T=4)[/dim]",
            title="Geração de Ideias"
        ))
        
        try:
            # 1. Criar estrutura
            self.criar_estrutura_outputs()
            
            # 2. Carregar eixos
            console.print("\n[bold]Passo 1: Carregando Eixos[/bold]")
            eixos = self.carregar_eixos()
            
            if len(eixos) == 0:
                raise ErroEixoInvalido("Nenhum eixo válido encontrado")
            
            # 3. Gerar ideias (LOOP DE 1 ITEM!)
            console.print(f"\n[bold]Passo 2: Gerando {len(eixos)} × {self.ideias_por_eixo} = {len(eixos) * self.ideias_por_eixo} ideias[/bold]")
            console.print("[yellow]⚠️ Gerando 1 por vez para evitar travamento[/yellow]\n")
            
            total_ideias = 0
            ideias_geradas = []
            
            with Progress() as progress:
                task = progress.add_task(
                    "[cyan]Gerando ideias...", 
                    total=len(eixos) * self.ideias_por_eixo
                )
                
                for eixo in eixos:
                    eixo_nome = eixo.get('nome', 'Eixo Desconhecido')
                    console.print(f"\n[bold cyan]Eixo: {eixo_nome}[/bold cyan]")
                    
                    for i in range(self.ideias_por_eixo):
                        # CRÍTICO: Gera APENAS 1 ideia por vez!
                        ideia = self.gerar_1_ideia(eixo, i + 1)
                        
                        # Salva imediatamente (não acumula em memória)
                        self.salvar_ideia(ideia)
                        
                        ideias_geradas.append(ideia)
                        total_ideias += 1
                        self.contador_global += 1
                        
                        # Atualiza progress bar
                        progress.update(task, advance=1)
                        
                        # Rate limit friendly (pequena pausa)
                        time.sleep(0.1)
            
            # 4. Atualizar progress
            self.atualizar_progress(total_ideias)
            
            # 5. Resumo
            console.print("\n" + "="*60)
            console.print(f"[bold green]✅ {total_ideias} IDEIAS GERADAS COM SUCESSO![/bold green]")
            console.print(f"[dim]Arquivos salvos em: {self.output_path}/[/dim]")
            console.print(f"[dim]Próxima etapa: T=5-9 (Produção de Vídeos)[/dim]")
            console.print("="*60 + "\n")
            
            # Mostrar exemplos
            console.print("[bold cyan]Exemplos de Ideias Geradas:[/bold cyan]")
            for i in range(min(5, len(ideias_geradas))):
                ideia = ideias_geradas[i]
                console.print(f"  • [{ideia['id']}] {ideia['titulo']}")
            
            if len(ideias_geradas) > 5:
                console.print(f"  ... e mais {len(ideias_geradas) - 5} ideias")
            
            return {
                "timestamp": "T=4",
                "total_ideias": total_ideias,
                "ideias_por_eixo": self.ideias_por_eixo,
                "eixos_processados": len(eixos),
                "output_path": self.output_path
            }
            
        except FileNotFoundError as e:
            console.print(f"[bold red]❌ Arquivo não encontrado: {e}[/bold red]")
            raise
        except ErroEixoInvalido as e:
            console.print(f"[bold red]❌ Erro nos eixos: {e}[/bold red]")
            raise
        except Exception as e:
            console.print(f"[bold red]❌ Erro inesperado: {e}[/bold red]")
            raise


def main():
    """Função para teste standalone do agente."""
    agente = Agente05GeradorIdeias()
    resultado = agente.executar()
    
    console.print("\n[bold cyan]Resumo Final:[/bold cyan]")
    console.print(json.dumps(resultado, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
