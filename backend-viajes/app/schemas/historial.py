
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class HistorialBase(BaseModel):
    ciudad_id: int = Field(gt=0)
    presupuesto_cop: Decimal = Field(gt=0, max_digits=15, decimal_places=2)
    clima: str = Field(min_length=1, max_length=255)
    tasa: Decimal = Field(gt=0, max_digits=18, decimal_places=8)
    valor_convertido: Decimal = Field(gt=0, max_digits=15, decimal_places=2)


class HistorialCreate(HistorialBase):
    pass


class HistorialResponse(HistorialBase):
    id: int
    usuario_id: int
    fecha: datetime

    model_config = ConfigDict(from_attributes=True)
