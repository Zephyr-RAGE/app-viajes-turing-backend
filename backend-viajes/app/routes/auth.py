
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.usuario import UsuarioCreate, UsuarioResponse
from app.schemas.auth import LoginRequest, TokenResponse
from app.services.usuario_service import UsuarioService
from app.services.auth_service import AuthService
from app.schemas.auth import LoginRequest, TokenResponse, RefreshRequest
from app.schemas.auth import LogoutRequest

from app.core.dependencies import get_current_user
from app.models.usuario import Usuario

from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer




router = APIRouter(prefix="/auth", tags=["Autenticación"])

bearer_scheme = HTTPBearer()


@router.post(
    "/register",
    response_model=UsuarioResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(data: UsuarioCreate, db: Session = Depends(get_db)):
    service = UsuarioService(db)

    try:
        return service.register(data)

    except ValueError as error:
        if str(error) == "USER_ALREADY_EXISTS":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={
                    "code": "USER_ALREADY_EXISTS",
                    "message": "El correo electrónico ya está registrado",
                },
            )
        raise


@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    service = AuthService(db)

    try:
        token_data = service.login(
            correo=data.correo,
            password=data.password,
        )

        return TokenResponse(data=token_data)

    except ValueError as error:
        if str(error) == "INVALID_CREDENTIALS":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "code": "INVALID_CREDENTIALS",
                    "message": "Correo o contraseña inválidos",
                },
            )
        raise


@router.post(
    "/refresh",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
)
def refresh(data: RefreshRequest, db: Session = Depends(get_db)):
    service = AuthService(db)

    try:
        token_data = service.refresh(data.refresh_token)

        return TokenResponse(data=token_data)

    except ValueError as error:
        error_code = str(error)

        messages = {
            "INVALID_REFRESH_TOKEN": "Refresh token inválido",
            "REVOKED_REFRESH_TOKEN": "Refresh token revocado",
            "EXPIRED_REFRESH_TOKEN": "Refresh token expirado",
        }

        if error_code in messages:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "code": error_code,
                    "message": messages[error_code],
                },
            )

        raise


@router.get("/me", response_model=UsuarioResponse)
def get_me(
    current_user: Usuario = Depends(get_current_user),
):
    return current_user


@router.post("/logout", status_code=status.HTTP_200_OK)
def logout(
    data: LogoutRequest,
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    current_user: Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    service = AuthService(db)

    try:
        service.logout(
            usuario_id=current_user.id,
            access_token=credentials.credentials,
            refresh_token=data.refresh_token,
        )

        return {
            "success": True,
            "message": "Sesión cerrada correctamente",
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
        )