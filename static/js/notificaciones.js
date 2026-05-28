// Notificaciones Module JavaScript
document.addEventListener('DOMContentLoaded', () => {
    console.log("🔔 MiniAmigixV Notificaciones: Online");
    
    // DOM Elements
    const notificationsList = document.querySelector('.notificaciones-list');
    const markAllReadBtn = document.getElementById('mark-all-read');
    const clearNotificationsBtn = document.getElementById('clear-notifications');
    const notificationContainer = document.getElementById('notification-container');
    
    // Initialize
    setupEventListeners();
    loadNotifications();
    
    // Functions
    function setupEventListeners() {
        // Mark all as read
        if (markAllReadBtn) {
            markAllReadBtn.addEventListener('click', markAllAsRead);
        }
        
        // Clear notifications
        if (clearNotificationsBtn) {
            clearNotificationsBtn.addEventListener('click', clearNotifications);
        }
        
        // Individual mark as read buttons
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('mark-as-read-btn')) {
                const notificationId = e.target.dataset.id;
                markAsRead(notificationId);
            }
        });
        
        // Notification item clicks (to go to related URL)
        document.addEventListener('click', (e) => {
            const notificationItem = e.target.closest('.notification-item');
            if (notificationItem && notificationItem.dataset.url) {
                window.location.href = notificationItem.dataset.url;
            }
        });
    }
    
    function loadNotifications() {
        // In a real app, this would fetch from the server
        // For demo, we'll simulate with some sample data
        const sampleNotifications = [
            {
                id: 1,
                title: 'Bienvenido a MiniAmigixV',
                message: '¡Gracias por unirte a nuestra comunidad! Descubre todas las funcionalidades disponibles.',
                type: 'info',
                time: 'Hace 2 horas',
                isRead: false
            },
            {
                id: 2,
                title: 'Recordatorio: Reunión de equipo',
                message: 'No olvides tu reunión de equipo hoy a las 15:00 en la sala de conferencias virtual.',
                type: 'reminder',
                time: 'Hace 1 día',
                isRead: false
            },
            {
                id: 3,
                title: 'Nueva actualización disponible',
                message: 'Se ha lanzado una nueva versión de MiniAmigixV con mejoras de rendimiento y nuevas funcionalidades.',
                type: 'update',
                time: 'Hace 3 días',
                isRead: true
            },
            {
                id: 4,
                title: 'Límite de almacenamiento alcanzado',
                message: 'Has alcanzado el 80% de tu límite de almacenamiento. Considera eliminar archivos antiguos.',
                type: 'warning',
                time: 'Hace 5 días',
                isRead: false
            }
        ];
        
        renderNotifications(sampleNotifications);
    }
    
    function renderNotifications(notifications) {
        if (!notificationsList) return;
        
        if (notifications.length === 0) {
            notificationsList.innerHTML = `
                <div class="empty-state">
                    <span class="material-icons-round">notifications_none</span>
                    <h2>No tienes notificaciones</h2>
                    <p>No hay notificaciones pendientes. ¡Mantente activo para recibir actualizaciones!</p>
                </div>
            `;
            return;
        }
        
        notificationsList.innerHTML = notifications.map(notification => {
            const icon = getNotificationIcon(notification.type);
            const timeAgo = notification.time || 'Hace poco';
            
            return `
                <div class="notification-item notification-${notification.type} ${notification.is_read ? '' : 'unread'}" 
                     data-id="${notification.id}">
                    <div class="notification-header">
                        <div class="notification-icon">
                            <span class="material-icons-round">${icon}</span>
                        </div>
                        <div class="notification-content">
                            <h3>${notification.title}</h3>
                            <p>${notification.message}</p>
                        </div>
                        <div class="notification-time">
                            <small>${timeAgo}</small>
                        </div>
                    </div>
                    <div class="notification-footer">
                        <button class="btn-icon mark-as-read-btn" data-id="${notification.id}">
                            <span class="material-icons-round">${notification.is_read ? 'mark_as_unread' : 'done'}</span>
                        </button>
                    </div>
                </div>
            `;
        }).join('');
    }
    
    function markAsRead(notificationId) {
        // In a real app, this would send a request to the server
        const notificationItem = document.querySelector(`.notification-item[data-id="${notificationId}"]`);
        if (notificationItem) {
            notificationItem.classList.remove('unread');
            notificationItem.classList.add('read');
            
            // Update the button
            const markBtn = notificationItem.querySelector('.mark-as-read-btn');
            if (markBtn) {
                markBtn.innerHTML = '<span class="material-icons-round">mark_as_unread</span>';
            }
            
            showNotification('Notificación marcada como leída', 'success');
        }
    }
    
    function markAllAsRead() {
        // In a real app, this would send a request to the server
        const notificationItems = document.querySelectorAll('.notification-item.unread');
        notificationItems.forEach(item => {
            item.classList.remove('unread');
            item.classList.add('read');
            
            const markBtn = item.querySelector('.mark-as-read-btn');
            if (markBtn) {
                markBtn.innerHTML = '<span class="material-icons-round">mark_as_unread</span>';
            }
        });
        
        showNotification('Todas las notificaciones marcadas como leídas', 'success');
    }
    
    function clearNotifications() {
        if (confirm('¿Estás seguro de que deseas eliminar todas las notificaciones? Esta acción no se puede deshacer.')) {
            // In a real app, this would send a request to the server
            notificationsList.innerHTML = `
                <div class="empty-state">
                    <span class="material-icons-round">notifications_none</span>
                    <h2>No tienes notificaciones</h2>
                    <p>No hay notificaciones pendientes. ¡Mantente activo para recibir actualizaciones!</p>
                </div>
            `;
            
            showNotification('Todas las notificaciones han sido eliminadas', 'info');
        }
    }
    
    function getNotificationIcon(type) {
        const icons = {
            'info': 'info',
            'success': 'check_circle',
            'warning': 'warning_amb',
            'error': 'error',
            'reminder': 'alarm',
            'system': 'settings',
            'update': 'system_update'
        };
        return icons[type] || 'notifications';
    }
    
    function showNotification(message, type = 'info') {
        // Reuse notification system from eventos if available
        if (typeof window.MiniAmigixEventos !== 'undefined' && window.MiniAmigixEventos.showNotification) {
            window.MiniAmigixEventos.showNotification(message, type);
        } else {
            // Simple fallback
            console.log(`[${type}] ${message}`);
            alert(message);
        }
    }
    
    console.log("🔔 Notificaciones module initialized");
});