/**
 * ============================================================
 * status-badge.js — ETIQUETA DE ESTADO (Componente reutilizable)
 * ============================================================
 * Web Component: <status-badge>
 * Muestra una pastilla de color con el estado de un registro.
 *
 * Atributo:
 *  - status : Texto del estado (activo, inactivo, pendiente,
 *             resuelto, en proceso)
 *
 * Uso en HTML/JS:
 *  <status-badge status="activo"></status-badge>
 *  <status-badge status="pendiente"></status-badge>
 * ============================================================
 */

class StatusBadge extends HTMLElement {
  // Redibujar cuando cambie el atributo 'status'
  static get observedAttributes() { return ['status']; }
  connectedCallback()      { this._render(); }
  attributeChangedCallback() { this._render(); }

  // ─── Mapea el estado a un color de badge y una etiqueta ──────────────────
  _render() {
    const s = this.getAttribute('status') || '';
    const map = {
      'activo':     ['badge-success', '✅ Activo'],
      'inactivo':   ['badge-danger',  '❌ Inactivo'],
      'pendiente':  ['badge-warning', '⏳ Pendiente'],
      'resuelto':   ['badge-success', '✅ Resuelto'],
      'en proceso': ['badge-info',    '🔄 En Proceso'],
    };
    const [cls, label] = map[s.toLowerCase()] ?? ['badge-info', s];
    this.innerHTML = `<span class="badge ${cls}">${label}</span>`;
  }
}

// Registrar el componente como <status-badge> en el DOM
customElements.define('status-badge', StatusBadge);
