from pydantic import BaseModel
from typing import Optional


class LoginRequest(BaseModel):
    username: str   # nombre de usuario (campo 'nombre' en la tabla)
    password: str   # contraseña en texto plano


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int         # segundos
    user: dict              # info básica del usuario autenticado


class AuthUser(BaseModel):
    id_usuario: Optional[int] = None
    nombre: str
    rol: str                # nombre_rol directamente
    estado: int = 1

    class Config:
        from_attributes = True
