// static/js/admin_rol.js
let permisosSeleccionadosEdit = [];
let permisosSeleccionadosAdd = [];

function redirigirBitacora(url) {
  if (url) {
    window.location.href = url;
  }
}

function openEditModal(id, nombre, descripcion, permisos) {
  document.getElementById('adminRolesEditId').value = id;
  document.getElementById('adminRolesEditNombre').value = nombre;
  document.getElementById('adminRolesEditDescripcion').value = descripcion;
  
  permisosSeleccionadosEdit = permisos ? permisos.split(', ').map(p => {
    for (let key in permisos_disponibles_dict) {
      if (permisos_disponibles_dict[key].trim() === p.trim()) return key;
    }
    return null;
  }).filter(p => p && p !== 'null') : [];
  
  updatePermisosList('edit');

  const modal = document.getElementById('adminRolesEditModal');
  modal.classList.add('active');
}

function closeEditModal() {
  const modal = document.getElementById('adminRolesEditModal');
  modal.classList.remove('active');
  permisosSeleccionadosEdit = [];
  updatePermisosList('edit');
}

function openAddModal() {
  document.getElementById('adminRolesAddNombre').value = '';
  document.getElementById('adminRolesAddDescripcion').value = '';
  permisosSeleccionadosAdd = [];
  updatePermisosList('add');
  const modal = document.getElementById('adminRolesAddModal');
  modal.classList.add('active');
}

function closeAddModal() {
  const modal = document.getElementById('adminRolesAddModal');
  modal.classList.remove('active');
}

function openAddPermisoModal() {
  document.getElementById('adminPermisosAddNombre').value = '';
  const modal = document.getElementById('adminPermisosAddModal');
  modal.classList.add('active');
}

function closeAddPermisoModal() {
  const modal = document.getElementById('adminPermisosAddModal');
  modal.classList.remove('active');
}

function openEditPermisoModal(id, nombre) {
  document.getElementById('adminPermisosEditId').value = id;
  document.getElementById('adminPermisosEditNombre').value = nombre;
  const modal = document.getElementById('adminPermisosEditModal');
  modal.classList.add('active');
}

function closeEditPermisoModal() {
  const modal = document.getElementById('adminPermisosEditModal');
  modal.classList.remove('active');
}

function addPermiso(mode) {
  let permisoSelect;
  if (mode === 'add') {
    permisoSelect = document.getElementById('adminRolesAddPermisoAdd');
  } else if (mode === 'edit') {
    permisoSelect = document.getElementById('adminRolesAddPermisoEdit');
  }

  setTimeout(() => {
    let permisoId = permisoSelect.value;
    const permisosSeleccionados = mode === 'edit' ? permisosSeleccionadosEdit : permisosSeleccionadosAdd;

    if (permisoId && !permisosSeleccionados.includes(permisoId)) {
      permisosSeleccionados.push(permisoId);
      updatePermisosList(mode);
      console.log(`Añadido permiso ID: ${permisoId}, Modo: ${mode}, Lista actual:`, permisosSeleccionados);
    } else {
      console.log(`No se añadió permiso. ID: ${permisoId}, Ya existe: ${permisosSeleccionados.includes(permisoId)}, Lista actual:`, permisosSeleccionados);
    }
    permisoSelect.value = ''; // Reiniciar a la opción por defecto
  }, 100);
}

window.onload = function() {
  const permisoSelectAdd = document.getElementById('adminRolesAddPermisoAdd');
  const permisoSelectEdit = document.getElementById('adminRolesAddPermisoEdit');
  if (permisoSelectAdd) {
    permisoSelectAdd.onchange = function() {
      console.log('Valor seleccionado al cambiar (Añadir):', this.value, 'Índice:', this.selectedIndex);
    };
  }
  if (permisoSelectEdit) {
    permisoSelectEdit.onchange = function() {
      console.log('Valor seleccionado al cambiar (Editar):', this.value, 'Índice:', this.selectedIndex);
    };
  }

  window.onclick = function(event) {
    const editModal = document.getElementById('adminRolesEditModal');
    const addModal = document.getElementById('adminRolesAddModal');
    const addPermisoModal = document.getElementById('adminPermisosAddModal');
    const editPermisoModal = document.getElementById('adminPermisosEditModal');
    if (event.target == editModal) {
      editModal.classList.remove('active');
      permisosSeleccionadosEdit = [];
      updatePermisosList('edit');
    }
    if (event.target == addModal) {
      addModal.classList.remove('active');
    }
    if (event.target == addPermisoModal) {
      addPermisoModal.classList.remove('active');
    }
    if (event.target == editPermisoModal) {
      editPermisoModal.classList.remove('active');
    }
  };
};

function removePermiso(permisoId, mode) {
  if (mode === 'edit') {
    permisosSeleccionadosEdit = permisosSeleccionadosEdit.filter(p => p !== permisoId);
    updatePermisosList('edit');
  } else {
    permisosSeleccionadosAdd = permisosSeleccionadosAdd.filter(p => p !== permisoId);
    updatePermisosList('add');
  }
}

function updatePermisosList(mode) {
  const permisosList = document.getElementById(mode === 'edit' ? 'adminRolesPermisosList' : 'adminRolesAddPermisosList');
  const permisosHidden = document.getElementById(mode === 'edit' ? 'adminRolesPermisosHidden' : 'adminRolesAddPermisosHidden');
  const permisosSeleccionados = mode === 'edit' ? permisosSeleccionadosEdit : permisosSeleccionadosAdd;

  permisosList.innerHTML = '';
  permisosSeleccionados.forEach(permisoId => {
    const permisoNombre = permisos_disponibles_dict[permisoId] || 'Permiso desconocido';
    const tag = document.createElement('span');
    tag.className = 'admin-usuarios-permiso-tag';
    tag.innerHTML = `
      ${permisoNombre}
      <span class="admin-usuarios-permiso-remove" onclick="removePermiso('${permisoId}', '${mode}')">×</span>
    `;
    permisosList.appendChild(tag);
  });
  permisosHidden.value = permisosSeleccionados.join(',');
  console.log(`Campo oculto actualizado (${mode}):`, permisosHidden.value);
}

function deletePermiso(permisoId) {
  if (confirm('¿Estás seguro de que quieres eliminar este permiso? Esto también eliminará su asignación a roles.')) {
    const form = document.createElement('form');
    form.method = 'post';
    form.action = '/admin-roles/';
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').cloneNode();
    const actionInput = document.createElement('input');
    actionInput.type = 'hidden';
    actionInput.name = 'action';
    actionInput.value = 'delete_permiso';
    const idInput = document.createElement('input');
    idInput.type = 'hidden';
    idInput.name = 'id_permiso';
    idInput.value = permisoId;
    form.appendChild(csrfToken);
    form.appendChild(actionInput);
    form.appendChild(idInput);
    document.body.appendChild(form);
    form.submit();
  }
}

function deleteRol(rolId) {
  if (confirm('¿Estás seguro de que quieres eliminar este rol? Esto también eliminará sus asignaciones de permisos.')) {
    const form = document.createElement('form');
    form.method = 'post';
    form.action = '/admin-roles/';
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').cloneNode();
    const actionInput = document.createElement('input');
    actionInput.type = 'hidden';
    actionInput.name = 'action';
    actionInput.value = 'delete';
    const idInput = document.createElement('input');
    idInput.type = 'hidden';
    idInput.name = 'id_rol';
    idInput.value = rolId;
    form.appendChild(csrfToken);
    form.appendChild(actionInput);
    form.appendChild(idInput);
    document.body.appendChild(form);
    form.submit();
  }
}