/**
 * ============================================================
 * toast-notification.js — NOTIFICACIONES EMERGENTES (Toast)
 * ============================================================
 * Web Component: <toast-notification>
 * Muestra mensajes de feedback al usuario (éxito, error,
 * advertencia, info) en la esquina de la pantalla.
 *
 * Se registra globalmente como window.toast para ser usado
 * desde cualquier parte del código así:
 *   window.toast?.show('Mensaje aquí', 'success')
 *   window.toast?.show('Error', 'error')
 *   window.toast?.show('Cuidado', 'warning')
 *   window.toast?.show('Info', 'info')
 *
 * Tipos disponibles: 'success' | 'error' | 'warning' | 'info'
 * Se cierra automáticamente después de 4 segundos (configurable).
 * ============================================================
 */

class ToastNotification extends HTMLElement {

  // Al conectarse al DOM, se registra como acceso global window.toast
  connectedCallback() {
    this.className = 'toast-container';
    window.toast = this; // Hacer disponible globalmente
  }

  // ─── Muestra una notificación emergente ───────────────────────────────────
  // message  : Texto a mostrar
  // type     : 'success' | 'error' | 'warning' | 'info'
  // duration : Tiempo en ms antes de desaparecer (por defecto 4 segundos)
  show(message, type = 'info', duration = 4000) {
    const icons = { success: '✅', error: '❌', warning: '⚠️', info: 'ℹ️' };

    const el = document.createElement('div');
    el.className = `toast ${type}`;
    el.innerHTML = `
      <span class="toast-icon">${icons[type] ?? '🔔'}</span>
      <span class="toast-msg">${message}</span>
      <button class="toast-close" title="Cerrar">✕</button>
    `;
    // Botón X para cerrar manualmente
    el.querySelector('.toast-close').onclick = () => el.remove();
    this.appendChild(el);

    // Auto-eliminar después del tiempo indicado
    setTimeout(() => el.remove(), duration);
  }
}

// Registrar el componente como <toast-notification> en el DOM
customElements.define('toast-notification', ToastNotification);