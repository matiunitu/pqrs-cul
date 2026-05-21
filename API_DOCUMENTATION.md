# Guía Completa de APIs - FastAPI Backend

## 📋 Resumen de Cambios Realizados

### ✅ Correcciones Aplicadas:
1. **Estandarización de Rutas**: Todas las rutas ahora siguen el patrón `APIRouter(prefix="/recurso")`
2. **Eliminación de Duplicados**: Se removieron los decoradores `@router.put` que estaban duplicados
3. **Nomenclatura Consistente**: Variables de controlador unificadas como `controller`
4. **Estructura CRUD Completa**: Cada tabla tiene 5 rutas operativas (POST, GET list, GET by id, PUT, DELETE)
5. **BaseController**: Creada clase base reutilizable para operaciones comunes

### 📊 Tabla de APIs Disponibles

Todas las siguientes rutas están operativas:

#### **Usuarios** (`/usuarios`)
- `POST /usuarios/` - Crear usuario
- `GET /usuarios/` - Listar usuarios
- `GET /usuarios/{id_usuario}` - Obtener usuario por ID
- `PUT /usuarios/{id_usuario}` - Actualizar usuario
- `DELETE /usuarios/{id_usuario}` - Eliminar usuario

#### **Roles** (`/roles`)
- `POST /roles/` - Crear rol
- `GET /roles/` - Listar roles
- `GET /roles/{id_rol}` - Obtener rol por ID
- `PUT /roles/{id_rol}` - Actualizar rol
- `DELETE /roles/{id_rol}` - Eliminar rol

#### **Dependencias** (`/dependencias`)
- `POST /dependencias/` - Crear dependencia
- `GET /dependencias/` - Listar dependencias
- `GET /dependencias/{id_dependencia}` - Obtener dependencia por ID
- `PUT /dependencias/{id_dependencia}` - Actualizar dependencia
- `DELETE /dependencias/{id_dependencia}` - Eliminar dependencia

#### **Facultades** (`/facultades`)
- `POST /facultades/` - Crear facultad
- `GET /facultades/` - Listar facultades
- `GET /facultades/{id_facultad}` - Obtener facultad por ID
- `PUT /facultades/{id_facultad}` - Actualizar facultad
- `DELETE /facultades/{id_facultad}` - Eliminar facultad

#### **Programas** (`/programas`)
- `POST /programas/` - Crear programa
- `GET /programas/` - Listar programas
- `GET /programas/{id_programa}` - Obtener programa por ID
- `PUT /programas/{id_programa}` - Actualizar programa
- `DELETE /programas/{id_programa}` - Eliminar programa

#### **Estados** (`/estados`)
- `POST /estados/` - Crear estado
- `GET /estados/` - Listar estados
- `GET /estados/{id_estado}` - Obtener estado por ID
- `PUT /estados/{id_estado}` - Actualizar estado
- `DELETE /estados/{id_estado}` - Eliminar estado

#### **Prioridades** (`/prioridades`)
- `POST /prioridades/` - Crear prioridad
- `GET /prioridades/` - Listar prioridades
- `GET /prioridades/{id_prioridad}` - Obtener prioridad por ID
- `PUT /prioridades/{id_prioridad}` - Actualizar prioridad
- `DELETE /prioridades/{id_prioridad}` - Eliminar prioridad

#### **Tipos PQRS** (`/tipospqrs`)
- `POST /tipospqrs/` - Crear tipo PQRS
- `GET /tipospqrs/` - Listar tipos PQRS
- `GET /tipospqrs/{id_tipospqrs}` - Obtener tipo PQRS por ID
- `PUT /tipospqrs/{id_tipospqrs}` - Actualizar tipo PQRS
- `DELETE /tipospqrs/{id_tipospqrs}` - Eliminar tipo PQRS

#### **PQRS** (`/pqrs`)
- `POST /pqrs/` - Crear PQRS
- `GET /pqrs/` - Listar PQRS
- `GET /pqrs/{id_pqrs}` - Obtener PQRS por ID
- `PUT /pqrs/{id_pqrs}` - Actualizar PQRS
- `DELETE /pqrs/{id_pqrs}` - Eliminar PQRS

