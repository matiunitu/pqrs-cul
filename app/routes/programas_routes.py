from fastapi import APIRouter, Request
from controllers.programas_controller import ProgramasController
from models.programa_model import Programa

router = APIRouter(prefix="/programas", tags=["programas"])
controller = ProgramasController()

@router.post("/", summary="Crear programa")
async def create_programa(request: Request):
    data = await request.json()
    campos = ["nombre_programa", "descripcion", "id_facultad"]
    programa_data = {k: data[k] for k in campos if k in data}
    programa = Programa(**programa_data)
    return controller.create_programa(programa)

@router.get("/", summary="Listar programas")
async def get_programas():
    return controller.get_programas()

@router.get("/{id_programa}", summary="Obtener programa")
async def get_programa(id_programa: int):
    return controller.get_programa(id_programa)

@router.put("/{id_programa}", summary="Actualizar programa")
async def update_programa(id_programa: int, request: Request):
    try:
        data = await request.json()
    except Exception:
        data = {}
    campos = ["nombre_programa", "descripcion", "id_facultad"]
    programa_data = {k: data[k] for k in campos if k in data}
    programa = Programa(**programa_data)
    return controller.update_programa(id_programa, programa)

@router.delete("/{id_programa}", summary="Eliminar programa")
async def delete_programa(id_programa: int):
    return controller.delete_programa(id_programa)
