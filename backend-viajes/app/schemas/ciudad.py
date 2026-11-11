
from pydantic import BaseModel, ConfigDict, Field


class CiudadBase(BaseModel):
    pais_id: int = Field(gt=0)
    nombre: str = Field(min_length=2, max_length=150)
    latitud: float | None = Field(default=None, ge=-90, le=90)
    longitud: float | None = Field(default=None, ge=-180, le=180)


class CiudadCreate(CiudadBase):
    pass


class CiudadResponse(CiudadBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
