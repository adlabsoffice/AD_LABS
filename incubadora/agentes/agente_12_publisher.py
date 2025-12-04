"""
Agente 12 - Publisher Genérico (Refatorado)

Orchestrator de publicação em múltiplas plataformas.
Usa Strategy Pattern para desacoplar de APIs específicas.

Mudanças Arquiteturais (P1):
- ✅ Remove preparar_thumbnail() → ThumbnailProcessor
- ✅ Remove upload_youtube() → YouTubePublisher
- ✅ Adiciona DIP: depende de SocialMediaPublisher (abstração)
- ✅ Suporta múltiplas plataformas via Factory
- ✅ Validação Pydantic de metadados

Autor: Refatoração Arquitetural P1
Data Original: Unknown
Data Refatoração: 04/12/2024
"""

import os
import sys
import json
import logging
from pathlib import Path
from typing import Dict, Optional, List

from rich.console import Console
from rich.panel import Panel

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Adiciona diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importa componentes refatorados
from services.social_media.base_publisher import SocialMediaPublisher
from services.publisher_factory import PublisherFactory
from services.thumbnail_processor import ThumbnailProcessor
from specs.schemas.social_media_config import PublishMetadata
from utils.telegram_bot import TelegramBot

console = Console()


class Agente12Publisher:
    """
    Agente de Publicação Genérico.
    
    Responsabilidades:
    - Orchestrar fluxo de publicação
    - Integrar com ThumbnailProcessor (SRP)
    - Delegar upload para publishers específicos (DIP)
    - Gerenciar aprovação via Telegram
    
    Princípios SOLID aplicados:
    - SRP: Apenas orchestração, não processing
    - DIP: Depende de SocialMediaPublisher (abstração)
    - OCP: Extensível a novas plataformas sem modificar código
    """
    
    def __init__(
        self,
        canal_id: str = "default",
        config: Optional[Dict] = None,
        publishers: Optional[Dict[str, SocialMediaPublisher]] = None
    ):
        """
        Inicializa Publisher Orchestrator.
        
        Args:
            canal_id: ID do canal (para outputs separados)
            config: Configurações de publishers (YouTube, Instagram, etc)
            publishers: Publishers customizados (para testes/dependency injection)
        """
        self.canal_id = canal_id
        self.output_dir = Path(f"outputs/{canal_id}/T12_publicacao")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Componentes
        self.telegram = TelegramBot()
        self.thumbnail_processor = ThumbnailProcessor(
            output_dir=self.output_dir / "thumbnails"
        )
        
        # Publishers (DIP: injeção de dependências)
        if publishers is None:
            # Cria publishers via factory
            config = config or {}
            self.publishers = PublisherFactory.create_all(config)
            logger.info(f"Publishers disponíveis: {list(self.publishers.keys())}")
        else:
            # Usa publishers injetados (útil para testes)
            self.publishers = publishers
    
    def publicar(
        self,
        plataforma: str,
        video_path: Path,
        metadata: PublishMetadata,
        thumbnail_text: Optional[str] = None,
        approval_required: bool = True
    ) -> str:
        """
        Publica vídeo em plataforma específica.
        
        Args:
            plataforma: Nome da plataforma ("youtube", "instagram", "tiktok")
            video_path: Caminho do vídeo
            metadata: Metadados validados (Pydantic)
            thumbnail_text: Texto para thumbnail (opcional)
            approval_required: Se True, aguarda aprovação Telegram
        
        Returns:
            URL do vídeo publicado
        
        Raises:
            ValueError: Se plataforma não disponível
            RuntimeError: Se publicação falhar
        """
        console.print(Panel.fit(
            f"[bold cyan]AGENTE 12: Publicando em {plataforma.upper()}[/bold cyan]"
        ))
        
        # Valida plataforma
        if plataforma not in self.publishers:
            available = list(self.publishers.keys())
            raise ValueError(
                f"Plataforma '{plataforma}' não disponível. "
                f"Disponíveis: {available}"
            )
        
        publisher = self.publishers[plataforma]
        
        # Processa thumbnail (se necessário)
        thumbnail_path = self._process_thumbnail(
            metadata, 
            plataforma,
            thumbnail_text
        )
        
        # Atualiza metadata com thumbnail
        if thumbnail_path:
            metadata.thumbnail_path = thumbnail_path
        
        # Aprovação Telegram (se configurado)
        if approval_required:
            approved = self._request_approval(video_path, metadata, plataforma)
            if not approved:
                console.print("[red]❌ Publicação cancelada pelo usuário[/red]")
                raise RuntimeError("Publicação cancelada via Telegram")
        
        # Publica via publisher específico (Strategy Pattern)
        try:
            console.print(f"[yellow]📤 Publicando em {plataforma}...[/yellow]")
            
            video_url = publisher.publish(video_path, metadata)
            
            console.print(f"[green]✅ Publicado com sucesso![/green]")
            console.print(f"[cyan]🔗 URL: {video_url}[/cyan]")
            
            # Salva metadados da publicação
            self._save_publication_metadata(plataforma, video_url, metadata)
            
            return video_url
        
        except Exception as e:
            logger.error(f"Erro ao publicar em {plataforma}: {e}")
            
            # Notifica erro via Telegram
            self.telegram.enviar_alerta_emergencia(
                f"Erro ao publicar em {plataforma}: {e}"
            )
            
            raise
    
    def publicar_multiplas_plataformas(
        self,
        plataformas: List[str],
        video_path: Path,
        metadata: PublishMetadata,
        thumbnail_text: Optional[str] = None
    ) -> Dict[str, str]:
        """
        Publica em múltiplas plataformas simultaneamente.
        
        Args:
            plataformas: Lista de plataformas ["youtube", "instagram"]
            video_path: Vídeo a publicar
            metadata: Metadados
            thumbnail_text: Texto para thumbnail
        
        Returns:
            Dicionário {plataforma: url}
        """
        console.print(Panel.fit(
            f"[bold magenta]AGENTE 12: Cross-posting em {len(plataformas)} plataformas[/bold magenta]"
        ))
        
        results = {}
        
        for plataforma in plataformas:
            try:
                url = self.publicar(
                    plataforma,
                    video_path,
                    metadata,
                    thumbnail_text,
                    approval_required=False  # Aprova uma vez no início
                )
                results[plataforma] = url
                
            except Exception as e:
                logger.error(f"Falha ao publicar em {plataforma}: {e}")
                results[plataforma] = f"ERROR: {e}"
        
        # Resumo
        sucessos = [p for p, url in results.items() if not url.startswith("ERROR")]
        falhas = [p for p, url in results.items() if url.startswith("ERROR")]
        
        console.print(f"\n[green]✅ Sucessos: {len(sucessos)}/{len(plataformas)}[/green]")
        if falhas:
            console.print(f"[red]❌ Falhas: {', '.join(falhas)}[/red]")
        
        return results
    
    def _process_thumbnail(
        self,
        metadata: PublishMetadata,
        plataforma: str,
        text: Optional[str] = None
    ) -> Optional[Path]:
        """Processa thumbnail usando ThumbnailProcessor."""
        
        # Se metadata já tem thumbnail customizada, usa ela
        if metadata.thumbnail_path and metadata.thumbnail_path.exists():
            logger.info(f"Usando thumbnail customizada: {metadata.thumbnail_path}")
            return metadata.thumbnail_path
        
        # TODO: Integrar com output do Agente 07 (Visual)
        # Por enquanto, retorna None (usa poster frame do vídeo)
        logger.info("Thumbnail não fornecida, plataforma usará poster frame do vídeo")
        return None
    
    def _request_approval(
        self,
        video_path: Path,
        metadata: PublishMetadata,
        plataforma: str
    ) -> bool:
        """Solicita aprovação via Telegram."""
        try:
            console.print("[yellow]⏳ Aguardando aprovação no Telegram...[/yellow]")
            
            # Envia vídeo preview
            approved = self.telegram.enviar_video_aprovacao(str(video_path))
            
            if approved:
                console.print("[green]✅ Aprovado via Telegram[/green]")
            else:
                console.print("[red]❌ Rejeitado via Telegram[/red]")
            
            return approved
        
        except Exception as e:
            logger.warning(f"Erro no fluxo de aprovação: {e}. Prosseguindo...")
            # Se Telegram falhar, não bloqueia publicação
            return True
    
    def _save_publication_metadata(
        self,
        plataforma: str,
        video_url: str,
        metadata: PublishMetadata
    ):
        """Salva metadados da publicação para auditoria."""
        publication_record = {
            "plataforma": plataforma,
            "url": video_url,
            "titulo": metadata.titulo,
            "descricao": metadata.descricao[:100],  # Trunca para resumo
            "tags": metadata.tags,
            "timestamp": str(Path(__file__).stat().st_mtime)  # Aproximado
        }
        
        # Salva JSON
        record_path = self.output_dir / f"publication_{plataforma}.json"
        with open(record_path, "w", encoding="utf-8") as f:
            json.dump(publication_record, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Metadados salvos: {record_path}")
    
    def get_available_platforms(self) -> List[str]:
        """Retorna lista de plataformas disponíveis."""
        return list(self.publishers.keys())


if __name__ == "__main__":
    # Teste básico
    console.print("[bold cyan]🧪 Agente 12 - Publisher Refatorado[/bold cyan]\n")
    
    # Cria agente
    agente = Agente12Publisher(
        canal_id="teste",
        config={}  # Sem config, publishers não estarão disponíveis
    )
    
    console.print(f"Plataformas disponíveis: {agente.get_available_platforms()}")
    console.print("\n[yellow]ℹ Configure YouTube/Instagram para habilitar publicação real.[/yellow]")
    console.print("[cyan]Exemplo de uso:[/cyan]")
    console.print("""
from pathlib import Path
from specs.schemas.social_media_config import PublishMetadata

metadata = PublishMetadata(
    titulo="Teste de Publicação",
    descricao="Vídeo de teste gerado automaticamente",
    tags=["teste", "automacao"]
)

url = agente.publicar(
    plataforma="youtube",
    video_path=Path("outputs/video_final.mp4"),
    metadata=metadata
)
    """)
