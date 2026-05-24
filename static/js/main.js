(function () {
  function pad2(n) {
    return String(n).padStart(2, '0');
  }

  function formatTime(d) {
    var hours = d.getHours();
    var minutes = d.getMinutes();

    var ampm = hours >= 12 ? 'PM' : 'AM';
    var h12 = hours % 12;
    if (h12 === 0) h12 = 12;

    return pad2(h12) + ':' + pad2(minutes) + ' ' + ampm;
  }

  function updateClock() {
    var el = document.getElementById('live-clock');
    if (!el) return;
    el.textContent = formatTime(new Date());
  }

  document.addEventListener('DOMContentLoaded', function () {
    // Reloj
    updateClock();
    setInterval(updateClock, 1000);

    // Clima (placeholder elegante)
    var weatherEl = document.getElementById('weather-status');
    if (weatherEl && !weatherEl.textContent) {
      weatherEl.textContent = 'Listo para conectar API';
    }

    // Botones (con comportamiento mínimo visible)
    var btn = document.querySelector('.btn-neon');
    if (btn) {
      btn.addEventListener('click', function (e) {
        e.preventDefault();
        // Acción visible: evita que parezca que no hace nada
        // Si luego agregas navegación/launcher real, reemplazar esta lógica.
        alert('Iniciando Partida...');
      });
    }
  });
})();

