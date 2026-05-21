from fastapi import APIRouter, Request
from controllers.estados_controller import EstadosController
from models.estado_model import Estado

router = APIRouter(prefix="/estados", tags=["estados"])
controller = EstadosController()

@router.post("/", summary="Crear estado")
async def create_estado(request: Request):
    data = await request.json()
    campos = ["nombre_estado"]
    estado_data = {k: data[k] for k in campos if k in data}
    estado = Estado(**estado_data)
    return controller.create_estado(estado)

@router.get("/", summary="Listar estados")
async def get_estados():
    return controller.get_estados()

@router.get("/{id_estado}", summary="Obtener estado")
async def get_estado(id_estado: int):
    return controller.get_estado(id_estado)

@router.put("/{id_estado}", summary="Actualizar estado")
async def update_estado(id_estado: int, request: Request):
    try:
        data = await request.json()
    except Exception:
        data = {}
    campos = ["nombre_estado"]
    estado_data = {k: data[k] for k in campos if k in data}
    estado = Estado(**estado_data)
    return controller.update_estado(id_estado, estado)

@router.delete("/{id_estado}", summary="Eliminar estado")
async def delete_estado(id_estado: int):
    return controller.delete_estado(id_estado)
