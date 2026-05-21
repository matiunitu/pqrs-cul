from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class HistorialEstados(BaseModel):
    id_historial: Optional[int] = None
    fecha_cambio: Optional[datetime] = None
    id_pqrs: Optional[int] = None
    id_estado_anterior: Optional[int] = None
    id_estado_nuevo: Optional[int] = None
    cambiado_por: Optional[int] = None

    class Config:
        from_attributes = True
