
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.usuario import Usuario


class UsuarioRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, usuario_id: int) -> Usuario | None:
        statement = select(Usuario).where(
            Usuario.id == usuario_id
        )

        return self.db.scalar(statement)

    def get_by_email(self, correo: str) -> Usuario | None:
        statement = select(Usuario).where(
            Usuario.correo == correo
        )

        return self.db.scalar(statement)

    def create(self, usuario: Usuario) -> Usuario:
        self.db.add(usuario)
        self.db.flush()
        self.db.refresh(usuario)

        return usuario
