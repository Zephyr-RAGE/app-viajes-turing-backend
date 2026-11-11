
from pydantic import BaseModel, EmailStr, Field


class LoginRequest(BaseModel):
    correo: EmailStr
    password: str = Field(min_length=8, max_length=128)


class RefreshRequest(BaseModel):
    refresh_token: str = Field(min_length=64, max_length=64)


class TokenData(BaseModel):
    access_token: str
    refresh_token: str
    expires_in: int = 900


class TokenResponse(BaseModel):
    success: bool = True
    data: TokenData


class LogoutRequest(BaseModel):
    refresh_token: str = Field(min_length=64, max_length=64)