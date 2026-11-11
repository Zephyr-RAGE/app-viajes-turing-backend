
from pydantic import BaseModel, ConfigDict, Field


class MonedaBase(BaseModel):
    codigo: str = Field(min_length=3, max_length=3)
    nombre: str = Field(min_length=2, max_length=100)
    simbolo: str = Field(min_length=1, max_length=10)


class MonedaCreate(MonedaBase):
    pass


class MonedaResponse(MonedaBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
