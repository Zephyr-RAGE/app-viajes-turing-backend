
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.ciudad import Ciudad


class CiudadRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, ciudad_id: int) -> Ciudad | None:
        statement = select(Ciudad).where(
            Ciudad.id == ciudad_id
        )
        return self.db.scalar(statement)

    def get_by_country(self, pais_id: int) -> list[Ciudad]:
        statement = (
            select(Ciudad)
            .where(Ciudad.pais_id == pais_id)
            .order_by(Ciudad.nombre)
        )
        return list(self.db.scalars(statement).all())

    def get_all(self) -> list[Ciudad]:
        statement = select(Ciudad).order_by(Ciudad.nombre)
        return list(self.db.scalars(statement).all())

    def create(self, ciudad: Ciudad) -> Ciudad:
        self.db.add(ciudad)
        self.db.flush()
        self.db.refresh(ciudad)
        return ciudad
