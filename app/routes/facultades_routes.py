from fastapi import APIRouter, Request
from controllers.facultades_controller import FacultadesController
from models.facultad_model import Facultad

router = APIRouter(prefix="/facultades", tags=["facultades"])
controller = FacultadesController()

@router.post("/", summary="Crear facultad")
async def create_facultad(request: Request):
    data = await request.json()
    campos = ["nombre_facultad", "descripcion"]
    facultad_data = {k: data[k] for k in campos if k in data}
    facultad = Facultad(**facultad_data)
    return controller.create_facultad(facultad)

@router.get("/", summary="Listar facultades")
async def get_facultades():
    return controller.get_facultades()

@router.get("/{id_facultad}", summary="Obtener facultad")
async def get_facultad(id_facultad: int):
    return controller.get_facultad(id_facultad)

@router.put("/{id_facultad}", summary="Actualizar facultad")
async def update_facultad(id_facultad: int, request: Request):
    try:
        data = await request.json()
    except Exception:
        data = {}
    campos = ["nombre_facultad", "descripcion"]
    facultad_data = {k: data[k] for k in campos if k in data}
    facultad = Facultad(**facultad_data)
    return controller.update_facultad(id_facultad, facultad)

@router.delete("/{id_facultad}", summary="Eliminar facultad")
async def delete_facultad(id_facultad: int):
    return controller.delete_facultad(id_facultad)
