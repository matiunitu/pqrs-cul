from pydantic import BaseModel
from typing import Optional


class Facultad(BaseModel):
    id_facultad: Optional[int] = None
    nombre_facultad: Optional[str] = None
    descripcion: Optional[str] = None

    class Config:
        from_attributes = True
