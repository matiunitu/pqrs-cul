from pydantic import BaseModel
from typing import Optional


class Programa(BaseModel):
    id_programa: Optional[int] = None
    nombre_programa: Optional[str] = None
    descripcion: Optional[str] = None
    id_facultad: Optional[int] = None

    class Config:
        from_attributes = True
