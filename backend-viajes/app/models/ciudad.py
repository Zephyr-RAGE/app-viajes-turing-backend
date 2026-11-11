from sqlalchemy import BigInteger, ForeignKey, Identity, String, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.connection import Base


class Ciudad(Base):

    __tablename__ = "ciudades"

    id: Mapped[int] = mapped_column(
        BigInteger,
        Identity(always=False),
        primary_key=True
    )

    pais_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("paises.id"),
        nullable=False
    )

    nombre: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    latitud: Mapped[float | None] = mapped_column(
        Float,
        nullable=True
    )

    longitud: Mapped[float | None] = mapped_column(
        Float,
        nullable=True
    )

    pais: Mapped["Pais"] = relationship(
        back_populates="ciudades"
    )

    historiales: Mapped[list["Historial"]] = relationship(
        back_populates="ciudad"
    )