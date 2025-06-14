// mapa.js
document.addEventListener('DOMContentLoaded', function () {
    const map = L.map('map').setView([-17.3833, -66.1667], 12); // Coordenadas iniciales
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
    }).addTo(map);

    const puntosData = JSON.parse(document.getElementById('initial-puntos-data').textContent);
    const modal = document.getElementById('reciclajeModal');
    const closeButton = document.querySelector('.close-button');
    const tipoSelect = document.getElementById('tipo');
    const idPuntoInput = document.getElementById('id_punto');

    // Añadir marcadores
    puntosData.forEach(punto => {
        L.marker([punto.latitud, punto.longitud])
            .addTo(map)
            .bindPopup(`<b>${punto.nombre}</b><br><button onclick="openModal(${punto.id_punto_reciclaje}, '${punto.nombre}')">Registrar</button>`)
            .on('click', () => openModal(punto.id_punto_reciclaje, punto.nombre));
    });

    // Función para abrir el modal y actualizar materiales
    window.openModal = function (puntoId, puntoNombre) {
        idPuntoInput.value = puntoId;
        document.querySelector('.modal h2').textContent = `Registrar en ${puntoNombre}`;
        updateMateriales(puntoId);
        modal.style.display = 'block';
    };

    // Cerrar modal
    closeButton.onclick = function () {
        modal.style.display = 'none';
    };

    window.onclick = function (event) {
        if (event.target == modal) {
            modal.style.display = 'none';
        }
    };

    // Función para actualizar materiales
    function updateMateriales(puntoId) {
        fetch(`/get_materiales_punto/${puntoId}/`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                tipoSelect.innerHTML = '<option value="">Seleccione</option>';
                data.forEach(material => {
                    const option = document.createElement('option');
                    option.value = material[0]; // id_material_reciclable
                    option.textContent = material[1]; // nombre
                    tipoSelect.appendChild(option);
                });
            })
            .catch(error => {
                console.error('Error fetching materiales:', error);
                tipoSelect.innerHTML = '<option value="">Error al cargar materiales</option>';
            });
    }
});