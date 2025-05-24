// reciclaje/static/js/scripts.js
document.addEventListener('DOMContentLoaded', function() {
  // Validar formulario de reciclaje
  const reciclajeForm = document.getElementById('reciclaje-form');
  reciclajeForm.addEventListener('submit', function(event) {
      const cantidadKg = document.getElementById('cantidad_kg').value;
      if (cantidadKg <= 0) {
          event.preventDefault();
          alert('La cantidad debe ser mayor que 0.');
      }
  });

  // Validar formulario de usuario
  const usuarioForm = document.getElementById('usuario-form');
  usuarioForm.addEventListener('submit', function(event) {
      const telefono = document.getElementById('telefono').value;
      const contraseña = document.getElementById('contraseña').value;

      if (telefono.length !== 10) {
          event.preventDefault();
          alert('El teléfono debe tener 10 dígitos.');
      }

      if (contraseña.length < 6) {
          event.preventDefault();
          alert('La contraseña debe tener al menos 6 caracteres.');
      }
  });
});