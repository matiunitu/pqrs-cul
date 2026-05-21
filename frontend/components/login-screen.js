/**
 * ============================================================
 * login-screen.js — PANTALLA DE INICIO DE SESIÓN
 * ============================================================
 * Web Component personalizado (<login-screen>).
 * Muestra el formulario de login y maneja la autenticación.
 *
 * Flujo:
 *  1. El usuario ingresa usuario y contraseña
 *  2. Se hace POST a /auth/login en el backend
 *  3. Si es exitoso, guarda el token JWT en sessionStorage
 *  4. Dispara el evento 'auth-success' para que app.js
 *     cambie a la pantalla del dashboard
 * ============================================================
 */

import { API_BASE_URL } from '../app.js';

class LoginScreen extends HTMLElement {

  // Se ejecuta cuando el componente se inserta en el DOM
  connectedCallback() {
    this.render();
    // Asignar el manejador del formulario de login
    this.querySelector('#loginForm').addEventListener('submit', e => this._onSubmit(e));
  }

  // ─── Renderizado del HTML del formulario de login ──────────────────────────
  render() {
    this.innerHTML = `
      <div class="login-bg">
        <div class="login-card animate-in">
          <div class="login-header">
            <div style="text-align: center; margin-bottom: 20px;">
              <img src="./assets/logo.png" alt="CUL Logo" style="height: 60px; object-fit: contain; border-radius: 8px;" onerror="this.src='https://ui-avatars.com/api/?name=CUL&background=1a73e8&color=fff&size=100&font-size=0.4'; this.onerror=null;" />
            </div>
            <h1>Sistemas PQRS - CUL</h1>
            <p>Ingresa tus credenciales para continuar</p>
          </div>

          <!-- Formulario de autenticación -->
          <form id="loginForm" autocomplete="off">
            <div class="form-group">
              <label for="lg-username">Usuario</label>
              <input id="lg-username" type="text" placeholder="ej: nelson" required />
            </div>
            <div class="form-group">
              <label for="lg-password">Contraseña</label>
              <input id="lg-password" type="password" placeholder="••••••••" required />
            </div>

            <button class="btn btn-primary" style="width:100%;justify-content:center;margin-top:8px" id="loginBtn" type="submit">
              Iniciar sesión
            </button>
          </form>


        </div>
      </div>
    `;
  }

  // ─── Manejador del submit del formulario ──────────────────────────────────
  // Realiza la petición de autenticación al backend y guarda el token
  async _onSubmit(e) {
    e.preventDefault();
    const btn = this.querySelector('#loginBtn');
    const username = this.querySelector('#lg-username').value.trim();
    const password = this.querySelector('#lg-password').value;

    // Deshabilitar el botón mientras procesa
    btn.disabled = true;
    btn.textContent = 'Entrando…';

    try {
      // Petición de login al endpoint del backend
      const res = await fetch(`${API_BASE_URL}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password }),
      });

      if (!res.ok) {
        const err = await res.json().catch(() => ({}));
        throw new Error(err.detail || `Error ${res.status}`);
      }

      const data = await res.json();

      // Guardar token y datos del usuario en sessionStorage
      // (se borra automáticamente al cerrar la pestaña del navegador)
      sessionStorage.setItem('jwt_token',  data.access_token);
      sessionStorage.setItem('jwt_user',   JSON.stringify(data.user));
      sessionStorage.setItem('jwt_expires', Date.now() + data.expires_in * 1000);

      // Notificar al resto de la app que el login fue exitoso
      this.dispatchEvent(new CustomEvent('auth-success', {
        bubbles: true,
        detail: { token: data.access_token, user: data.user, expiresIn: data.expires_in },
      }));
    } catch (err) {
      // Mostrar el error al usuario (credenciales incorrectas, servidor caído, etc.)
      window.toast?.show(err.message, 'error');
    } finally {
      // Rehabilitar el botón siempre, haya éxito o error
      btn.disabled = false;
      btn.textContent = 'Iniciar sesión';
    }
  }
}

// Registrar el componente como <login-screen> en el DOM
customElements.define('login-screen', LoginScreen);
