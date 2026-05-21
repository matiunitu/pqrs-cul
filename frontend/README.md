# Frontend - Sistema de Gestión PQRS

Sistema de gestión de PQRS (Peticiones, Quejas, Reclamos y Sugerencias) con 3 roles diferentes: Administrador, Docente y Estudiante.

## 📁 Estructura de Archivos

```
frontend/
├── index.html      # Página principal
├── styles.css      # Estilos CSS con Bootstrap
├── app.js          # Lógica de JavaScript
└── README.md       # Este archivo
```

## 🚀 Características

### 🔐 Sistema de Autenticación
- Login básico con usuario y contraseña
- Selección de rol (Administrador, Docente, Estudiante)
- Sesión persistente con localStorage
- Logout seguro

### 👤 Roles Disponibles

#### 👨‍💼 Administrador
- Panel Principal
- Gestionar Usuarios
- Gestionar PQRS
- Reportes
- Configuración

#### 👨‍🏫 Docente
- Panel Principal
- Poner Queja
- Mis Quejas
- Mi Perfil

#### 👨‍🎓 Estudiante
- Panel Principal
- Poner Queja
- Mis Quejas
- Mi Perfil

## 🎯 Cómo Usar

### 1. Abrir el Frontend
Simple abre el archivo `index.html` en tu navegador

```bash
# Opción 1: Doble click en index.html
# Opción 2: Click derecho > Abrir con navegador
# Opción 3: Desde terminal
python -m http.server 8080
# Luego accede a http://localhost:8080
```

### 2. Credenciales de Prueba

**Usuarios demo (cualquier contraseña funciona):**
- Usuario: `admin` | Contraseña: `123` | Rol: Cualquiera
- Usuario: `docente` | Contraseña: `123` | Rol: Cualquiera
- Usuario: `estudiante` | Contraseña: `123` | Rol: Cualquiera

### 3. Navegar por el Sistema

1. Selecciona un usuario
2. Selecciona un rol
3. Haz clic en "Iniciar Sesión"
4. Usa el menú lateral para navegar por las diferentes secciones
5. Haz clic en "Cerrar Sesión" para salir

## 🎨 Diseño

- **Framework CSS**: Bootstrap 5.3
- **Tema**: Moderno y limpio
- **Responsive**: Compatible con móvil, tablet y desktop
- **Colores**: Azul principal (#0d6efd)

## 📋 Secciones Disponibles

### Administrador
- **Panel Principal**: Estadísticas y bienvenida
- **Gestionar Usuarios**: Crear, editar, eliminar usuarios
- **Gestionar PQRS**: Ver y resolver PQRS
- **Reportes**: Estadísticas y descargas
- **Configuración**: Ajustes del sitio

### Docente/Estudiante
- **Panel Principal**: Estadísticas personales
- **Poner Queja**: Formulario para enviar PQRS
- **Mis Quejas**: Ver historial de quejas
- **Mi Perfil**: Editar información personal

## 💡 Funcionalidades

✅ Login responsive y atractivo
✅ Menú dinámico según el rol
✅ Navegación fluida entre secciones
✅ Tablas con datos de ejemplo
✅ Formularios funcionales
✅ Alertas y notificaciones
✅ Sesión persistente
✅ Logout seguro

## 🔧 Tecnologías

- **HTML5**: Estructura semántica
- **CSS3**: Estilos avanzados
- **JavaScript**: Lógica del cliente
- **Bootstrap 5**: Framework CSS
- **LocalStorage**: Persistencia de datos

## 📱 Compatibilidad

- Chrome ✓
- Firefox ✓
- Safari ✓
- Edge ✓
- Modo responsivo ✓

## 🚀 Próximas Mejoras (Futuro)

- Conectar con API backend
- Validación de formularios avanzada
- Animaciones mejoradas
- Sistema de notificaciones
- Exportar reportes a PDF
- Búsqueda y filtrado en tablas
- Paginación

## 📞 Información de Contacto

Para consultas o sugerencias, contacta al administrador del sistema.

---

**Versión**: 1.0  
**Última actualización**: 2026-03-10
