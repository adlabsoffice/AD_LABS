import os
import json
import sys
from typing import Dict, List
from rich.console import Console
from rich.panel import Panel

console = Console()

class Agente07EditorJSON:
    """
    Agente Editor Lógico (Sem GPU).
    Responsabilidade: Montar a 'Timeline' do vídeo em um arquivo JSON.
    Não renderiza pixels, apenas define O QUE vai acontecer e QUANDO.
    """
    def __init__(self):
        self.output_dir = os.path.join("outputs", "T07_projetos_video")
        os.makedirs(self.output_dir, exist_ok=True)

    def criar_projeto_video(self, roteiro: Dict, imagens: List[Dict], audios: Dict) -> Dict:
        """
        Combina Roteiro + Imagens + Áudio em um arquivo de projeto.
        """
        console.print(Panel.fit("[bold cyan]AGENTE 07: Editor Lógico[/bold cyan]\nMontando Timeline..."))
        
        projeto = {
            "id": f"proj_{roteiro.get('id', 'video')}",
            "titulo": roteiro.get("titulo_final", "Video Sem Titulo"),
            "resolucao": [1920, 1080],
            "fps": 30,
            "timeline": []
        }
        
        blocos = roteiro.get("blocos", [])
        faixas_audio = audios.get("faixas_mixadas") or audios.get("faixas", [])
        
        # Mapear assets por bloco_id para acesso rápido
        map_imagens = {img["bloco_id"]: img["arquivo"] for img in imagens}
        map_audios = {aud["bloco_id"]: aud for aud in faixas_audio}
        
        tempo_acumulado = 0.0
        
        for i, bloco in enumerate(blocos):
            bloco_id = i # Assumindo sequencial 0-indexado
            
            # Asset de Áudio (Mestre do Tempo)
            audio_info = map_audios.get(bloco_id)
            if not audio_info:
                console.print(f"[yellow]⚠ Bloco {i}: Sem áudio. Usando duração padrão de 5s.[/yellow]")
                duracao = 5.0
                audio_path = None
            else:
                duracao = audio_info.get("duracao", 5.0)
                # Se tiver áudio mixado (do Agente 09), usa ele. Se não, usa o bruto.
                audio_path = audio_info.get("arquivo_mixado") or audio_info.get("arquivo")
            
            # Asset de Imagem
            imagem_path = map_imagens.get(bloco_id)
            if not imagem_path:
                console.print(f"[red]⚠ Bloco {i}: Sem imagem gerada![/red]")
                # Em produção, usaria um placeholder
                imagem_path = "assets/placeholder.png" 
            
            # Definição do Clip na Timeline
            clip = {
                "id": f"clip_{i}",
                "start_time": tempo_acumulado,
                "duration": duracao,
                "type": "image_clip",
                "assets": {
                    "image": imagem_path,
                    "audio": audio_path
                },
                "effects": [
                    {
                        "type": "ken_burns", # Zoom/Pan automático
                        "zoom_start": 1.0,
                        "zoom_end": 1.15, # Zoom in suave de 15%
                        "pan_direction": "center" # ou 'left', 'right' aleatório
                    },
                    {
                        "type": "fade_in",
                        "duration": 0.5
                    }
                ],
                "subtitle": {
                    "text": bloco.get("fala", ""),
                    "style": "default"
                }
            }
            
            projeto["timeline"].append(clip)
            tempo_acumulado += duracao
            
        projeto["duracao_total"] = tempo_acumulado
        
        # Salvar Projeto
        self.salvar_projeto(projeto)
        
        console.print(f"[green]✅ Projeto de Vídeo Criado![/green]")
        console.print(f"   Duração: {tempo_acumulado:.1f}s")
        console.print(f"   Clips: {len(projeto['timeline'])}")
        
        return projeto

    def salvar_projeto(self, projeto: Dict):
        filename = f"{projeto['id']}.json"
        filepath = os.path.join(self.output_dir, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(projeto, f, indent=2, ensure_ascii=False)
        console.print(f"[dim]Arquivo de projeto salvo: {filepath}[/dim]")

if __name__ == "__main__":
    # Teste
    editor = Agente07EditorJSON()
    # Mock data para teste
    editor.criar_projeto_video(
        {"id": "test", "blocos": [{"fala": "Oi"}]}, 
        [{"bloco_id": 0, "arquivo": "img.png"}], 
        {"faixas": [{"bloco_id": 0, "duracao": 2.0, "arquivo": "aud.mp3"}]}
    )
