let mapAdd, mapEdit, markerAdd, markerEdit;

function initializeMapAdd() {
  if (!mapAdd) {
    const container = document.getElementById('mapAdminAdd');
    if (!container) return; // Evitar errores si el contenedor no existe
    container.style.visibility = 'hidden';
    mapAdd = L.map('mapAdminAdd', { zoomControl: false, attributionControl: false }).setView([-17.3833, -66.1567], 12);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { maxZoom: 19 }).addTo(mapAdd);
    markerAdd = L.marker([-17.3833, -66.1567], { icon: L.icon({ iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png', iconSize: [25, 41], iconAnchor: [12, 41] }) }).addTo(mapAdd);
    mapAdd.on('click', function (e) {
      const latlng = e.latlng;
      mapAdd.panTo(latlng); // Centrar el mapa en el clic
      markerAdd.setLatLng(latlng);
      document.getElementById('adminPuntosAddLatitud').value = latlng.lat.toFixed(4);
      document.getElementById('adminPuntosAddLongitud').value = latlng.lng.toFixed(4);
    });
    setTimeout(() => {
      mapAdd.invalidateSize();
      container.style.visibility = 'visible';
    }, 100); // Pequeño retraso para asegurar el renderizado
  } else {
    mapAdd.invalidateSize();
  }
}

function initializeMapEdit(lat, lng) {
  if (!mapEdit) {
    const container = document.getElementById('mapAdminEdit');
    if (!container) return;
    container.style.visibility = 'hidden';
    mapEdit = L.map('mapAdminEdit', { zoomControl: false, attributionControl: false }).setView([lat, lng], 12);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { maxZoom: 19 }).addTo(mapEdit);
    markerEdit = L.marker([lat, lng], { icon: L.icon({ iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png', iconSize: [25, 41], iconAnchor: [12, 41] }) }).addTo(mapEdit);
    mapEdit.on('click', function (e) {
      const latlng = e.latlng;
      mapEdit.panTo(latlng);
      markerEdit.setLatLng(latlng);
      document.getElementById('adminPuntosEditLatitud').value = latlng.lat.toFixed(4);
      document.getElementById('adminPuntosEditLongitud').value = latlng.lng.toFixed(4);
    });
    setTimeout(() => {
      mapEdit.invalidateSize();
      container.style.visibility = 'visible';
    }, 100);
  } else {
    mapEdit.setView([lat, lng], 12);
    markerEdit.setLatLng([lat, lng]);
    mapEdit.invalidateSize();
  }
}

function searchLocationAdd() {
  const query = document.getElementById('adminPuntosAddSearch').value;
  fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(query)}`)
    .then(response => response.json())
    .then(data => {
      if (data.length > 0) {
        const { lat, lon } = data[0];
        mapAdd.setView([lat, lon], 15);
        markerAdd.setLatLng([lat, lon]);
        document.getElementById('adminPuntosAddLatitud').value = lat;
        document.getElementById('adminPuntosAddLongitud').value = lon;
      } else {
        alert('No se encontraron resultados.');
      }
    })
    .catch(error => console.error('Error en la búsqueda:', error));
}

function searchLocationEdit() {
  const query = document.getElementById('adminPuntosEditSearch').value;
  fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(query)}`)
    .then(response => response.json())
    .then(data => {
      if (data.length > 0) {
        const { lat, lon } = data[0];
        mapEdit.setView([lat, lon], 15);
        markerEdit.setLatLng([lat, lon]);
        document.getElementById('adminPuntosEditLatitud').value = lat;
        document.getElementById('adminPuntosEditLongitud').value = lon;
      } else {
        alert('No se encontraron resultados.');
      }
    })
    .catch(error => console.error('Error en la búsqueda:', error));
}

window.openAddModal = function () {
  document.getElementById('adminPuntosAddNombre').value = '';
  document.getElementById('adminPuntosAddCapacidad').value = '0';
  document.getElementById('adminPuntosAddHoraApertura').value = '08:00';
  document.getElementById('adminPuntosAddHoraCierre').value = '18:00';
  document.getElementById('adminPuntosAddLatitud').value = '-17.3833';
  document.getElementById('adminPuntosAddLongitud').value = '-66.1567';
  document.getElementById('adminPuntosAddEstado').value = 'Disponible';
  document.querySelectorAll('#adminPuntosAddModal input[name="materiales"]').forEach(checkbox => checkbox.checked = false);
  document.querySelectorAll('#adminPuntosAddModal input[name="condiciones"]').forEach(input => input.value = '');

  initializeMapAdd();
  document.getElementById('adminPuntosAddModal').classList.add('active');
};

window.closeAddModal = function () {
  document.getElementById('adminPuntosAddModal').classList.remove('active');
};

window.openEditModal = function (id, nombre, capacidad, hora_apertura, hora_cierre, latitud, longitud, estado, material_conditions) {
  document.getElementById('adminPuntosEditId').value = id;
  document.getElementById('adminPuntosEditNombre').value = nombre;
  document.getElementById('adminPuntosEditCapacidad').value = capacidad;
  document.getElementById('adminPuntosEditHoraApertura').value = hora_apertura;
  document.getElementById('adminPuntosEditHoraCierre').value = hora_cierre;
  document.getElementById('adminPuntosEditLatitud').value = latitud;
  document.getElementById('adminPuntosEditLongitud').value = longitud;
  document.getElementById('adminPuntosEditEstado').value = estado;
  const materialConditionsMap = material_conditions ? material_conditions.split(',').reduce((map, item) => {
    const [matId, cond] = item.split(':');
    map[matId] = cond;
    return map;
  }, {}) : {};
  const checkboxes = document.querySelectorAll('#adminPuntosEditModal input[name="materiales"]');
  const conditionInputs = document.querySelectorAll('#adminPuntosEditModal input[name="condiciones"]');
  checkboxes.forEach((checkbox, index) => {
    checkbox.checked = materialConditionsMap[checkbox.value] !== undefined;
    conditionInputs[index].value = materialConditionsMap[checkbox.value] || '';
  });

  initializeMapEdit(latitud, longitud);
  document.getElementById('adminPuntosEditModal').classList.add('active');
};

window.closeEditModal = function () {
  document.getElementById('adminPuntosEditModal').classList.remove('active');
};