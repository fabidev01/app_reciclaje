document.addEventListener('DOMContentLoaded', function() {
  // Animación de scroll al hacer clic en la navegación
  document.querySelectorAll('.main-nav a').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute('href'));
      target.scrollIntoView({ behavior: 'smooth' });
      setTimeout(() => target.classList.add('visible'), 100); // Añadir clase visible tras el scroll
    });
  });

  // Mostrar fecha actual
  const currentDate = new Date().toLocaleDateString('es-ES', { year: 'numeric', month: 'long', day: 'numeric' });
  document.getElementById('currentDate').textContent = currentDate;

  // Simular datos desde Impacto_Ambiental_Diario (reemplazar con fetch si hay API)
  const environmentalData = [
    { material: 'Plástico', cantidad_reciclada: 2.0, co2_reducido: 1.0, fecha: '01/03/2025' },
    { material: 'Metal', cantidad_reciclada: 1.5, co2_reducido: 0.3, fecha: '02/03/2025' },
    { material: 'Vidrio', cantidad_reciclada: 3.0, co2_reducido: 2.4, fecha: '03/03/2025' },
    { material: 'Papel', cantidad_reciclada: 1.0, co2_reducido: 1.0, fecha: '04/03/2025' },
    { material: 'Cartón', cantidad_reciclada: 2.5, co2_reducido: 0.75, fecha: '05/03/2025' }
  ];

  // Calcular estadísticas
  const totalKg = environmentalData.reduce((sum, item) => sum + item.cantidad_reciclada, 0);
  const totalCO2 = environmentalData.reduce((sum, item) => sum + item.co2_reducido, 0);
  const bestMaterial = environmentalData.reduce((max, item) => max.cantidad_reciclada > item.cantidad_reciclada ? max : item, environmentalData[0]);
  const dailyGoal = 10.0; // Meta diaria en kg (ajustable)
  const progress = (totalKg / dailyGoal) * 100;

  // Actualizar DOM
  document.getElementById('totalRecycled').textContent = totalKg.toFixed(2) + ' Kg';
  document.getElementById('totalCO2').textContent = totalCO2.toFixed(2) + ' Kg';
  document.getElementById('totalKgTable').textContent = totalKg.toFixed(2);
  document.getElementById('totalCO2Table').textContent = totalCO2.toFixed(2);
  document.getElementById('bestMaterial').textContent = bestMaterial.material;
  document.getElementById('bestTrend').textContent = '↑ ' + bestMaterial.cantidad_reciclada.toFixed(2) + ' Kg';
  document.getElementById('dailyProgress').textContent = progress.toFixed(2) + '%';
  document.getElementById('progressFill').style.width = progress + '%';

  // Rellenar tabla
  const tableBody = document.getElementById('environmentalTableBody');
  environmentalData.forEach(item => {
    const row = document.createElement('tr');
    row.innerHTML = `
      <td class="material-cell ${item.material.toLowerCase().replace(' ', '-')}">${item.material}</td>
      <td>${item.cantidad_reciclada.toFixed(2)}</td>
      <td>${item.co2_reducido.toFixed(2)}</td>
      <td class="trend-up">↑</td> <!-- Simulación, ajusta con datos reales -->
    `;
    tableBody.appendChild(row);
  });

  // Configurar gráfico
  const ctx = document.getElementById('recyclingChart').getContext('2d');
  new Chart(ctx, {
    type: 'line',
    data: {
      labels: environmentalData.map(item => item.fecha),
      datasets: [{
        label: 'Cantidad Reciclada (Kg)',
        data: environmentalData.map(item => item.cantidad_reciclada),
        borderColor: '#4caf50',
        backgroundColor: 'rgba(76, 175, 80, 0.2)',
        fill: true,
        tension: 0.4
      }]
    },
    options: {
      responsive: true,
      scales: {
        y: { beginAtZero: true }
      }
    }
  });
});