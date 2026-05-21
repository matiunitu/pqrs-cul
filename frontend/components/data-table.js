
class DataTable extends HTMLElement {
  constructor() {
    super();
    this._columns  = [];
    this._rows     = [];
    this._actions  = [];
    this._emptyMsg = 'Sin registros';
  }

  set columns(v)  { this._columns = v;  this.render(); }
  set rows(v)     { this._rows = v;     this.render(); }
  set actions(v)  { this._actions = v;  this.render(); }
  set emptyMsg(v) { this._emptyMsg = v; this.render(); }

  connectedCallback() { this.render(); }

  render() {
    const hasActions = this._actions.length > 0;

    const headers = this._columns.map(c =>
      `<th>${c.label}</th>`
    ).join('') + (hasActions ? '<th>Acciones</th>' : '');

    const rows = this._rows.length === 0
      ? `<tr><td colspan="${this._columns.length + (hasActions ? 1 : 0)}" style="text-align:center;padding:32px;color:var(--text-muted)">${this._emptyMsg}</td></tr>`
      : this._rows.map(row => {
          const cells = this._columns.map(col => {
            const raw = row[col.key] ?? '—';
            const val = col.render ? col.render(raw, row) : raw;
            return `<td>${val}</td>`;
          }).join('');

          const actBtns = this._actions.map((act, i) =>
            `<button class="btn btn-sm ${act.cls ?? 'btn-ghost'}" data-row="${encodeURIComponent(JSON.stringify(row))}" data-act="${i}">${act.label}</button>`
          ).join('');

          return `<tr>${cells}${hasActions ? `<td><div class="actions">${actBtns}</div></td>` : ''}</tr>`;
        }).join('');

    this.innerHTML = `
      <div style="overflow-x:auto">
        <table class="data-table">
          <thead><tr>${headers}</tr></thead>
          <tbody>${rows}</tbody>
        </table>
      </div>
    `;

    // Bind action buttons
    this.querySelectorAll('[data-act]').forEach(btn => {
      btn.addEventListener('click', () => {
        const row = JSON.parse(decodeURIComponent(btn.dataset.row));
        const idx = parseInt(btn.dataset.act);
        this._actions[idx]?.onClick(row);
      });
    });
  }
}

customElements.define('data-table', DataTable);
