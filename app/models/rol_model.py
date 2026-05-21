from pydantic import BaseModel
from typing import Optional


class Rol(BaseModel):
    id_rol: Optional[int] = None
    nombre_rol: Optional[str] = None
    descripcion: Optional[str] = None

    class Config:
        from_attributes = True

