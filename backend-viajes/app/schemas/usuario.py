
from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    model_validator,
)


class UsuarioBase(BaseModel):
    nombre: str = Field(min_length=2, max_length=100)
    correo: EmailStr
    idioma: str = Field(default="es", min_length=2, max_length=5)


class UsuarioCreate(UsuarioBase):
    password: str = Field(min_length=8, max_length=128)
    password_confirmation: str = Field(
        min_length=8,
        max_length=128,
    )

    
class UsuarioCreate(UsuarioBase):
    password: str = Field(min_length=8, max_length=128)
    password_confirmation: str = Field(
        min_length=8,
        max_length=128,
    )

    @model_validator(mode="after")
    def validate_password(self):
        password = self.password

        if not any(char.islower() for char in password):
            raise ValueError("La contraseña debe contener una minúscula")

        if not any(char.isupper() for char in password):
            raise ValueError("La contraseña debe contener una mayúscula")

        if not any(char.isdigit() for char in password):
            raise ValueError("La contraseña debe contener un número")

        if self.password != self.password_confirmation:
            raise ValueError("Las contraseñas no coinciden")

        return self



class UsuarioResponse(UsuarioBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
