from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Respuesta(BaseModel):
    id_respuesta: Optional[int] = None
    mensaje: Optional[str] = None
    fecha_respuesta: Optional[datetime] = None
    id_pqrs: Optional[int] = None
    id_usuario: Optional[int] = None

    class Config:
        from_attributes = True
