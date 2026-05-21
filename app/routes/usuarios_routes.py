from fastapi import APIRouter, Request
from controllers.usuarios_controller import UsuariosController
from models.usuario_model import Usuario, UsuarioUpdate

router = APIRouter(prefix="/usuarios", tags=["usuarios"])
controller = UsuariosController()


@router.post("/", summary="Crear usuario")
async def create_usuario(request: Request):
    data = await request.json()
    campos = ["nombre", "tipo_documento", "documento", "correo", "telefono",
              "id_rol", "id_programa", "activo", "estado", "password_hash"]
    usuario_data = {k: data[k] for k in campos if k in data and data[k] is not None}
    if not usuario_data.get('tipo_documento'):
        usuario_data['tipo_documento'] = 'CC'
    usuario = Usuario(**usuario_data)
    return controller.create_usuario(usuario)


@router.get("/", summary="Listar usuarios")
async def get_usuarios():
    return controller.get_usuarios()


@router.get("/by-rol/{nombre_rol}", summary="Listar usuarios por nombre de rol")
async def get_usuarios_by_rol(nombre_rol: str):
    return controller.get_usuarios_by_rol(nombre_rol)


@router.get("/{id_usuario}", summary="Obtener usuario por ID")
async def get_usuario(id_usuario: int):
    return controller.get_usuario(id_usuario)


@router.put("/{id_usuario}", summary="Actualizar usuario")
async def update_usuario(id_usuario: int, request: Request):
    try:
        data = await request.json()
    except Exception:
        data = {}
    
    # Permitimos actualización parcial usando UsuarioUpdate
    usuario_update = UsuarioUpdate(**data)
    return controller.update_usuario(id_usuario, usuario_update)


@router.put("/{id_usuario}/password", summary="Cambiar contraseña de usuario")
async def change_password(id_usuario: int, request: Request):
    data = await request.json()
    new_password = data.get("password")
    if not new_password:
        return {"error": "Se requiere la nueva contraseña"}
    return controller.change_password(id_usuario, new_password)


@router.delete("/{id_usuario}", summary="Eliminar usuario")
async def delete_usuario(id_usuario: int):
    return controller.delete_usuario(id_usuario)

@router.post("/{from_id}/reasignar/{to_id}", summary="Reasignar PQRS y referencias de un usuario a otro (ADMIN)")
async def reasignar_pqrs(from_id: int, to_id: int, delete_source: bool = False):
    return controller.reasignar_pqrs(from_id, to_id, delete_source)
