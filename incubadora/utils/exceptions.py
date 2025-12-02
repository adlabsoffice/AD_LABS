"""
Exceções customizadas para o sistema de fallback de APIs.
"""

class APIError(Exception):
    """Erro base para todas as APIs."""
    pass

class QuotaExceededError(APIError):
    """Quota da API foi excedida (429)."""
    pass

class TimeoutError(APIError):
    """Timeout na chamada da API."""
    pass

class InvalidResponseError(APIError):
    """Resposta da API inválida, vazia ou mal formatada."""
    pass

class AuthError(APIError):
    """Erro de autenticação (401/403)."""
    pass

class AllAPIsFailed(APIError):
    """Todas as APIs configuradas (e seus fallbacks) falharam."""
    pass
