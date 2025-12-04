"""
Social Media Configuration Schemas - Pydantic Models

Validação de configurações para publishers de redes sociais.
Garante type safety e validação em tempo de execução.

Autor: Refatoração Arquitetural P1
Data: 04/12/2024
"""

from pathlib import Path
from typing import List, Literal, Optional
from pydantic import BaseModel, Field, validator


class YouTubeConfig(BaseModel):
    """Configuração para YouTube Publisher."""
    
    client_id: str = Field(..., description="OAuth2 Client ID do Google Cloud Console")
    client_secret: str = Field(..., description="OAuth2 Client Secret")
    refresh_token: str = Field(..., description="Refresh token OAuth2 gerado via youtube_oauth_setup.py")
    
    default_privacy: Literal["public", "unlisted", "private"] = Field(
        default="unlisted",
        description="Privacy padrão dos vídeos"
    )
    default_category: int = Field(
        default=22,
        description="Categoria YouTube (22 = People & Blogs)"
    )
    
    max_retries: int = Field(default=3, ge=1, le=10)
    
    class Config:
        schema_extra = {
            "example": {
                "client_id": "123456789.apps.googleusercontent.com",
                "client_secret": "YOUR_CLIENT_SECRET",
                "refresh_token": "YOUR_REFRESH_TOKEN",
                "default_privacy": "unlisted",
                "default_category": 22,
                "max_retries": 3
            }
        }


class InstagramConfig(BaseModel):
    """Configuração para Instagram Publisher."""
    
    # Opção 1: Official API (futuro)
    access_token: Optional[str] = Field(
        default=None,
        description="Access token da Instagram Graph API"
    )
    
    # Opção 2: instagrapi (atual)
    username: Optional[str] = Field(default=None, description="Username Instagram")
    password: Optional[str] = Field(default=None, description="Password Instagram")
    
    use_official_api: bool = Field(
        default=False,
        description="Se True, usa Graph API. Se False, usa instagrapi"
    )
    
    max_retries: int = Field(default=3, ge=1, le=10)
    
    @validator("access_token", "username", "password")
    def validate_credentials(cls, v, values, field):
        """Valida que pelo menos um método de auth está configurado."""
        use_official = values.get("use_official_api", False)
        
        if use_official and field.name == "access_token" and not v:
            raise ValueError("access_token obrigatório quando use_official_api=True")
        
        if not use_official and field.name in ["username", "password"] and not v:
            # Só valida se já passou pelo campo use_official_api
            if "use_official_api" in values:
                raise ValueError(f"{field.name} obrigatório quando use_official_api=False")
        
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "username": "seu_usuario",
                "password": "sua_senha",
                "use_official_api": False,
                "max_retries": 3
            }
        }


class TikTokConfig(BaseModel):
    """Configuração para TikTok Publisher (placeholder)."""
    
    api_key: Optional[str] = Field(default=None, description="TikTok API Key (quando aprovado)")
    api_secret: Optional[str] = Field(default=None, description="TikTok API Secret")
    
    status: Literal["not_implemented", "pending_approval", "active"] = Field(
        default="not_implemented",
        description="Status da integração TikTok"
    )
    
    alternative_workflow: str = Field(
        default="n8n_workflows/03_tiktok_posting.json",
        description="Workflow alternativo enquanto API não está disponível"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "status": "not_implemented",
                "alternative_workflow": "n8n_workflows/03_tiktok_posting.json"
            }
        }


class PublishMetadata(BaseModel):
    """Metadados para publicação de vídeo."""
    
    titulo: str = Field(..., min_length=1, max_length=100, description="Título do vídeo")
    descricao: str = Field(default="", max_length=5000, description="Descrição do vídeo")
    tags: List[str] = Field(default_factory=list, description="Tags/hashtags")
    thumbnail_path: Optional[Path] = Field(default=None, description="Caminho da thumbnail customizada")
    
    # Metadados específicos por plataforma
    youtube_category: Optional[int] = Field(default=None, description="Categoria YouTube (override)")
    youtube_privacy: Optional[Literal["public", "unlisted", "private"]] = Field(
        default=None,
        description="Privacy YouTube (override)"
    )
    
    instagram_caption: Optional[str] = Field(
        default=None,
        max_length=2200,
        description="Caption Instagram (override, max 2200 chars)"
    )
    
    @validator("tags")
    def validate_tags(cls, v):
        """Remove tags vazias e limita quantidade."""
        tags = [tag.strip() for tag in v if tag.strip()]
        if len(tags) > 30:
            raise ValueError("Máximo 30 tags permitidas")
        return tags
    
    class Config:
        schema_extra = {
            "example": {
                "titulo": "Como Jesus Lidaria com Dinheiro Hoje?",
                "descricao": "Explorando ensinamentos bíblicos sobre finanças...",
                "tags": ["financas", "biblia", "jesus", "dinheiro"],
                "thumbnail_path": None,
                "youtube_category": 22,
                "youtube_privacy": "unlisted"
            }
        }


class ApprovalFlowConfig(BaseModel):
    """Configuração do fluxo de aprovação via Telegram."""
    
    require_telegram_approval: bool = Field(
        default=True,
        description="Se True, aguarda aprovação manual via Telegram"
    )
    
    timeout_minutos: int = Field(
        default=10,
        ge=1,
        le=60,
        description="Timeout para aprovação (em minutos)"
    )
    
    auto_publish_after_hours: Optional[int] = Field(
        default=None,
        ge=1,
        description="Se definido, publica automaticamente após X horas sem resposta"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "require_telegram_approval": True,
                "timeout_minutos": 10,
                "auto_publish_after_hours": None
            }
        }


# Export schemas
__all__ = [
    "YouTubeConfig",
    "InstagramConfig",
    "TikTokConfig",
    "PublishMetadata",
    "ApprovalFlowConfig"
]
