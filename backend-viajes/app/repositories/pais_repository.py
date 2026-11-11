
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.pais import Pais


class PaisRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, pais_id: int) -> Pais | None:
        statement = select(Pais).where(
            Pais.id == pais_id
        )
        return self.db.scalar(statement)

    def get_all(self) -> list[Pais]:
        statement = select(Pais).order_by(Pais.nombre)
        return list(self.db.scalars(statement).all())

    def create(self, pais: Pais) -> Pais:
        self.db.add(pais)
        self.db.flush()
        self.db.refresh(pais)
        return pais
