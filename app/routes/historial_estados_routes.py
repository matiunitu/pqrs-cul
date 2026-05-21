from fastapi import APIRouter, Request
from controllers.historial_estados_controller import HistorialEstadosController
from models.historial_estados_model import HistorialEstados

router = APIRouter(prefix="/historial_estados", tags=["historial_estados"])
controller = HistorialEstadosController()

@router.post("/", summary="Crear historial de estado")
async def create_historial_estado(request: Request):
    data = await request.json()
    campos = ["id_pqrs", "id_estado_anterior", "id_estado_nuevo", "cambiado_por"]
    historial_estados_data = {k: data[k] for k in campos if k in data}
    historial_estados = HistorialEstados(**historial_estados_data)
    return controller.create_historial_estados(historial_estados)

@router.get("/", summary="Listar historial de estado")
async def get_historiales_estados():
    return controller.get_historiales_estados()

@router.get("/{id_historial}", summary="Obtener historial estado")
async def get_historial_estado(id_historial: int):
    return controller.get_historial_estados(id_historial)

@router.put("/{id_historial}", summary="Actualizar historial estado")
async def update_historial_estado(id_historial: int, request: Request):
    try:
        data = await request.json()
    except Exception:
        data = {}
    campos = ["id_pqrs", "id_estado_anterior", "id_estado_nuevo", "cambiado_por"]
    historial_estados_data = {k: data[k] for k in campos if k in data}
    historial_estados = HistorialEstados(**historial_estados_data)
    return controller.update_historial_estados(id_historial, historial_estados)

@router.delete("/{id_historial}", summary="Eliminar historial estado")
async def delete_historial_estado(id_historial: int):
    return controller.delete_historial_estados(id_historial)
