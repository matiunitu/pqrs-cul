from pydantic import BaseModel
from typing import Optional


class Prioridad(BaseModel):
    id_prioridad: Optional[int] = None
    nombre_prioridad: Optional[str] = None
    nivel: Optional[int] = None

    class Config:
        from_attributes = True
