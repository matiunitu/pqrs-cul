class EmptyState extends HTMLElement {
  connectedCallback() {
    const icon = this.getAttribute('icon') || '📭';
    const msg  = this.getAttribute('message') || 'Sin datos disponibles';
    this.innerHTML = `
      <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;padding:48px 24px;color:var(--text-muted)">
        <div style="font-size:3rem;margin-bottom:12px">${icon}</div>
        <p style="font-size:0.95rem">${msg}</p>
      </div>`;
  }
}
customElements.define('empty-state', EmptyState);
