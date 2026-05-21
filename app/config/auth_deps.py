from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from config.jwt_config import decode_token

security = HTTPBearer()

# Permisos por rol
ROLE_PERMISSIONS = {
    "admin": [
        "usuarios:read", "usuarios:write", "usuarios:delete",
        "pqrs:read", "pqrs:write", "pqrs:delete",
        "roles:read", "roles:write",
        "reportes:read",
        "configuracion:read", "configuracion:write",
    ],
    "docente": [
        "pqrs:read", "pqrs:write",
        "respuestas:read", "respuestas:write",
        "perfil:read", "perfil:write",
    ],
    "estudiante": [
        "pqrs:read", "pqrs:write",
        "perfil:read", "perfil:write",
    ],
}


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    payload = decode_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return payload


def require_role(*roles: str):
    """Dependencia: verifica que el usuario tenga uno de los roles indicados."""
    def _check(current_user: dict = Depends(get_current_user)):
        user_role = current_user.get("rol")
        if user_role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Acceso denegado. Se requiere uno de los roles: {list(roles)}",
            )
        return current_user
    return _check


def require_permission(permission: str):
    """Dependencia: verifica que el rol del usuario tenga el permiso indicado."""
    def _check(current_user: dict = Depends(get_current_user)):
        user_role = current_user.get("rol")
        allowed = ROLE_PERMISSIONS.get(user_role, [])
        if permission not in allowed:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permiso '{permission}' denegado para el rol '{user_role}'",
            )
        return current_user
    return _check
