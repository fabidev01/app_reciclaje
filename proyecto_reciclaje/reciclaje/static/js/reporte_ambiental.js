class ReporteAmbiental {
  constructor() {
    this.chart = null;
    this.initializeReport();
  }

  initializeReport() {
    this.mostrarFechaActual();
    this.crearGrafico();
    this.animarCarga();
  }

  mostrarFechaActual() {
    const hoy = new Date();
    const opciones = { year: 'numeric', month: 'long', day: 'numeric', weekday: 'long' };
    document.getElementById('currentDate').textContent = hoy.toLocaleDateString('es-ES', opciones);
  }

  crearGrafico() {
    fetch('/reporte-ambiental/data/')
      .then(response => {
        if (!response.ok) throw new Error('Error fetching data');
        return response.json();
      })
      .then(data => {
        const ctx = document.getElementById('recyclingChart').getContext('2d');
        if (this.chart) this.chart.destroy();
        if (!data.labels || data.labels.length === 0 || !data.datasets || data.datasets.length === 0) {
          console.warn('No data available for chart');
          return;
        }
        this.chart = new Chart(ctx, {
          type: 'line',
          data: {
            labels: data.labels,
            datasets: data.datasets
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              title: { display: true, text: 'Tendencia de Reciclaje', font: { size: 16, weight: 'bold' }, color: '#2e7d32' },
              legend: { position: 'bottom', labels: { usePointStyle: true, padding: 20, font: { size: 12 } } }
            },
            scales: {
              y: { beginAtZero: true, title: { display: true, text: 'Kilogramos Reciclados', color: '#555', font: { size: 14 } }, grid: { color: '#e8f5e9' } },
              x: { title: { display: true, text: 'Fechas', color: '#555', font: { size: 14 } }, grid: { color: '#e8f5e9' } }
            },
            interaction: { intersect: false, mode: 'index' },
            animation: { duration: 2000, easing: 'easeInOutQuart' }
          }
        });
      })
      .catch(error => console.error('Error en el gráfico:', error));
  }

  static getMaterialColor(material) {
    const colors = {
      'Plástico': '#ff5722',
      'Papel': '#795548',
      'Metal': '#607d8b',
      'Vidrio': '#2196f3',
      'Orgánico': '#4caf50',
      'Electrónico': '#9c27b0'
    };
    return colors[material] || '#000000';
  }

  animarCarga() {
    const tableElements = document.querySelectorAll('#environmentalTableBody .fade-in-up');
    tableElements.forEach((el, index) => {
      setTimeout(() => {
        el.style.opacity = '1';
        el.style.transform = 'translateY(0)';
      }, index * 100);
    });

    const summaryCards = document.querySelectorAll('.summary-card');
    summaryCards.forEach((card, index) => {
      card.style.opacity = '0';
      card.style.transform = 'translateY(20px)';
      card.style.transition = 'all 0.6s ease-out';
      setTimeout(() => {
        card.style.opacity = '1';
        card.style.transform = 'translateY(0)';
      }, 800 + (index * 200));
    });
  }
}

document.addEventListener('DOMContentLoaded', function() {
  const reporte = new ReporteAmbiental();
});