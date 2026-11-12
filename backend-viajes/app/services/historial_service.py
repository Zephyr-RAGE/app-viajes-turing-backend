
from datetime import datetime, timezone
from decimal import Decimal, ROUND_HALF_UP

from sqlalchemy.orm import Session

from app.models.historial import Historial
from app.repositories.historial_repository import HistorialRepository
from app.repositories.ciudad_repository import CiudadRepository
from app.schemas.historial import HistorialCreate
from app.services.tasa_cambio_service import TasaCambioService
from app.services.clima_service import ClimaService


class HistorialService:

    def __init__(self, db: Session):
        self.db = db
        self.repository = HistorialRepository(db)
        self.ciudad_repository = CiudadRepository(db)
        self.tasa_service = TasaCambioService(db)
        self.clima_service = ClimaService(db)

    def create(
        self,
        data: HistorialCreate,
        usuario_id: int,
    ) -> Historial:

        ciudad = self.ciudad_repository.get_by_id(data.ciudad_id)

        if ciudad is None:
            raise ValueError("CITY_NOT_FOUND")

        if ciudad.pais is None or ciudad.pais.moneda is None:
            raise ValueError("CURRENCY_NOT_FOUND")

        try:
            tasa = self.tasa_service.obtener_tasa(
                ciudad.pais.moneda_id
            )

            clima = self.clima_service.obtener_clima(
                ciudad.id
            )

            valor_convertido = (
                data.presupuesto_cop * tasa.tasa
            ).quantize(
                Decimal("0.01"),
                rounding=ROUND_HALF_UP,
            )

            historial = Historial(
                usuario_id=usuario_id,
                ciudad_id=ciudad.id,
                presupuesto_cop=data.presupuesto_cop,
                clima=f"{clima['descripcion']}, {clima['temperatura']} °C",
                tasa=tasa.tasa,
                valor_convertido=valor_convertido,
                fecha=datetime.now(timezone.utc),
            )

            self.repository.create(historial)

            self.db.commit()
            self.db.refresh(historial)

            return historial

        except Exception:
            self.db.rollback()
            raise

    def get_by_user(self, usuario_id: int) -> list[Historial]:
        return self.repository.get_by_user(usuario_id)

    def get_by_id(
        self,
        historial_id: int,
        usuario_id: int,
    ) -> Historial | None:
        return self.repository.get_by_id(
            historial_id,
            usuario_id,
        )

    def delete(
    self,
    historial_id: int,
    usuario_id: int,
    ) -> bool:

        historial = self.repository.get_by_id(
            historial_id,
            usuario_id,
    )
        if historial is None:
            return False
        try:
            self.repository.delete(historial)
            self.db.commit()
            return True
        
        except Exception:
            self.db.rollback()
            raise

    
    def update(
        self,
        historial_id: int,
        data: HistorialCreate,
        usuario_id: int,
    ) -> Historial | None:

        historial = self.repository.get_by_id(
            historial_id,
            usuario_id,
        )

        if historial is None:
            return None

        ciudad = self.ciudad_repository.get_by_id(data.ciudad_id)

        if ciudad is None:
            raise ValueError("CITY_NOT_FOUND")

        if ciudad.pais is None or ciudad.pais.moneda is None:
            raise ValueError("CURRENCY_NOT_FOUND")

        try:
            tasa = self.tasa_service.obtener_tasa(
                ciudad.pais.moneda_id
            )

            clima = self.clima_service.obtener_clima(ciudad.id)

            valor_convertido = (
                data.presupuesto_cop * tasa.tasa
            ).quantize(
                Decimal("0.01"),
                rounding=ROUND_HALF_UP,
            )

            historial.ciudad_id = ciudad.id
            historial.presupuesto_cop = data.presupuesto_cop
            historial.clima = (
                f"{clima['descripcion']}, "
                f"{clima['temperatura']} °C"
            )
            historial.tasa = tasa.tasa
            historial.valor_convertido = valor_convertido
            historial.fecha = datetime.now(timezone.utc)

            self.db.commit()
            self.db.refresh(historial)

            return historial

        except Exception:
            self.db.rollback()
            raise
       


