import os
import json
from datetime import datetime
from typing import Dict, Optional
from rich.console import Console

console = Console()

class CheckpointManager:
    """
    Gerencia estado do pipeline para permitir retomada após falha.
    Salva checkpoints após cada etapa aprovada.
    """
    
    def __init__(self, canal_nome: str, ideia_id: str):
        self.canal_nome = canal_nome
        self.ideia_id = ideia_id
        self.checkpoint_dir = os.path.join("outputs", "checkpoints")
        os.makedirs(self.checkpoint_dir, exist_ok=True)
        
        self.checkpoint_file = os.path.join(
            self.checkpoint_dir,
            f"{canal_nome}_{ideia_id}_checkpoint.json"
        )
        
        self.estado = self._carregar_ou_criar()
    
    def _carregar_ou_criar(self) -> Dict:
        """Carrega checkpoint existente ou cria novo."""
        if os.path.exists(self.checkpoint_file):
            with open(self.checkpoint_file, "r", encoding="utf-8") as f:
                console.print(f"[yellow]📂 Checkpoint existente encontrado: {self.checkpoint_file}[/yellow]")
                return json.load(f)
        else:
            return {
                "canal": self.canal_nome,
                "ideia_id": self.ideia_id,
                "timestamp_inicio": datetime.now().isoformat(),
                "checkpoints": {}
            }
    
    def marcar_etapa(self, etapa: str, status: str, dados: Optional[Dict] = None):
        """
        Marca uma etapa como completa.
        
        Args:
            etapa: Nome da etapa (ex: 'roteiro', 'imagens', 'audio', 'video')
            status: Status da etapa (ex: 'aprovado', 'rejeitado', 'pendente')
            dados: Dados adicionais da etapa (caminhos de arquivos, etc)
        """
        self.estado["checkpoints"][etapa] = {
            "status": status,
            "timestamp": datetime.now().isoformat(),
            "dados": dados or {}
        }
        
        self._salvar()
        console.print(f"[green]✓ Checkpoint salvo: {etapa} = {status}[/green]")
    
    def obter_status_etapa(self, etapa: str) -> Optional[str]:
        """Retorna status de uma etapa (ou None se não existe)."""
        checkpoint = self.estado["checkpoints"].get(etapa)
        if checkpoint:
            return checkpoint["status"]
        return None
    
    def pode_pular_etapa(self, etapa: str) -> bool:
        """Verifica se etapa já foi aprovada (para retomada)."""
        status = self.obter_status_etapa(etapa)
        return status == "aprovado"
    
    def obter_dados_etapa(self, etapa: str) -> Optional[Dict]:
        """Retorna dados salvos de uma etapa."""
        checkpoint = self.estado["checkpoints"].get(etapa)
        if checkpoint:
            return checkpoint.get("dados")
        return None
    
    def limpar(self):
        """Remove checkpoint (após conclusão bem-sucedida)."""
        if os.path.exists(self.checkpoint_file):
            os.remove(self.checkpoint_file)
            console.print(f"[dim]Checkpoint removido: {self.checkpoint_file}[/dim]")
    
    def _salvar(self):
        """Persiste estado em disco."""
        with open(self.checkpoint_file, "w", encoding="utf-8") as f:
            json.dump(self.estado, f, indent=2, ensure_ascii=False)
    
    def tem_checkpoint_pendente(self) -> bool:
        """Verifica se existe checkpoint de sessão anterior."""
        return os.path.exists(self.checkpoint_file)
    
    def resumir_progresso(self):
        """Imprime resumo do progresso atual."""
        console.print("\n[bold cyan]📊 Progresso do Pipeline:[/bold cyan]")
        
        etapas = ["roteiro", "imagens", "audio", "video"]
        for etapa in etapas:
            status = self.obter_status_etapa(etapa)
            if status == "aprovado":
                console.print(f"  ✅ {etapa.capitalize()}: Aprovado")
            elif status == "rejeitado":
                console.print(f"  ❌ {etapa.capitalize()}: Rejeitado")
            elif status == "pendente":
                console.print(f"  ⏳ {etapa.capitalize()}: Aguardando aprovação")
            else:
                console.print(f"  ⚪ {etapa.capitalize()}: Não iniciado")
        
        console.print()


if __name__ == "__main__":
    # Teste
    cp = CheckpointManager("teste_canal", "ideia_001")
    cp.marcar_etapa("roteiro", "aprovado", {"arquivo": "roteiro.json"})
    cp.marcar_etapa("imagens", "pendente")
    cp.resumir_progresso()
    
    print(f"Pode pular roteiro? {cp.pode_pular_etapa('roteiro')}")
    print(f"Pode pular imagens? {cp.pode_pular_etapa('imagens')}")
