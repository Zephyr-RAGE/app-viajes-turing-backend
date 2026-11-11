
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.token import decode_access_token
from app.database.session import get_db
from app.models.usuario import Usuario
from app.repositories.token_repository import TokenRepository
from app.repositories.usuario_repository import UsuarioRepository


bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> Usuario:

    unauthorized = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={
            "code": "INVALID_ACCESS_TOKEN",
            "message": "Token de acceso inválido o expirado",
        },
        headers={"WWW-Authenticate": "Bearer"},
    )

    if credentials is None or credentials.scheme.lower() != "bearer":
        raise unauthorized

    try:
        payload = decode_access_token(credentials.credentials)

        usuario_id = int(payload["sub"])
        jti = payload["jti"]

        if not isinstance(jti, str) or not jti:
            raise ValueError("JTI inválido")

    except (ValueError, KeyError, TypeError):
        raise unauthorized

    token_repository = TokenRepository(db)

    if token_repository.is_access_token_revoked(jti):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "code": "REVOKED_ACCESS_TOKEN",
                "message": "El token de acceso ha sido revocado",
            },
            headers={"WWW-Authenticate": "Bearer"},
        )

    usuario_repository = UsuarioRepository(db)
    usuario = usuario_repository.get_by_id(usuario_id)

    if usuario is None:
        raise unauthorized

    return usuario
