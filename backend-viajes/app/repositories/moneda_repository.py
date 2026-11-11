
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.moneda import Moneda


class MonedaRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, moneda_id: int) -> Moneda | None:
        statement = select(Moneda).where(
            Moneda.id == moneda_id
        )
        return self.db.scalar(statement)

    def get_all(self) -> list[Moneda]:
        statement = select(Moneda).order_by(Moneda.nombre)
        return list(self.db.scalars(statement).all())

    def create(self, moneda: Moneda) -> Moneda:
        self.db.add(moneda)
        self.db.flush()
        self.db.refresh(moneda)
        return moneda
