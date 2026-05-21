/**
 * ============================================================
 * app-dashboard.js — DASHBOARD PRINCIPAL (Todos los roles)
 * ============================================================
 * Web Component: <app-dashboard>
 * Este es el componente más importante del frontend.
 * Se encarga de renderizar TODA la interfaz después del login.
 *
 * Secciones por ROL:
 *  🔵 ADMIN       → dashboard, usuarios, gestión PQRS,
 *                   responder PQRS, roles y reportes
 *  🟡 DOCENTE     → dashboard, nueva PQRS, mis PQRS,
 *                   responder PQRS, perfil
 *  🟢 ESTUDIANTE  → dashboard, nueva PQRS, mis PQRS, perfil
 *
 * Estructura del archivo:
 *  1. Configuración de menús por rol  (ROLE_CONFIG)
 *  2. Permisos por rol                (ROLE_PERMISSIONS)
 *  3. Clase AppDashboard
 *     - render()          → Estructura HTML base (navbar + sidebar)
 *     - _navigate()       → Cambiar de sección activa
 *     - _renderSection()  → Enrutador de secciones
 *     - _pageDashboard()  → Panel principal (todos los roles)
 *     - _pageUsuarios()   → Gestión usuarios (solo ADMIN)
 *     - _pagePQRS()       → Gestión PQRS (solo ADMIN)
 *     - _showPQRSModal()  → Modal detalle + acciones admin
 *     - _pageRoles()      → Roles y permisos (solo ADMIN)
 *     - _pageReportes()   → Power BI (solo ADMIN)
 *     - _pageNuevaPQRS()  → Crear PQRS (DOCENTE + ESTUDIANTE)
 *     - _pageMisPQRS()    → Ver mis PQRS (DOCENTE + ESTUDIANTE)
 *     - _pageResponderPQRS() → Responder PQRS (ADMIN + DOCENTE)
 *     - _pagePerfil()     → Mi perfil (DOCENTE + ESTUDIANTE)
 *     - _startTimer()     → Cuenta regresiva del token JWT
 * ============================================================
 */

import { apiCall, logout } from '../app.js';

// ─────────────────────────────────────────────────────────────────────────────
// CONFIGURACIÓN DE MENÚS POR ROL
// Define qué opciones de navegación ve cada rol en el sidebar.
// ─────────────────────────────────────────────────────────────────────────────
const ROLE_CONFIG = {
  admin: {
    label: 'Administrador',
    icon: '👨‍💼',
    color: '#6c63ff',
    menu: [
      { id: 'dashboard', label: 'Panel Principal', icon: '📊' },
      { id: 'usuarios', label: 'Usuarios', icon: '👥' },
      { id: 'pqrs', label: 'Gestión PQRS', icon: '📋' },
      { id: 'respuestas', label: 'Todas las Respuestas', icon: '💬' },
      { id: 'responder-pqrs', label: 'Responder PQRS', icon: '📨' },
      { id: 'roles', label: 'Roles & Permisos', icon: '🔑' },
      { id: 'reportes', label: 'Reportes Power BI', icon: '📈' },
    ],
  },
  docente: {
    label: 'Docente',
    icon: '👨‍🏫',
    color: '#10b981',
    menu: [
      { id: 'dashboard', label: 'Panel Principal', icon: '📊' },
      { id: 'nueva-pqrs', label: 'Nueva PQRS', icon: '📝' },
      { id: 'mis-pqrs', label: 'Mis PQRS', icon: '📋' },
      { id: 'pqrs-respondidos', label: 'PQRS Respondidos', icon: '✅' },
      { id: 'responder-pqrs', label: 'Responder PQRS', icon: '💬' },
      { id: 'perfil', label: 'Mi Perfil', icon: '👤' },
    ],
  },
  estudiante: {
    label: 'Estudiante',
    icon: '👨‍🎓',
    color: '#3b82f6',
    menu: [
      { id: 'dashboard', label: 'Panel Principal', icon: '📊' },
      { id: 'nueva-pqrs', label: 'Nueva PQRS', icon: '📝' },
      { id: 'mis-pqrs', label: 'Mis PQRS', icon: '📋' },
      { id: 'perfil', label: 'Mi Perfil', icon: '👤' },
    ],
  },
};

// ─────────────────────────────────────────────────────────────────────────────
// PERMISOS POR ROL
// Lista de acciones permitidas para cada rol.
// Se usa en la sección de Roles & Permisos para mostrar las capacidades.
// ─────────────────────────────────────────────────────────────────────────────
const ROLE_PERMISSIONS = {
  admin: [
    'usuarios:read', 'usuarios:write', 'usuarios:delete',
    'pqrs:read', 'pqrs:write', 'pqrs:delete',
    'roles:read', 'roles:write',
    'reportes:read', 'configuracion:read', 'configuracion:write',
  ],
  docente: [
    'pqrs:read', 'pqrs:write',
    'respuestas:read', 'respuestas:write',
    'perfil:read', 'perfil:write',
  ],
  estudiante: [
    'pqrs:read', 'pqrs:write',
    'perfil:read', 'perfil:write',
  ],
};

class AppDashboard extends HTMLElement {

  // Inicialización interna de variables al insertar el componente en el DOM
  connectedCallback() {
    this._user = null;  // Datos del usuario autenticado
    this._token = null;  // Token JWT
    this._section = 'dashboard'; // Sección activa
    this._timer = null;  // Referencia al intervalo del temporizador JWT
  }

  /**
   * Llamado desde app.js después de un login exitoso.
   * Recibe los datos del usuario y el token para montar la interfaz.
   */
  init(user, token, expiresAt) {
    this._user = user;
    this._token = token;
    this._expiresAt = expiresAt;
    this.render();           // Dibuja navbar + sidebar
    this._startTimer();      // Inicia la cuenta regresiva del token
    this._navigate('dashboard'); // Navega a la sección inicial
  }

  render() {
    const rol = this._user?.rol ?? 'estudiante';
    const cfg = ROLE_CONFIG[rol] ?? ROLE_CONFIG.estudiante;
    const initials = (this._user?.nombre ?? '?').slice(0, 2).toUpperCase();

    const menuItems = cfg.menu.map(m => `
      <button class="nav-item" data-section="${m.id}" id="nav-${m.id}">
        <span class="icon">${m.icon}</span> ${m.label}
      </button>
    `).join('');

    this.innerHTML = `
      <div class="dashboard-layout">

        <!-- Navbar -->
        <nav class="app-navbar">
          <div class="navbar-brand" style="display: flex; align-items: center; gap: 10px;">
            <img src="./assets/logo.png" alt="CUL Logo" style="height: 28px; object-fit: contain; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.1));" onerror="this.style.display='none'; document.getElementById('fallbackDot').style.display='inline-block';" />
            <span class="dot" id="fallbackDot" style="display:none;"></span>
            Sistemas PQRS - CUL
          </div>
          <div class="navbar-user">
            <span class="token-timer" id="timerBadge">⏱ 60:00</span>
            <div class="user-avatar" title="${this._user?.nombre}">${initials}</div>
            <span style="font-size:0.85rem">
              ${this._user?.nombre}
              <span class="badge badge-accent" style="margin-left:6px">${cfg.label}</span>
            </span>
            <button class="btn btn-ghost btn-sm" id="logoutBtn">🚪 Salir</button>
          </div>
        </nav>

        <!-- Sidebar -->
        <aside class="app-sidebar">
          <div class="sidebar-label">Menú</div>
          <div id="sidebarMenu">${menuItems}</div>
        </aside>

        <!-- Content -->
        <main class="app-main" id="mainContent">
          <div class="animate-in" id="pageContent"></div>
        </main>
      </div>

      <!-- Toast global -->
      <toast-notification></toast-notification>
    `;

    // Events
    this.querySelector('#logoutBtn').onclick = () => logout();
    this.querySelectorAll('.nav-item').forEach(btn => {
      btn.onclick = () => this._navigate(btn.dataset.section);
    });
  }

  // ─── Navegación entre secciones ───────────────────────────────────────────
  // Marca el botón activo en el sidebar y renderiza la sección correspondiente
  _navigate(section) {
    this._section = section;

    // Quitar 'active' de todos los botones y poner en el seleccionado
    this.querySelectorAll('.nav-item').forEach(b => b.classList.remove('active'));
    this.querySelector(`#nav-${section}`)?.classList.add('active');

    // Limpiar el contenido actual y renderizar la nueva sección
    const el = this.querySelector('#pageContent');
    if (el) {
      el.className = 'animate-in';
      el.innerHTML = '';
      this._renderSection(section, el);
    }
  }

  // ─── Enrutador de secciones ────────────────────────────────────────────────
  // Decide qué función de página llamar según el ID de sección
  _renderSection(id, target) {
    switch (id) {
      case 'dashboard': this._pageDashboard(target); break; // Todos los roles
      case 'usuarios': this._pageUsuarios(target); break; // Solo ADMIN
      case 'pqrs': this._pagePQRS(target); break; // Solo ADMIN
      case 'roles': this._pageRoles(target); break; // Solo ADMIN
      case 'reportes': this._pageReportes(target); break; // Solo ADMIN
      case 'nueva-pqrs': this._pageNuevaPQRS(target); break; // DOCENTE + ESTUDIANTE
      case 'mis-pqrs': this._pageMisPQRS(target); break; // DOCENTE + ESTUDIANTE
      case 'respuestas': this._pageRespuestas(target); break; // Solo ADMIN
      case 'responder-pqrs': this._pageResponderPQRS(target); break; // ADMIN + DOCENTE
      case 'pqrs-respondidos': this._pagePqrsRespondidos(target); break; // DOCENTE
      case 'perfil': this._pagePerfil(target); break; // DOCENTE + ESTUDIANTE
      default: target.innerHTML = '<p>Sección no disponible</p>';
    }
  }

