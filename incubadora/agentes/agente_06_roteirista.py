"""
Agente 06 - Roteirista Universal

REFATORADO: 04/12/2024
- Validação com Pydantic schemas (ISP)
- Garantia de campo 'speaker' em todos os blocos
- Validação de duração automática
- Retry se roteiro exceder duração alvo

Integração com schemas: VideoScript, SceneBlock
"""

import os
import json
import sys
import logging
from typing import Dict, Optional
from rich.console import Console
from rich.panel import Panel

# Adiciona diretório pai ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Imports de serviços
try:
    from utils.api_manager import APIManager
    from specs.schemas.video_pipeline import VideoScript, SceneBlock, validate_roteiro_json
except ImportError:
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from utils.api_manager import APIManager
    from specs.schemas.video_pipeline import VideoScript, SceneBlock, validate_roteiro_json

console = Console()
logger = logging.getLogger(__name__)


class Agente06Roteirista:
    """
    Roteirista Universal - Gera roteiros validados a partir de ideias.
    
    Responsabilidades (SRP):
    - Carregar templates de roteiro
    - Gerar roteiro via LLM
    - Validar output com Pydantic
    - Retry se duração exceder alvo
    
    NÃO é responsável por:
    - Geração de imagens (Agente Visual)
    - Geração de áudio (Agente Narrador)
    """
    
    # Configurações de duração
    DURACAO_ALVO = 60  # segundos
    DURACAO_MAX = 70   # 120% do alvo
    MAX_RETRIES = 3    # Tentativas de ajuste
    
    def __init__(self):
        self.api_manager = APIManager()
        self.templates_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 
            "specs", 
            "templates"
        )
        self.output_dir = os.path.join("outputs", "T05_roteiros")
        os.makedirs(self.output_dir, exist_ok=True)
        
        logger.info("Agente06Roteirista inicializado")
    
    def _carregar_template(self, nome_template: str) -> str:
        """Carrega o conteúdo de um template markdown."""
        filepath = os.path.join(self.templates_dir, f"{nome_template}.md")
        
        if not os.path.exists(filepath):
            filepath = nome_template if os.path.exists(nome_template) else filepath
        
        if not os.path.exists(filepath):
            logger.error(f"Template não encontrado: {filepath}")
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
        Gera roteiro COM validação Pydantic.
        
        Args:
            ideia: Dicionário com dados da ideia
            template_name: Nome do template a usar
            
        Returns:
            Dict com roteiro validado
        """
        console.print(Panel.fit(
            f"[bold cyan]AGENTE 06: Roteirista Universal[/bold cyan]\n"
            f"Template: {template_name}"
        ))
        
        # 1. Carregar Template
        try:
            template_content = self._carregar_template(template_name)
            console.print(f"[green]✓ Template '{template_name}' carregado.[/green]")
        except FileNotFoundError:
            console.print(f"[red]Erro: Template '{template_name}' não existe. Usando fallback genérico.[/red]")
            template_content = "Crie um roteiro de vídeo curto com Hook, Corpo e CTA."
        
        # 2. Gerar com retry se exceder duração
        for tentativa in range(self.MAX_RETRIES):
            try:
                console.print(f"[yellow]Tentativa {tentativa + 1}/{self.MAX_RETRIES}: Gerando roteiro...[/yellow]")
                
                # Monta prompt com instruções de duração
                prompt = self._montar_prompt(ideia, template_content, tentativa)
                
                # Chama LLM
                resposta_json_str = self.api_manager.chamar_com_fallback(
                    "llm_roteiro",
                    self._call_llm,
                    prompt=prompt,
                    system_prompt="Você é um roteirista JSON. Retorne apenas JSON válido sem markdown."
                )
                
                # Limpa markdown
                roteiro_dict = self._limpar_e_parsear_json(resposta_json_str)
                
                # NOVO: Valida com Pydantic
                roteiro_validado = self._validar_e_ajustar(roteiro_dict, ideia, template_name)
                
                # Se passou validação, retorna
                console.print(f"[green]✅ Roteiro validado com {len(roteiro_validado['scenes'])} cenas![/green]")
                
                # Salva
                self.salvar_roteiro(roteiro_validado)
                
                return roteiro_validado
            
            except ValueError as e:
                # Erro de validação Pydantic
                console.print(f"[yellow]⚠️ Tentativa {tentativa + 1} falhou: {e}[/yellow]")
                
                if tentativa == self.MAX_RETRIES - 1:
                    console.print(f"[bold red]❌ Roteiro não validou após {self.MAX_RETRIES} tentativas![/bold red]")
                    raise
                
                # Continua para próxima tentativa
                continue
            
            except Exception as e:
                console.print(f"[bold red]❌ Erro na geração do roteiro: {e}[/bold red]")
                raise
    
    def _montar_prompt(self, ideia: Dict, template_content: str, tentativa: int) -> str:
        """
        Monta prompt com instruções de duração.
        
        Args:
            ideia: Dados da ideia
            template_content: Conteúdo do template
            tentativa: Número da tentativa atual (0-indexed)
            
        Returns:
            Prompt formatado
        """
        # Aviso se é retry
        aviso_retry = ""
        if tentativa > 0:
            aviso_retry = f"\n\n⚠️ ATENÇÃO: TENTATIVA {tentativa + 1}. O roteiro anterior estava MUITO LONGO. REDUZA o número de cenas ou a duração de cada uma para ficar ABAIXO de {self.DURACAO_MAX} segundos totais!"
        
        prompt = f"""
ATUE COMO UM ROTEIRISTA DE ELITE PARA YOUTUBE.

