from fastapi import APIRouter, Request
from controllers.historial_controller import HistorialController
from models.historial_model import Historial

router = APIRouter(prefix="/historial", tags=["historial"])
controller = HistorialController()

@router.post("/", summary="Crear historial")
async def create_historial(request: Request):
    data = await request.json()
    campos = ["id_usuario", "accion", "cambiado_por"]
    historial_data = {k: data[k] for k in campos if k in data}
    historial = Historial(**historial_data)
    return controller.create_historial(historial)

@router.get("/", summary="Listar historial")
async def get_historiales():
    return controller.get_historiales()

@router.get("/{id_historial}", summary="Obtener historial por ID")
async def get_historial(id_historial: int):
    return controller.get_historial(id_historial)

@router.put("/{id_historial}", summary="Actualizar historial")
async def update_historial(id_historial: int, request: Request):
    try:
        data = await request.json()
    except Exception:
        data = {}
    campos = ["id_usuario", "accion", "cambiado_por"]
    historial_data = {k: data[k] for k in campos if k in data}
    historial = Historial(**historial_data)
    return controller.update_historial(id_historial, historial)

@router.delete("/{id_historial}", summary="Eliminar historial")
async def delete_historial(id_historial: int):
    return controller.delete_historial(id_historial)
