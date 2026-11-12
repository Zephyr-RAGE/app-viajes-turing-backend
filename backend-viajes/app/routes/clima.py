
from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.database.session import get_db
from app.models.usuario import Usuario
from app.schemas.clima import ClimaResponse
from app.services.clima_service import ClimaService


router = APIRouter(
    prefix="/clima",
    tags=["Clima"],
)


@router.get(
    "/{ciudad_id}",
    response_model=ClimaResponse,
    status_code=status.HTTP_200_OK,
)
def obtener_clima(
    ciudad_id: int = Path(gt=0),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    service = ClimaService(db)

    try:
        return service.obtener_clima(ciudad_id)

    except ValueError as error:
        error_code = str(error)

        errors = {
            "CITY_NOT_FOUND": (
                status.HTTP_404_NOT_FOUND,
                "La ciudad solicitada no existe",
            ),
            "CITY_COORDINATES_NOT_FOUND": (
                status.HTTP_422_UNPROCESSABLE_ENTITY,
                "La ciudad no tiene coordenadas registradas",
            ),
            "EXTERNAL_API_ERROR": (
                status.HTTP_502_BAD_GATEWAY,
                "No fue posible obtener información del clima",
            ),
            "EXTERNAL_API_TIMEOUT": (
                status.HTTP_504_GATEWAY_TIMEOUT,
                "El servicio del clima tardó demasiado en responder",
            ),
        }

        if error_code in errors:
            status_code, message = errors[error_code]

            raise HTTPException(
                status_code=status_code,
                detail={
                    "code": error_code,
                    "message": message,
                },
            )

        raise
