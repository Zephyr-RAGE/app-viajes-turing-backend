from pydantic import BaseModel


class ClimaResponse(BaseModel):
    ciudad_id: int
    ciudad: str
    temperatura: float
    unidad: str
    descripcion: str