document.addEventListener('DOMContentLoaded', () => {
    console.log("⚡ MiniAmigixV System: Online");

    // Funcionalidad de modo oscuro
    const darkModeToggles = Array.from(document.querySelectorAll('.toggle-dark-mode'));
    const updateDarkModeButtons = (isDark) => {
        darkModeToggles.forEach(button => {
            const icon = isDark ? 'light_mode' : 'dark_mode';
            const label = button.classList.contains('btn-action')
                ? `<span>${isDark ? 'Modo claro' : 'Modo oscuro'}</span>`
                : '';

            button.innerHTML = `<span class="material-icons-round">${icon}</span>${label}`;
            button.setAttribute('title', isDark ? 'Modo Claro' : 'Modo Oscuro');
        });
    };

    if (darkModeToggles.length) {
        const darkEnabled = localStorage.getItem('darkMode') === 'enabled';
        if (darkEnabled) {
            document.body.classList.add('dark-mode');
        }

        updateDarkModeButtons(darkEnabled);

        darkModeToggles.forEach((toggle) => {
            toggle.addEventListener('click', () => {
                document.body.classList.toggle('dark-mode');
                const enabled = document.body.classList.contains('dark-mode');
                localStorage.setItem('darkMode', enabled ? 'enabled' : 'disabled');
                updateDarkModeButtons(enabled);
            });
        });
    }

    // Seleccionamos el contenedor principal de los widgets
    const mainContent = document.getElementById('dashboard-content');

    // Guardamos el HTML inicial del dashboard (los 4 widgets) para poder regresar a él fácilmente.
    // Use try/catch and explicit guard to avoid "Cannot read properties of null" errors
    let dashboardBackup = '';
    if (mainContent) {
        try {
            dashboardBackup = mainContent.innerHTML;
        } catch (e) {
            console.warn('Could not read dashboard content for backup', e);
            dashboardBackup = '';
        }
    }

    // Función genérica para cargar módulos usando Fetch
    async function loadModule(url, moduleName) {
        if (!mainContent) {
            window.location.href = url;
            return;
        }

        try {
            // Animación de salida
            mainContent.style.opacity = '0';
            mainContent.style.transform = 'scale(0.95)';
            mainContent.style.transition = 'all 0.3s ease';

            // Esperamos un momento a que termine la animación
            setTimeout(async () => {
                const response = await fetch(url);
                if (!response.ok) throw new Error(`Error al cargar ${moduleName}`);
                
                const html = await response.text();
                
                // Insertamos el nuevo HTML del módulo
                mainContent.innerHTML = html;
                
                // Animación de entrada con brillo neón
                mainContent.style.opacity = '1';
                mainContent.style.transform = 'scale(1)';

            // Si es el módulo de Arena Zen, buscamos y vinculamos el botón de retorno
            if (moduleName === 'Arena Zen') {
                const btnBack = document.getElementById('btn-back-home');
                if (btnBack) {
                    btnBack.addEventListener('click', restoreDashboard);
                }
            }

            // Si es el Módulo de Ánimo del Día, vinculamos eventos del botón (sin scripts inline en fragmentos)
            if (moduleName === 'Ánimo del Día') {
                bindAnimosRefreshButton();
            }
            
            // Si es el Panel de Administración, inicializamos sus funciones y cargamos estadísticas
            if (moduleName === 'Panel de Administración') {
                initAdminPanel();
            }
            }, 300);

        } catch (error) {
            console.error(error);
            if (mainContent) {
                mainContent.innerHTML = `
                    <div class="error-container" style="color: #ff007f; text-shadow: 0 0 10px #ff007f; text-align: center; padding: 2rem;">
                        <span class="material-icons-round" style="font-size: 4rem;">error</span>
                        <p>No se pudo conectar con el módulo de ${moduleName}. Inténtalo de nuevo.</p>
                    </div>
                `;
                mainContent.style.opacity = '1';
            }
        }
    }

    // Función para restaurar el dashboard original
    function restoreDashboard() {
        if (!mainContent) return;

        mainContent.style.opacity = '0';
        setTimeout(() => {
            mainContent.innerHTML = dashboardBackup;
            mainContent.style.opacity = '1';
            // Volvemos a vincular los eventos a los botones del dashboard original
            bindDashboardButtons();
        }, 250);
    }

    // Función para vincular todos los botones del dashboard
    function bindDashboardButtons() {
        // Botón de Arena Zen
        const btnZen = document.getElementById('btn-launch-zen');
        if (btnZen) {
            btnZen.addEventListener('click', (e) => {
                e.preventDefault();
                loadModule('/juegos/arena-zen/', 'Arena Zen');
            });
        }

        // Botón del Traductor
        const btnTranslator = document.getElementById('btn-launch-translator');
        if (btnTranslator) {
            btnTranslator.addEventListener('click', (e) => {
                e.preventDefault();
                loadModule('/traductor/', 'Traductor');
            });
        }

        // Botón del Blog
        const btnBlog = document.getElementById('btn-launch-blog');
        if (btnBlog) {
            btnBlog.addEventListener('click', (e) => {
                e.preventDefault();
                loadModule('/blog/', 'Blog');
            });
        }

        // Botón del Ánimo del Día
        const btnAnimos = document.getElementById('btn-launch-animos');
        if (btnAnimos) {
            btnAnimos.addEventListener('click', (e) => {
                e.preventDefault();
                loadModule('/chat/animos/', 'Ánimo del Día');
            });
        }

        // Botón del Panel de Administración (solo para staff)
        const btnAdmin = document.getElementById('btn-launch-admin');
        if (btnAdmin) {
            btnAdmin.addEventListener('click', (e) => {
                e.preventDefault();
                loadModule('/chat/admin-panel/', 'Panel de Administración');
            });
        }
    }

    // --- RELOJ EN TIEMPO REAL ---
    const clockElements = document.querySelectorAll('#live-clock, #dashboard-clock');
    if (clockElements.length) {
        function updateClock() {
            const now = new Date();
            const hours = String(now.getHours()).padStart(2, '0');
            const minutes = String(now.getMinutes()).padStart(2, '0');
            const formattedTime = `${hours}:${minutes}`;
            clockElements.forEach((element) => {
                element.textContent = formattedTime;
            });
        }
        updateClock();
        setInterval(updateClock, 1000);
    }

    // Función para vincular el botón de refresco del módulo Ánimo del Día (sin scripts inline en fragmentos)
    function bindAnimosRefreshButton() {
        const container = document.querySelector('.animos-container');
        if (!container) return;

        const refreshBtn = document.getElementById('btn-refresh-vibe');
        if (!refreshBtn) return;

        // Evita listeners duplicados al reinyectar HTML dinámicamente
        if (refreshBtn.dataset.bound === 'true') return;
        refreshBtn.dataset.bound = 'true';

        refreshBtn.addEventListener('click', async () => {
            // Efecto visual
            refreshBtn.style.transform = 'scale(0.95)';
            setTimeout(() => {
                refreshBtn.style.transform = 'scale(1)';
            }, 150);

            try {
                const response = await fetch('/chat/animos/');
                if (!response.ok) throw new Error('Error al actualizar el ánimo del día');

                const html = await response.text();

                // Insertamos solo el nuevo módulo
                const parser = new DOMParser();
                const doc = parser.parseFromString(html, 'text/html');
                const newContainer = doc.querySelector('.animos-container');

                if (newContainer) {
                    const currentContainer = document.querySelector('.animos-container');
                    if (currentContainer) {
                        currentContainer.innerHTML = newContainer.innerHTML;

                        // Rearmamos el binding sin duplicar listeners:
                        // el botón del fragmento se reemplaza (innerHTML), así que limpiamos el flag y volvemos a enganchar.
                        const newBtn = document.getElementById('btn-refresh-vibe');
                        if (newBtn) {
                            newBtn.dataset.bound = 'false';
                        }
                        bindAnimosRefreshButton();

                    }
                }
            } catch (error) {
                console.error(error);
                refreshBtn.style.background = 'rgba(255, 0, 0, 0.2)';
                refreshBtn.style.borderColor = '#ff007f';
                refreshBtn.style.color = '#ff007f';
                setTimeout(() => {
                    refreshBtn.style.background = 'transparent';
                    refreshBtn.style.borderColor = '#ba55d3';
                    refreshBtn.style.color = '#ba55d3';
                }, 2000);
            }
        });
    }

    // Funciones específicas para el Panel de Administración
    function initAdminPanel() {
        // Cargar estadísticas iniciales
        loadAdminStats();
        
        // Manejar el formulario de anuncio global
        const announcementForm = document.getElementById('global-announcement-form');
        if (announcementForm) {
            announcementForm.addEventListener('submit', function(e) {
                e.preventDefault();
                // En una implementación real, esto enviaría los datos al backend
                alert('¡Alerta global enviada! (Funcionalidad simulada)');
                announcementForm.reset();
            });
        }
        
        // Funciones placeholder para los botones de configuración
        window.adjustGameClicks = function() {
            alert('Clicks base de juegos aumentados! (Funcionalidad simulada)');
        };
        
        window.toggleMaintenanceMode = function() {
            alert('Modo mantenimiento activado! (Funcionalidad simulada)');
        };
        
        window.clearSystemLogs = function() {
            alert('Registros antiguos limpiados! (Funcionalidad simulada)');
        };
    }
    
    // Cargar estadísticas del admin panel
    function loadAdminStats() {
        fetch('/api/admin-stats/')
            .then(response => response.json())
            .then(data => {
                // Actualizar los elementos de estadísticas
                const statUsers = document.getElementById('stat-users');
                const statIA = document.getElementById('stat-ia');
                const statTickets = document.getElementById('stat-tickets');
                const statStudy = document.getElementById('stat-study');
                
                if (statUsers) statUsers.textContent = data.total_usuarios;
                if (statIA) statIA.textContent = data.uso_ia_consultas;
                if (statTickets) statTickets.textContent = data.tickets_soporte;
                if (statStudy) statStudy.textContent = data.horas_estudio_total;
            })
            .catch(error => {
                console.error('Error loading admin stats:', error);
                // Mostrar valores por defecto en caso de error
                const u = document.getElementById('stat-users');
                const ia = document.getElementById('stat-ia');
                const t = document.getElementById('stat-tickets');
                const s = document.getElementById('stat-study');
                if (u) u.textContent = '--';
                if (ia) ia.textContent = '--';
                if (t) t.textContent = '--';
                if (s) s.textContent = '--';
            });
    }

    // Reforzar switchView dentro de DOMContentLoaded con la versión completa
    // (la versión básica ya está definida en el <head> del template)
    if (typeof window._switchViewFull !== 'function') {
        window._switchViewFull = function(viewName, el) {
            document.querySelectorAll('.view-section, .view').forEach(function(s) {
                s.classList.remove('active');
                s.style.display = 'none';
            });
            document.querySelectorAll('.nav-item').forEach(function(n) {
                n.classList.remove('active');
            });
            if (el) {
                el.classList.add('active');
            } else {
                var navItem = document.querySelector('[data-view="' + viewName + '"]');
                if (navItem) navItem.classList.add('active');
            }
            var target = document.getElementById('view-' + viewName);
            if (target) {
                target.style.display = viewName === 'home' ? 'flex' : 'block';
                target.classList.add('active');
            } else {
                console.warn('switchView: vista no encontrada:', viewName);
                window.location.href = '/' + viewName + '/';
            }
        };
        window.switchView = window._switchViewFull;
        if (typeof switchView !== 'undefined') { switchView = window._switchViewFull; }
    }

    // Función para ocultar/mostrar el reloj basada en preferencias
    function toggleTimeVisibility() {
        const checkbox = document.getElementById('config-hide-time');
        const clockWidget = document.getElementById('live-clock');
        const weatherStatus = document.getElementById('weather-status');

        if (clockWidget && weatherStatus) {
            if (checkbox && checkbox.checked) {
                clockWidget.style.transition = "opacity 0.3s ease";
                clockWidget.style.opacity = "0";
                weatherStatus.style.opacity = "0";
                setTimeout(() => {
                    clockWidget.style.display = "none";
                    weatherStatus.style.display = "none";
                }, 300);
            } else {
                clockWidget.style.display = "block";
                weatherStatus.style.display = "block";
                setTimeout(() => {
                    clockWidget.style.opacity = "1";
                    weatherStatus.style.opacity = "1";
                }, 10);
            }
        }
    }

    // Inicializamos las escuchas al cargar la página por primera vez
    if (mainContent) {
        bindDashboardButtons();
    }

    // Aplicar preferencia de ocultar tiempo globalmente (todas las páginas)
    // Si no hay checkbox en la página, no hacemos nada.
    try {
        toggleTimeVisibility();
    } catch (e) {
        // no romper otras páginas
    }
});