  // =============================================================
  // SECCIÓN: PANEL PRINCIPAL (Todos los roles)
  // Muestra tarjetas con estadísticas generales del sistema.
  // El admin ve: total usuarios, total PQRS, estado de la BD.
  // =============================================================
  async _pageDashboard(el) {
    const rol = this._user?.rol;
    const cfg = ROLE_CONFIG[rol] ?? ROLE_CONFIG.estudiante;

    el.innerHTML = `
      <div class="page-header">
        <h2>${cfg.icon} Bienvenido, ${this._user?.nombre}</h2>
        <p>Rol: <strong>${cfg.label}</strong> — ${new Date().toLocaleDateString('es-CO', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })}</p>
      </div>
      <div class="stats-grid" id="statsGrid">
        <stat-card label="Cargando…" value="…" icon="🔄"></stat-card>
      </div>
    `;

    // Cargar stats reales
    try {
      const [usuarios, pqrs, roles] = await Promise.all([
        apiCall('/usuarios/').catch(() => []),
        apiCall('/pqrs/').catch(() => []),
        apiCall('/roles/').catch(() => []),
      ]);

      const statsGrid = el.querySelector('#statsGrid');
      statsGrid.innerHTML = `
        <stat-card label="Usuarios"      value="${usuarios.length}" icon="👥" trend="↑ activos"></stat-card>
        <stat-card label="PQRS totales"  value="${pqrs.length}"    icon="📋" trend="registradas"></stat-card>
        <stat-card label="Estado BD"     value="✅"              icon="🟢" trend="Neon PostgreSQL"></stat-card>
      `;

    } catch (e) {
      console.error(e);
    }
  }

  // =============================================================
  // SECCIÓN: GESTIÓN DE USUARIOS (Solo ADMIN)
  // Muestra la tabla con todos los usuarios del sistema.
  // Permite crear, editar y eliminar usuarios.
  // Usa DataTables si está disponible para buscar y paginar.
  // =============================================================
  async _pageUsuarios(el) {
    el.innerHTML = `
      <div class="page-header">
        <h2>👥 Gestión de Usuarios</h2>
        <button class="btn btn-primary btn-sm" id="newUserBtn">+ Nuevo usuario</button>
      </div>
      <div class="card">
        <div id="usuariosTableWrap">
          <p style="color:var(--text-muted);text-align:center;padding:24px">Cargando…</p>
        </div>
      </div>
    `;

    el.querySelector('#newUserBtn').onclick = () => this._formUsuario(el);

    const wrap = el.querySelector('#usuariosTableWrap');
    try {
      const rows = await apiCall('/usuarios/');
      let html = `<table id="usuariosTable" class="display" style="width:100%; font-size:0.9rem">
        <thead><tr style="text-align:left"><th>ID</th><th>Nombre</th><th>Correo</th><th>Teléfono</th><th>Estado</th><th>Creado</th><th>Acciones</th></tr></thead>
        <tbody>`;

      rows.forEach(r => {
        const estadoBadge = `<span class="badge ${r.estado == 1 ? 'badge-success' : 'badge-danger'}">${r.estado == 1 ? 'Activo' : 'Inactivo'}</span>`;
        const fecha = r.created_at ? new Date(r.created_at).toLocaleDateString('es-CO') : '—';
        html += `<tr>
          <td>${r.id_usuario}</td>
          <td>${r.nombre ?? ''}</td>
          <td>${r.correo ?? ''}</td>
          <td>${r.telefono ?? ''}</td>
          <td>${estadoBadge}</td>
          <td>${fecha}</td>
          <td>
            <button class="btn btn-ghost btn-sm edit-btn" data-id="${r.id_usuario}">✏️ Editar</button>
            <button class="btn btn-warning btn-sm reassign-btn" data-id="${r.id_usuario}">🔁 Reasignar</button>
            <button class="btn btn-danger btn-sm del-btn" data-id="${r.id_usuario}">🗑 Eliminar</button>
          </td>
        </tr>`;
      });
      html += `</tbody></table>`;
      wrap.innerHTML = html;

      if (window.$ && window.$.fn.DataTable) {
        $('#usuariosTable').DataTable({ language: { url: '//cdn.datatables.net/plug-ins/1.13.6/i18n/es-ES.json' } });
      }

      wrap.querySelectorAll('.edit-btn').forEach(btn => {
        btn.onclick = () => {
          const row = rows.find(r => r.id_usuario == btn.dataset.id);
          this._formUsuario(el, row);
        };
      });
      wrap.querySelectorAll('.del-btn').forEach(btn => {
        btn.onclick = () => this._deleteUsuario(btn.dataset.id, el);
      });

      wrap.querySelectorAll('.reassign-btn').forEach(btn => {
        btn.onclick = async () => {
          const fromId = btn.dataset.id;
          const toId = prompt('Ingrese ID del usuario destino para reasignar las PQRS (ej. 17):');
          if (!toId) return;
          const confirmDelete = confirm('¿Desea eliminar el usuario origen después de reasignar? Esto eliminará al usuario origen si no tiene referencias posteriores.');
          try {
            await apiCall(`/usuarios/${fromId}/reasignar/${toId}?delete_source=${confirmDelete}`, 'POST');
            window.toast?.show('Reasignación completada', 'success');
            // Recargar la lista de usuarios
            this._pageUsuarios(el);
          } catch (err) {
            window.toast?.show(err.message || 'Error en la reasignación', 'error');
          }
        };
      });
    } catch (e) {
      wrap.innerHTML = `<p style="color:var(--danger);text-align:center;padding:20px">${e.message}</p>`;
    }
  }

  async _formUsuario(container, row = null) {
    const isEdit = !!row;
    const section = container.querySelector('#mainSection') ?? container;
    section.innerHTML = `
      <div class="page-header">
        <h2>${isEdit ? '✏️ Editar' : '➕ Nuevo'} Usuario</h2>
        <button class="btn btn-ghost btn-sm" id="backBtn">← Volver</button>
      </div>
      <div class="card" style="max-width:560px">
        <form id="userForm">
          <div class="form-group"><label>Nombre completo</label><input id="f-nombre" value="${row?.nombre ?? ''}" required /></div>
          <div class="form-group">
            <label>Tipo de documento</label>
            <select id="f-tipo-doc">
              <option value="CC" ${(row?.tipo_documento ?? 'CC') === 'CC' ? 'selected' : ''}>CC — Cédula de ciudadanía</option>
              <option value="TI" ${row?.tipo_documento === 'TI' ? 'selected' : ''}>TI — Tarjeta de identidad</option>
              <option value="CE" ${row?.tipo_documento === 'CE' ? 'selected' : ''}>CE — Cédula extranjería</option>
              <option value="PP" ${row?.tipo_documento === 'PP' ? 'selected' : ''}>PP — Pasaporte</option>
            </select>
          </div>
          <div class="form-group"><label>Número de documento</label><input id="f-documento" value="${row?.documento ?? ''}" required /></div>
          <div class="form-group"><label>Correo electrónico</label><input id="f-correo" type="email" value="${row?.correo ?? ''}" required /></div>
          <div class="form-group"><label>Teléfono</label><input id="f-telefono" value="${row?.telefono ?? ''}" required /></div>
          <div class="form-group">
            <label>Rol</label>
            <select id="f-rol"><option value="">Cargando roles…</option></select>
          </div>
          <div class="form-group">
            <label>Programa académico</label>
            <select id="f-programa"><option value="">Cargando programas…</option></select>
          </div>
          ${!isEdit ? `<div class="form-group"><label>Contraseña (opcional, por defecto: 1234)</label><input id="f-password" type="password" placeholder="Dejar vacío para usar 1234" /></div>` : ''}
          <div class="form-group"><label>Estado</label>
            <select id="f-estado">
              <option value="1" ${!isEdit || row?.estado == 1 ? 'selected' : ''}>Activo</option>
              <option value="0" ${row?.estado == 0 ? 'selected' : ''}>Inactivo</option>
            </select>
          </div>
          <div style="display:flex;gap:10px;margin-top:8px">
            <button type="submit" class="btn btn-primary">${isEdit ? 'Actualizar' : 'Crear usuario'}</button>
            <button type="button" class="btn btn-ghost" id="cancelBtn">Cancelar</button>
          </div>
        </form>
      </div>
    `;

    // Load roles and programas into dropdowns
    try {
      const [allRoles, allProgramas] = await Promise.all([
        apiCall('/roles/'),
        apiCall('/programas/').catch(() => []),
      ]);

      // Mostrar solo los 3 roles canónicos: admin, docente, estudiante
      // Aceptar tanto 'funcionario' como 'estudiante' desde la BD y mostrarlos como 'estudiante'
      const mainRoles = ['admin', 'docente', 'funcionario', 'estudiante'];
      const seen = new Set();
      const roles = [];
      for (const r of allRoles) {
        const nameLower = (r.nombre_rol || '').toLowerCase();
        if (mainRoles.includes(nameLower)) {
          // Normalizar ambos 'funcionario' y 'estudiante' a la etiqueta 'estudiante'
          const canonical = (nameLower === 'funcionario' || nameLower === 'estudiante') ? 'estudiante' : nameLower;
          if (!seen.has(canonical)) {
            seen.add(canonical);
            roles.push({ ...r, _display: canonical });
          }
        }
      }
      const sel = section.querySelector('#f-rol');
      sel.innerHTML = roles.map(r =>
        `<option value="${r.id_rol}" ${r.id_rol === (row?.id_rol ?? 3) ? 'selected' : ''}>${r._display ?? (r.nombre_rol ?? 'Sin nombre').toLowerCase()}</option>`
      ).join('');

      // Cargar programas
      const selProg = section.querySelector('#f-programa');
      if (allProgramas.length > 0) {
        selProg.innerHTML = allProgramas.map(p =>
          `<option value="${p.id_programa}" ${p.id_programa === (row?.id_programa ?? allProgramas[0].id_programa) ? 'selected' : ''}>${p.nombre_programa}</option>`
        ).join('');
      } else {
        selProg.innerHTML = '<option value="1">Programa por defecto</option>';
      }
    } catch (e) { /* keep placeholder */ }

    const back = () => this._pageUsuarios(container);
    section.querySelector('#backBtn').onclick = back;
    section.querySelector('#cancelBtn').onclick = back;

    section.querySelector('#userForm').addEventListener('submit', async e => {
      e.preventDefault();
      const data = {
        nombre: section.querySelector('#f-nombre').value,
        tipo_documento: section.querySelector('#f-tipo-doc').value,
        documento: section.querySelector('#f-documento').value,
        correo: section.querySelector('#f-correo').value,
        telefono: section.querySelector('#f-telefono').value,
        id_rol: parseInt(section.querySelector('#f-rol').value),
        id_programa: parseInt(section.querySelector('#f-programa').value) || row?.id_programa || 1,
        estado: parseInt(section.querySelector('#f-estado').value),
      };
      if (!isEdit) {
        const pw = section.querySelector('#f-password')?.value;
        if (pw) data.password_hash = pw;
      }
      try {
        if (isEdit) await apiCall(`/usuarios/${row.id_usuario}`, 'PUT', data);
        else await apiCall('/usuarios/', 'POST', data);
        window.toast?.show(isEdit ? 'Usuario actualizado' : 'Usuario creado', 'success');
        this._pageUsuarios(container);
      } catch (err) { window.toast?.show(err.message, 'error'); }
    });
  }

