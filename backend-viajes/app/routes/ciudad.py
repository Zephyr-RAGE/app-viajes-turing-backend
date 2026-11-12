from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.services.ciudad_service import CiudadService
from app.schemas.ciudad import CiudadResponse


router = APIRouter(
    prefix="/catalogos/ciudades",
    tags=["Catálogos"]
)


@router.get("/", response_model=list[CiudadResponse])
def get_ciudades(
    pais_id: int | None = Query(default=None, gt=0),
    db: Session = Depends(get_db)
):
    service = CiudadService(db)

    if pais_id is not None:
        return service.get_by_country(pais_id)

    return service.get_all()