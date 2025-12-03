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
        EMOÇÃO ALVO: {eixo['emocao_central']}
        ÂNGULO: {eixo['angulo_abordagem']}
        
        REGRAS DE OURO (BLUEPRINT TOP 100):
        1. TÍTULO: Entre 6 e 8 palavras. Title Case. Sem Emojis. (Ex: "I Survived 50 Hours In Antarctica")
        2. FOCO: Creator-Centric ("Eu fiz", "Eu vi") ou Curiosidade Extrema.
        3. THUMBNAIL: Deve ter rosto expressivo e fundo de alto contraste.
        
        Retorne JSON:
        {{
            "titulo": "Título Otimizado (6-8 palavras, Title Case)",
            "thumbnail_desc": "Descrição visual da thumb (Rosto + Fundo Escuro)",
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
        
        console.print("\n" + "="*60)
        console.print(f"[bold green]✅ {contador_geral} IDEIAS GERADAS COM SUCESSO![/bold green]")
        console.print(f"[dim]Salvas em: {self.output_dir}[/dim]")
        console.print("="*60 + "\n")

if __name__ == "__main__":
    agente = Agente05GeradorIdeias()
    agente.executar()
