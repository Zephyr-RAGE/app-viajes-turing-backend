from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    BigInteger,
    DateTime,
    ForeignKey,
    Identity,
    Numeric,
    String
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.connection import Base


class Historial(Base):

    __tablename__ = "historial"

    id: Mapped[int] = mapped_column(
        BigInteger,
        Identity(always=False),
        primary_key=True
    )

    usuario_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("usuarios.id"),
        nullable=False
    )

    ciudad_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("ciudades.id"),
        nullable=False
    )

    presupuesto_cop: Mapped[Decimal] = mapped_column(
        Numeric(15, 2),
        nullable=False
    )

    clima: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    tasa: Mapped[Decimal] = mapped_column(
        Numeric(18, 8),
        nullable=False
    )

    valor_convertido: Mapped[Decimal] = mapped_column(
        Numeric(15, 2),
        nullable=False
    )

    fecha: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )

    usuario: Mapped["Usuario"] = relationship(
        back_populates="historiales"
    )

    ciudad: Mapped["Ciudad"] = relationship(
        back_populates="historiales"
    )