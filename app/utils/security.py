from fastapi import Header, HTTPException, status
from app.config import settings


def verify_token(authorization: str = Header(..., description="Bearer <token>")):
    """
    Valida o token Bearer fixo no header Authorization.
    Lança 401 se ausente ou inválido.
    """
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Formato inválido. Use: Authorization: Bearer <token>",
        )
    token = authorization.removeprefix("Bearer ").strip()
    if not settings.AUTH_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="AUTH_TOKEN não configurado no servidor",
        )
    if token != settings.AUTH_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado",
        )