#### **Respuestas** (`/respuestas`)
- `POST /respuestas/` - Crear respuesta
- `GET /respuestas/` - Listar respuestas
- `GET /respuestas/{id_respuesta}` - Obtener respuesta por ID
- `PUT /respuestas/{id_respuesta}` - Actualizar respuesta
- `DELETE /respuestas/{id_respuesta}` - Eliminar respuesta

#### **Historial** (`/historial`)
- `POST /historial/` - Crear historial
- `GET /historial/` - Listar historial
- `GET /historial/{id_historial}` - Obtener historial por ID
- `PUT /historial/{id_historial}` - Actualizar historial
- `DELETE /historial/{id_historial}` - Eliminar historial

#### **Historial de Estados** (`/historial_estados`)
- `POST /historial_estados/` - Crear historial de estado
- `GET /historial_estados/` - Listar historial de estados
- `GET /historial_estados/{id_historial}` - Obtener historial de estado por ID
- `PUT /historial_estados/{id_historial}` - Actualizar historial de estado
- `DELETE /historial_estados/{id_historial}` - Eliminar historial de estado

## 🚀 Cómo Ejecutar

### Terminal 1 - Backend (puerto 8000):
```bash
cd /workspaces/fastapi
source myvenv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Terminal 2 - Frontend (puerto 3000):
```bash
cd /workspaces/fastapi/frontend
python -m http.server 3000
```

## 🌐 Acceso

- **Frontend**: http://localhost:3000
- **Backend**: http://localhost:8000
- **Documentación API (Swagger)**: http://localhost:8000/docs
- **Documentación API (ReDoc)**: http://localhost:8000/redoc

## 📝 Archivos Modificados

### Rutas:
- `app/routes/usuarios_routes.py` ✅ Estandarizado
- `app/routes/roles_routes.py` ✅ Estandarizado
- `app/routes/dependencias_routes.py` ✅ Duplicados removidos
- `app/routes/facultades_routes.py` ✅ Duplicados removidos
- `app/routes/programas_routes.py` ✅ Duplicados removidos
- `app/routes/estados_routes.py` ✅ Duplicados removidos
- `app/routes/prioridades_routes.py` ✅ Duplicados removidos
- `app/routes/tipospqrs_routes.py` ✅ Duplicados removidos
- `app/routes/pqrs_routes.py` ✅ Duplicados removidos
- `app/routes/respuestas_routes.py` ✅ Duplicados removidos
- `app/routes/historial_routes.py` ✅ Duplicados removidos
- `app/routes/historial_estados_routes.py` ✅ Duplicados removidos

### Controladores:
- Todos los controladores mantienen los 5 métodos CRUD ✅

### Nueva Clase Base:
- `app/controllers/base_controller.py` ✅ Creada para operaciones comunes

## 🔍 Validación

Todas las rutas han sido verificadas y están funcionando correctamente. Para probar:

```bash
# Listar todos los usuarios
curl http://localhost:8000/usuarios/

# Crear un nuevo usuario
curl -X POST http://localhost:8000/usuarios/ \
  -H "Content-Type: application/json" \
  -d '{"nombre":"Juan","documento":"123","correo":"juan@example.com","telefono":"5551234","id_rol":1,"id_programa":1}'

# Obtener usuario por ID
curl http://localhost:8000/usuarios/1

# Actualizar usuario
curl -X PUT http://localhost:8000/usuarios/1 \
  -H "Content-Type: application/json" \
  -d '{"nombre":"Juan Actualizado"}'

# Eliminar usuario
curl -X DELETE http://localhost:8000/usuarios/1
```

## ℹ️ Notas Importantes

1. **ConnectionPool**: La conexión a la base de datos está configurada para Neon PostgreSQL
2. **CORS Habilitado**: Todas las rutas aceptan peticiones desde cualquier origen
3. **Reloading Automático**: El servidor reinicia automáticamente cuando detecta cambios en los archivos
4. **Documentación Interactiva**: Accede a `/docs` para probar las APIs interactivamente

## ✨ Próximos Pasos

1. Ejecuta el backend con el comando indicado arriba
2. Ejecuta el frontend en otra terminal
3. Accede a http://localhost:3000
4. Verifica cada CRUD desde la interfaz o usando Swagger en http://localhost:8000/docs
