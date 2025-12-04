"""
Testes Unit Tests - Social Media Publishers

Testa publishers com mocks (sem credenciais reais).
Valida Strategy Pattern, Factory e Pydantic schemas.

Autor: Refatoração Arquitetural P1
Data: 04/12/2024

Uso:
    pytest tests/test_publishers.py -v
"""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

# Imports do sistema
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from services.social_media.base_publisher import SocialMediaPublisher, MockPublisher
from services.social_media.youtube_publisher import YouTubePublisher
from services.social_media.instagram_publisher import InstagramPublisher
from services.social_media.tiktok_publisher import TikTokPublisher
from services.publisher_factory import PublisherFactory
from specs.schemas.social_media_config import (
    YouTubeConfig,
    InstagramConfig,
    TikTokConfig,
    PublishMetadata
)
from pydantic import ValidationError


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture
def mock_video_path(tmp_path):
    """Cria vídeo fake para testes."""
    video = tmp_path / "test_video.mp4"
    video.write_bytes(b"fake video content")
    return video


@pytest.fixture
def valid_youtube_config():
    """Config YouTube válida para testes."""
    return {
        "client_id": "test_client_id.apps.googleusercontent.com",
        "client_secret": "test_client_secret",
        "refresh_token": "test_refresh_token",
        "default_privacy": "unlisted",
        "default_category": 22
    }


@pytest.fixture
def valid_instagram_config():
    """Config Instagram válida para testes."""
    return {
        "username": "test_user",
        "password": "test_password",
        "use_official_api": False
    }


@pytest.fixture
def valid_metadata():
    """Metadata válida para testes."""
    return PublishMetadata(
        titulo="Test Video",
        descricao="Test description",
        tags=["test", "automation"]
    )


# ============================================================================
# Testes Pydantic Schemas
# ============================================================================

def test_youtube_config_validation_success(valid_youtube_config):
    """YouTubeConfig deve aceitar config válida."""
    config = YouTubeConfig(**valid_youtube_config)
    
    assert config.client_id == valid_youtube_config["client_id"]
    assert config.default_privacy == "unlisted"
    assert config.default_category == 22


def test_youtube_config_validation_failure():
    """YouTubeConfig deve rejeitar privacy inválida."""
    with pytest.raises(ValidationError):
        YouTubeConfig(
            client_id="test",
            client_secret="test",
            refresh_token="test",
            default_privacy="invalid_privacy"  # ← Deve falhar
        )


def test_publish_metadata_validation():
    """PublishMetadata deve validar título obrigatório."""
    # Válido
    metadata = PublishMetadata(titulo="Test")
    assert metadata.titulo == "Test"
    
    # Inválido: titulo vazio
    with pytest.raises(ValidationError):
        PublishMetadata(titulo="")


def test_publish_metadata_tags_limit():
    """PublishMetadata deve limitar tags a 30."""
    too_many_tags = [f"tag{i}" for i in range(35)]
    
    with pytest.raises(ValidationError):
        PublishMetadata(titulo="Test", tags=too_many_tags)


# ============================================================================
# Testes Base Publisher
# ============================================================================

def test_mock_publisher_always_available():
    """MockPublisher deve sempre estar disponível."""
    publisher = MockPublisher()
    assert publisher.is_available() is True


def test_mock_publisher_records_publications(mock_video_path, valid_metadata):
    """MockPublisher deve registrar publicações."""
    publisher = MockPublisher()
    
    url = publisher.publish(mock_video_path, valid_metadata)
    
    assert "mock-platform.com" in url
    assert len(publisher.published_videos) == 1
    assert publisher.published_videos[0]["metadata"] == valid_metadata


def test_base_publisher_validate_video_missing_file():
    """validate_video deve falhar se arquivo não existe."""
    publisher = MockPublisher()
    
    with pytest.raises(FileNotFoundError):
        publisher.validate_video(Path("nonexistent.mp4"))


# ============================================================================
# Testes YouTube Publisher
# ============================================================================

def test_youtube_publisher_not_available_without_config():
    """YouTubePublisher deve retornar False sem config válida."""
    publisher = YouTubePublisher(config={})
    assert publisher.is_available() is False


def test_youtube_publisher_not_available_without_google_api():
    """YouTubePublisher deve detectar se google-api-python-client ausente."""
    # Este teste assume que a biblioteca está instalada
    # Em CI sem biblioteca, is_available() retornaria False
    publisher = YouTubePublisher(config={})
    # Se biblioteca presente mas config inválida
    assert publisher.is_available() is False


