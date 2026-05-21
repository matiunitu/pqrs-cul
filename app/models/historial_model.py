from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class Historial(BaseModel):
    id_historial: Optional[int] = None
    id_usuario: Optional[int] = None
    accion: Optional[str] = None
    fecha: Optional[datetime] = None
    cambiado_por: Optional[str] = None

    class Config:
        from_attributes = True

