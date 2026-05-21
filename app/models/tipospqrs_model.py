from pydantic import BaseModel
from typing import Optional


class Tipospqrs(BaseModel):
    id_tipospqrs: Optional[int] = None
    nombre_tipospqrs: Optional[str] = None
    descripcion: Optional[str] = None

    class Config:
        from_attributes = True
