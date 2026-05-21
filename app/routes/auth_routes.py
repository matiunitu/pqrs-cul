from fastapi import APIRouter, Depends
from controllers.auth_controller import AuthController
from models.auth_model import LoginRequest, TokenResponse
from config.auth_deps import get_current_user

router = APIRouter(prefix="/auth", tags=["autenticación"])
controller = AuthController()


@router.post("/login", response_model=TokenResponse, summary="Iniciar sesión — obtiene JWT temporal (60 min)")
async def login(data: LoginRequest):
    """
    Credenciales demo:
    - **username**: nelson
    - **rol**: admin
    - **password**: 1234
    """
    return controller.login(data)


@router.post("/seed", summary="Crear usuario demo nelson/admin/1234 (solo dev)")
async def seed():
    """Crea el usuario de prueba en la base de datos si no existe."""
    return controller.seed_demo_user()


@router.get("/me", summary="Información del usuario autenticado")
async def me(current_user: dict = Depends(get_current_user)):
    return {
        "id_usuario": current_user.get("id_usuario"),
        "nombre":     current_user.get("nombre"),
        "rol":        current_user.get("rol"),
    }
