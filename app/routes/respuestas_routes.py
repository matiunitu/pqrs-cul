from fastapi import APIRouter, Request
from controllers.respuestas_controller import RespuestasController
from models.respuesta_model import Respuesta

router = APIRouter(prefix="/respuestas", tags=["respuestas"])
controller = RespuestasController()

@router.post("/", summary="Crear respuesta")
async def create_respuesta(request: Request):
    data = await request.json()
    campos = ["mensaje", "id_pqrs", "id_usuario"]
    respuesta_data = {k: data[k] for k in campos if k in data}
    respuesta = Respuesta(**respuesta_data)
    return controller.create_respuesta(respuesta)

@router.get("/", summary="Listar respuestas")
async def get_respuestas():
    return controller.get_respuestas()

@router.get("/{id_respuesta}", summary="Obtener respuesta")
async def get_respuesta(id_respuesta: int):
    return controller.get_respuesta(id_respuesta)

@router.put("/{id_respuesta}", summary="Actualizar respuesta")
async def update_respuesta(id_respuesta: int, request: Request):
    try:
        data = await request.json()
    except Exception:
        data = {}
    campos = ["mensaje", "id_pqrs", "id_usuario"]
    respuesta_data = {k: data[k] for k in campos if k in data}
    respuesta = Respuesta(**respuesta_data)
    return controller.update_respuesta(id_respuesta, respuesta)

@router.delete("/{id_respuesta}", summary="Eliminar respuesta")
async def delete_respuesta(id_respuesta: int):
    return controller.delete_respuesta(id_respuesta)
