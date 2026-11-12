from sqlalchemy.orm import Session

from app.models.ciudad import Ciudad
from app.repositories.ciudad_repository import CiudadRepository


class CiudadService:

    def __init__(self, db: Session):
        self.repository = CiudadRepository(db)

    def get_all(self) -> list[Ciudad]:
        return self.repository.get_all()

    def get_by_country(self, pais_id: int) -> list[Ciudad]:
        return self.repository.get_by_country(pais_id)