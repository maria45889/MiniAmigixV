// Configuraciones Module JavaScript
document.addEventListener('DOMContentLoaded', () => {
    console.log('⚙️ MiniAmigixV Configuraciones: Online');

    const storageKey = 'MiniAmigixSettings';
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabPanes = document.querySelectorAll('.tab-pane');
    const saveSettingsBtn = document.getElementById('save-settings');
    const resetSettingsBtn = document.getElementById('reset-settings');
    const notificationContainer = document.getElementById('notification-container');
    const manageAccountBtn = document.getElementById('manage-account');
    const googleAuthLink = document.getElementById('google-auth-link');

    let settingsChanged = false;
    let currentSettings = getDefaultSettings();

    setupEventListeners();
    loadSettings();

    function setupEventListeners() {
        tabButtons.forEach(button => {
            button.addEventListener('click', () => {
                const tabId = button.dataset.tab;
                tabButtons.forEach(btn => btn.classList.remove('active'));
                button.classList.add('active');
                tabPanes.forEach(pane => pane.classList.toggle('active', pane.id === tabId + '-tab'));
            });
        });

        // Tuerca única (modo + idioma + notificaciones) - aplica cambios inmediatos
        // Importante: si aún no está renderizado el control, no rompe.
        const unifiedToggle = document.getElementById('unified-settings-toggle');
        if (unifiedToggle) {
            unifiedToggle.addEventListener('click', () => {
                unifiedToggle.classList.toggle('open');
            });
        }

        if (saveSettingsBtn) {
            saveSettingsBtn.addEventListener('click', saveAllSettings);
        }


        if (resetSettingsBtn) {
            resetSettingsBtn.addEventListener('click', resetSettings);
        }

        if (manageAccountBtn) {
            manageAccountBtn.addEventListener('click', () => {
                window.location.href = '/perfil/';
            });
        }

        document.querySelectorAll('.settings-card input, .settings-card select').forEach(input => {
            input.addEventListener('change', () => setSaveButtonState(true));
            input.addEventListener('input', () => setSaveButtonState(true));
        });
    }

    function getDefaultSettings() {
        return {
            show_clock: true,
            show_weather: true,
            show_sidebar: true,
            show_notifications_badge: true,
            language: 'es',
            date_format: 'd/m/Y',
            time_format: 'H:i',
            first_day_of_week: '0',
            enable_animations: true,
            enable_sounds: true,
            enable_particles: false,
            theme_preference: 'dark',
            email_notifications: true,
            push_notifications: true,
            reminder_advance_time: '30',
            profile_visibility: 'private',
            allow_messages_from: 'contacts',
            show_online_status: true,
            data_collection: true,
            google_login_enabled: true,
            remember_device: false,
            enable_2fa: false,
        };
    }

    function loadSettings() {
        const savedSettings = localStorage.getItem(storageKey);
        if (savedSettings) {
            try {
                currentSettings = Object.assign(getDefaultSettings(), JSON.parse(savedSettings));
            } catch (error) {
                console.warn('No se pudo cargar la configuración guardada:', error);
                currentSettings = getDefaultSettings();
            }
        }

        updateUIFromSettings(currentSettings);
        applyImmediateChanges(currentSettings);
        setSaveButtonState(false);
    }

    function collectSettingsFromUI() {
        return {
            show_clock: getCheckboxValue('show-clock', true),
            show_weather: getCheckboxValue('show-weather', true),
            show_sidebar: getCheckboxValue('show-sidebar', true),
            show_notifications_badge: getCheckboxValue('show-notifications-badge', true),
            language: getInputValue('language', 'es'),
            date_format: getInputValue('date-format', 'd/m/Y'),
            time_format: getInputValue('time-format', 'H:i'),
            first_day_of_week: getInputValue('first-day-of-week', '0'),
            enable_animations: getCheckboxValue('enable-animations', true),
            enable_sounds: getCheckboxValue('enable-sounds', true),
            enable_particles: getCheckboxValue('enable-particles', false),
            theme_preference: getInputValue('theme-preference', 'dark'),
            email_notifications: getCheckboxValue('email-notifications', true),
            push_notifications: getCheckboxValue('push-notifications', true),
            reminder_advance_time: getInputValue('reminder-advance-time', '30'),
            profile_visibility: getInputValue('profile-visibility', 'private'),
            allow_messages_from: getInputValue('allow-messages-from', 'contacts'),
            show_online_status: getCheckboxValue('show-online-status', true),
            data_collection: getCheckboxValue('data-collection', true),
            google_login_enabled: getCheckboxValue('google-login-enabled', true),
            remember_device: getCheckboxValue('remember-device', false),
            enable_2fa: getCheckboxValue('enable-2fa', false),
        };
    }

    function saveAllSettings() {
        if (!settingsChanged) {
            showNotification('No hay cambios que guardar', 'info');
            return;
        }

        const settings = collectSettingsFromUI();
        fakeApiCall('/api/user/settings/', 'POST', settings)
            .then(response => {
                if (!response.success) {
                    throw new Error(response.error || 'No se pudo guardar la configuración');
                }

                currentSettings = settings;
                localStorage.setItem(storageKey, JSON.stringify(settings));
                applyImmediateChanges(settings);
                setSaveButtonState(false);
                showNotification('Configuraciones guardadas correctamente', 'success');
            })
            .catch(error => {
                console.error('Error saving settings:', error);
                showNotification('Error al guardar configuraciones: ' + error.message, 'error');
            });
    }

    function resetSettings() {
        if (!confirm('¿Estás seguro de que deseas restablecer todas las configuraciones a los valores predeterminados?')) {
            return;
        }

        currentSettings = getDefaultSettings();
        updateUIFromSettings(currentSettings);
        applyImmediateChanges(currentSettings);
        setSaveButtonState(true);
        showNotification('Configuraciones restablecidas a los valores predeterminados', 'success');
    }

    function updateUIFromSettings(settings) {
        setCheckboxValue('show-clock', settings.show_clock);
        setCheckboxValue('show-weather', settings.show_weather);
        setCheckboxValue('show-sidebar', settings.show_sidebar);
        setCheckboxValue('show-notifications-badge', settings.show_notifications_badge);
        setInputValue('language', settings.language);
        setInputValue('date-format', settings.date_format);
        setInputValue('time-format', settings.time_format);
        setInputValue('first-day-of-week', settings.first_day_of_week);
        setCheckboxValue('enable-animations', settings.enable_animations);
        setCheckboxValue('enable-sounds', settings.enable_sounds);
        setCheckboxValue('enable-particles', settings.enable_particles);
        setInputValue('theme-preference', settings.theme_preference);
        setCheckboxValue('email-notifications', settings.email_notifications);
        setCheckboxValue('push-notifications', settings.push_notifications);
        setInputValue('reminder-advance-time', settings.reminder_advance_time);
        setInputValue('profile-visibility', settings.profile_visibility);
        setInputValue('allow-messages-from', settings.allow_messages_from);
        setCheckboxValue('show-online-status', settings.show_online_status);
        setCheckboxValue('data-collection', settings.data_collection);
        setCheckboxValue('google-login-enabled', settings.google_login_enabled);
        setCheckboxValue('remember-device', settings.remember_device);
        setCheckboxValue('enable-2fa', settings.enable_2fa);
    }

    function applyImmediateChanges(settings) {
        toggleClockVisibility(settings.show_clock);
        toggleWeatherVisibility(settings.show_weather);
        toggleSidebarVisibility(settings.show_sidebar);
        toggleNotificationsBadge(settings.show_notifications_badge);
        applyTheme(settings.theme_preference);
        toggleGoogleAuthVisibility(settings.google_login_enabled);
    }

    function toggleClockVisibility(show) {
        const clockWidget = document.getElementById('live-clock');
        if (clockWidget) {
            clockWidget.style.display = show ? 'block' : 'none';
        }
    }

    function toggleWeatherVisibility(show) {
        const weatherStatus = document.getElementById('weather-status');
        if (weatherStatus) {
            weatherStatus.style.display = show ? 'block' : 'none';
        }
    }

    function toggleSidebarVisibility(show) {
        const sidebar = document.querySelector('.sidebar');
        if (sidebar) {
            sidebar.style.display = show ? 'block' : 'none';
        }
    }

    function toggleNotificationsBadge(show) {
        const notificationAction = document.querySelector('.sidebar-action[title="Notificaciones"]');
        if (notificationAction) {
            notificationAction.style.display = show ? 'inline-flex' : 'none';
        }
    }

    function toggleGoogleAuthVisibility(enabled) {
        const googleAuthItem = document.querySelector('.nav-item.google-auth');
        if (googleAuthItem) {
            googleAuthItem.style.display = enabled ? 'flex' : 'none';
        }
        if (googleAuthLink) {
            googleAuthLink.classList.toggle('disabled-link', !enabled);
        }
    }

    function applyTheme(theme) {
        document.body.classList.remove('dark-mode', 'light-mode', 'neon-mode');
        if (theme === 'dark') {
            document.body.classList.add('dark-mode');
        } else if (theme === 'light') {
            document.body.classList.add('light-mode');
        } else if (theme === 'neon') {
            document.body.classList.add('neon-mode');
        }
    }

    function getCheckboxValue(id, fallback) {
        const element = document.getElementById(id);
        return element ? element.checked : fallback;
    }

    function getInputValue(id, fallback) {
        const element = document.getElementById(id);
        return element ? element.value : fallback;
    }

    function setCheckboxValue(id, value) {
        const element = document.getElementById(id);
        if (element) {
            element.checked = Boolean(value);
        }
    }

    function setInputValue(id, value) {
        const element = document.getElementById(id);
        if (element) {
            element.value = value;
        }
    }

    function setSaveButtonState(enabled) {
        settingsChanged = enabled;
        if (saveSettingsBtn) {
            saveSettingsBtn.disabled = !enabled;
            saveSettingsBtn.style.opacity = enabled ? '1' : '0.5';
        }
    }

    function fakeApiCall(url, method, data) {
        return new Promise(resolve => {
            setTimeout(() => {
                resolve({
                    success: true,
                    message: 'Configuraciones guardadas con éxito'
                });
            }, 300);
        });
    }

    function showNotification(message, type = 'info') {
        if (!notificationContainer) {
            console.log(`[${type}] ${message}`);
            return;
        }

        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.innerHTML = `
            <div class="notification-content">
                <span class="material-icons-round notification-icon">${getNotificationIcon(type)}</span>
                <div class="notification-text"><p>${message}</p></div>
                <button class="notification-close" aria-label="Cerrar notificación">
                    <span class="material-icons-round">close</span>
                </button>
            </div>
        `;

        notificationContainer.appendChild(notification);
        const closeButton = notification.querySelector('.notification-close');
        if (closeButton) {
            closeButton.addEventListener('click', () => notification.remove());
        }

        setTimeout(() => {
            if (notification.parentNode) notification.remove();
        }, 4500);
    }

    function getNotificationIcon(type) {
        const icons = {
            info: 'info',
            success: 'check_circle',
            warning: 'warning',
            error: 'error'
        };
        return icons[type] || 'info';
    }

    console.log('⚙️ Configuraciones module initialized');
});
