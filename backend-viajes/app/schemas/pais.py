
from pydantic import BaseModel, ConfigDict, Field


class PaisBase(BaseModel):
    nombre: str = Field(min_length=2, max_length=100)
    codigo: str = Field(min_length=2, max_length=2)
    moneda_id: int = Field(gt=0)


class PaisCreate(PaisBase):
    pass


class PaisResponse(PaisBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