SUA MISSÃO: Transformar a IDEIA abaixo em um ROTEIRO TÉCNICO seguindo rigorosamente o TEMPLATE fornecido.

---
INPUT: A IDEIA
Título: {ideia.get('titulo')}
Hook Visual: {ideia.get('hook_visual')}
Sinopse: {ideia.get('sinopse')}
Estilo Visual: {ideia.get('visual_style_ref', 'Padrão do Canal')}
Emoção Central: {ideia.get('emocao_central', 'neutro')}

REGRAS DE OURO (BLUEPRINT TOP 100):
1. LINGUAGEM: Nível 5ª série (FKGL < 5.0). Palavras simples.
2. RITMO: 168-187 palavras por minuto. Sem enrolação.
3. TOM: Positivo ou Neutro. Evitar negatividade pura.
4. FOCO: Histórias pessoais ("Eu") > Fatos genéricos.
5. DURAÇÃO: Máximo {self.DURACAO_MAX} segundos TOTAL. Cada cena: 8-12 segundos.
---

INPUT: O TEMPLATE (Siga a estrutura de tempo e blocos)
{template_content}

---{aviso_retry}

SAÍDA ESPERADA (JSON PURO):
Retorne um JSON com a seguinte estrutura EXATA:
{{
    "title": "Título Otimizado",
    "target_duration": {self.DURACAO_ALVO},
    "dominant_emotion": "{ideia.get('emocao_central', 'neutro')}",
    "template_used": "react",
    "scenes": [
        {{
            "speaker": "Jesus",
            "dialogue": "Texto exato que o personagem vai falar. Use pontuação para ritmo.",
            "visual_prompt": "Descrição DETALHADA para gerador de imagens (estilo, iluminação, ação, cenário). NÃO use nomes de pessoas reais.",
            "duration_seconds": 8.5,
            "emotion": "alegria"
        }},
        ...
    ]
}}

ATENÇÃO CRÍTICA:
- Campo "speaker" é OBRIGATÓRIO em TODAS as cenas (ex: "Jesus", "Narrador")
- Campo "emotion" deve ser um de: alegria, tristeza, raiva, medo, surpresa, neutro
- Duração TOTAL de todas as cenas NÃO pode exceder {self.DURACAO_MAX} segundos
- Cada cena: mínimo 3s, máximo 15s
- Retorne APENAS o JSON, sem markdown, sem explicações
        """
        
        return prompt
    
    def _limpar_e_parsear_json(self, resposta_json_str: str) -> Dict:
        """
        Limpa markdown e parseia JSON.
        
        Args:
            resposta_json_str: String com JSON (possivelmente com markdown)
            
        Returns:
            Dicionário parseado
        """
        # Limpeza de Markdown
        if "```json" in resposta_json_str:
            resposta_json_str = resposta_json_str.split("```json")[1].split("```")[0]
        elif "```" in resposta_json_str:
            resposta_json_str = resposta_json_str.split("```")[1].split("```")[0]
        
        return json.loads(resposta_json_str.strip())
    
    def _validar_e_ajustar(self, roteiro_dict: Dict, ideia: Dict, template_name: str) -> Dict:
        """
        Valida roteiro com Pydantic e adiciona metadados.
        
        Args:
            roteiro_dict: Dicionário com roteiro gerado
            ideia: Dados da ideia original
            template_name: Nome do template usado
            
        Returns:
            Dict validado com metadados adicionais
            
        Raises:
            ValueError: Se validação falhar
        """
        try:
            # Valida com Pydantic (ISP - Interface Segregation)
            roteiro_validado = VideoScript.model_validate(roteiro_dict)
            
            # Converte de volta para dict
            roteiro_final = roteiro_validado.model_dump(mode='json')
            
            # Adiciona metadados
            roteiro_final["id"] = f"rot_{ideia.get('id', 'manual')}"
            roteiro_final["ideia_origem"] = ideia.get("id")
            roteiro_final["template_usado"] = template_name
            roteiro_final["status"] = "gerado"
            
            # Log de validação
            total_duration = sum(s["duration_seconds"] for s in roteiro_final["scenes"])
            console.print(f"   ✅ Validação Pydantic: PASSOU")
            console.print(f"   📊 Duração total: {total_duration:.1f}s (alvo: {self.DURACAO_ALVO}s, max: {self.DURACAO_MAX}s)")
            
            return roteiro_final
        
        except Exception as e:
            logger.error(f"Erro de validação Pydantic: {e}")
            raise ValueError(f"Roteiro inválido: {e}")
    
    def salvar_roteiro(self, roteiro: Dict):
        """Salva roteiro em arquivo JSON."""
        filename = f"{roteiro['id']}.json"
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(roteiro, f, indent=2, ensure_ascii=False)
        
        console.print(f"[dim]Salvo em: {filepath}[/dim]")


# Compatibilidade com código antigo
Agente05Roteirista = Agente06Roteirista


if __name__ == "__main__":
    # Teste Manual
    import logging
    logging.basicConfig(level=logging.INFO)
    
    agente = Agente06Roteirista()
    ideia_teste = {
        "id": "teste_01",
        "titulo": "Jesus Reage: Primo Rico",
        "hook_visual": "Jesus com cara de choque olhando um gráfico de juros compostos",
        "sinopse": "Jesus analisa os conselhos financeiros modernos à luz da Bíblia.",
        "visual_style_ref": "Cinematic 4K",
        "emocao_central": "surpresa"
    }
    
    try:
        roteiro = agente.gerar_roteiro(ideia_teste, template_name="react")
        print(f"\n✅ Roteiro gerado e validado com {len(roteiro['scenes'])} cenas!")
    except Exception as e:
        print(f"\n❌ Erro: {e}")
