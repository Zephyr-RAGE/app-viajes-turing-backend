
import hashlib
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.refresh_token import RefreshToken
from app.models.token_revocado import TokenRevocado


class TokenRepository:

    def __init__(self, db: Session):
        self.db = db

    @staticmethod
    def hash_token(token: str) -> str:
        return hashlib.sha256(token.encode("utf-8")).hexdigest()

    def create_refresh_token(
        self,
        usuario_id: int,
        token: str,
        expires_at: datetime,
    ) -> RefreshToken:

        refresh_token = RefreshToken(
            usuario_id=usuario_id,
            token_hash=self.hash_token(token),
            expires_at=expires_at,
        )

        self.db.add(refresh_token)
        self.db.flush()
        self.db.refresh(refresh_token)

        return refresh_token

    def get_refresh_token(self, token: str) -> RefreshToken | None:
        token_hash = self.hash_token(token)

        statement = select(RefreshToken).where(
            RefreshToken.token_hash == token_hash
        )

        return self.db.scalar(statement)

    def revoke_refresh_token(self, token: str) -> bool:
        refresh_token = self.get_refresh_token(token)

        if refresh_token is None or refresh_token.revoked_at is not None:
            return False

        refresh_token.revoked_at = datetime.now(timezone.utc)
        self.db.flush()

        return True

    def revoke_access_token(self, jti: str) -> None:
        existing = self.db.get(TokenRevocado, jti)

        if existing is not None:
            return

        revoked_token = TokenRevocado(
            jti=jti,
            revoked_at=datetime.now(timezone.utc),
        )

        self.db.add(revoked_token)
        self.db.flush()

    def is_access_token_revoked(self, jti: str) -> bool:
        statement = select(TokenRevocado).where(
            TokenRevocado.jti == jti
        )

        return self.db.scalar(statement) is not None
