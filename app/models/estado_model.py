from pydantic import BaseModel
from typing import Optional


class Estado(BaseModel):
    id_estado: Optional[int] = None
    nombre_estado: Optional[str] = None

    class Config:
        from_attributes = True
