/**
 * ============================================================
 * stat-card.js — TARJETA DE ESTADÍSTICA (Componente reutilizable)
 * ============================================================
 * Web Component: <stat-card>
 * Se usa en el Panel Principal (dashboard) de todos los roles
 * para mostrar métricas como: total de usuarios, PQRS, etc.
 *
 * Atributos:
 *  - label : Texto del título de la tarjeta
 *  - value : Valor numérico o texto a mostrar en grande
 *  - icon  : Emoji o símbolo visual
 *  - trend : Texto pequeño debajo del valor (ej. "↑ activos")
 *
 * Uso en HTML/JS:
 *  <stat-card label="Usuarios" value="42" icon="👥" trend="↑ activos"></stat-card>
 * ============================================================
 */

class StatCard extends HTMLElement {
  // Atributos que, al cambiar, provocan un re-renderizado
  static get observedAttributes() { return ['label','value','trend','icon']; }

  connectedCallback()              { this.render(); }
  attributeChangedCallback()       { this.render(); }

  // ─── Renderiza la tarjeta con los atributos actuales ──────────────────────
  render() {
    const label = this.getAttribute('label') ?? '—';
    const value = this.getAttribute('value') ?? '0';
    const trend = this.getAttribute('trend') ?? '';
    const icon  = this.getAttribute('icon')  ?? '📊';

    this.className = 'stat-box';
    this.innerHTML = `
      <div class="label">${icon} ${label}</div>
      <div class="value">${value}</div>
      ${trend ? `<div class="trend">${trend}</div>` : ''}
    `;
  }
}

// Registrar el componente como <stat-card> en el DOM
customElements.define('stat-card', StatCard);
