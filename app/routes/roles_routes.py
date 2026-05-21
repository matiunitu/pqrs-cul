from fastapi import APIRouter, Request
from controllers.roles_controller import RolesController
from models.rol_model import Rol

router = APIRouter(prefix="/roles", tags=["roles"])
controller = RolesController()

@router.post("/", summary="Crear rol")
async def create_rol(request: Request):
    data = await request.json()
    campos = ["nombre_rol", "descripcion"]
    rol_data = {k: data[k] for k in campos if k in data}
    rol = Rol(**rol_data)
    return controller.create_role(rol)

@router.get("/", summary="Listar roles")
async def get_roles():
    return controller.get_roles()

@router.get("/{id_rol}", summary="Obtener rol por ID")
async def get_rol(id_rol: int):
    return controller.get_role(id_rol)

@router.put("/{id_rol}", summary="Actualizar rol")
async def update_rol(id_rol: int, request: Request):
    try:
        data = await request.json()
    except Exception:
        data = {}
    campos = ["nombre_rol", "descripcion"]
    rol_data = {k: data[k] for k in campos if k in data}
    rol = Rol(**rol_data)
    return controller.update_role(id_rol, rol)

@router.delete("/{id_rol}", summary="Eliminar rol")
async def delete_rol(id_rol: int):
    return controller.delete_role(id_rol)
