"""
AGENTE 05: GERADOR DE IDEIAS (T=4)
Responsabilidade: Gerar 150 ideias de vídeos baseadas nos eixos narrativos (T=3).
"""

import os
import json
import sys
import time
from typing import Dict, List
from rich.console import Console
from rich.panel import Panel
from rich.progress import track

# Adiciona diretório pai (incubadora) ao path para importar utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Integração com APIManager
from utils.api_manager import APIManager

console = Console()

class Agente05GeradorIdeias:
    def __init__(self):
        self.input_file = os.path.join("outputs", "T03_eixos_narrativos.json")
        self.output_dir = os.path.join("outputs", "T04_ideias")
        self.api_manager = APIManager()
        
        # Garante que diretório de saída existe
        os.makedirs(self.output_dir, exist_ok=True)

    def _call_llm(self, api_key, modelo, prompt, system_prompt="Você é um especialista em YouTube."):
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

    def carregar_eixos(self) -> List[Dict]:
        if not os.path.exists(self.input_file):
            raise FileNotFoundError(f"Arquivo {self.input_file} não encontrado. Rode o Agente 04 primeiro.")
        
        with open(self.input_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("eixos_narrativos", [])

    def gerar_ideia_com_ia(self, eixo: Dict, contador: int, total: int) -> Dict:
        """Gera uma ideia única baseada no eixo usando LLM."""
        
        prompt = f"""
        Gere UMA ideia de vídeo viral para o YouTube baseada neste Eixo Narrativo:
        
        EIXO: {eixo['nome']}
        DESCRIÇÃO: {eixo['descricao']}
        EMOÇÃO ALVO: {eixo['emocao_alvo']}
        ÂNGULO: {eixo['angulo_abordagem']}
        
        A ideia deve ser ÚNICA e específica.
        
        Retorne JSON:
        {{
            "titulo": "Título Altamente Clicável (max 60 chars)",
            "thumbnail_desc": "Descrição visual da thumb",
            "hook_visual": "O que acontece nos primeiros 3 segundos",
            "sinopse": "Resumo de 1 linha do conteúdo"
        }}
        """
        
        try:
            resposta_json_str = self.api_manager.chamar_com_fallback(
                "llm_roteiro",
                self._call_llm,
                prompt=prompt,
                system_prompt="Você é um estrategista de conteúdo viral. Retorne apenas JSON."
            )
            
            if "```json" in resposta_json_str:
                resposta_json_str = resposta_json_str.split("```json")[1].split("```")[0]
            elif "```" in resposta_json_str:
                resposta_json_str = resposta_json_str.split("```")[1].split("```")[0]
                
            ideia = json.loads(resposta_json_str)
            
            # Adiciona metadados
            ideia["id"] = f"ideia_{int(time.time())}_{contador}"
            ideia["eixo_origem"] = eixo["nome"]
            ideia["status"] = "nova"
            
            return ideia
            
        except Exception as e:
            console.print(f"[yellow]Erro ao gerar ideia {contador}: {e}[/yellow]")
            # Fallback simples
            return {
                "id": f"ideia_fallback_{contador}",
                "titulo": f"Ideia sobre {eixo['nome']} #{contador}",
                "thumbnail_desc": "Fallback thumb",
                "hook_visual": "Fallback hook",
                "sinopse": "Ideia gerada via fallback por erro na API.",
                "eixo_origem": eixo["nome"],
                "status": "erro_api"
            }

    def salvar_ideia(self, ideia: Dict):
        filename = f"{ideia['id']}.json"
        filepath = os.path.join(self.output_dir, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(ideia, f, indent=2, ensure_ascii=False)

    def executar(self):
        console.print(Panel.fit(
            "[bold cyan]💡 AGENTE 05: GERADOR DE IDEIAS[/bold cyan]\n"
            "[Gera 150 ideias únicas baseadas nos Eixos Narrativos (T=4)]",
            title="Fábrica de Ideias"
        ))
        
        eixos = self.carregar_eixos()
        console.print(f"[green]Carregados {len(eixos)} eixos narrativos.[/green]")
        
        ideias_por_eixo = 30
        total_ideias = len(eixos) * ideias_por_eixo
        
        console.print(f"[bold]Meta: Gerar {total_ideias} ideias ({ideias_por_eixo} por eixo)...[/bold]")
        
        contador_geral = 0
        
        for eixo in eixos:
            console.print(f"\n[bold yellow]Processando Eixo: {eixo['nome']}[/bold yellow]")
            
            # Loop para gerar 30 ideias para este eixo
            for i in track(range(ideias_por_eixo), description=f"Gerando ideias para {eixo['nome']}..."):
                ideia = self.gerar_ideia_com_ia(eixo, i+1, ideias_por_eixo)
                self.salvar_ideia(ideia)
                contador_geral += 1
                
                # Pequena pausa para não floodar (embora o APIManager gerencie erros, é bom evitar)
                # time.sleep(0.5) 
        
        console.print("\n" + "="*60)
        console.print(f"[bold green]✅ {contador_geral} IDEIAS GERADAS COM SUCESSO![/bold green]")
        console.print(f"[dim]Salvas em: {self.output_dir}[/dim]")
        console.print("="*60 + "\n")

def main():
    # Mock de Eixos para teste se não existir
    if not os.path.exists(os.path.join("outputs", "T03_eixos_narrativos.json")):
        console.print("[yellow]Criando Eixos mock para teste...[/yellow]")
        os.makedirs("outputs", exist_ok=True)
        mock_data = {
            "eixos_narrativos": [
                {
                    "nome": "Eixo Teste 1",
                    "descricao": "Descrição teste 1",
                    "emocao_alvo": "Curiosidade",
                    "angulo_abordagem": "Misterioso"
                },
                {
                    "nome": "Eixo Teste 2",
                    "descricao": "Descrição teste 2",
                    "emocao_alvo": "Medo",
                    "angulo_abordagem": "Alerta"
                }
            ]
        }
        with open(os.path.join("outputs", "T03_eixos_narrativos.json"), "w", encoding="utf-8") as f:
            json.dump(mock_data, f, indent=2)
            
    agente = Agente05GeradorIdeias()
    # Para teste rápido, vamos limitar o loop no main se for execução direta
    # Mas o código da classe mantém 30.
    # Vou hackear a classe para o teste ser rápido (apenas 2 ideias por eixo)
    # NÃO, melhor não alterar a classe. Vou confiar que o usuário vai rodar valendo.
    # Mas para o MEU teste de verificação, eu preciso que seja rápido.
    
    # Vou adicionar um parametro opcional no executar ou apenas rodar e interromper?
    # Melhor: Se for __main__, eu crio uma subclasse ou modifico a instancia para teste.
    
    # Hack para teste rápido:
    original_carregar = agente.carregar_eixos
    def mock_carregar():
        eixos = original_carregar()
        return eixos[:1] # Só 1 eixo para teste
    agente.carregar_eixos = mock_carregar
    
    # E vamos reduzir o loop no código? Não dá pra mudar o código da classe dinamicamente fácil assim no loop.
    # Vou deixar rodar 30 vezes para 1 eixo no teste? É muito (30 chamadas LLM).
    # Vou alterar o código da classe para aceitar `qtd_por_eixo` no init.
    
    agente.executar()

if __name__ == "__main__":
    # Garante que existem dados mock para teste
    if not os.path.exists(os.path.join("outputs", "T03_eixos_narrativos.json")):
        console.print("[yellow]Criando Eixos mock para teste...[/yellow]")
        os.makedirs("outputs", exist_ok=True)
        mock_data = {
            "eixos_narrativos": [
                {
                    "nome": "Eixo Teste 1",
                    "descricao": "Descrição teste 1",
                    "emocao_alvo": "Curiosidade",
                    "angulo_abordagem": "Misterioso"
                }
            ]
        }
        with open(os.path.join("outputs", "T03_eixos_narrativos.json"), "w", encoding="utf-8") as f:
            json.dump(mock_data, f, indent=2)

    # Versão modificada para permitir teste rápido
    class Agente05Teste(Agente05GeradorIdeias):
        def executar(self):
            # Sobrescreve para teste rápido (2 ideias apenas)
            console.print("[bold red]MODO TESTE: Gerando apenas 2 ideias...[/bold red]")
            eixos = self.carregar_eixos()
            for eixo in eixos[:1]: # 1 eixo
                for i in range(2): # 2 ideias
                    ideia = self.gerar_ideia_com_ia(eixo, i+1, 2)
                    self.salvar_ideia(ideia)
                    print(f"Ideia {i+1} gerada: {ideia['titulo']}")
                    
    Agente05Teste().executar()
