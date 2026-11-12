
from decimal import Decimal, InvalidOperation

import httpx
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.tasa_cambio import TasaCambio
from app.repositories.moneda_repository import MonedaRepository
from app.repositories.tasa_cambio_repository import TasaCambioRepository


class TasaCambioService:

    API_URL = "https://v6.exchangerate-api.com/v6/latest/COP"

    def __init__(self, db: Session):
        self.db = db
        self.moneda_repository = MonedaRepository(db)
        self.tasa_repository = TasaCambioRepository(db)

    def obtener_tasa(self, moneda_id: int) -> TasaCambio:

        moneda = self.moneda_repository.get_by_id(moneda_id)

        if moneda is None:
            raise ValueError("CURRENCY_NOT_FOUND")

        try:
            response = httpx.get(
                self.API_URL,
                headers={
                    "Authorization": f"Bearer {settings.EXCHANGE_RATE_API_KEY}"
                },
                timeout=10.0,
            )

            response.raise_for_status()

            data = response.json()

            if data.get("result") != "success":
                raise ValueError("EXTERNAL_API_ERROR")

            if data.get("base_code") != "COP":
                raise ValueError("EXTERNAL_API_ERROR")

            rates = data.get("conversion_rates", {})
            tasa_recibida = rates.get(moneda.codigo)

            if tasa_recibida is None:
                raise ValueError("EXTERNAL_API_ERROR")

            try:
                tasa_decimal = Decimal(str(tasa_recibida))
            except (InvalidOperation, ValueError):
                raise ValueError("EXTERNAL_API_ERROR")

            if not tasa_decimal.is_finite() or tasa_decimal <= 0:
                raise ValueError("EXTERNAL_API_ERROR")

        except httpx.TimeoutException:
            raise ValueError("EXTERNAL_API_TIMEOUT")

        except httpx.HTTPError:
            raise ValueError("EXTERNAL_API_ERROR")

        except (ValueError, TypeError):
            raise ValueError("EXTERNAL_API_ERROR")

        try:
            nueva_tasa = TasaCambio(
                moneda_id=moneda.id,
                moneda_base="COP",
                tasa=tasa_decimal,
            )

            self.tasa_repository.create(nueva_tasa)

            self.db.commit()
            self.db.refresh(nueva_tasa)

            return nueva_tasa

        except Exception:
            self.db.rollback()
            raise