  async _deleteUsuario(id, el) {
    const ok = await this._modalConfirm({
      titulo: 'Eliminar Usuario',
      mensaje: '¿Estás seguro de que deseas eliminar este usuario? Esta acción no se puede deshacer.',
      labelOk: '🗑 Sí, eliminar',
      tipo: 'danger',
    });
    if (!ok) return;
    try {
      await apiCall(`/usuarios/${id}`, 'DELETE');
      window.toast?.show('Usuario eliminado', 'success');
      this._pageUsuarios(el);
    } catch (e) { window.toast?.show(e.message, 'error'); }
  }

  // =============================================================
  // SECCIÓN: GESTIÓN DE PQRS (Solo ADMIN)
  // Muestra la tabla con todas las PQRS del sistema.
  // El admin puede hacer clic en una fila para abrir el modal
  // de detalle, donde puede cambiar estado/prioridad o eliminar.
  // =============================================================
  async _pagePQRS(el) {
    el.innerHTML = `
      <div class="page-header"><h2>📋 Gestión de PQRS</h2></div>
      <div class="card">
        <div id="pqrsWrap"><p style="text-align:center;padding:24px;color:var(--text-muted)">Cargando…</p></div>
      </div>
    `;
    const wrap = el.querySelector('#pqrsWrap');
    try {
      const rows = await apiCall('/pqrs/');
      let html = `<table id="pqrsTable" class="display" style="width:100%; font-size:0.9rem">
        <thead><tr style="text-align:left"><th>ID</th><th>Radicado</th><th>Usuario ID</th><th>Tipo</th><th>Estado BD</th><th>Actualizado</th><th>Acciones</th></tr></thead>
        <tbody>`;

      rows.forEach(r => {
        const estadoBadge = `<span class="badge badge-info">ID ${r.id_estado ?? '—'}</span>`;
        const fecha = r.updated_at ? new Date(r.updated_at).toLocaleString('es-CO') : '—';
        html += `<tr>
          <td>${r.id_pqrs}</td>
          <td>${r.radicado ?? ''}</td>
          <td>${r.id_usuario ?? ''}</td>
          <td>${r.id_tipospqrs ?? ''}</td>
          <td>${estadoBadge}</td>
          <td>${fecha}</td>
          <td>
            <button class="btn btn-ghost btn-sm ver-btn" data-id="${r.id_pqrs}">👁 Ver</button>
          </td>
        </tr>`;
      });
      html += `</tbody></table>`;
      wrap.innerHTML = html;

      if (window.$ && window.$.fn.DataTable) {
        $('#pqrsTable').DataTable({ language: { url: '//cdn.datatables.net/plug-ins/1.13.6/i18n/es-ES.json' } });
      }

      wrap.querySelectorAll('.ver-btn').forEach(btn => {
        btn.onclick = () => {
          const row = rows.find(r => r.id_pqrs == btn.dataset.id);
          this._showPQRSModal(row);
        };
      });
    } catch (e) {
      wrap.innerHTML = `<p style="color:var(--danger);padding:20px">${e.message}</p>`;
    }
  }

  // =============================================================
  // MODAL: DETALLE DE UNA PQRS (Solo ADMIN al hacer clic en 'Ver')
  // Muestra toda la información de una PQRS específica.
  // ADMIN puede además:
  //   - Cambiar el estado (Pendiente, En proceso, Resuelto, etc.)
  //   - Cambiar la prioridad (Baja, Media, Alta, Urgente)
  //   - Eliminar la PQRS (borra también sus respuestas e historial)
  // =============================================================
  async _showPQRSModal(p) {
    let resps = [];
    let estados = [];
    let prioridades = [];
    let estadoActualName = '';
    let prioridadActualName = '';
    try {
      const allResps = await apiCall('/respuestas/');
      resps = allResps.filter(r => r.id_pqrs === p.id_pqrs);
      if (this._user?.rol === 'admin') {
        const allEstados = await apiCall('/estados/').catch(() => []);
        estados = allEstados.filter((v, i, a) => a.findIndex(t => (t.nombre_estado === v.nombre_estado)) === i);
        estadoActualName = allEstados.find(x => x.id_estado == p.id_estado)?.nombre_estado || '';

        const allPrioridades = await apiCall('/prioridades/').catch(() => []);
        prioridades = allPrioridades.filter((v, i, a) => a.findIndex(t => (t.nombre_prioridad === v.nombre_prioridad)) === i);
        prioridadActualName = allPrioridades.find(x => x.id_prioridad == p.id_prioridad)?.nombre_prioridad || '';
      }
    } catch (e) { /* ignore */ }

    const TIPO = { 1: 'Queja', 2: 'Petición', 3: 'Reclamo', 4: 'Sugerencia' };
    const PRIO = {
      3: '<span class="badge badge-danger">🔴 Alta</span>',
      2: '<span class="badge badge-warning">🟡 Media</span>',
      1: '<span class="badge badge-success">🟢 Baja</span>',
    };

    let estadoDisplay = '';
    if (estadoActualName) {
      const isSuccess = estadoActualName.toLowerCase().includes('resuelt');
      estadoDisplay = `<span class="badge ${isSuccess ? 'badge-success' : 'badge-warning'}">${isSuccess ? '✅ ' : '⏳ '}${estadoActualName}</span>`;
    } else {
      estadoDisplay = resps.length > 0
        ? '<span class="badge badge-success">✅ Resuelta</span>'
        : '<span class="badge badge-warning">⏳ Pendiente</span>';
    }
    const ESTADO = estadoDisplay;


    let prioridadDisplay = PRIO[p.id_prioridad] ?? '—';
    if (prioridadActualName) {
      const isAlta = prioridadActualName.toLowerCase().includes('alta') || prioridadActualName.toLowerCase().includes('urgente');
      const isMedia = prioridadActualName.toLowerCase().includes('media');
      const badgeColor = isAlta ? 'badge-danger' : (isMedia ? 'badge-warning' : 'badge-success');
      const pIcon = isAlta ? '🔴 ' : (isMedia ? '🟡 ' : '🟢 ');
      prioridadDisplay = `<span class="badge ${badgeColor}">${pIcon}${prioridadActualName}</span>`;
    }

    const modal = document.createElement('div');
    modal.style.cssText = 'position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,0.5);display:flex;align-items:center;justify-content:center;z-index:9999;padding:20px;';

    modal.innerHTML = `
      <div class="card animate-in" style="width:100%;max-width:650px;max-height:90vh;overflow-y:auto;position:relative;">
        <button id="closeModal" style="position:absolute;top:16px;right:16px;background:none;border:none;font-size:1.8rem;cursor:pointer;color:var(--text);line-height:1">&times;</button>
        <h2 style="margin-bottom:20px;padding-right:24px;">Detalle de PQRS #${p.id_pqrs}</h2>
        
        <div style="display:grid;grid-template-columns:repeat(auto-fit, minmax(200px, 1fr));gap:14px;margin-bottom:20px;font-size:0.9rem;background:var(--bg-base);padding:16px;border-radius:8px;border:1px solid var(--border)">
          <div><strong style="color:var(--text-muted);display:block;font-size:0.75rem">Radicado</strong>${p.radicado ?? '—'}</div>
          <div><strong style="color:var(--text-muted);display:block;font-size:0.75rem">Usuario Creador</strong>ID ${p.id_usuario}</div>
          <div><strong style="color:var(--text-muted);display:block;font-size:0.75rem">Tipo</strong>${TIPO[p.id_tipospqrs] ?? '—'}</div>
          <div><strong style="color:var(--text-muted);display:block;font-size:0.75rem">Prioridad</strong>${prioridadDisplay}</div>
          <div><strong style="color:var(--text-muted);display:block;font-size:0.75rem">Estado Actual</strong>${ESTADO}</div>
          <div><strong style="color:var(--text-muted);display:block;font-size:0.75rem">Fecha de Creación</strong>${p.fecha_creacion ? new Date(p.fecha_creacion).toLocaleString('es-CO') : '—'}</div>
        </div>

        ${this._user?.rol === 'admin' ? `
        <div style="margin-bottom:20px;padding:12px;background:var(--bg-elevated);border:1px solid var(--border);border-radius:8px;">
          <h4 style="margin-bottom:8px;">⚙️ Administración</h4>
          <div style="display:flex;gap:10px;align-items:flex-end;">
            <div style="flex:1">
              <label style="font-size:0.8rem;color:var(--text-muted);display:block;margin-bottom:4px">Cambiar Estado</label>
              <select id="admin-estado" style="width:100%;padding:6px;border-radius:4px;border:1px solid var(--border)">
                ${estados.length > 0 ? estados.map(e => `<option value="${e.id_estado}" ${e.nombre_estado === estadoActualName || e.id_estado == p.id_estado ? 'selected' : ''}>${e.nombre_estado}</option>`).join('') : `
                  <option value="1" ${p.id_estado == 1 ? 'selected' : ''}>Activo</option>
                  <option value="2" ${p.id_estado == 2 ? 'selected' : ''}>Inactivo</option>
                `}
              </select>
            </div>
            <div style="flex:1">
              <label style="font-size:0.8rem;color:var(--text-muted);display:block;margin-bottom:4px">Cambiar Prioridad</label>
              <select id="admin-prioridad" style="width:100%;padding:6px;border-radius:4px;border:1px solid var(--border)">
                ${prioridades.length > 0 ? prioridades.map(pr => `<option value="${pr.id_prioridad}" ${pr.nombre_prioridad === prioridadActualName || pr.id_prioridad == p.id_prioridad ? 'selected' : ''}>${pr.nombre_prioridad}</option>`).join('') : `
                  <option value="1" ${p.id_prioridad == 1 ? 'selected' : ''}>Baja</option>
                  <option value="2" ${p.id_prioridad == 2 ? 'selected' : ''}>Media</option>
                  <option value="3" ${p.id_prioridad == 3 ? 'selected' : ''}>Alta</option>
                `}
              </select>
            </div>
            <button id="admin-update-btn" class="btn btn-primary btn-sm" style="height:34px;">Actualizar</button>
            <button id="admin-delete-btn" class="btn btn-danger btn-sm" style="height:34px;">🗑 Eliminar</button>
          </div>
        </div>
        ` : ''}

        <div style="margin-bottom:20px;">
          <h4 style="margin-bottom:8px;border-bottom:1px solid var(--border);padding-bottom:4px">📝 Descripción de la Solicitud</h4>
          <p style="white-space:pre-wrap;font-size:0.9rem;margin:0;line-height:1.5">${p.descripcion ?? '—'}</p>
        </div>

        ${resps.length > 0 ? `
        <div>
          <h4 style="margin-bottom:8px;border-bottom:1px solid var(--border);padding-bottom:4px">💬 Respuestas Emitidas</h4>
          ${resps.map(r => `
            <div style="background:var(--bg-elevated);padding:14px;border-left:4px solid var(--accent);border-radius:6px;margin-bottom:10px;font-size:0.875rem">
              <p style="margin:0 0 6px;line-height:1.4">${r.mensaje}</p>
              <span style="color:var(--text-muted);font-size:0.75rem">Respondido por Usuario ID ${r.id_usuario ?? '?'} el ${r.fecha_respuesta ? new Date(r.fecha_respuesta).toLocaleString('es-CO') : ''}</span>
            </div>
          `).join('')}
        </div>
        ` : `
        <div style="background:var(--bg-base);padding:12px;border-radius:6px;border:1px dashed var(--border);text-align:center;color:var(--text-muted);font-size:0.85rem">
          Aún no hay respuestas para esta solicitud.
        </div>
        `}
      </div>
    `;

    modal.querySelector('#closeModal').onclick = () => modal.remove();
    modal.onclick = (e) => { if (e.target === modal) modal.remove(); };

    const updateBtn = modal.querySelector('#admin-update-btn');
    if (updateBtn) {
      updateBtn.onclick = async () => {
        const newEstado = parseInt(modal.querySelector('#admin-estado').value);
        const newPrioridad = parseInt(modal.querySelector('#admin-prioridad').value);
        try {
          updateBtn.disabled = true;
          updateBtn.textContent = 'Actualizando...';
          const payload = {
            ...p,
            id_estado: newEstado,
            id_prioridad: newPrioridad
          };
          // Eliminamos campos que puedan dar conflicto si no son correctos, aunque el backend exige todos
          // p ya tiene radicado, descripcion, etc.
          await apiCall(`/pqrs/update_pqrs/${p.id_pqrs}`, 'PUT', payload);
          modal.remove();
          // Modal de éxito tras actualizar PQRS
          await this._modalInfo({
            titulo: 'PQRS actualizada',
            mensaje: `La PQRS <strong>#${p.id_pqrs}</strong> fue actualizada correctamente con el nuevo estado y prioridad.`,
            tipo: 'success',
            labelOk: 'Aceptar',
          });
          this._pagePQRS(document.querySelector('#pageContent')); // Refrescar la tabla
        } catch (err) {
          window.toast?.show('Error al actualizar: ' + err.message, 'error');
          updateBtn.disabled = false;
          updateBtn.textContent = 'Actualizar';
        }
      };
    }

    const deleteBtn = modal.querySelector('#admin-delete-btn');
    if (deleteBtn) {
      deleteBtn.onclick = async () => {
        const ok = await this._modalConfirm({
          titulo: `Eliminar PQRS #${p.id_pqrs}`,
          mensaje: `¿Deseas eliminar permanentemente la PQRS con radicado <strong>${p.radicado ?? p.id_pqrs}</strong>?<br>Esta acción también borrará sus respuestas e historial y <strong>no se puede deshacer</strong>.`,
          labelOk: '🗑 Sí, eliminar',
          tipo: 'danger',
        });
        if (!ok) return;
        try {
          deleteBtn.disabled = true;
          deleteBtn.textContent = 'Eliminando...';
          await apiCall(`/pqrs/delete_pqrs/${p.id_pqrs}`, 'DELETE');
          window.toast?.show('PQRS eliminada correctamente', 'success');
          modal.remove();
          this._pagePQRS(document.querySelector('#pageContent'));
        } catch (err) {
          window.toast?.show('Error al eliminar: ' + err.message, 'error');
          deleteBtn.disabled = false;
          deleteBtn.textContent = '🗑 Eliminar';
        }
      };
    } // fin if (deleteBtn)

    document.body.appendChild(modal);
  }

