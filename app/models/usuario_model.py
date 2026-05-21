from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class Usuario(BaseModel):
    id_usuario: Optional[int] = None
    nombre: str
    tipo_documento: str = 'CC'
    documento: str
    correo: str
    telefono: str
    id_rol: int
    id_programa: Optional[int] = 1
    activo: bool = True
    estado: Optional[int] = 1
    password_hash: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    tipo_documento: Optional[str] = None
    documento: Optional[str] = None
    correo: Optional[str] = None
    telefono: Optional[str] = None
    id_rol: Optional[int] = None
    id_programa: Optional[int] = None
    activo: Optional[bool] = None
    estado: Optional[int] = None
    password_hash: Optional[str] = None

