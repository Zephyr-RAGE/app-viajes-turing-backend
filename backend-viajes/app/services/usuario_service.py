
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.models.usuario import Usuario
from app.repositories.usuario_repository import UsuarioRepository
from app.schemas.usuario import UsuarioCreate


class UsuarioService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = UsuarioRepository(db)

    def register(self, data: UsuarioCreate) -> Usuario:
        existing_user = self.repository.get_by_email(data.correo)

        if existing_user is not None:
            raise ValueError("USER_ALREADY_EXISTS")

        usuario = Usuario(
            nombre=data.nombre,
            correo=data.correo,
            password_hash=hash_password(data.password),
            idioma=data.idioma,
        )

        try:
            usuario = self.repository.create(usuario)
            self.db.commit()
            self.db.refresh(usuario)

            return usuario

        except Exception:
            self.db.rollback()
            raise