  // =============================================================
  // SECCIÓN: ROLES Y PERMISOS (Solo ADMIN)
  // Muestra una vista informativa de los 3 roles del sistema
  // y qué permisos tiene cada uno.
  // =============================================================
  _pageRoles(el) {
    const rolesData = [
      {
        nombre: 'admin', label: 'Administrador', icon: '👨‍💼', color: '#6c63ff',
        desc: 'Control total del sistema: usuarios, PQRS, configuración y reportes.'
      },
      {
        nombre: 'docente', label: 'Docente', icon: '👨‍🏫', color: '#10b981',
        desc: 'Puede crear y gestionar PQRS propias y responder solicitudes.'
      },
      {
        nombre: 'estudiante', label: 'Estudiante', icon: '👨‍🎓', color: '#3b82f6',
        desc: 'Puede consultar y crear sus propias PQRS únicamente.'
      },
    ];

    const cards = rolesData.map(r => {
      const perms = ROLE_PERMISSIONS[r.nombre] ?? [];
      const permChips = perms.map(p => `<li>${p}</li>`).join('');
      return `
        <div class="role-card">
          <div class="role-name">${r.icon} ${r.label} <span class="badge badge-accent">${r.nombre}</span></div>
          <div class="role-desc">${r.desc}</div>
          <ul class="perm-list">${permChips}</ul>
        </div>
      `;
    }).join('');

    el.innerHTML = `
      <div class="page-header">
        <h2>🔑 Roles y Permisos</h2>
        <p>El sistema tiene 3 roles base — controlados con JWT. El token incluye el campo <code>rol</code>.</p>
      </div>
      <div class="role-grid">${cards}</div>
    `;
  }


  // =============================================================
  // SECCIÓN: REPORTES POWER BI (Solo ADMIN)
  // Espacio reservado para incrustar gráficas de Power BI.
  // Para activarlo: reemplazar el div placeholder con un <iframe>
  // copiado desde Power BI Service > Publicar en Web.
  // =============================================================
  _pageReportes(el) {
    el.innerHTML = `
      <div class="page-header">
        <h2>📈 Reportes e Indicadores</h2>
        <p>Análisis de PQRS — Power BI</p>
      </div>

      <div class="card" style="padding:0;overflow:hidden;">
        <div style="padding:16px 20px;border-bottom:1px solid var(--border);display:flex;align-items:center;gap:10px;">
          <span style="font-size:1.3rem">📊</span>
          <div>
            <h3 style="margin:0;font-size:1rem">Panel de Control PQRS</h3>
            <p style="margin:0;font-size:0.8rem;color:var(--text-muted)">Datos en tiempo real desde Power BI</p>
          </div>
        </div>
        <div style="position:relative;width:100%;padding-top:56.25%;">
          <iframe
            title="pqrs"
            src="https://app.powerbi.com/reportEmbed?reportId=2b7307e7-d31a-40c7-ab7a-d6ace5af1746&autoAuth=true&ctid=740be6bd-fd36-470e-94d9-0f0c777fadb9"
            frameborder="0"
            allowFullScreen="true"
            style="position:absolute;top:0;left:0;width:100%;height:100%;border:none;"
          ></iframe>
        </div>
      </div>
    `;
  }

