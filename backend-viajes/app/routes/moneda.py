from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.services.moneda_service import MonedaService
from app.schemas.moneda import MonedaResponse


router = APIRouter(
    prefix="/catalogos/monedas",
    tags=["Catálogos"]
)


@router.get("/", response_model=list[MonedaResponse])
def get_monedas(
    db: Session = Depends(get_db)
):
    service = MonedaService(db)

    return service.get_all()