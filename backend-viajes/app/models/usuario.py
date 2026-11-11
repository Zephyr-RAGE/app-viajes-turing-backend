from datetime import datetime, timezone

from sqlalchemy import BigInteger, Identity, String, DateTime, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.connection import Base


class Usuario(Base):

    __tablename__ = "usuarios"

    __table_args__ = (
    UniqueConstraint("correo", name="uq_usuarios_correo"),
)

    id: Mapped[int] = mapped_column(
        BigInteger,
        Identity(always=False),
        primary_key=True
    )

    nombre: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    correo: Mapped[str] = mapped_column(
    String(150),
    nullable=False
)

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    idioma: Mapped[str] = mapped_column(
        String(5),
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
    DateTime(timezone=True),
    nullable=False,
    default=lambda: datetime.now(timezone.utc)
    )   

    updated_at: Mapped[datetime] = mapped_column(
    DateTime(timezone=True),
    nullable=False,
    default=lambda: datetime.now(timezone.utc),
    onupdate=lambda: datetime.now(timezone.utc)
    )

    historiales: Mapped[list["Historial"]] = relationship(
        back_populates="usuario"
    )