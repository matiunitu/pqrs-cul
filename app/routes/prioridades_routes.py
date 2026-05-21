from fastapi import APIRouter, Request
from controllers.prioridades_controller import PrioridadesController
from models.prioridad_model import Prioridad

router = APIRouter(prefix="/prioridades", tags=["prioridades"])
controller = PrioridadesController()

@router.post("/", summary="Crear prioridad")
async def create_prioridad(request: Request):
    data = await request.json()
    campos = ["nombre_prioridad", "nivel"]
    prioridad_data = {k: data[k] for k in campos if k in data}
    prioridad = Prioridad(**prioridad_data)
    return controller.create_prioridad(prioridad)

@router.get("/", summary="Listar prioridades")
async def get_prioridades():
    return controller.get_prioridades()

@router.get("/{id_prioridad}", summary="Obtener prioridad")
async def get_prioridad(id_prioridad: int):
    return controller.get_prioridad(id_prioridad)

@router.put("/{id_prioridad}", summary="Actualizar prioridad")
async def update_prioridad(id_prioridad: int, request: Request):
    try:
        data = await request.json()
    except Exception:
        data = {}
    campos = ["nombre_prioridad", "nivel"]
    prioridad_data = {k: data[k] for k in campos if k in data}
    prioridad = Prioridad(**prioridad_data)
    return controller.update_prioridad(id_prioridad, prioridad)

@router.delete("/{id_prioridad}", summary="Eliminar prioridad")
async def delete_prioridad(id_prioridad: int):
    return controller.delete_prioridad(id_prioridad)
