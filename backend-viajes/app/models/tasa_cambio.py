
from datetime import datetime

from sqlalchemy import (
    BigInteger,
    DateTime,
    ForeignKey,
    Identity,
    Numeric,
    String,
    func
)
from sqlalchemy.orm import Mapped, mapped_column

from app.database.connection import Base


class TasaCambio(Base):

    __tablename__ = "tasas_cambio"

    id: Mapped[int] = mapped_column(
        BigInteger,
        Identity(always=False),
        primary_key=True
    )

    moneda_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("monedas.id"),
        nullable=False
    )

    moneda_base: Mapped[str] = mapped_column(
        String(3),
        nullable=False,
        default="COP"
    )

    tasa: Mapped[float] = mapped_column(
        Numeric(18, 8),
        nullable=False
    )

    fecha: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )
