from pydantic import BaseModel
from typing import Optional


class Dependencia(BaseModel):
    id_dependencia: Optional[int] = None
    nombre_dependencia: Optional[str] = None
    descripcion: Optional[str] = None

    class Config:
        from_attributes = True

