
from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.database.session import get_db
from app.models.usuario import Usuario
from app.schemas.tasa_cambio import TasaCambioResponse
from app.services.tasa_cambio_service import TasaCambioService


router = APIRouter(
    prefix="/tasas-cambio",
    tags=["Tasas de cambio"],
)


@router.get(
    "/{moneda_id}",
    response_model=TasaCambioResponse,
    status_code=status.HTTP_200_OK,
)
def obtener_tasa(
    moneda_id: int = Path(gt=0),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    service = TasaCambioService(db)

    try:
        return service.obtener_tasa(moneda_id)

    except ValueError as error:
        error_code = str(error)

        errors = {
            "CURRENCY_NOT_FOUND": (
                status.HTTP_404_NOT_FOUND,
                "La moneda solicitada no existe",
            ),
            "EXTERNAL_API_ERROR": (
                status.HTTP_502_BAD_GATEWAY,
                "No fue posible obtener una tasa válida del servicio externo",
            ),
            "EXTERNAL_API_TIMEOUT": (
                status.HTTP_504_GATEWAY_TIMEOUT,
                "El servicio externo tardó demasiado en responder",
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
