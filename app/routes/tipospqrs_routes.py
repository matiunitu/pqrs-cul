from fastapi import APIRouter, Request
from controllers.tipospqrs_controller import TipospqrsController
from models.tipospqrs_model import Tipospqrs

router = APIRouter(prefix="/tipospqrs", tags=["tipospqrs"])
controller = TipospqrsController()

@router.post("/", summary="Crear tipo PQRS")
async def create_tipospqrs(request: Request):
    data = await request.json()
    campos = ["nombre_tipospqrs", "descripcion"]
    tipospqrs_data = {k: data[k] for k in campos if k in data}
    tipospqrs = Tipospqrs(**tipospqrs_data)
    return controller.create_tipospqrs(tipospqrs)

@router.get("/", summary="Listar tipos PQRS")
async def get_tipospqrs():
    return controller.get_todos_tipospqrs()

@router.get("/{id_tipospqrs}", summary="Obtener tipo PQRS")
async def get_tipospqrs_by_id(id_tipospqrs: int):
    return controller.get_tipospqrs(id_tipospqrs)

@router.put("/{id_tipospqrs}", summary="Actualizar tipo PQRS")
async def update_tipospqrs(id_tipospqrs: int, request: Request):
    try:
        data = await request.json()
    except Exception:
        data = {}
    campos = ["nombre_tipospqrs", "descripcion"]
    tipospqrs_data = {k: data[k] for k in campos if k in data}
    tipospqrs = Tipospqrs(**tipospqrs_data)
    return controller.update_tipospqrs(id_tipospqrs, tipospqrs)

@router.delete("/{id_tipospqrs}", summary="Eliminar tipo PQRS")
async def delete_tipospqrs(id_tipospqrs: int):
    return controller.delete_tipospqrs(id_tipospqrs)
