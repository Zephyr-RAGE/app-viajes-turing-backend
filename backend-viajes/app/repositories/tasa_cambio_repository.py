
from sqlalchemy import select, desc
from sqlalchemy.orm import Session

from app.models.tasa_cambio import TasaCambio


class TasaCambioRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_latest_by_moneda(
        self,
        moneda_id: int
    ) -> TasaCambio | None:

        statement = (
            select(TasaCambio)
            .where(TasaCambio.moneda_id == moneda_id)
            .order_by(desc(TasaCambio.fecha))
            .limit(1)
        )

        return self.db.scalar(statement)

    def create(self, tasa: TasaCambio) -> TasaCambio:
        self.db.add(tasa)
        self.db.flush()
        self.db.refresh(tasa)

        return tasa
