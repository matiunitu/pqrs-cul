from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import sys
import os
import psycopg2.extras

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Parchear RealDictRow para que soporte acceso por índice entero (como tuplas)
# Esto soluciona los KeyError: 0 en los controladores que asumen tuplas.
_old_getitem = psycopg2.extras.RealDictRow.__getitem__
def _new_getitem(self, item):
    if isinstance(item, int):
        return list(self.values())[item]
    return _old_getitem(self, item)
psycopg2.extras.RealDictRow.__getitem__ = _new_getitem

# Importar rutas
from routes.auth_routes import router as auth_router
from routes.usuarios_routes import router as usuarios_router
from routes.roles_routes import router as roles_router
from routes.dependencias_routes import router as dependencias_router
from routes.historial_routes import router as historial_router
from routes.facultades_routes import router as facultades_router
from routes.programas_routes import router as programas_router
from routes.tipospqrs_routes import router as tipospqrs_router
from routes.estados_routes import router as estados_router
from routes.prioridades_routes import router as prioridades_router
from routes.pqrs_routes import router as pqrs_router
from routes.respuestas_routes import router as respuestas_router
from routes.historial_estados_routes import router as historial_estados_router

# Crear app FastAPI
app = FastAPI(
    title="API de Gestión de Usuarios Universitarios",
    description="""
## API PQRS Universitaria

### Autenticación JWT
Usa `/auth/login` para obtener un token temporal (60 minutos).

**Credenciales demo:**
| Campo    | Valor  |
|----------|--------|
| username | nelson |
| password | 1234   |
| rol      | admin  |

### Roles disponibles
| Rol        | Permisos                                  |
|------------|-------------------------------------------|
| admin      | CRUD completo + usuarios + reportes       |
| docente    | PQRS + respuestas + perfil                |
| estudiante | PQRS propias + perfil                     |

### Estado de registros
Todas las tablas principales usan `estado` (SMALLINT):
- **1** = activo
- **0** = inactivo/eliminado (soft-delete)

Las tablas también registran `created_at` y `updated_at` automáticamente.
    """,
    version="2.0.0",
)

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Rutas ────────────────────────────────────────────────────────────────────
app.include_router(auth_router)          # /auth/*
app.include_router(usuarios_router)
app.include_router(roles_router)
app.include_router(dependencias_router)
app.include_router(facultades_router)
app.include_router(programas_router)
app.include_router(tipospqrs_router)
app.include_router(estados_router)
app.include_router(prioridades_router)
app.include_router(pqrs_router)
app.include_router(respuestas_router)
app.include_router(historial_router)
app.include_router(historial_estados_router)


@app.api_route("/", methods=["GET", "HEAD"], summary="Saludo base")
async def root():
    return {
        "message": "API PQRS v2.0 activa",
        "docs": "/docs",
        "auth": "POST /auth/login → { username, password }",
        "seed": "POST /auth/seed → crea usuario demo nelson/1234/admin",
    }