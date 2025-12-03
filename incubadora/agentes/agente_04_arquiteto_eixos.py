"""
AGENTE 04: ARQUITETO DE EIXOS
Timestamp: T=3
Responsabilidade: Transformar clusters em 5 "eixos emocionais" estruturados
"""

import os
import json
import sys
from typing import Dict, List
from rich.console import Console
from rich.panel import Panel
from rich.progress import track

# Adiciona diretório pai (incubadora) ao path para importar utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Integração com APIManager
from utils.api_manager import APIManager

console = Console()


class ErroClusterInvalido(Exception):
    """Exceção para cluster inválido."""
    pass


class Agente04ArquitetoEixos:
    """
    Agente 04: Arquiteto de Eixos
    Transforma cada cluster em "eixo emocional" (formato de conteúdo estruturado)
    Usa LLM para criar estruturas narrativas complexas.
    """
    
    def __init__(self):
        self.input_path = "outputs"
        self.output_path = "outputs/T03_eixos"
        self.clusters_file = "T02_clusters.json"
        self.num_eixos = 5
        self.api_manager = APIManager()
    
    def _call_llm(self, api_key, modelo, prompt, system_prompt="Você é um arquiteto de narrativas."):
        """Função auxiliar para chamar LLM via APIManager."""
        import requests
        
        if "gemini" in modelo or "google" in modelo:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{modelo}:generateContent?key={api_key}"
            payload = {"contents": [{"parts": [{"text": f"{system_prompt}\n\n{prompt}"}]}]}
            response = requests.post(url, json=payload, timeout=30)
            response.raise_for_status()
            return response.json()["candidates"][0]["content"]["parts"][0]["text"]
            
        elif "llama" in modelo or "groq" in modelo:
            from groq import Groq
            client = Groq(api_key=api_key)
            completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                model=modelo,
            )
            return completion.choices[0].message.content
            
        elif "claude" in modelo:
            import anthropic
            client = anthropic.Anthropic(api_key=api_key)
            message = client.messages.create(
                model=modelo,
                max_tokens=2000,
                system=system_prompt,
                messages=[{"role": "user", "content": prompt}]
            )
            return message.content[0].text
        else:
            raise ValueError(f"Modelo desconhecido: {modelo}")

    def criar_estrutura_outputs(self):
        """Cria pasta de output para eixos."""
        os.makedirs(self.output_path, exist_ok=True)
        console.print(f"[dim]Pasta {self.output_path}/ verificada[/dim]")
    
    def carregar_clusters(self) -> Dict:
        """Carrega arquivo de clusters gerado pelo Agente 03."""
        filepath = os.path.join(self.input_path, self.clusters_file)
        
        if not os.path.exists(filepath):
            raise FileNotFoundError(
                f"Arquivo {filepath} não encontrado. "
                "Execute Agente 03 (Analista) primeiro."
            )
        
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
            console.print(f"[green]✓ Clusters carregados: {filepath}[/green]")
            return data
        except json.JSONDecodeError as e:
            raise ErroClusterInvalido(f"JSON inválido em {filepath}: {e}")
    
    def validar_clusters(self, clusters_data: Dict) -> bool:
        """Valida se dados de clusters estão no formato esperado."""
        if "clusters" not in clusters_data:
            raise ErroClusterInvalido("Campo 'clusters' não encontrado no JSON")
        
        clusters = clusters_data["clusters"]
        if not isinstance(clusters, list):
            raise ErroClusterInvalido("'clusters' deve ser uma lista")
        
        if len(clusters) < 1:
            raise ErroClusterInvalido("Pelo menos 1 cluster deve existir")
        
        return True
    
    def criar_eixo_de_cluster(self, cluster: Dict, eixo_numero: int) -> Dict:
        """
        Cria um eixo emocional estruturado a partir de um cluster usando LLM.
        """
        
        prompt = f"""
        Transforme este Cluster de Vídeos em um "Eixo Narrativo" estruturado para um canal Dark/Viral.
        
        CLUSTER: {cluster.get('nome')}
        EMOÇÃO CENTRAL: {cluster.get('emocao_central')}
        DESCRIÇÃO: {cluster.get('descricao')}
        EXEMPLOS: {json.dumps(cluster.get('exemplos_titulos', []), ensure_ascii=False)}
        
        Defina:
        1. Padrão Dramático (A jornada emocional do espectador)
        2. Personagem Tipo (Quem vive essa história?)
        3. Ângulo de Abordagem (Como contar isso de forma única?)
        
        Retorne JSON:
        {{
            "nome": "Nome criativo do Eixo",
            "emocao_central": "Emoção principal",
            "personagem_tipo": "Arquétipo do personagem",
            "padrao_dramatico": "Ex: Situação Inicial -> Conflito -> Resolução",
            "angulo_abordagem": "Ex: Investigativo / Denúncia / Inspiracional",
            "descricao": "Resumo do conceito do eixo",
            "saturacao": "baixa/média/alta",
            "forca": "baixa/média/alta",
            "risco": "baixo/médio/alto"
        }}
        """
        
        try:
            resposta_json_str = self.api_manager.chamar_com_fallback(
                "llm_roteiro",
                self._call_llm,
                prompt=prompt,
                system_prompt="Você é um showrunner de TV experiente. Retorne apenas JSON."
            )
            
            if "```json" in resposta_json_str:
                resposta_json_str = resposta_json_str.split("```json")[1].split("```")[0]
            elif "```" in resposta_json_str:
                resposta_json_str = resposta_json_str.split("```")[1].split("```")[0]
                
            eixo_ia = json.loads(resposta_json_str)
            
            # Mescla com dados estruturais
            eixo = {
                "id": f"eixo_{eixo_numero:02d}",
                "cluster_origem": cluster.get("id"),
                "timestamp": "T=3",
                "status": "validado",
                **eixo_ia # Usa dados da IA
            }
            
            return eixo
            
        except Exception as e:
            console.print(f"[yellow]Erro na criação do Eixo IA: {e}. Usando fallback.[/yellow]")
            # Fallback para lógica determinística antiga
            return {
                "id": f"eixo_{eixo_numero:02d}",
                "nome": f"Eixo {cluster.get('nome')}",
                "cluster_origem": cluster.get("id"),
                "emocao_central": cluster.get("emocao_central", "Geral"),
                "padrao_dramatico": "setup -> conflito -> resolução",
                "descricao": "Eixo gerado via fallback.",
                "timestamp": "T=3",
                "status": "fallback"
            }
    
    def validar_eixo(self, eixo: Dict) -> bool:
        """Valida se eixo tem todos campos obrigatórios."""
        campos_obrigatorios = ["id", "nome", "emocao_central", "padrao_dramatico"]
        
        for campo in campos_obrigatorios:
            if campo not in eixo:
                console.print(f"[yellow]⚠ Campo obrigatório ausente: {campo}[/yellow]")
                return False
        
        return True
    
    def salvar_eixo(self, eixo: Dict, eixo_numero: int):
        """Salva eixo em arquivo JSON individual."""
        filename = f"eixo_{eixo_numero:02d}.json"
        filepath = os.path.join(self.output_path, filename)
        
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(eixo, f, indent=2, ensure_ascii=False)
            console.print(f"[green]✓ Eixo salvo: {filename}[/green]")
        except Exception as e:
            console.print(f"[red]Erro ao salvar {filename}: {e}[/red]")
            raise
    
    def salvar_todos_eixos(self, eixos: List[Dict]):
        """Salva todos os eixos em um único arquivo para o Agente 05 ler fácil."""
        filepath = os.path.join(self.input_path, "T03_eixos_narrativos.json")
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump({"eixos_narrativos": eixos}, f, indent=2, ensure_ascii=False)
            console.print(f"[green]✅ Arquivo consolidado salvo: {filepath}[/green]")
        except Exception as e:
            console.print(f"[red]Erro ao salvar consolidado: {e}[/red]")

    def atualizar_progress(self):
        """Atualiza arquivo progress.json."""
        progress_file = os.path.join(self.input_path, "progress.json")
        try:
            if os.path.exists(progress_file):
                with open(progress_file, "r", encoding="utf-8") as f:
                    progress = json.load(f)
            else:
                progress = {}
            
            progress.update({
                "timestamp_atual": "T=3",
                "ultimo_agente": "arquiteto_eixos",
                "status": "eixos_criados",
                "proxima_acao": "Executar Agente 05: Gerador de Ideias",
                "checkpoint": {
                    "eixos_criados": self.num_eixos,
                    "ideias_geradas": 0,
                    "videos_produzidos": 0
                }
            })
            
            with open(progress_file, "w", encoding="utf-8") as f:
                json.dump(progress, f, indent=2, ensure_ascii=False)
        except Exception:
            pass
    
    def executar(self) -> List[Dict]:
        console.print(Panel.fit(
            "[bold cyan]📐 AGENTE 04: ARQUITETO DE EIXOS[/bold cyan]\n"
            "[dim]Transformando clusters em eixos emocionais (T=3)[/dim]",
            title="Criação de Eixos"
        ))
        
        try:
            # 1. Criar estrutura
            self.criar_estrutura_outputs()
            
            # 2. Carregar clusters
            console.print("\n[bold]Passo 1: Carregando Clusters[/bold]")
            clusters_data = self.carregar_clusters()
            self.validar_clusters(clusters_data)
            
            clusters = clusters_data["clusters"]
            console.print(f"[green]✓ {len(clusters)} cluster(s) encontrado(s)[/green]")
            
            # 3. Criar eixos (sempre 5, mesmo se houver menos clusters)
            console.print(f"\n[bold]Passo 2: Criando {self.num_eixos} Eixos[/bold]")
            eixos_criados = []
            
            for i in track(range(self.num_eixos), description="Gerando eixos..."):
                eixo_numero = i + 1
                
                # Se temos cluster correspondente, usa ele
                # Se não, reutiliza clusters (round-robin)
                cluster_idx = i % len(clusters)
                cluster = clusters[cluster_idx]
                
                # Cria eixo
                eixo = self.criar_eixo_de_cluster(cluster, eixo_numero)
                
                # Valida
                if not self.validar_eixo(eixo):
                    console.print(f"[red]⚠ Eixo {eixo_numero} inválido, pulando...[/red]")
                    continue
                
                # Salva
                self.salvar_eixo(eixo, eixo_numero)
                eixos_criados.append(eixo)
            
            # Salva consolidado para Agente 05
            self.salvar_todos_eixos(eixos_criados)
            
            # 4. Atualizar progress
            self.atualizar_progress()
            
            # 5. Resumo
            console.print("\n" + "="*60)
            console.print(f"[bold green]✅ {len(eixos_criados)} EIXOS CRIADOS COM SUCESSO![/bold green]")
            console.print(f"[dim]Arquivos salvos em: {self.output_path}/[/dim]")
            console.print(f"[dim]Próxima etapa: T=4 (Agente 05: Gerador de Ideias)[/dim]")
            console.print("="*60 + "\n")
            
            # Mostrar resumo dos eixos
            console.print("[bold cyan]Resumo dos Eixos:[/bold cyan]")
            for eixo in eixos_criados:
                console.print(f"  • {eixo['nome']} - {eixo['emocao_central']}")
            
            return eixos_criados
            
        except Exception as e:
            console.print(f"[bold red]❌ Erro: {e}[/bold red]")
        console.print(f"\n[bold]Eixo {i}:[/bold]")
        console.print(json.dumps(eixo, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
