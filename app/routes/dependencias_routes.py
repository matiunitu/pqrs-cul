from fastapi import APIRouter, Request
from controllers.dependencias_controller import DependenciasController
from models.dependencia_model import Dependencia

router = APIRouter(prefix="/dependencias", tags=["dependencias"])
controller = DependenciasController()

@router.post("/", summary="Crear dependencia")
async def create_dependencia(request: Request):
    data = await request.json()
    campos = ["nombre_dependencia", "descripcion"]
    dependencia_data = {k: data[k] for k in campos if k in data}
    dependencia = Dependencia(**dependencia_data)
    return controller.create_dependencia(dependencia)

@router.get("/", summary="Listar dependencias")
async def get_dependencias():
    return controller.get_dependencias()

@router.get("/{id_dependencia}", summary="Obtener dependencia por ID")
async def get_dependencia(id_dependencia: int):
    return controller.get_dependencia(id_dependencia)

@router.put("/{id_dependencia}", summary="Actualizar dependencia")
async def update_dependencia(id_dependencia: int, request: Request):
    try:
        data = await request.json()
    except Exception:
        data = {}
    campos = ["nombre_dependencia", "descripcion"]
    dependencia_data = {k: data[k] for k in campos if k in data}
    dependencia = Dependencia(**dependencia_data)
    return controller.update_dependencia(id_dependencia, dependencia)

@router.delete("/{id_dependencia}", summary="Eliminar dependencia")
async def delete_dependencia(id_dependencia: int):
    return controller.delete_dependencia(id_dependencia)
