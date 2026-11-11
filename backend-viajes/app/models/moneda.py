from sqlalchemy import BigInteger, Identity, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from sqlalchemy import UniqueConstraint

from app.database.connection import Base


class Moneda(Base):

    __tablename__ = "monedas"

    __table_args__ = (
    UniqueConstraint("codigo", name="uq_monedas_codigo"),
)

    id: Mapped[int] = mapped_column(
        BigInteger,
        Identity(always=False),
        primary_key=True
    )

    codigo: Mapped[str] = mapped_column(
    String(3),
    nullable=False
)

    nombre: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    simbolo: Mapped[str] = mapped_column(
        String(10),
        nullable=False
    )

    paises: Mapped[list["Pais"]] = relationship(
        back_populates="moneda"
    )