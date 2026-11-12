
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class TasaCambioResponse(BaseModel):
    id: int
    moneda_id: int
    moneda_base: str
    tasa: Decimal
    fecha: datetime

    model_config = ConfigDict(from_attributes=True)
