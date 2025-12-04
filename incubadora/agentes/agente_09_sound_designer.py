import os
import json
import random
from rich.console import Console

# Importar pydub para mixagem real de áudio
try:
    from pydub import AudioSegment
    from pydub.effects import normalize
    PYDUB_AVAILABLE = True
except ImportError:
    PYDUB_AVAILABLE = False
    print("WARNING: pydub não instalado. Instale com: pip install pydub")

console = Console()

class Agente09SoundDesigner:
    def __init__(self, config=None):
        self.output_dir = os.path.join("outputs", "T09_audio_mixed")
        os.makedirs(self.output_dir, exist_ok=True)
        self.config = config or {}
        
        # Mapa de SFX (Poderia ser carregado de um JSON externo)
        self.sfx_map = {
            "dinheiro": ["cash_register.mp3", "coins_drop.mp3"],
            "erro": ["error_buzz.mp3", "fail_trombone.mp3"],
            "sucesso": ["success_chime.mp3", "level_up.mp3"],
            "transicao": ["whoosh.mp3", "swoosh.mp3"],
            "impacto": ["boom.mp3", "hit.mp3"]
        }
        
        self.assets_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "assets", "audio")
        
        # Garante estrutura de diretórios
        os.makedirs(os.path.join(self.assets_dir, "sfx"), exist_ok=True)
        os.makedirs(os.path.join(self.assets_dir, "music"), exist_ok=True)

    def _get_asset_path(self, category, filename):
        """Retorna caminho absoluto do asset."""
        return os.path.join(self.assets_dir, category, filename)

    def mixar_audio_cinema(self, audios, roteiro):
        """
        Mixa voz, trilha sonora dinâmica e efeitos sonoros (SFX).
        """
        console.print(f"[bold yellow]AGENTE 09: Iniciando Mixagem de Cinema (Sound Design)...[/bold yellow]")
        
        audios_mixados = []
        faixas = audios.get('faixas', [])
        
        if not faixas:
            console.print("[red]ALERTA: Nenhuma faixa de audio recebida![/red]")
            return {"faixas_mixadas": []}

        for faixa in faixas:
            bloco_id = faixa['bloco_id']
            
            # Recuperar texto para análise de sentimento/SFX
            blocos = roteiro.get('blocos', [])
            texto = ""
            audio_fx_sugerido = None
            
            if bloco_id < len(blocos):
                bloco_data = blocos[bloco_id]
                texto = bloco_data.get('fala', '')
                audio_fx_sugerido = bloco_data.get('audio_fx') # Sugestão do Roteirista
            
            # Escolha de SFX
            sfx_path = None
            sfx_name = "Nenhum"
            
            # 1. Prioridade: Sugestão do Roteirista
            if audio_fx_sugerido:
                # Tenta mapear sugestão genérica para arquivo
                for key in self.sfx_map:
                    if key in audio_fx_sugerido.lower():
                        sfx_file = random.choice(self.sfx_map[key])
                        sfx_path = self._get_asset_path("sfx", sfx_file)
                        sfx_name = sfx_file
                        break
            
            # 2. Fallback: Análise de Texto Simples
            if not sfx_path:
                if "dinheiro" in texto.lower() or "rico" in texto.lower():
                    sfx_file = random.choice(self.sfx_map["dinheiro"])
                    sfx_path = self._get_asset_path("sfx", sfx_file)
                    sfx_name = sfx_file
            
            console.print(f"   [cyan]Bloco {bloco_id+1}:[/cyan] Voz + Trilha + SFX: {sfx_name}")
            
            # MIXAGEM REAL
            output_file = os.path.join(self.output_dir, f"mixed_bloco_{bloco_id:03d}.mp3")
            
            if not PYDUB_AVAILABLE:
                # Mock se não tiver pydub (para não quebrar pipeline em dev)
                console.print(f"      -> [yellow]Pydub ausente. Copiando arquivo original.[/yellow]")
                import shutil
                shutil.copy(faixa['arquivo'], output_file)
            else:
                try:
                    # 1. Carregar Narração
                    narration = AudioSegment.from_file(faixa['arquivo'])
                    
                    # 2. Carregar Trilha (Looping se necessário)
                    music_dir = os.path.join(self.assets_dir, "music")
                    music_files = [f for f in os.listdir(music_dir) if f.endswith(".mp3")]
                    
                    if music_files:
                        music_file = random.choice(music_files)
                        music_path = os.path.join(music_dir, music_file)
                        console.print(f"      -> [cyan]Adicionando trilha: {music_file}[/cyan]")
                        
                        bg_music = AudioSegment.from_file(music_path)
                        
                        # Ajustar volume (-15dB para fundo)
                        bg_music = bg_music - 15
                        
                        # Loop para cobrir narração
                        if len(bg_music) < len(narration):
                            loops = int(len(narration) / len(bg_music)) + 1
                            bg_music = bg_music * loops
                            
                        # Cortar excesso
                        bg_music = bg_music[:len(narration)]
                        
                        # Fade in/out
                        bg_music = bg_music.fade_in(2000).fade_out(2000)
                        
                        # Mixar (Overlay)
                        music = bg_music
                    else:
                        console.print(f"      -> [yellow]Nenhuma música encontrada em {music_dir}. Usando silêncio.[/yellow]")
                        music = AudioSegment.silent(duration=len(narration))
                    
                    # 3. Carregar SFX (Overlay no início ou fim)
                    if sfx_path and os.path.exists(sfx_path):
                        sfx = AudioSegment.from_file(sfx_path)
                        # Reduzir volume do SFX
                        sfx = sfx - 5
                        mixed = narration.overlay(sfx, position=0)
                    else:
                        mixed = narration
                    
                    # Mixar música de fundo
                    mixed = mixed.overlay(music)
                    
                    # 4. Normalizar e Exportar
                    mixed = normalize(mixed)
                    mixed.export(output_file, format="mp3", bitrate="192k")
                    
                except Exception as e:
                    console.print(f"      -> [red]Erro Mixagem: {e}[/red]")
                    # Fallback: usa original
                    import shutil
                    shutil.copy(faixa['arquivo'], output_file)

            # Atualiza lista
            faixa_mixada = faixa.copy()
            faixa_mixada['arquivo_mixado'] = output_file
            audios_mixados.append(faixa_mixada)
            
        return {"faixas_mixadas": audios_mixados}

if __name__ == "__main__":
    # Teste
    agente = Agente09SoundDesigner()
    print("Agente 09 inicializado.")
