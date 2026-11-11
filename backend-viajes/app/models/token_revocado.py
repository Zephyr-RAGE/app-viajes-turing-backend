
from datetime import datetime, timezone

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.connection import Base


class TokenRevocado(Base):

    __tablename__ = "tokens_revocados"

    jti: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
    )

    revoked_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )
