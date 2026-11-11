from sqlalchemy import BigInteger, ForeignKey, Identity, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.connection import Base


class Pais(Base):

    __tablename__ = "paises"

    __table_args__ = (
    UniqueConstraint("codigo", name="uq_paises_codigo"),
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

    codigo: Mapped[str] = mapped_column(
    String(2),
    nullable=False
)

    moneda_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("monedas.id"),
        nullable=False
    )

    moneda: Mapped["Moneda"] = relationship(
        back_populates="paises"
    )

    ciudades: Mapped[list["Ciudad"]] = relationship(
        back_populates="pais"
    )