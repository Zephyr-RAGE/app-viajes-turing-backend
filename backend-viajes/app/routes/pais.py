from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.services.pais_service import PaisService
from app.schemas.pais import PaisResponse


router = APIRouter(
    prefix="/catalogos/paises",
    tags=["Catálogos"]
)


@router.get("/", response_model=list[PaisResponse])
def get_paises(
    db: Session = Depends(get_db)
):
    service = PaisService(db)

    return service.get_all()