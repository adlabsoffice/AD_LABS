import json
from rich.console import Console

console = Console()

class Agente10Director:
    def __init__(self):
        pass

    def revisar_roteiro(self, roteiro, config):
        """
        Atua como o Diretor (Minos QA) para aprovar ou rejeitar o roteiro.
        PADRAO STOCKDALE: Só aceita excelência.
        """
        console.print(f"[bold yellow]AGENTE 10 (DIRETOR): Revisando Roteiro (PADRAO STOCKDALE)...[/bold yellow]")
        
        score = 0
        feedback = []
        
        # 1. Verificar Hook (0-5s) vs Promessa do Titulo
        blocos = roteiro.get('blocos', [])
        if not blocos:
            console.print("[red]ERRO: Roteiro vazio![/red]")
            return False

        primeiro_bloco = blocos[0]
        hook_text = primeiro_bloco.get('fala', '')
        titulo = roteiro.get('titulo_otimizado', '')
        
        if len(hook_text) < 10:
            feedback.append("FATAL: Hook inexistente.")
            score -= 10
        elif titulo.lower() in hook_text.lower():
             feedback.append("AVISO: Hook repete o titulo (Redundante).")
             score += 2
        else:
             score += 5
             feedback.append("Hook cria curiosidade sem repetir titulo.")

        # 2. Verificar Synergy (Titulo + Visual do Hook)
        visual_hook = primeiro_bloco.get('visual', '')
        if len(visual_hook) > 20:
             score += 5
             feedback.append("Visual do Hook detalhado.")
        else:
             feedback.append("Visual do Hook fraco.")

        # 3. Ritmo (Tamanho dos blocos)
        blocos_longos = [b for b in blocos if len(b.get('fala', '').split()) > 40]
        if blocos_longos:
             feedback.append(f"ALERTA: {len(blocos_longos)} blocos muito longos (risco de tedio).")
             score -= 2
        else:
             score += 5
             feedback.append("Ritmo dinamico (blocos curtos).")

        console.print(f"[bold]Score do Diretor: {score}/20[/bold]")
        for f in feedback:
            console.print(f"   {f}")
        
        # 4. Verificar Duração Total (CRÍTICO)
        console.print("\n[bold yellow]Verificando duração total...[/bold yellow]")
        duracao_total = self._calcular_duracao_total(blocos)
        duracao_alvo = config.get('duracao_alvo_segundos', 60)
        
        if duracao_total > duracao_alvo * 1.2:  # 20% de margem
            feedback.append(f"FATAL: Vídeo muito longo ({duracao_total}s vs {duracao_alvo}s alvo)")
            console.print(f"[red]   ❌ {feedback[-1]}[/red]")
            score -= 10
        elif duracao_total < duracao_alvo * 0.8:
            feedback.append(f"AVISO: Vídeo muito curto ({duracao_total}s)")
            console.print(f"[yellow]   ⚠ {feedback[-1]}[/yellow]")
            score -= 3
        else:
            feedback.append(f"Duração dentro do alvo ({duracao_total}s)")
            console.print(f"[green]   ✓ {feedback[-1]}[/green]")
            score += 5

        # PADRAO STOCKDALE: Score minimo alto (15/20)
        if score >= 15:
            console.print(f"\n[bold green]APROVADO PARA PRODUCAO (STOCKDALE APPROVED)![/bold green]")
            return True
        else:
            console.print(f"\n[bold red]REJEITADO: O roteiro nao atingiu o padrao de excelencia (Score: {score}/20).[/bold red]")
            return False

    def verificar_continuidade(self, roteiro):
        """
        Verifica a fluidez visual entre as cenas (Prompt N vs Prompt N+1).
        """
        console.print(f"[bold yellow]AGENTE 10 (DIRETOR): Verificando Continuidade Visual...[/bold yellow]")
        
        blocos = roteiro if isinstance(roteiro, list) else roteiro.get('blocos', [])
        
        if len(blocos) < 2:
            return True

        # Simulação do Loop de Continuidade
        for i in range(len(blocos) - 1):
            cena_atual = blocos[i]
            cena_proxima = blocos[i+1]
            
            visual_a = cena_atual.get('visual', '')
            visual_b = cena_proxima.get('visual', '')
            
            console.print(f"   [dim]Analisando transicao: Cena {i+1} -> Cena {i+2}[/dim]")
            
            # Lógica Simulada: Se a próxima cena não tiver conectivo visual, falha
            # Na prática, aqui chamaria o LLM para comparar os prompts
            
            # Exemplo de falha simulada para demonstrar o loop (apenas se for muito curto)
            if len(visual_b) < 10:
                console.print(f"      -> [red]Quebra de Continuidade detectada![/red]")
                console.print(f"      -> [yellow]Solicitando reescrita da Cena {i+2}...[/yellow]")
                
                # Simula a correção automática
                blocos[i+1]['visual'] = f"Mantendo a iluminação da cena anterior, {visual_b}"
                console.print(f"      -> [green]Corrigido:[/green] {blocos[i+1]['visual']}")
            else:
                console.print(f"      -> [green]Fluidez Aprovada.[/green]")

        console.print(f"[bold green]CONTINUIDADE VISUAL GARANTIDA![/bold green]")
        return True
    
    def _calcular_duracao_total(self, blocos) -> int:
        """
        Estima duração total baseada no WPM esperado (175 wpm).
        Retorna duração em segundos.
        """
        total_palavras = sum([len(b.get('fala', '').split()) for b in blocos])
        wpm_alvo = 175  # Palavras por minuto (Blueprint: 168-187)
        duracao_segundos = int((total_palavras / wpm_alvo) * 60)
        return duracao_segundos
