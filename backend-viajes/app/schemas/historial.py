
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class HistorialCreate(BaseModel):

    ciudad_id: int = Field(gt=0)

    presupuesto_cop: Decimal = Field(
        gt=0,
        max_digits=15,
        decimal_places=2,
    )


class HistorialResponse(BaseModel):

    id: int
    usuario_id: int
    ciudad_id: int
    presupuesto_cop: Decimal
    clima: str
    tasa: Decimal
    valor_convertido: Decimal
    fecha: datetime

    model_config = ConfigDict(from_attributes=True)
