from sqlalchemy.orm import Session

from app.repositories.pais_repository import PaisRepository
from app.models.pais import Pais


class PaisService:

    def __init__(self, db: Session):
        self.repository = PaisRepository(db)

    def get_all(self) -> list[Pais]:
        return self.repository.get_all()