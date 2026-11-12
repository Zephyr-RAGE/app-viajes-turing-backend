from sqlalchemy.orm import Session

from app.models.moneda import Moneda
from app.repositories.moneda_repository import MonedaRepository


class MonedaService:

    def __init__(self, db: Session):
        self.repository = MonedaRepository(db)

    def get_all(self) -> list[Moneda]:
        return self.repository.get_all()