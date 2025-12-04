import json
import os
import sys
import time
from pathlib import Path
from typing import List, Dict, Optional

# Adiciona diretório raiz ao path para imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.api_manager import APIManager
from rich.console import Console
from rich.panel import Panel

console = Console()

class FactoryProcessAgent:
    def __init__(self):
        self.api_manager = APIManager()
        self.output_dir = Path("d:/AD_LABS/incubadora/data/factory_processes")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def _call_llm(self, api_key, modelo, prompt, system_prompt="Você é um especialista industrial."):
        """Função auxiliar para chamar LLM via APIManager."""
        import requests
        
        if "gemini" in modelo or "google" in modelo:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{modelo}:generateContent?key={api_key}"
            payload = {"contents": [{"parts": [{"text": f"{system_prompt}\n\n{prompt}"}]}]}
            response = requests.post(url, json=payload, timeout=60)
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

    def enrich_knowledge(self, product_name: str) -> str:
        """
        Fase 1: Pesquisa Técnica (Simulada via LLM)
        Obtém detalhes técnicos reais do processo de fabricação para evitar alucinações genéricas.
        """
        console.print(f"[yellow]🔍 Pesquisando detalhes técnicos sobre a fabricação de: {product_name}...[/yellow]")
        
        prompt = f"""
        Atue como um Engenheiro Industrial Sênior especialista em {product_name}.
        
        Sua tarefa é listar o PROCESSO TÉCNICO COMPLETO de fabricação industrial de: {product_name}.
        
        Liste os passos cronológicos reais, focando em:
        1. Nomes específicos das máquinas (ex: não diga "máquina de esquentar", diga "túnel de pasteurização" ou "forno rotativo").
        2. Matérias-primas exatas e aditivos comuns.
        3. Temperaturas, tempos e processos químicos/físicos chave (ex: fermentação, decantação, extrusão).
        4. Etapas de controle de qualidade.
        
        Seja técnico e preciso. O objetivo é usar isso para criar um vídeo documental realista estilo "How It's Made".
        """
        
        try:
            response = self.api_manager.chamar_com_fallback(
                "llm_roteiro",
                self._call_llm,
                prompt=prompt,
                system_prompt="Você é um engenheiro industrial."
            )
            
            console.print(Panel(response[:500] + "...", title="Contexto Técnico Obtido", border_style="blue"))
            return response
        except Exception as e:
            console.print(f"[red]❌ Falha ao obter contexto técnico: {e}[/red]")
            return ""

    def generate_100_prompts(self, product_name: str, technical_context: str) -> str:
        """
        Fase 2: Geração dos 100 Prompts Visuais
        Usa o prompt "Expert Prompt Generator" injetando o contexto técnico.
        """
        console.print(f"[yellow]🎬 Gerando 100 prompts visuais para {product_name}...[/yellow]")
        
        base_prompt = f"""
        You are an expert prompt generator for factory-process videos.

        TASK:
        Generate EXACTLY 100 short video prompts, numbered 1 to 100, for a “Inside a Modern {product_name} Factory: From Raw Material to Final Product (Full Process)” style video.

        CONTEXT (TECHNICAL DETAILS TO USE):
        {technical_context}

        OUTPUT LANGUAGE:
        - Write ALL prompts in English.
        - Do NOT add explanations, titles or section names. Only the numbered list of prompts.

        STYLE:
        - Each prompt must describe ONE micro-scene of about 5–8 seconds.
        - Only visual actions: what the camera sees (machines, workers, raw materials, liquids, conveyor belts, close-ups, wide shots, movements, textures, lights).
        - No narration, no dialogue, no on-screen text, no subtitles.
        - Tone: industrial, satisfying, continuous factory process, similar to “How It’s Made” / “factory process” videos.

        PROCESS COVERAGE:
        Internally, cover the COMPLETE industrial process of {product_name}, in logical order, including:
        - Raw material sourcing or harvesting related to {product_name}
        - Transport to factory
        - Reception, weighing and initial quality control
        - Cleaning and preparation of the raw material(s)
        - Primary processing (crushing, grinding, mixing, cooking, pressing, molding, etc., as appropriate for {product_name})
        - Secondary processing (separation, refinement, filtration, drying, cooling, fermentation, etc., as appropriate)
        - Quality control and lab testing
        - Storage in tanks, silos or warehouses
        - Bottling or primary packaging of {product_name}
        - Sealing, labeling and coding
        - Boxing, palletizing and final warehouse ready for distribution

        FORMAT:
        - Return ONLY the prompts, exactly in this format:
        "1. [visual description of the first 5–8 second scene]"
        "2. [visual description of the second 5–8 second scene]"
        ...
        "100. [visual description of the hundredth 5–8 second scene]"

        RULES:
        - The 100 scenes must be chronological, showing the journey from raw material to finished {product_name} ready to ship.
        - Every line MUST be a shot description that could be used directly in a text-to-video AI.
        - Focus on clear, concrete visuals: camera angle, movement, what is visible, how materials look and move.
        - USE THE TECHNICAL TERMS from the provided context (machine names, specific processes).

        Now generate the 100 prompts for: {product_name}.
        """
        
        try:
            response = self.api_manager.chamar_com_fallback(
                "llm_roteiro",
                self._call_llm,
                prompt=base_prompt,
                system_prompt="You are an expert prompt generator."
            )
            return response
        except Exception as e:
            console.print(f"[red]❌ Falha ao gerar prompts: {e}[/red]")
            return ""

    def parse_prompts(self, raw_text: str) -> List[Dict]:
        """
        Limpa e estrutura a lista de prompts.
        """
        prompts = []
        lines = raw_text.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Tenta extrair número e texto (ex: "1. Visual description...")
            # Remove aspas se houver
            clean_line = line.replace('"', '').replace("'", "")
            
            parts = clean_line.split('.', 1)
            if len(parts) == 2 and parts[0].isdigit():
                seq_num = int(parts[0])
                prompt_text = parts[1].strip()
                
                prompts.append({
                    "id": seq_num,
                    "prompt": prompt_text,
                    "duration": "5s" # Padrão definido no plano
                })
        
        return prompts

    def run(self, product_name: str):
        console.print(Panel(f"🏭 Iniciando Agente de Processo Industrial: {product_name}", style="bold green"))
        
        # 1. Enriquecimento
        technical_context = self.enrich_knowledge(product_name)
        if not technical_context:
            console.print("[red]Abortando devido a falta de contexto técnico.[/red]")
            return
            
        # 2. Geração
        raw_prompts = self.generate_100_prompts(product_name, technical_context)
        if not raw_prompts:
            console.print("[red]Falha na geração dos prompts.[/red]")
            return
            
        # 3. Parsing e Salvamento
        structured_prompts = self.parse_prompts(raw_prompts)
        
        output_data = {
            "product": product_name,
            "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "total_scenes": len(structured_prompts),
            "technical_context_summary": technical_context[:200] + "...",
            "scenes": structured_prompts
        }
        
        # Sanitiza nome do arquivo
        safe_name = "".join([c for c in product_name if c.isalnum() or c in (' ', '-', '_')]).strip().replace(' ', '_').lower()
        file_path = self.output_dir / f"factory_process_{safe_name}.json"
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
            
        console.print(f"[green]✅ Processo concluído! {len(structured_prompts)} cenas geradas.[/green]")
        console.print(f"[blue]📁 Arquivo salvo em: {file_path}[/blue]")
        
        return file_path

if __name__ == "__main__":
    # Exemplo de uso via linha de comando
    if len(sys.argv) > 1:
        product = " ".join(sys.argv[1:])
    else:
        product = "Olive Oil" # Default do exemplo
        
    agent = FactoryProcessAgent()
    agent.run(product)
