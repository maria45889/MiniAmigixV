// Profile Module JavaScript
document.addEventListener('DOMContentLoaded', () => {
    console.log("👤 MiniAmigixV Perfil: Online");
    
    // DOM Elements
    const profilePictureInput = document.getElementById('profile-picture-input');
    const profilePictureContainer = document.querySelector('.profile-picture-container');
    const profilePreview = document.getElementById('profile-preview');
    const profilePictureOverlay = document.querySelector('.profile-picture-overlay');
    const personalInfoForm = document.getElementById('personal-info-form');
    const saveVisualSettingsBtn = document.getElementById('save-visual-settings');
    const changePasswordBtn = document.getElementById('change-password');
    const exportDataBtn = document.getElementById('export-data');
    const deleteAccountBtn = document.getElementById('delete-account');
    const notificationContainer = document.getElementById('notification-container');
    
    // Initialize
    setupEventListeners();
    applyAllSettings();
    
    // Functions
    function setupEventListeners() {
        // Profile picture upload
        if (profilePictureContainer && profilePictureInput) {
            profilePictureContainer.addEventListener('click', () => {
                profilePictureInput.click();
            });
            profilePictureInput.addEventListener('change', handleProfilePictureUpload);
        }
        
        // Personal info form
        if (personalInfoForm) {
            personalInfoForm.addEventListener('submit', savePersonalInfo);
        }
        
        // Visual settings
        saveVisualSettingsBtn.addEventListener('click', saveVisualSettings);
        
        // Action buttons
        changePasswordBtn.addEventListener('click', () => showNotification('Funcionalidad de cambio de contraseña en desarrollo', 'info'));
        exportDataBtn.addEventListener('click', () => showNotification('Funcionalidad de exportación de datos en desarrollo', 'info'));
        deleteAccountBtn.addEventListener('click', () => {
            if (confirm('¿Estás seguro de que deseas eliminar tu cuenta? Esta acción no se puede deshacer.')) {
                showNotification('Funcionalidad de eliminación de cuenta en desarrollo', 'info');
            }
        });
        
        // Tab switching
        setupTabSwitching();
    }
    
    function setupTabSwitching() {
        const tabButtons = document.querySelectorAll('.tab-btn');
        const tabContents = document.querySelectorAll('.tab-content');
        
        tabButtons.forEach(button => {
            button.addEventListener('click', () => {
                const tabId = button.dataset.tab;
                
                // Update active tab button
                tabButtons.forEach(btn => btn.classList.remove('active'));
                button.classList.add('active');
                
                // Show corresponding tab content
                tabContents.forEach(content => {
                    content.classList.remove('active');
                    if (content.id === tabId + '-tab') {
                        content.classList.add('active');
                    }
                });
            });
        });
    }
    
    function handleProfilePictureUpload(e) {
        const file = e.target.files[0];
        if (!file) return;
        
        // Validate file type
        if (!file.type.startsWith('image/')) {
            showNotification('Por favor selecciona un archivo de imagen válido', 'error');
            return;
        }
        
        // Validate file size (5MB max)
        if (file.size > 5 * 1024 * 1024) {
            showNotification('El archivo es demasiado grande. Máximo 5MB permitido', 'error');
            return;
        }

        const formData = new FormData();
        formData.append('profile_picture', file);

        // Upload image to server
        fetch('/actualizar-perfil/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                if (data.profile_picture_url) {
                    if (profilePreview) {
                        profilePreview.src = data.profile_picture_url;
                    } else {
                        const pictureContainer = document.querySelector('.profile-picture-container');
                        if (pictureContainer) {
                            const img = document.createElement('img');
                            img.id = 'profile-preview';
                            img.src = data.profile_picture_url;
                            img.alt = 'Foto de perfil';
                            pictureContainer.insertBefore(img, pictureContainer.firstChild);
                        }
                    }
                }
                showNotification(data.message || 'Foto de perfil actualizada', 'success');
            } else {
                showNotification(data.error || 'Error al actualizar la foto', 'error');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showNotification('Error de conexión. Por favor intenta de nuevo.', 'error');
        });
    }

    function savePersonalInfo(e) {
        e.preventDefault();
        
        const username = document.getElementById('username').value.trim();
        const displayName = document.getElementById('display-name').value.trim();
        const aiName = document.getElementById('ai-name').value.trim();
        
        // Prepare data
        const data = {};
        if (username !== '') data.username = username;
        if (displayName !== '') data.display_name = displayName;
        if (aiName !== '') data.ai_name = aiName;
        
        // Send to server
        fetch('/actualizar-perfil/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showNotification(data.message || 'Información personal actualizada', 'success');
                if (data.display_name) {
                    document.querySelector('#profile-name').textContent = data.display_name;
                }
                if (data.username) {
                    document.querySelector('#profile-username').textContent = data.username;
                }
            } else {
                showNotification(data.error || 'Error al actualizar información', 'error');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showNotification('Error de conexión. Por favor intenta de nuevo.', 'error');
        });
    }
    
    function saveVisualSettings() {
        // Get all visual settings
        const profileBackground = document.getElementById('profile-background').value;
        const appBackground = document.getElementById('app-background').value;
        const screenAppearance = document.getElementById('screen-appearance').value;
        const fontSize = document.getElementById('font-size') ? document.getElementById('font-size').value : 'medium';
        const themePreference = document.querySelector('input[name="theme"]:checked') ? 
                              document.querySelector('input[name="theme"]:checked').value : 'dark';
        
        // Prepare data
        const data = {
            profile_background: profileBackground,
            app_background: appBackground,
            screen_appearance: screenAppearance,
            font_size: fontSize,
            theme_preference: themePreference
        };
        
        // Send to server
        fetch('/actualizar-perfil/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showNotification(data.message || 'Apariencia guardada correctamente', 'success');
                if (data.theme_preference) {
                    applyTheme(data.theme_preference);
                }
                applyAllSettings();
            } else {
                showNotification(data.error || 'Error al guardar apariencia', 'error');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showNotification('Error de conexión. Por favor intenta de nuevo.', 'error');
        });
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
        localStorage.setItem('theme', theme);
    }

    function applyAppBackground(background) {
        if (background === 'dark-gradient') {
            document.body.style.background = 'linear-gradient(135deg, #090b24 0%, #121b40 100%)';
        } else if (background === 'neon-grid') {
            document.body.style.background = 'radial-gradient(circle at top left, rgba(0,255,255,0.12), transparent 40%), linear-gradient(180deg, #05060d, #0c1133)';
        } else if (background === 'stars') {
            document.body.style.background = 'radial-gradient(circle at top, rgba(255,255,255,0.08), transparent 35%), #090b18';
        } else if (background === 'waves') {
            document.body.style.background = 'linear-gradient(135deg, #0b1a3e 0%, #0f2a5c 50%, #071025 100%)';
        } else {
            document.body.style.background = '';
        }
    }

    function applyProfileBackground(background) {
        const section = document.querySelector('.profile-picture-section');
        if (!section) return;
        if (background === 'space') {
            section.style.backgroundImage = 'url(/static/data/space-bg.jpg)';
            section.style.backgroundSize = 'cover';
        } else if (background === 'nature') {
            section.style.backgroundImage = 'url(/static/data/nature-bg.jpg)';
            section.style.backgroundSize = 'cover';
        } else if (background === 'abstract') {
            section.style.backgroundImage = 'linear-gradient(135deg, rgba(86, 30, 255, 0.18), rgba(0, 255, 239, 0.18))';
        } else if (background === 'minimal') {
            section.style.backgroundImage = 'linear-gradient(135deg, rgba(255,255,255,0.04), rgba(255,255,255,0.1))';
        } else {
            section.style.backgroundImage = '';
        }
    }

    function applyScreenAppearance(appearance) {
        const container = document.querySelector('.profile-container');
        if (!container) return;
        container.style.gap = appearance === 'compact' ? '15px' : appearance === 'large' ? '35px' : '25px';
    }

    function applyFontSize(size) {
        if (size === 'small') {
            document.documentElement.style.fontSize = '14px';
        } else if (size === 'large') {
            document.documentElement.style.fontSize = '18px';
        } else if (size === 'extra-large') {
            document.documentElement.style.fontSize = '20px';
        } else {
            document.documentElement.style.fontSize = '16px';
        }
    }

    function applyAllSettings() {
        const profileBackground = document.getElementById('profile-background') ? document.getElementById('profile-background').value : 'default';
        const appBackground = document.getElementById('app-background') ? document.getElementById('app-background').value : 'default';
        const screenAppearance = document.getElementById('screen-appearance') ? document.getElementById('screen-appearance').value : 'standard';
        const fontSize = document.getElementById('font-size') ? document.getElementById('font-size').value : 'medium';
        const themePreference = document.querySelector('input[name="theme"]:checked') ? document.querySelector('input[name="theme"]:checked').value : 'dark';
        applyTheme(themePreference);
        applyAppBackground(appBackground);
        applyProfileBackground(profileBackground);
        applyScreenAppearance(screenAppearance);
        applyFontSize(fontSize);
    }
    
    function showNotification(message, type = 'info') {
        // Reuse notification system from eventos if available
        if (typeof window.MiniAmigixEventos !== 'undefined' && window.MiniAmigixEventos.showNotification) {
            window.MiniAmigixEventos.showNotification(message, type);
        } else {
            // Simple fallback notification
            const notification = document.createElement('div');
            notification.className = `notification notification-${type}`;
            notification.innerHTML = `
                <div class="notification-content">
                    <span class="material-icons-round notification-icon">
                        ${getNotificationIcon(type)}
                    </span>
                    <div class="notification-text">
                        <p>${message}</p>
                    </div>
                    <button class="notification-close" aria-label="Cerrar notificación">
                        <span class="material-icons-round">close</span>
                    </button>
                </div>
            `;
            
            notificationContainer.appendChild(notification);
            
            // Add close functionality
            notification.querySelector('.notification-close').addEventListener('click', () => {
                notification.remove();
            });
            
            // Auto remove after 5 seconds
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.remove();
                }
            }, 5000);
        }
    }
    
    function getNotificationIcon(type) {
        const icons = {
            'info': 'info',
            'success': 'check_circle',
            'warning': 'warning',
            'error': 'error'
        };
        return icons[type] || 'info';
    }
    
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    
    // Initialize theme from localStorage
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        applyTheme(savedTheme);
    }
    
    console.log("👤 Perfil module initialized");
});

// Export functions for use in other modules if needed
window.MiniAmigixPerfil = {
    savePersonalInfo,
    saveVisualSettings,
    applyTheme
};