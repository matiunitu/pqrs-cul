/**
 * ============================================================
 * app.js — ORQUESTADOR PRINCIPAL DEL FRONTEND
 * ============================================================
 * Este archivo es el punto de entrada de toda la aplicación.
 * Se encarga de:
 *  - Definir la URL base de la API del badsaddsdckend (FastAPI)
 *  - Proveer la función apiCall() para hacer petidxasdadadaciones HTTP
 *  - Manejar el login/logout y restaurar sesiones guardadas
 *  - Escuchar el evento 'auth-success' que dispara login-screen.js
 * ============================================================
 */

// ─── URL base del backend FastAPI ──────────────────────────────────────────────
// Detecta automáticamente si estamos en entorno local o en producción (ej. Vercel)
const isLocalhost = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';

export const API_BASE_URL = isLocalhost ? 'http://localhost:8000' : 'https://pqrs-cul-eee2.onrender.com';

// ─── Función helper para hacer peticiones a la API ─────────────────────────────
// Agrega automáticamente el token JWT al header Authorization si existe.
// Lanza un Error si el servidor responde con error (401, 403, 500, etc.)
export async function apiCall(endpoint, method = 'GET', data = null) {
  const token = sessionStorage.getItem('jwt_token');
  const headers = { 'Content-Type': 'application/json', 'Accept': 'application/json' };
  if (token) headers['Authorization'] = `Bearer ${token}`;

  const opts = { method, headers, cache: 'no-store' };
  if (data) opts.body = JSON.stringify(data);

  const res = await fetch(`${API_BASE_URL}${endpoint}`, opts);

  // Manejo de errores de autenticación / autorización
  if (res.status === 401 || res.status === 403) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail ?? `HTTP ${res.status}`);
  }
  // Manejo de cualquier otro error HTTP
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail ?? `Error ${res.status}`);
  }
  return res.json();
}

// ─── Función de Logout ─────────────────────────────────────────────────────────
// Limpia el token y los datos del usuario del sessionStorage,
// y vuelve a mostrar la pantalla de login.
export function logout() {
  sessionStorage.removeItem('jwt_token');
  sessionStorage.removeItem('jwt_user');
  sessionStorage.removeItem('jwt_expires');

  const dashboard = document.getElementById('dashboardShell');
  const login     = document.getElementById('loginScreen');

  dashboard.hidden = true;
  login.hidden     = false;
  login.render?.();

  window.toast?.show('Sesión cerrada', 'info');
}

// ─── Bootstrap / Inicialización de la App ─────────────────────────────────────
// Se ejecuta cuando el DOM está listo (DOMContentLoaded).
// Verifica si ya hay una sesión activa guardada y la restaura.
// También escucha el evento de login exitoso del componente login-screen.
function bootstrap() {
  const loginEl  = document.getElementById('loginScreen');
  const dashEl   = document.getElementById('dashboardShell');

  // Escuchar evento de login exitoso (disparado por login-screen.js)
  document.addEventListener('auth-success', e => {
    const { token, user, expiresIn } = e.detail;
    loginEl.hidden  = true;
    dashEl.hidden   = false;

    // Inicializar el dashboard con los datos del usuario autenticado
    dashEl.init(user, token, Date.now() + expiresIn * 1000);
  });

  // Restaurar sesión si el token aún no ha expirado (al recargar la página)
  const saved      = sessionStorage.getItem('jwt_token');
  const savedUser  = sessionStorage.getItem('jwt_user');
  const savedExp   = parseInt(sessionStorage.getItem('jwt_expires') ?? '0');

  if (saved && savedUser && savedExp > Date.now()) {
    loginEl.hidden  = true;
    dashEl.hidden   = false;
    dashEl.init(JSON.parse(savedUser), saved, savedExp);
  }
}

// Esperar a que los Web Components estén registrados antes de arrancar
window.addEventListener('DOMContentLoaded', bootstrap);
