
import secrets
from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session

from app.core.security import verify_password
from app.core.token import create_access_token, decode_access_token
from app.repositories.usuario_repository import UsuarioRepository
from app.repositories.token_repository import TokenRepository
from app.schemas.auth import TokenData



class AuthService:

    def __init__(self, db: Session):
        self.db = db
        self.usuario_repository = UsuarioRepository(db)
        self.token_repository = TokenRepository(db)

    def login(self, correo: str, password: str) -> TokenData:

        usuario = self.usuario_repository.get_by_email(correo)

        if usuario is None or not verify_password(
            password,
            usuario.password_hash,
        ):
            raise ValueError("INVALID_CREDENTIALS")

        access_token = create_access_token(
            usuario_id=usuario.id,
            idioma=usuario.idioma,
        )

        refresh_token = secrets.token_hex(32)

        expires_at = datetime.now(timezone.utc) + timedelta(days=7)

        try:
            self.token_repository.create_refresh_token(
                usuario_id=usuario.id,
                token=refresh_token,
                expires_at=expires_at,
            )

            self.db.commit()

        except Exception:
            self.db.rollback()
            raise

        return TokenData(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=900,
        )

    
    def refresh(self, token: str) -> TokenData:

        refresh_token = self.token_repository.get_refresh_token(token)

        if refresh_token is None:
            raise ValueError("INVALID_REFRESH_TOKEN")

        if refresh_token.revoked_at is not None:
            raise ValueError("REVOKED_REFRESH_TOKEN")

        now = datetime.now(timezone.utc)

        if refresh_token.expires_at <= now:
            raise ValueError("EXPIRED_REFRESH_TOKEN")

        usuario = self.usuario_repository.get_by_id(
            refresh_token.usuario_id
        )

        if usuario is None:
            raise ValueError("INVALID_REFRESH_TOKEN")

        new_access_token = create_access_token(
            usuario_id=usuario.id,
            idioma=usuario.idioma,
        )

        new_refresh_token = secrets.token_hex(32)

        new_expires_at = now + timedelta(days=7)

        try:
            self.token_repository.revoke_refresh_token(token)

            self.token_repository.create_refresh_token(
                usuario_id=usuario.id,
                token=new_refresh_token,
                expires_at=new_expires_at,
            )

            self.db.commit()

        except Exception:
            self.db.rollback()
            raise

        return TokenData(
            access_token=new_access_token,
            refresh_token=new_refresh_token,
            expires_in=900,
        )

    def logout(
    self,
    usuario_id: int,
    access_token: str,
    refresh_token: str,
    ) -> None:

        # Validar el access token
        try:
            payload = decode_access_token(access_token)

            token_usuario_id = int(payload["sub"])
            jti = payload["jti"]

            if token_usuario_id != usuario_id:
                raise ValueError("INVALID_ACCESS_TOKEN")

            if not isinstance(jti, str) or not jti:
                raise ValueError("INVALID_ACCESS_TOKEN")

        except (ValueError, KeyError, TypeError):
            raise ValueError("INVALID_ACCESS_TOKEN")

        # Buscar el refresh token en la base de datos
        stored_refresh_token = self.token_repository.get_refresh_token(
            refresh_token
        )

        if stored_refresh_token is None:
            raise ValueError("INVALID_REFRESH_TOKEN")

        if stored_refresh_token.usuario_id != usuario_id:
            raise ValueError("INVALID_REFRESH_TOKEN")

        if stored_refresh_token.revoked_at is not None:
            raise ValueError("REVOKED_REFRESH_TOKEN")

        if stored_refresh_token.expires_at <= datetime.now(timezone.utc):
            raise ValueError("EXPIRED_REFRESH_TOKEN")

        # Revocar ambos tokens
        try:
            self.token_repository.revoke_access_token(jti)

            revoked = self.token_repository.revoke_refresh_token(
                refresh_token
            )

            if not revoked:
                raise ValueError("REVOKED_REFRESH_TOKEN")

            self.db.commit()

        except Exception:
            self.db.rollback()
            raise