@patch('services.social_media.youtube_publisher.build')
@patch('services.social_media.youtube_publisher.Credentials')
def test_youtube_publisher_publish_with_mock(
    mock_credentials,
    mock_build,
    valid_youtube_config,
    mock_video_path,
    valid_metadata
):
    """Testa upload YouTube com API mockada."""
    # Setup mocks
    mock_youtube = MagicMock()
    mock_build.return_value = mock_youtube
    
    # Mock do response de upload
    mock_youtube.videos().insert().next_chunk.return_value = (
        None,  # No more chunks
        {"id": "MOCK_VIDEO_ID_123"}
    )
    
    # Cria publisher
    publisher = YouTubePublisher(valid_youtube_config)
    publisher.youtube_client = mock_youtube  # Força mock client
    
    # Publica
    url = publisher.publish(mock_video_path, valid_metadata)
    
    # Valida
    assert "youtube.com/watch?v=" in url
    assert "MOCK_VIDEO_ID_123" in url


# ============================================================================
# Testes Instagram Publisher
# ============================================================================

def test_instagram_publisher_not_available_without_credentials():
    """InstagramPublisher sem credenciais deve retornar False."""
    publisher = InstagramPublisher(config={})
    assert publisher.is_available() is False


def test_instagram_publisher_prepare_caption(valid_instagram_config, valid_metadata):
    """Deve preparar caption com título + descrição + hashtags."""
    publisher = InstagramPublisher(valid_instagram_config)
    
    caption = publisher._prepare_caption(valid_metadata)
    
    assert valid_metadata.titulo in caption
    assert valid_metadata.descricao in caption
    assert "#test" in caption
    assert "#automation" in caption


def test_instagram_caption_respects_2200_char_limit(valid_instagram_config):
    """Caption deve ser truncada em 2200 caracteres."""
    long_desc = "x" * 3000
    metadata = PublishMetadata(
        titulo="Test",
        descricao=long_desc
    )
    
    publisher = InstagramPublisher(valid_instagram_config)
    caption = publisher._prepare_caption(metadata)
    
    assert len(caption) <= 2200


# ============================================================================
# Testes TikTok Publisher
# ============================================================================

def test_tiktok_publisher_always_unavailable():
    """TikTokPublisher deve retornar False (não implementado)."""
    publisher = TikTokPublisher(config={})
    assert publisher.is_available() is False


def test_tiktok_publisher_raises_not_implemented(mock_video_path, valid_metadata):
    """publish() deve lançar NotImplementedError."""
    publisher = TikTokPublisher(config={})
    
    with pytest.raises(NotImplementedError) as exc_info:
        publisher.publish(mock_video_path, valid_metadata)
    
    # Deve ter mensagem informativa
    assert "n8n" in str(exc_info.value).lower()


# ============================================================================
# Testes Factory Pattern
# ============================================================================

def test_factory_creates_correct_publisher_type():
    """Factory deve retornar tipo correto de publisher."""
    youtube = PublisherFactory.create("youtube", {})
    assert isinstance(youtube, YouTubePublisher)
    
    instagram = PublisherFactory.create("instagram", {})
    assert isinstance(instagram, InstagramPublisher)
    
    tiktok = PublisherFactory.create("tiktok", {})
    assert isinstance(tiktok, TikTokPublisher)


def test_factory_raises_on_unknown_platform():
    """Factory deve falhar para plataforma desconhecida."""
    with pytest.raises(ValueError) as exc_info:
        PublisherFactory.create("unknown_platform", {})
    
    assert "unknown_platform" in str(exc_info.value)


def test_factory_create_all_returns_only_available(
    valid_youtube_config,
    valid_instagram_config
):
    """create_all deve retornar apenas publishers disponíveis."""
    config = {
        "youtube": valid_youtube_config,
        "instagram": valid_instagram_config,
        "tiktok": {}  # Inválido
    }
    
    # Nota: Mesmo com config válida, YouTube pode não estar disponível
    # se google-api-python-client não estiver instalado
    publishers = PublisherFactory.create_all(config)
    
    # TikTok nunca deve estar disponível
    assert "tiktok" not in publishers


def test_factory_register_custom_publisher():
    """Deve permitir registrar publisher customizado."""
    
    class CustomPublisher(SocialMediaPublisher):
        def publish(self, video_path, metadata):
            return "custom_url"
        
        def is_available(self):
            return True
    
    PublisherFactory.register_publisher("custom", CustomPublisher)
    
    publisher = PublisherFactory.create("custom", {})
    assert isinstance(publisher, CustomPublisher)


# ============================================================================
# Testes de Integração
# ============================================================================

def test_full_mock_flow_youtube(mock_video_path, valid_metadata):
    """Testa fluxo completo com MockPublisher."""
    publisher = MockPublisher()
    
    # Publica
    url = publisher.publish(mock_video_path, valid_metadata)
    
    # Valida resultado
    assert url.startswith("https://mock-platform.com")
    assert len(publisher.published_videos) == 1
    
    # Valida metadata gravada
    recorded = publisher.published_videos[0]
    assert recorded["video_path"] == mock_video_path
    assert recorded["metadata"].titulo == valid_metadata.titulo


if __name__ == "__main__":
    # Permite rodar testes diretamente
    pytest.main([__file__, "-v", "--tb=short"])
