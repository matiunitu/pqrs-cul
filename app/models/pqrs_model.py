from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Pqrs(BaseModel):
    id_pqrs: Optional[int] = None
    radicado: Optional[str] = None
    descripcion: Optional[str] = None
    fecha_creacion: Optional[datetime] = None
    fecha_limite: Optional[datetime] = None
    id_usuario: Optional[int] = None
    id_dependencia: Optional[int] = None
    id_tipospqrs: Optional[int] = None
    id_estado: Optional[int] = None
    id_prioridad: Optional[int] = None

    class Config:
        from_attributes = True
