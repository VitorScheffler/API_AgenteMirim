import secrets
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.config import settings

bearer_scheme = HTTPBearer(auto_error=True)


def verify_token(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    """
    Valida o Bearer Token usando comparação segura (timing-safe).
    Registra IP do cliente em caso de token inválido.
    """
    token_valido = secrets.compare_digest(
        credentials.credentials.encode("utf-8"),
        settings.AUTH_TOKEN.encode("utf-8"),
    )
    if not token_valido:
        client_ip = request.client.host if request.client else "desconhecido"
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