  // =============================================================
  // SECCIÓN: NUEVA PQRS (DOCENTE + ESTUDIANTE)
  // Formulario para que el usuario cree una nueva solicitud PQRS.
  // Campos: tipo, asunto, descripción, prioridad, docente destino.
  // Si se selecciona un docente, la descripción incluye el prefijo
  // [Para docente: nombre] para que el docente la filtre en su bandeja.
  // =============================================================
  async _pageNuevaPQRS(el) {
    const rol = this._user?.rol ?? 'estudiante';
    el.innerHTML = `
      <div class="page-header"><h2>📝 Nueva PQRS</h2></div>
      <div class="card" style="max-width:600px">
        <form id="pqrsForm">
          <div class="form-group">
            <label>Tipo de solicitud</label>
            <select id="f-tipo" required>
              <option value="">— Selecciona —</option>
              <option value="1">Queja</option>
              <option value="2">Petición</option>
              <option value="3">Reclamo</option>
              <option value="4">Sugerencia</option>
            </select>
          </div>
          <div class="form-group"><label>Asunto</label><input id="f-asunto" required /></div>
          <div class="form-group"><label>Descripción detallada</label><textarea id="f-desc" rows="4" required></textarea></div>
          <div class="form-group">
            <label>Prioridad</label>
            <select id="f-prior">
              <option value="1">🟢 Baja</option>
              <option value="2" selected>🟡 Media</option>
              <option value="3">🔴 Alta</option>
            </select>
          </div>
          <div class="form-group">
            <label>👨‍🏫 Dirigido a docente (opcional)</label>
            <select id="f-docente">
              <option value="">— Sin asignar / General —</option>
              <option value="loading" disabled>Cargando docentes…</option>
            </select>
          </div>
          <div class="form-group">
            <label>📧 Correo para notificación</label>
            <input id="f-email" type="email" placeholder="tu@correo.com" value="${this._user?.correo ?? ''}" required />
            <small style="color:var(--text-muted);font-size:0.78rem;margin-top:4px;display:block">Recibirás la confirmación de tu PQRS en este correo.</small>
          </div>
          <div style="display:flex;gap:10px">
            <button type="submit" class="btn btn-primary">Enviar PQRS</button>
            <button type="reset" class="btn btn-ghost">Limpiar</button>
          </div>
        </form>
      </div>
    `;

    // Load docentes dropdown for everyone
    try {
      const docentes = await apiCall('/usuarios/by-rol/docente');
      const sel = el.querySelector('#f-docente');
      const myId = this._user?.id_usuario;
      sel.innerHTML = '<option value="">— Sin asignar / General —</option>' +
        docentes.filter(d => d.id_usuario !== myId)
          .map(d => `<option value="${d.nombre}">${d.nombre}</option>`).join('');
    } catch (e) { /* leave as-is */ }

    el.querySelector('#pqrsForm').addEventListener('submit', async e => {
      e.preventDefault();
      const docenteNombre = el.querySelector('#f-docente')?.value ?? '';
      const descBase = el.querySelector('#f-desc').value;
      const descripcion = docenteNombre
        ? `[Para docente: ${docenteNombre}]\n${descBase}`
        : descBase;

      const data = {
        id_usuario: this._user?.id_usuario,
        id_tipospqrs: parseInt(el.querySelector('#f-tipo').value),
        radicado: el.querySelector('#f-asunto').value.trim().slice(0, 80) + ' — RAD-' + Date.now(),
        descripcion,
        id_prioridad: parseInt(el.querySelector('#f-prior').value),
        id_estado: 1,
        id_dependencia: null,
      };
      try {
        await apiCall('/pqrs/create_pqrs', 'POST', data);

        // Usar el correo digitado en el formulario
        const correoUsuario = el.querySelector('#f-email')?.value || this._user?.correo || '';

        try {
          await fetch('https://api.emailjs.com/api/v1.0/email/send', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              service_id: 'service_25libn5',
              template_id: 'template_tu878js',
              user_id: 'o3tsRNH8slV7K4jTP',
              template_params: {
                name: this._user?.nombre || 'Usuario',
                title: data.radicado,
                email: correoUsuario
              }
            })
          });
          console.log('Notificación EmailJS enviada a:', correoUsuario);
        } catch (emailErr) {
          console.error('Error enviando notificación EmailJS:', emailErr);
        }

        window.toast?.show('✅ PQRS enviada exitosamente', 'success');
        this._navigate('mis-pqrs');
      } catch (err) { window.toast?.show(err.message, 'error'); }
    });
  }


  // =============================================================
  // SECCIÓN: MIS PQRS (DOCENTE + ESTUDIANTE)
  // Muestra al usuario solo sus propias PQRS.
  // Indica si cada PQRS ya fue respondida o sigue pendiente.
  // Si hay respuestas, las muestra directamente en la tarjeta.
  // =============================================================
  async _pageMisPQRS(el) {
    el.innerHTML = `
      <div class="page-header"><h2>📋 Mis PQRS</h2>
        <button class="btn btn-primary btn-sm" id="refreshBtn">🔄 Actualizar</button>
      </div>
      <div class="card">
        <div id="misPqrsWrap"><p style="text-align:center;padding:24px;color:var(--text-muted)">Cargando…</p></div>
      </div>
    `;
    el.querySelector('#refreshBtn').onclick = () => this._pageMisPQRS(el);
    const wrap = el.querySelector('#misPqrsWrap');
    try {
      const [allPqrs, allResp] = await Promise.all([
        apiCall('/pqrs/'),
        apiCall('/respuestas/').catch(() => []),
      ]);
      const myId = this._user?.id_usuario;
      const rows = allPqrs.filter(p => p.id_usuario === myId);

      if (!rows.length) {
        wrap.innerHTML = '<empty-state icon="📭" message="No tienes PQRS registradas aún"></empty-state>';
        return;
      }

      const respMap = {};
      for (const r of allResp) {
        if (!respMap[r.id_pqrs]) respMap[r.id_pqrs] = [];
        respMap[r.id_pqrs].push(r);
      }

      const PRIO = { 3: '<span class="badge badge-danger">Alta</span>', 2: '<span class="badge badge-warning">Media</span>', 1: '<span class="badge badge-success">Baja</span>' };

      wrap.innerHTML = rows.map(p => {
        const resps = respMap[p.id_pqrs] ?? [];
        const respBadge = resps.length
          ? `<span class="badge badge-success">✅ Respondida (${resps.length})</span>`
          : `<span class="badge badge-warning">⏳ Sin respuesta</span>`;
        const respSection = resps.length ? resps.map(r =>
          `<div style="margin-top:10px;padding:12px;background:#f0fdf4;border-left:3px solid var(--success);border-radius:6px;font-size:0.875rem">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px">
              <strong style="color:var(--success)">💬 Respuesta recibida</strong>
              <span style="font-size:0.75rem;color:var(--text-muted)">
                📅 ${r.fecha_respuesta ? new Date(r.fecha_respuesta).toLocaleString('es-CO') : '—'}
              </span>
            </div>
            <p style="margin:0;color:var(--text-primary)">${r.mensaje}</p>
          </div>`).join('') : '';
        return `
          <div style="border:1px solid var(--border);border-radius:var(--radius);padding:16px;margin-bottom:12px;position:relative;background:var(--bg-surface);box-shadow:var(--shadow)">
            <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:8px">
              <div>
                <strong>${p.radicado ?? 'Sin radicado'}</strong>
                <span style="margin-left:8px;font-size:0.8rem;color:var(--text-muted)">#${p.id_pqrs}</span>
              </div>
              <div style="display:flex;gap:6px;align-items:center;flex-wrap:wrap">
                ${PRIO[p.id_prioridad] ?? ''}
                ${respBadge}
                <button class="btn btn-danger btn-sm del-pqrs-btn" data-id="${p.id_pqrs}" title="Eliminar PQRS">🗑</button>
              </div>
            </div>
            <p style="margin:8px 0;font-size:0.875rem;color:var(--text-secondary)">${p.descripcion ?? '—'}</p>
            <span style="font-size:0.75rem;color:var(--text-muted)">📅 Creado: ${p.fecha_creacion ? new Date(p.fecha_creacion).toLocaleDateString('es-CO') : '—'}</span>
            ${respSection}
          </div>`;
      }).join('');

      wrap.querySelectorAll('.del-pqrs-btn').forEach(btn => {
        btn.onclick = (e) => {
          e.stopPropagation();
          this._deletePQRS(btn.dataset.id, el);
        };
      });
    } catch (e) {
      wrap.innerHTML = `<p style="color:var(--danger);padding:20px">${e.message}</p>`;
    }
  }

  // Helper para eliminar una PQRS desde la vista del usuario
  async _deletePQRS(id, el) {
    const ok = await this._modalConfirm({
      titulo: 'Eliminar PQRS',
      mensaje: '¿Estás seguro de que deseas eliminar esta PQRS? Esta acción borrará permanentemente la solicitud y no se puede deshacer.',
      labelOk: '🗑 Sí, eliminar',
      tipo: 'danger',
    });

    if (!ok) return;

    try {
      await apiCall(`/pqrs/delete_pqrs/${id}`, 'DELETE');
      window.toast?.show('PQRS eliminada con éxito', 'success');
      this._pageMisPQRS(el); // Recargar la sección
    } catch (err) {
      window.toast?.show(err.message, 'error');
    }
  }

  // =============================================================
  // SECCIÓN: PQRS RESPONDIDOS (DOCENTE)
  // Muestra todas las PQRS a las que el docente ya ha enviado
  // una respuesta. Para cada PQRS muestra la pregunta y la
  // respuesta que el docente escribió.
  // =============================================================
  async _pagePqrsRespondidos(el) {
    el.innerHTML = `
      <div class="page-header">
        <h2>✅ PQRS Respondidos</h2>
        <button class="btn btn-ghost btn-sm" id="refreshRespondidos">🔄 Actualizar</button>
      </div>
      <div class="card"><div id="respondidosWrap"><p style="text-align:center;padding:24px;color:var(--text-muted)">Cargando…</p></div></div>
    `;
    el.querySelector('#refreshRespondidos').onclick = () => this._pagePqrsRespondidos(el);
    const wrap = el.querySelector('#respondidosWrap');

    try {
      const [todasRespuestas, todasPqrs] = await Promise.all([
        apiCall('/respuestas/'),
        apiCall('/pqrs/'),
      ]);

      const myId = this._user?.id_usuario;
      const myName = (this._user?.nombre ?? '').toLowerCase();

      // Respuestas enviadas por este docente
      const misRespuestas = todasRespuestas.filter(r => r.id_usuario === myId);

      if (misRespuestas.length === 0) {
        wrap.innerHTML = `
          <div style="text-align:center;padding:48px 24px;color:var(--text-muted)">
            <div style="font-size:3rem;margin-bottom:12px">📭</div>
            <h3 style="color:var(--text-secondary);margin-bottom:6px">Sin respuestas aún</h3>
            <p>Aún no has respondido ninguna PQRS.</p>
          </div>`;
        return;
      }

      const TIPO = { 1: 'Queja', 2: 'Petición', 3: 'Reclamo', 4: 'Sugerencia' };

      const cards = misRespuestas.map(resp => {
        const pqrs = todasPqrs.find(p => p.id_pqrs === resp.id_pqrs);
        // Limpiar el prefijo [Para docente: xxx] de la descripción
        const rawDesc = pqrs?.descripcion ?? '—';
        const cleanDesc = rawDesc.replace(/^\[Para docente: [^\]]+\]\n?/i, '').trim();
        const tipoLabel = TIPO[pqrs?.id_tipospqrs] ?? '—';
        const fechaResp = resp.fecha_respuesta
          ? new Date(resp.fecha_respuesta).toLocaleString('es-CO')
          : '—';
        const fechaPqrs = pqrs?.fecha_creacion
          ? new Date(pqrs.fecha_creacion).toLocaleDateString('es-CO')
          : '—';

        return `
          <div style="border:1px solid var(--border);border-radius:var(--radius);padding:20px;margin-bottom:16px;background:var(--bg-surface);box-shadow:var(--shadow)">
            <!-- Encabezado -->
            <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:8px;margin-bottom:14px">
              <div>
                <span style="font-size:0.75rem;color:var(--text-muted);display:block;margin-bottom:4px">PQRS #${pqrs?.id_pqrs ?? resp.id_pqrs} — ${tipoLabel}</span>
                <strong style="font-size:1rem;color:var(--text-primary)">${pqrs?.radicado ?? 'Sin radicado'}</strong>
              </div>
              <div style="display:flex;gap:6px;flex-wrap:wrap;align-items:center">
                <span class="badge badge-success">✅ Respondido</span>
                <span class="badge badge-info">${tipoLabel}</span>
              </div>
            </div>

            <!-- Solicitud original -->
            <div style="background:var(--bg-elevated);border-radius:var(--radius-sm);padding:12px 14px;margin-bottom:12px;border-left:3px solid var(--accent)">
              <span style="font-size:0.73rem;font-weight:600;color:var(--accent);text-transform:uppercase;letter-spacing:0.05em;display:block;margin-bottom:6px">📝 Solicitud original</span>
              <p style="font-size:0.875rem;margin:0;line-height:1.5;color:var(--text-primary)">${cleanDesc}</p>
              <span style="font-size:0.75rem;color:var(--text-muted);display:block;margin-top:6px">Creado el ${fechaPqrs}</span>
            </div>

            <!-- Tu respuesta -->
            <div style="background:#f0fdf4;border-radius:var(--radius-sm);padding:12px 14px;border-left:3px solid var(--success)">
              <span style="font-size:0.73rem;font-weight:600;color:var(--success);text-transform:uppercase;letter-spacing:0.05em;display:block;margin-bottom:6px">💬 Tu respuesta</span>
              <p style="font-size:0.875rem;margin:0;line-height:1.5;color:var(--text-primary)">${resp.mensaje ?? '—'}</p>
              <span style="font-size:0.75rem;color:var(--text-muted);display:block;margin-top:6px">Respondido el ${fechaResp}</span>
            </div>
          </div>`;
      }).join('');

      wrap.innerHTML = `
        <p style="font-size:0.85rem;color:var(--text-muted);margin-bottom:16px">
          📋 Total respondidos: <strong>${misRespuestas.length}</strong>
        </p>
        ${cards}`;

    } catch (e) {
      wrap.innerHTML = `<p style="color:var(--danger);padding:20px">${e.message}</p>`;
    }
  }

  // =============================================================
  // SECCIÓN: TODAS LAS RESPUESTAS (Solo ADMIN)
  // Tabla completa con todas las respuestas emitidas en el sistema.
  // Muestra: PQRS, radicado, quién respondió, el mensaje,
  // la fecha y el estado actual de la PQRS.
  // Los PQRS con estado "Resuelto / Respondido / Cerrado" aparecen
  // con un badge verde; el resto con su estado real.
  // =============================================================
  async _pageRespuestas(el) {
    el.innerHTML = `
      <div class="page-header">
        <h2>💬 Todas las Respuestas</h2>
        <button class="btn btn-ghost btn-sm" id="refreshRespAdmin">🔄 Actualizar</button>
      </div>
      <div class="card">
        <div id="respAdminWrap"><p style="text-align:center;padding:24px;color:var(--text-muted)">Cargando…</p></div>
      </div>
    `;
    el.querySelector('#refreshRespAdmin').onclick = () => this._pageRespuestas(el);
    const wrap = el.querySelector('#respAdminWrap');

    try {
      const [respuestas, pqrsList, usuarios, estados] = await Promise.all([
        apiCall('/respuestas/'),
        apiCall('/pqrs/'),
        apiCall('/usuarios/').catch(() => []),
        apiCall('/estados/').catch(() => []),
      ]);

      if (respuestas.length === 0) {
        wrap.innerHTML = `
          <div style="text-align:center;padding:48px 24px;color:var(--text-muted)">
            <div style="font-size:3rem;margin-bottom:12px">📭</div>
            <h3 style="color:var(--text-secondary);margin-bottom:6px">Sin respuestas</h3>
            <p>Aún no hay respuestas registradas en el sistema.</p>
          </div>`;
        return;
      }

      // Mapas para lookup rápido
      const pqrsMap = {};
      pqrsList.forEach(p => { pqrsMap[p.id_pqrs] = p; });

      const userMap = {};
      usuarios.forEach(u => { userMap[u.id_usuario] = u.nombre; });

      // Estados únicos por nombre
      const estadoMap = {};
      estados.forEach(e => { estadoMap[e.id_estado] = e.nombre_estado; });

      const TIPO = { 1: 'Queja', 2: 'Petición', 3: 'Reclamo', 4: 'Sugerencia' };

      // Función para determinar el badge del estado de la PQRS
      const estadoBadge = (pqrs) => {
        if (!pqrs) return '<span class="badge badge-warning">⏳ Sin datos</span>';
        const nombre = (estadoMap[pqrs.id_estado] ?? '').toLowerCase();
        if (nombre.includes('resuelt') || nombre.includes('respond') || nombre.includes('cerrad')) {
          return `<span class="badge badge-success">✅ ${estadoMap[pqrs.id_estado] ?? 'Resuelto'}</span>`;
        }
        if (nombre.includes('proceso')) {
          return `<span class="badge badge-info">🔄 ${estadoMap[pqrs.id_estado] ?? 'En proceso'}</span>`;
        }
        return `<span class="badge badge-warning">⏳ ${estadoMap[pqrs.id_estado] ?? 'Pendiente'}</span>`;
      };

      // Ordenar: más recientes primero
      const sorted = [...respuestas].sort((a, b) =>
        new Date(b.fecha_respuesta ?? 0) - new Date(a.fecha_respuesta ?? 0)
      );

      let html = `
        <p style="font-size:0.85rem;color:var(--text-muted);margin-bottom:16px">
          📋 Total de respuestas: <strong>${sorted.length}</strong>
        </p>
        <table class="data-table" style="font-size:0.875rem">
          <thead>
            <tr>
              <th>#</th>
              <th>PQRS / Radicado</th>
              <th>Tipo</th>
              <th>Respondido por</th>
              <th>Mensaje</th>
              <th>Fecha Respuesta</th>
              <th>Estado PQRS</th>
            </tr>
          </thead>
          <tbody>`;

      sorted.forEach((r, i) => {
        const pqrs = pqrsMap[r.id_pqrs];
        const radicado = pqrs?.radicado ?? `PQRS #${r.id_pqrs}`;
        const tipo = TIPO[pqrs?.id_tipospqrs] ?? '—';
        const respondidoPor = userMap[r.id_usuario] ?? `ID ${r.id_usuario}`;
        const fecha = r.fecha_respuesta
          ? new Date(r.fecha_respuesta).toLocaleString('es-CO')
          : '—';
        const msgCorto = (r.mensaje ?? '—').length > 80
          ? (r.mensaje).slice(0, 80) + '…'
          : (r.mensaje ?? '—');

        html += `
          <tr>
            <td style="color:var(--text-muted)">${i + 1}</td>
            <td><strong style="font-size:0.82rem">${radicado}</strong></td>
            <td><span class="badge badge-info">${tipo}</span></td>
            <td style="font-weight:500">${respondidoPor}</td>
            <td style="max-width:260px;color:var(--text-secondary)">${msgCorto}</td>
            <td style="font-size:0.8rem;color:var(--text-muted)">${fecha}</td>
            <td>${estadoBadge(pqrs)}</td>
          </tr>`;
      });

      html += `</tbody></table>`;
      wrap.innerHTML = html;

    } catch (e) {
      wrap.innerHTML = `<p style="color:var(--danger);padding:20px">${e.message}</p>`;
    }
  }

  // ── RESPONDER PQRS (Docente) ─────────────────────────────────────────────────
  // =============================================================
  // SECCIÓN: RESPONDER PQRS (ADMIN + DOCENTE)
  // Muestra la bandeja de PQRS pendientes de respuesta.
  // • ADMIN ve solo las PQRS "generales" (sin asignar a docente)
  // • DOCENTE ve solo las PQRS dirigidas a su nombre
  //   (las que tienen [Para docente: NombreDocente] en descripción)
  // =============================================================
  async _pageResponderPQRS(el) {
    el.innerHTML = `
      <div class="page-header"><h2>💬 Responder PQRS</h2>
        <button class="btn btn-ghost btn-sm" id="refreshBtn2">🔄 Actualizar</button>
      </div>
      <div style="margin-bottom:12px;padding:10px 14px;background:var(--bg-elevated);border:1px solid var(--border-accent);border-radius:var(--radius-sm);font-size:0.85rem">
        ${this._user?.rol === 'admin'
        ? `🔵 <strong>Bandeja de Administrador</strong> — Viendo PQRS generales sin asignar a docentes`
        : `🟡 <strong>Bandeja de Docente</strong> — Viendo PQRS dirigidas específicamente a <strong>${this._user?.nombre}</strong>`}
      </div>
      <div class="card"><div id="respWrap"><p style="text-align:center;padding:24px;color:var(--text-muted)">Cargando…</p></div></div>
    `;
    el.querySelector('#refreshBtn2').onclick = () => this._pageResponderPQRS(el);
    const wrap = el.querySelector('#respWrap');
    try {
      const [allPqrs, allResp, allUsuarios] = await Promise.all([
        apiCall('/pqrs/'),
        apiCall('/respuestas/').catch(() => []),
        apiCall('/usuarios/').catch(() => []),
      ]);

      const respondedIds = new Set(allResp.map(r => r.id_pqrs));
      const pending = allPqrs.filter(p => !respondedIds.has(p.id_pqrs));

      if (!pending.length) {
        wrap.innerHTML = '<empty-state icon="🎉" message="¡No hay PQRS pendientes de respuesta!"></empty-state>';
        return;
      }

      const userMap = {};
      allUsuarios.forEach(u => { userMap[u.id_usuario] = u.nombre; });

      const myName = (this._user?.nombre ?? '').toLowerCase();
      const TIPO = { 1: 'Queja', 2: 'Petición', 3: 'Reclamo', 4: 'Sugerencia' };
      const PRIO = {
        3: '<span class="badge badge-danger">🔴 Alta</span>',
        2: '<span class="badge badge-warning">🟡 Media</span>',
        1: '<span class="badge badge-success">🟢 Baja</span>',
      };

      // Sort: ones directed to me first
      // Filter PQRS based on role
      const isAdmin = this._user?.rol === 'admin';

      const filteredPending = pending.filter(p => {
        const desc = (p.descripcion ?? '').toLowerCase();
        const hasAssignment = desc.match(/^\[para docente: ([^\]]+)\]/i);

        if (hasAssignment) {
          // Si está dirigido a un docente:
          // El Admin no lo ve (lo atiende el docente)
          if (isAdmin) return false;
          // El Docente SOLO lo ve si es su nombre
          return hasAssignment[1].trim() === myName;
        }

        // Si NO está asignado (es General):
        // Lo ve el Admin, los docentes NO.
        return isAdmin;
      });

      if (!filteredPending.length) {
        wrap.innerHTML = '<empty-state icon="🎉" message="No hay PQRS pendientes en tu bandeja"></empty-state>';
        return;
      }

      filteredPending.sort((a, b) => new Date(b.fecha_creacion) - new Date(a.fecha_creacion));

      wrap.innerHTML = filteredPending.map(p => {
        const desc = p.descripcion ?? '—';
        const isForMe = desc.toLowerCase().includes(`[para docente: ${myName}]`);
        const cleanDesc = desc.replace(/^\[Para docente:[^\]]+\]\n?/i, '');
        const creadorNombre = userMap[p.id_usuario] ?? `ID ${p.id_usuario}`;
        const borderColor = isForMe ? 'var(--accent)' : 'var(--border)';
        const badge = isForMe
          ? `<span class="badge badge-accent">🎯 Dirigida a ti</span>`
          : `<span class="badge badge-info">📬 General</span>`;

        return `
          <div style="border:2px solid ${borderColor};border-radius:var(--radius);padding:16px;margin-bottom:14px;${isForMe ? 'background:var(--bg-elevated)' : ''}" id="pqrs-${p.id_pqrs}">
            <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:8px;margin-bottom:8px">
              <div>
                ${badge}
                <strong style="margin-left:6px">${p.radicado ?? 'Sin radicado'}</strong>
                <span style="font-size:0.78rem;color:var(--text-muted);margin-left:6px">#${p.id_pqrs}</span>
              </div>
              <div style="display:flex;gap:6px;flex-wrap:wrap">
                ${PRIO[p.id_prioridad] ?? ''}
                <span class="badge badge-info">${TIPO[p.id_tipospqrs] ?? 'Tipo ' + p.id_tipospqrs}</span>
              </div>
            </div>
            <p style="margin:0 0 4px;font-size:0.875rem">${cleanDesc}</p>
            <p style="font-size:0.78rem;color:var(--text-muted)">👤 Enviado por: <strong>${creadorNombre}</strong>
              ${p.fecha_creacion ? ' · ' + new Date(p.fecha_creacion).toLocaleDateString('es-CO') : ''}</p>
            <div style="display:flex;gap:8px;margin-top:10px">
              <textarea class="resp-text" rows="2"
                style="flex:1;background:var(--bg-base);border:1px solid var(--border);border-radius:6px;padding:8px;color:inherit;resize:vertical;font-size:0.875rem"
                placeholder="Escribe tu respuesta…"></textarea>
              <button class="btn btn-primary btn-sm send-resp" data-id="${p.id_pqrs}" style="align-self:flex-end">Enviar</button>
            </div>
          </div>`;
      }).join('');

      wrap.querySelectorAll('.send-resp').forEach(btn => {
        btn.onclick = async () => {
          const card = wrap.querySelector(`#pqrs-${btn.dataset.id}`);
          const msg = card.querySelector('.resp-text').value.trim();
          if (!msg) { window.toast?.show('Escribe una respuesta primero', 'warning'); return; }
          btn.disabled = true; btn.textContent = 'Enviando…';
          try {
            const idPqrs = parseInt(btn.dataset.id);

            // 1. Guardar la respuesta
            await apiCall('/respuestas/', 'POST', {
              mensaje: msg,
              id_pqrs: idPqrs,
              id_usuario: this._user?.id_usuario,
            });

            // 2. Actualizar el estado de la PQRS a "Respondido"
            //    Buscar el id del estado "Respondido" (o similar) en la BD
            try {
              const estados = await apiCall('/estados/').catch(() => []);
              // Preferir estados con nombre exacto: Respondido > Resuelto
              const estadoRespondido = estados.find(e =>
                e.nombre_estado?.toLowerCase().includes('respond')
              ) || estados.find(e =>
                e.nombre_estado?.toLowerCase().includes('resuelt')
              );
              if (estadoRespondido) {
                // Obtener la PQRS actual para no perder sus otros campos
                const pqrsActual = await apiCall(`/pqrs/${idPqrs}`);
                await apiCall(`/pqrs/update_pqrs/${idPqrs}`, 'PUT', {
                  ...pqrsActual,
                  id_estado: estadoRespondido.id_estado,
                });
              }
            } catch (stateErr) {
              console.warn('No se pudo actualizar el estado de la PQRS:', stateErr);
            }

            window.toast?.show('✅ Respuesta enviada y PQRS marcada como Respondida', 'success');
            card.style.opacity = '0.5';
            card.style.pointerEvents = 'none';
            btn.textContent = '✓ Enviado';
          } catch (err) {
            window.toast?.show(err.message, 'error');
            btn.disabled = false; btn.textContent = 'Enviar';
          }
        };
      });
    } catch (e) {
      wrap.innerHTML = `<p style="color:var(--danger);padding:20px">${e.message}</p>`;
    }
  }

  // =============================================================
  // SECCIÓN: MI PERFIL (DOCENTE + ESTUDIANTE)
  // Muestra nombre, rol y datos del usuario autenticado.
  // Incluye botón para cambiar contraseña con _modalFormulario.
  // =============================================================
  async _pagePerfil(el) {
    const rol = this._user?.rol ?? 'estudiante';
    const cfg = ROLE_CONFIG[rol] ?? ROLE_CONFIG.estudiante;

    // Mostrar skeleton mientras se cargan los datos completos
    el.innerHTML = `
      <div class="page-header"><h2>👤 Mi Perfil</h2></div>
      <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:20px;align-items:start">
        <div class="card" style="text-align:center">
          <div style="width:80px;height:80px;border-radius:50%;background:var(--accent-dim);border:2px solid var(--border-accent);display:flex;align-items:center;justify-content:center;font-size:2rem;font-weight:700;color:var(--accent-light);margin:0 auto 14px">
            ${(this._user?.nombre ?? '?').slice(0, 2).toUpperCase()}
          </div>
          <h3 style="margin-bottom:6px">${this._user?.nombre ?? '—'}</h3>
          <p style="margin-top:4px"><span class="badge badge-accent">${cfg.label}</span></p>
          <button class="btn btn-ghost btn-sm" id="changePassBtn" style="margin-top:18px;width:100%">🔒 Cambiar contraseña</button>
        </div>
        <div class="card">
          <h4 style="margin-bottom:16px;padding-bottom:10px;border-bottom:1px solid var(--border)">📋 Datos de la cuenta</h4>
          <div id="perfilDatos" style="display:flex;flex-direction:column;gap:14px;font-size:0.9rem">
            <p style="color:var(--text-muted)">Cargando datos…</p>
          </div>
        </div>
      </div>
    `;

    // Cargar datos completos del usuario desde la API
    try {
      const userData = await apiCall(`/usuarios/${this._user?.id_usuario}`);
      // Enriquecer this._user con los datos completos para que EmailJS los use
      this._user = { ...this._user, ...userData };

      el.querySelector('#perfilDatos').innerHTML = `
        <div>
          <span style="color:var(--text-muted);font-size:0.75rem;display:block;margin-bottom:2px">CORREO ELECTRÓNICO</span>
          <strong>${userData.correo ?? '—'}</strong>
        </div>
        <div>
          <span style="color:var(--text-muted);font-size:0.75rem;display:block;margin-bottom:2px">DOCUMENTO</span>
          <strong>${userData.tipo_documento ?? ''} ${userData.documento ?? '—'}</strong>
        </div>
        <div>
          <span style="color:var(--text-muted);font-size:0.75rem;display:block;margin-bottom:2px">TELÉFONO</span>
          <strong>${userData.telefono ?? '—'}</strong>
        </div>
        <div>
          <span style="color:var(--text-muted);font-size:0.75rem;display:block;margin-bottom:2px">ROL</span>
          <span class="badge badge-accent">${cfg.label}</span>
        </div>
      `;
    } catch (e) {
      el.querySelector('#perfilDatos').innerHTML = `<p style="color:var(--danger)">Error cargando datos: ${e.message}</p>`;
    }

    // ── Botón cambiar contraseña → abre _modalFormulario ──────────
    el.querySelector('#changePassBtn').onclick = () => {
      this._modalFormulario({
        titulo: '🔒 Cambiar Contraseña',
        campos: [
          { id: 'pass_nueva', label: 'Nueva contraseña', type: 'password', placeholder: 'Mínimo 6 caracteres', required: true },
          { id: 'pass_confirm', label: 'Confirmar contraseña', type: 'password', placeholder: 'Repite la contraseña', required: true },
        ],
        labelOk: 'Guardar contraseña',
        onSubmit: async (formData) => {
          if (formData.pass_nueva.length < 6) throw new Error('La contraseña debe tener al menos 6 caracteres.');
          if (formData.pass_nueva !== formData.pass_confirm) throw new Error('Las contraseñas no coinciden.');
          await apiCall(`/usuarios/${this._user?.id_usuario}/password`, 'PUT', {
            password: formData.pass_nueva,
          });
          await this._modalInfo({
            titulo: '¡Contraseña actualizada!',
            mensaje: 'Tu contraseña fue cambiada exitosamente. Úsala la próxima vez que inicies sesión.',
            tipo: 'success',
            labelOk: 'Perfecto',
          });
        },
      });
    };
  }

  // =============================================================
  // MODALES REUTILIZABLES
  // Cuatro tipos de ventanas modales premium para el dashboard:
  //   1. _modalConfirm()    → Confirmación de acciones destructivas
  //   2. _modalInfo()       → Éxito / Información general
  //   3. _modalWarning()    → Advertencia con detalle
  //   4. _modalFormulario() → Formulario rápido (ej: cambiar contraseña)
  // Todos retornan una Promesa que se resuelve cuando el usuario
  // interactúa con el modal (aceptar / cancelar / cerrar).
  // =============================================================

  /**
   * Modal 1 — CONFIRMACIÓN
   * Abre un modal de confirmación y retorna true si el usuario confirma.
   * @param {Object} opts - { titulo, mensaje (HTML), labelOk, labelCancel, tipo }
   * @returns {Promise<boolean>}
   */
  _modalConfirm({ titulo = 'Confirmar', mensaje = '¿Estás seguro?', labelOk = 'Aceptar', labelCancel = 'Cancelar', tipo = 'danger' } = {}) {
    return new Promise(resolve => {
      const palette = tipo === 'danger'
        ? { accent: '#ef4444', dim: 'rgba(239,68,68,0.12)', icon: '⚠️' }
        : { accent: '#6c63ff', dim: 'rgba(108,99,255,0.12)', icon: '❓' };

      const overlay = document.createElement('div');
      overlay.className = 'modal-overlay';
      overlay.innerHTML = `
        <div class="modal-box modal-confirm" role="dialog" aria-modal="true">
          <div class="modal-icon-ring" style="background:${palette.dim};color:${palette.accent}">${palette.icon}</div>
          <h3 class="modal-title">${titulo}</h3>
          <p class="modal-body">${mensaje}</p>
          <div class="modal-actions">
            <button class="btn btn-ghost" id="mCancelBtn">${labelCancel}</button>
            <button class="btn modal-ok-btn" id="mOkBtn" style="background:${palette.accent};color:#fff">${labelOk}</button>
          </div>
        </div>
      `;
      document.body.appendChild(overlay);
      requestAnimationFrame(() => overlay.classList.add('modal-visible'));

      const close = (val) => {
        overlay.classList.remove('modal-visible');
        overlay.addEventListener('transitionend', () => overlay.remove(), { once: true });
        resolve(val);
      };

      overlay.querySelector('#mOkBtn').onclick = () => close(true);
      overlay.querySelector('#mCancelBtn').onclick = () => close(false);
      overlay.onclick = (e) => { if (e.target === overlay) close(false); };
    });
  }

  /**
   * Modal 2 — INFORMACIÓN / ÉXITO
   * Muestra un modal informativo con ícono de éxito o informativo.
   * @param {Object} opts - { titulo, mensaje (HTML), tipo ('success'|'info'), labelOk }
   * @returns {Promise<void>}
   */
  _modalInfo({ titulo = 'Información', mensaje = '', tipo = 'success', labelOk = 'Entendido' } = {}) {
    return new Promise(resolve => {
      const palette = tipo === 'success'
        ? { accent: '#10b981', dim: 'rgba(16,185,129,0.12)', icon: '✅' }
        : { accent: '#3b82f6', dim: 'rgba(59,130,246,0.12)', icon: 'ℹ️' };

      const overlay = document.createElement('div');
      overlay.className = 'modal-overlay';
      overlay.innerHTML = `
        <div class="modal-box modal-info" role="dialog" aria-modal="true">
          <div class="modal-icon-ring" style="background:${palette.dim};color:${palette.accent}">${palette.icon}</div>
          <h3 class="modal-title">${titulo}</h3>
          <p class="modal-body">${mensaje}</p>
          <div class="modal-actions modal-actions-center">
            <button class="btn modal-ok-btn" id="mOkBtn" style="background:${palette.accent};color:#fff">${labelOk}</button>
          </div>
        </div>
      `;
      document.body.appendChild(overlay);
      requestAnimationFrame(() => overlay.classList.add('modal-visible'));

      const close = () => {
        overlay.classList.remove('modal-visible');
        overlay.addEventListener('transitionend', () => overlay.remove(), { once: true });
        resolve();
      };

      overlay.querySelector('#mOkBtn').onclick = close;
      overlay.onclick = (e) => { if (e.target === overlay) close(); };
    });
  }

  /**
   * Modal 3 — ADVERTENCIA
   * Muestra un modal de advertencia con detalle expandible.
   * @param {Object} opts - { titulo, mensaje (HTML), detalle, labelOk, labelCancel }
   * @returns {Promise<boolean>}
   */
  _modalWarning({ titulo = 'Advertencia', mensaje = '', detalle = '', labelOk = 'Continuar', labelCancel = 'Cancelar' } = {}) {
    return new Promise(resolve => {
      const overlay = document.createElement('div');
      overlay.className = 'modal-overlay';
      overlay.innerHTML = `
        <div class="modal-box modal-warning" role="dialog" aria-modal="true">
          <div class="modal-icon-ring" style="background:rgba(245,158,11,0.12);color:#f59e0b">🚨</div>
          <h3 class="modal-title">${titulo}</h3>
          <p class="modal-body">${mensaje}</p>
          ${detalle ? `
          <details class="modal-detail" style="margin-top:12px;font-size:0.82rem;color:var(--text-muted);background:var(--bg-base);border:1px solid var(--border);border-radius:8px;padding:10px 14px">
            <summary style="cursor:pointer;font-weight:600">Ver detalle técnico</summary>
            <pre style="margin-top:8px;white-space:pre-wrap;font-size:0.78rem">${detalle}</pre>
          </details>` : ''}
          <div class="modal-actions">
            <button class="btn btn-ghost" id="mCancelBtn">${labelCancel}</button>
            <button class="btn modal-ok-btn" id="mOkBtn" style="background:#f59e0b;color:#fff">${labelOk}</button>
          </div>
        </div>
      `;
      document.body.appendChild(overlay);
      requestAnimationFrame(() => overlay.classList.add('modal-visible'));

      const close = (val) => {
        overlay.classList.remove('modal-visible');
        overlay.addEventListener('transitionend', () => overlay.remove(), { once: true });
        resolve(val);
      };

      overlay.querySelector('#mOkBtn').onclick = () => close(true);
      overlay.querySelector('#mCancelBtn').onclick = () => close(false);
      overlay.onclick = (e) => { if (e.target === overlay) close(false); };
    });
  }

  /**
   * Modal 4 — FORMULARIO RÁPIDO
   * Muestra un modal con campos de formulario dinámicos.
   * @param {Object} opts
   *   titulo    - Título del modal
   *   campos    - Array de { id, label, type, placeholder, required, value }
   *   labelOk   - Texto del botón de envío
   *   onSubmit  - async fn(data) llamada con { id: value } de cada campo
   * @returns {Promise<void>}
   */
  _modalFormulario({ titulo = 'Formulario', campos = [], labelOk = 'Guardar', onSubmit = async () => { } } = {}) {
    return new Promise(resolve => {
      const camposHTML = campos.map(c => `
        <div class="form-group">
          <label for="mf-${c.id}">${c.label}${c.required ? ' <span style="color:#ef4444">*</span>' : ''}</label>
          ${c.type === 'textarea'
          ? `<textarea id="mf-${c.id}" rows="3" placeholder="${c.placeholder ?? ''}" ${c.required ? 'required' : ''}>${c.value ?? ''}</textarea>`
          : `<input id="mf-${c.id}" type="${c.type ?? 'text'}" placeholder="${c.placeholder ?? ''}" value="${c.value ?? ''}" ${c.required ? 'required' : ''} />`
        }
        </div>
      `).join('');

      const overlay = document.createElement('div');
      overlay.className = 'modal-overlay';
      overlay.innerHTML = `
        <div class="modal-box modal-form" role="dialog" aria-modal="true">
          <button class="modal-close-x" id="mCloseX" aria-label="Cerrar">&times;</button>
          <h3 class="modal-title" style="margin-bottom:20px">${titulo}</h3>
          <form id="mForm" novalidate>
            ${camposHTML}
            <div class="modal-actions" style="margin-top:20px">
              <button type="button" class="btn btn-ghost" id="mCancelBtn">Cancelar</button>
              <button type="submit" class="btn btn-primary" id="mOkBtn">${labelOk}</button>
            </div>
          </form>
        </div>
      `;
      document.body.appendChild(overlay);
      requestAnimationFrame(() => overlay.classList.add('modal-visible'));

      const close = () => {
        overlay.classList.remove('modal-visible');
        overlay.addEventListener('transitionend', () => overlay.remove(), { once: true });
        resolve();
      };

      overlay.querySelector('#mCloseX').onclick = close;
      overlay.querySelector('#mCancelBtn').onclick = close;
      overlay.onclick = (e) => { if (e.target === overlay) close(); };

      overlay.querySelector('#mForm').addEventListener('submit', async e => {
        e.preventDefault();
        const okBtn = overlay.querySelector('#mOkBtn');
        const data = {};
        campos.forEach(c => { data[c.id] = overlay.querySelector(`#mf-${c.id}`)?.value ?? ''; });
        try {
          okBtn.disabled = true;
          okBtn.textContent = 'Guardando…';
          await onSubmit(data);
          close();
        } catch (err) {
          window.toast?.show(err.message || 'Error al guardar', 'error');
          okBtn.disabled = false;
          okBtn.textContent = labelOk;
        }
      });
    });
  }

  // =============================================================
  // TEMPORIZADOR JWT — Cuenta regresiva visible en la navbar
  // Avisa al usuario cuando quedan menos de 10 minutos (amarillo)
  // y menos de 5 minutos (rojo). Al llegar a 0 hace logout auto.
  // =============================================================
  _startTimer() {
    clearInterval(this._timer);
    this._warnedExpiry = false; // bandera para mostrar el modal de advertencia solo una vez
    this._timer = setInterval(() => {
      const remaining = Math.floor((this._expiresAt - Date.now()) / 1000);
      const badge = this.querySelector('#timerBadge');
      if (!badge) return;

      if (remaining <= 0) {
        clearInterval(this._timer);
        // Modal de advertencia: sesión expirada
        this._modalWarning({
          titulo: 'Sesión expirada',
          mensaje: 'Tu sesión JWT ha expirado. Serás redirigido al inicio de sesión automáticamente.',
          labelOk: 'Entendido',
          labelCancel: '',
        }).then(() => logout());
        return;
      }

      // Mostrar _modalWarning una sola vez cuando quedan 5 minutos
      if (remaining <= 300 && !this._warnedExpiry) {
        this._warnedExpiry = true;
        this._modalWarning({
          titulo: '⏳ Sesión por expirar',
          mensaje: 'Tu sesión expirará en menos de <strong>5 minutos</strong>. Guarda tu trabajo o renueva el acceso cerrando sesión y volviendo a ingresar.',
          detalle: `Token expira: ${new Date(this._expiresAt).toLocaleString('es-CO')}`,
          labelOk: 'Entendido',
          labelCancel: 'Cerrar sesión ahora',
        }).then(continuar => { if (!continuar) logout(); });
      }

      const m = String(Math.floor(remaining / 60)).padStart(2, '0');
      const s = String(remaining % 60).padStart(2, '0');
      badge.textContent = `⏱ ${m}:${s}`;
      badge.className = 'token-timer' + (remaining < 300 ? ' danger' : remaining < 600 ? ' warning' : '');
    }, 1000);
  }

  // Decodifica el token JWT para leer su payload (sin verificar firma)
  _decodeToken() {
    try {
      const parts = (this._token ?? '').split('.');
      return JSON.parse(atob(parts[1]));
    } catch { return null; }
  }

  // Limpiar el intervalo del timer al quitar el componente del DOM
  disconnectedCallback() {
    clearInterval(this._timer);
  }
}

// Registrar el componente como <app-dashboard> en el DOM
customElements.define('app-dashboard', AppDashboard);
