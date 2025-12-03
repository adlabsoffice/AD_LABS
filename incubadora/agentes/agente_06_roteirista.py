import os
import json
import sys
from typing import Dict, Optional
from rich.console import Console
from rich.panel import Panel

# Adiciona diretório pai (incubadora) ao path para importar utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Integração com APIManager
try:
    from utils.api_manager import APIManager
except ImportError:
    # Fallback se rodar direto da pasta agentes
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from utils.api_manager import APIManager

console = Console()

class Agente05Roteirista:
    def __init__(self):
        self.api_manager = APIManager()
        self.templates_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "specs", "templates")
        self.output_dir = os.path.join("outputs", "T05_roteiros")
        os.makedirs(self.output_dir, exist_ok=True)

    def _carregar_template(self, nome_template: str) -> str:
        """Carrega o conteúdo de um template markdown."""
        filepath = os.path.join(self.templates_dir, f"{nome_template}.md")
        if not os.path.exists(filepath):
            # Tenta achar sem extensão ou com caminho completo se falhar
            filepath = nome_template if os.path.exists(nome_template) else filepath
            
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Template não encontrado: {filepath}")
            
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()

    def _call_llm(self, api_key, modelo, prompt, system_prompt="Você é um roteirista profissional."):
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
                max_tokens=4000,
                system=system_prompt,
                messages=[{"role": "user", "content": prompt}]
            )
            return message.content[0].text
        else:
            raise ValueError(f"Modelo desconhecido: {modelo}")

    def gerar_roteiro(self, ideia: Dict, template_name: str = "react") -> Dict:
        """
        Gera um roteiro completo baseado em uma Ideia e um Template.
        """
        console.print(Panel.fit(f"[bold cyan]AGENTE 05: Roteirista Universal[/bold cyan]\nTemplate: {template_name}"))
        
        # 1. Carregar Template
        try:
            template_content = self._carregar_template(template_name)
            console.print(f"[green]✓ Template '{template_name}' carregado.[/green]")
        except FileNotFoundError:
            console.print(f"[red]Erro: Template '{template_name}' não existe. Usando fallback genérico.[/red]")
            template_content = "Crie um roteiro de vídeo curto com Hook, Corpo e CTA."

        # 2. Preparar Prompt
        prompt = f"""
        ATUE COMO UM ROTEIRISTA DE ELITE PARA YOUTUBE.
        
        SUA MISSÃO: Transformar a IDEIA abaixo em um ROTEIRO TÉCNICO seguindo rigorosamente o TEMPLATE fornecido.
        
        ---
        INPUT: A IDEIA
        Título: {ideia.get('titulo')}
        Hook Visual: {ideia.get('hook_visual')}
        Sinopse: {ideia.get('sinopse')}
        Estilo Visual: {ideia.get('visual_style_ref', 'Padrão do Canal')}
        
        REGRAS DE OURO (BLUEPRINT TOP 100):
        1. LINGUAGEM: Nível 5ª série (FKGL < 5.0). Palavras simples.
        2. RITMO: 168-187 palavras por minuto. Sem enrolação.
        3. TOM: Positivo ou Neutro. Evitar negatividade pura.
        4. FOCO: Histórias pessoais ("Eu") > Fatos genéricos.
        ---
        
        INPUT: O TEMPLATE (Siga a estrutura de tempo e blocos)
        {template_content}
        
        ---
        
        SAÍDA ESPERADA (JSON PURO):
        Retorne um JSON com a seguinte estrutura exata:
        {{
            "titulo_final": "Título Otimizado",
            "estimativa_duracao": "XX minutos",
            "blocos": [
                {{
                    "id": 1,
                    "tipo": "HOOK",
                    "tempo_estimado": "00:00-00:05",
                    "visual": "Descrição DETALHADA para o gerador de imagem (inclua estilo, iluminação, ação). NÃO use nomes de pessoas reais, descreva a aparência.",
                    "fala": "Texto exato que o narrador vai ler. Use pontuação para ritmo.",
                    "audio_fx": "Efeitos sonoros sugeridos (ex: Boom, Whoosh)"
                }},
                ...
            ]
        }}
        """

        # 3. Chamar LLM
        try:
            console.print(f"[yellow]Gerando roteiro com IA...[/yellow]")
            resposta_json_str = self.api_manager.chamar_com_fallback(
                "llm_roteiro",
                self._call_llm,
                prompt=prompt,
                system_prompt="Você é um roteirista JSON. Retorne apenas JSON válido sem markdown."
            )
            
            # Limpeza de Markdown
            if "```json" in resposta_json_str:
                resposta_json_str = resposta_json_str.split("```json")[1].split("```")[0]
            elif "```" in resposta_json_str:
                resposta_json_str = resposta_json_str.split("```")[1].split("```")[0]
                
            roteiro = json.loads(resposta_json_str)
            
            # Adiciona metadados
            roteiro["id"] = f"rot_{ideia.get('id', 'manual')}"
            roteiro["ideia_origem"] = ideia.get("id")
            roteiro["template_usado"] = template_name
            roteiro["status"] = "gerado"
            
            # Salvar
            self.salvar_roteiro(roteiro)
            
            console.print(f"[green]✅ Roteiro gerado com {len(roteiro.get('blocos', []))} blocos![/green]")
            return roteiro

        except Exception as e:
            console.print(f"[bold red]❌ Erro na geração do roteiro: {e}[/bold red]")
            raise

    def salvar_roteiro(self, roteiro: Dict):
        filename = f"{roteiro['id']}.json"
        filepath = os.path.join(self.output_dir, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(roteiro, f, indent=2, ensure_ascii=False)
        console.print(f"[dim]Salvo em: {filepath}[/dim]")

if __name__ == "__main__":
    # Teste Manual
    agente = Agente05Roteirista()
    ideia_teste = {
        "id": "teste_01",
        "titulo": "Jesus Reage: Primo Rico",
        "hook_visual": "Jesus com cara de choque olhando um gráfico de juros compostos",
        "sinopse": "Jesus analisa os conselhos financeiros modernos à luz da Bíblia.",
        "visual_style_ref": "Pixar 3D"
    }
    agente.gerar_roteiro(ideia_teste, template_name="react")
