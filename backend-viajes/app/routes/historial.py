
from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.database.session import get_db
from app.models.usuario import Usuario
from app.schemas.historial import HistorialCreate, HistorialResponse
from app.services.historial_service import HistorialService


router = APIRouter(
    prefix="/historial",
    tags=["Historial"],
)


@router.post(
    "/",
    response_model=HistorialResponse,
    status_code=status.HTTP_201_CREATED,
)
def crear_historial(
    data: HistorialCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    service = HistorialService(db)

    try:
        return service.create(
            data=data,
            usuario_id=current_user.id,
        )

    except ValueError as error:
        errores = {
            "CITY_NOT_FOUND": (404, "La ciudad no existe"),
            "CURRENCY_NOT_FOUND": (404, "No se encontró la moneda de destino"),
            "CITY_COORDINATES_NOT_FOUND": (422, "La ciudad no tiene coordenadas"),
            "EXTERNAL_API_ERROR": (502, "Error al consultar un servicio externo"),
            "EXTERNAL_API_TIMEOUT": (504, "Tiempo de espera agotado al consultar un servicio externo"),
        }

        codigo, mensaje = errores.get(
            str(error),
            (500, "Error interno al crear el historial"),
        )

        raise HTTPException(
            status_code=codigo,
            detail={
                "code": str(error),
                "message": mensaje,
            },
        )


@router.get(
    "/",
    response_model=list[HistorialResponse],
    status_code=status.HTTP_200_OK,
)
def obtener_historial(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    service = HistorialService(db)

    return service.get_by_user(current_user.id)


@router.get(
    "/{historial_id}",
    response_model=HistorialResponse,
    status_code=status.HTTP_200_OK,
)
def obtener_historial_por_id(
    historial_id: int = Path(gt=0),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    service = HistorialService(db)

    historial = service.get_by_id(
        historial_id=historial_id,
        usuario_id=current_user.id,
    )

    if historial is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "code": "HISTORY_NOT_FOUND",
                "message": "El registro no existe o no pertenece al usuario",
            },
        )

    return historial


@router.delete(
    "/{historial_id}",
    status_code=status.HTTP_200_OK,
)
def eliminar_historial(
    historial_id: int = Path(gt=0),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    service = HistorialService(db)

    eliminado = service.delete(
        historial_id=historial_id,
        usuario_id=current_user.id,
    )

    if not eliminado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "code": "HISTORY_NOT_FOUND",
                "message": "El registro no existe o no pertenece al usuario",
            },
        )

    return {
        "success": True,
        "message": "Historial eliminado correctamente",
    }


@router.put(
    "/{historial_id}",
    response_model=HistorialResponse,
    status_code=status.HTTP_200_OK,
)
def actualizar_historial(
    data: HistorialCreate,
    historial_id: int = Path(gt=0),
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    service = HistorialService(db)

    try:
        historial = service.update(
            historial_id=historial_id,
            data=data,
            usuario_id=current_user.id,
        )

        if historial is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "code": "HISTORY_NOT_FOUND",
                    "message": "El registro no existe o no pertenece al usuario",
                },
            )

        return historial

    except ValueError as error:
        errores = {
            "CITY_NOT_FOUND": (404, "La ciudad no existe"),
            "CURRENCY_NOT_FOUND": (404, "No se encontró la moneda de destino"),
            "CITY_COORDINATES_NOT_FOUND": (422, "La ciudad no tiene coordenadas"),
            "EXTERNAL_API_ERROR": (502, "Error al consultar un servicio externo"),
            "EXTERNAL_API_TIMEOUT": (504, "Tiempo de espera agotado al consultar un servicio externo"),
        }

        codigo, mensaje = errores.get(
            str(error),
            (500, "Error interno al actualizar el historial"),
        )

        raise HTTPException(
            status_code=codigo,
            detail={
                "code": str(error),
                "message": mensaje,
            },
        )




