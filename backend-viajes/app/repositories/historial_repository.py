
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.historial import Historial


class HistorialRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(
        self,
        historial_id: int,
        usuario_id: int
    ) -> Historial | None:

        statement = select(Historial).where(
            Historial.id == historial_id,
            Historial.usuario_id == usuario_id
        )

        return self.db.scalar(statement)

    def get_by_user(self, usuario_id: int) -> list[Historial]:
        statement = (
            select(Historial)
            .where(Historial.usuario_id == usuario_id)
            .order_by(Historial.fecha.desc())
        )

        return list(self.db.scalars(statement).all())

    def create(self, historial: Historial) -> Historial:
        self.db.add(historial)
        self.db.flush()
        self.db.refresh(historial)
        return historial
