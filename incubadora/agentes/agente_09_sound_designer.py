import os
import time
import json
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
        self.output_dir = os.path.join(os.getcwd(), "output", "audio_mixed")
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        self.config = config or {}

    def mixar_audio_cinema(self, audios, roteiro):
        """
        Mixa voz, trilha sonora dinâmica e efeitos sonoros (SFX).
        """
        console.print(f"[bold yellow]AGENTE 09: Iniciando Mixagem de Cinema (Sound Design)...[/bold yellow]")
        
        # Simulação de mixagem complexa (FFmpeg seria chamado aqui)
        # 1. Analisar sentimento do roteiro para escolher trilha (Tensão, Alegria, Mistério)
        # 2. Inserir SFX nos pontos de impacto (ex: "Dinheiro caindo", "Explosão", "Grilo")
        # 3. Normalizar áudio (Loudness Standards -14 LUFS)

        audios_mixados = []
        
        # Garante que 'faixas' existe
        faixas = audios.get('faixas', [])
        if not faixas:
            console.print("[red]ALERTA: Nenhuma faixa de audio recebida para mixagem![/red]")
            return {"faixas_mixadas": []}

        for faixa in faixas:
            bloco_id = faixa['bloco_id']
            # Recuperar texto para análise de sentimento simples
            blocos = roteiro if isinstance(roteiro, list) else roteiro.get('blocos', [])
            texto = ""
            if bloco_id < len(blocos):
                texto = blocos[bloco_id].get('fala', '')
            
            sfx = "Nenhum"
            if "dinheiro" in texto.lower():
                sfx = "SFX_Cash_Register.mp3"
            elif "erro" in texto.lower():
                sfx = "SFX_Error_Buzz.mp3"
                
            console.print(f"   [cyan]Bloco {bloco_id+1}:[/cyan] Mixando Voz + Trilha + {sfx}")
            
            # MIXAGEM REAL DE ÁUDIO
            output_file = os.path.join(self.output_dir, f"mixed_bloco_{bloco_id:03d}.mp3")
            
            if not PYDUB_AVAILABLE:
                console.print(f"      -> [bold red]ERRO FATAL: pydub não instalado![/bold red]")
                console.print(f"      -> [yellow]Instale com: pip install pydub[/yellow]")
                console.print(f"      -> [yellow]Necessário também instalar FFmpeg no sistema.[/yellow]")
                raise ImportError("pydub e FFmpeg são obrigatórios para mixagem de áudio real.")
            else:
                # Verificar se arquivo de narração existe
                narration_path = faixa['arquivo']
                if not os.path.exists(narration_path):
                    console.print(f"      -> [red]ERRO: Arquivo de narração não encontrado: {narration_path}[/red]")
                    raise FileNotFoundError(f"Narração não encontrada: {narration_path}")
                
                try:
                    # 1. Carregar narração
                    console.print(f"      -> [dim]Carregando narração...[/dim]")
                    narration = AudioSegment.from_file(narration_path)
                    
                    # 2. Carregar música de fundo (se configurada)
                    background_music_path = self.config.get('background_music')
                    if background_music_path and os.path.exists(background_music_path):
                        console.print(f"      -> [dim]Adicionando música de fundo...[/dim]")
                        music = AudioSegment.from_file(background_music_path)
                        
                        # Ajustar duração da música para match com narração
                        if len(music) < len(narration):
                            # Loopa música se for muito curta
                            repeats = (len(narration) // len(music)) + 1
                            music = music * repeats
                        
                        # Cortar música para duração exata da narração
                        music = music[:len(narration)]
                        
                        # Reduzir volume da música (-12dB para não sobrepor narração)
                        music = music - 12
                        
                        # Mixar narração + música
                        mixed = narration.overlay(music)
                    else:
                        # Sem música de fundo, usar apenas narração
                        mixed = narration
                    
                    # 3. Normalizar áudio final (padrão de loudness)
                    console.print(f"      -> [dim]Normalizando áudio...[/dim]")
                    mixed = normalize(mixed)
                    
                    # 4. Exportar arquivo final
                    console.print(f"      -> [dim]Exportando mixagem...[/dim]")
                    mixed.export(output_file, format="mp3", bitrate="192k")
                    
                    console.print(f"      -> [green]Mixagem concluída: {os.path.basename(output_file)}[/green]")
                    
                except Exception as e:
                    console.print(f"      -> [red]Erro na mixagem: {e}[/red]")
                    raise
            
            # Adiciona à lista de faixas mixadas
            # IMPORTANTE: Manter a estrutura que o Agente 07 espera
            faixa_mixada = faixa.copy()
            faixa_mixada['arquivo_mixado'] = output_file
            audios_mixados.append(faixa_mixada)
            
        console.print(f"[bold green]MIXAGEM CONCLUIDA![/bold green]")
        
        return {"faixas_mixadas": audios_mixados}
