// Eventos Module JavaScript
document.addEventListener('DOMContentLoaded', () => {
    console.log("📅 MiniAmigixV Eventos: Online");
    
    // DOM Elements
    const addEventForm = document.getElementById('add-event-form');
    const upcomingList = document.getElementById('upcoming-list');
    const calendarDays = document.getElementById('calendar-days');
    const currentMonthYear = document.getElementById('current-month-year');
    const prevMonthBtn = document.getElementById('prev-month');
    const nextMonthBtn = document.getElementById('next-month');
    const notificationContainer = document.getElementById('notification-container');
    
    // State
    let events = JSON.parse(localStorage.getItem('miniAmigixEvents') || '[]');
    let holidays = [
        { name: 'Navidad', date: '12-25', icon: 'card_giftcard' },
        { name: 'Año Nuevo', date: '01-01', icon: 'celebration' },
        { name: 'Día del Padre', date: '06-19', icon: 'family_restroom', note: 'Tercer domingo de junio' },
        { name: 'Día del Niño', date: '06-01', icon: 'child_friendly' },
        { name: 'Independencia', date: '08-10', icon: 'flag' }
    ];
    let currentDate = new Date();
    let displayDate = new Date(currentDate.getFullYear(), currentDate.getMonth(), 1);
    
    // Initialize
    renderCalendar();
    renderUpcomingEvents();
    renderHolidays();
    startClock();
    checkReminders();
    
    // Event Listeners
    addEventForm.addEventListener('submit', handleAddEvent);
    prevMonthBtn.addEventListener('click', () => {
        displayDate = new Date(displayDate.getFullYear(), displayDate.getMonth() - 1, 1);
        renderCalendar();
    });
    nextMonthBtn.addEventListener('click', () => {
        displayDate = new Date(displayDate.getFullYear(), displayDate.getMonth() + 1, 1);
        renderCalendar();
    });
    
    // Functions
    function handleAddEvent(e) {
        e.preventDefault();
        
        const title = document.getElementById('event-title').value.trim();
        const description = document.getElementById('event-description').value.trim();
        const dateStr = document.getElementById('event-date').value;
        const type = document.getElementById('event-type').value;
        const reminderTime = parseInt(document.getElementById('reminder-time').value);
        
        if (!title || !dateStr) return;
        
        const eventDate = new Date(dateStr);
        if (isNaN(eventDate.getTime())) return;
        
        const newEvent = {
            id: Date.now() + Math.random(),
            title,
            description,
            date: eventDate.toISOString(),
            type,
            reminderTime,
            completed: false
        };
        
        events.push(newEvent);
        saveEvents();
        renderUpcomingEvents();
        
        // Reset form
        addEventForm.reset();
        document.getElementById('event-title').focus();
        
        // Show success notification
        showNotification(`Evento "${title}" agregado exitosamente`, 'success');
    }
    
    function renderCalendar() {
        const year = displayDate.getFullYear();
        const month = displayDate.getMonth();
        
        currentMonthYear.textContent = new Date(year, month).toLocaleDateString('es-ES', { 
            year: 'numeric', 
            month: 'long' 
        });
        
        // Clear previous days
        calendarDays.innerHTML = '';
        
        // Get first day of month and number of days
        const firstDay = new Date(year, month, 1);
        const daysInMonth = new Date(year, month + 1, 0).getDate();
        
        // Add empty cells for days before the 1st
        const startingDay = firstDay.getDay(); // 0 = Sunday, 1 = Monday, etc.
        for (let i = 0; i < startingDay; i++) {
            const emptyDiv = document.createElement('div');
            emptyDiv.className = 'calendar-day empty';
            calendarDays.appendChild(emptyDiv);
        }
        
        // Add days of the month
        for (let day = 1; day <= daysInMonth; day++) {
            const dayDiv = document.createElement('div');
            dayDiv.className = 'calendar-day';
            dayDiv.textContent = day;
            
            // Check if today
            const today = new Date();
            if (day === today.getDate() && month === today.getMonth() && year === today.getFullYear()) {
                dayDiv.classList.add('today');
            }
            
            // Check if there are events on this day
            const eventsOnDay = events.filter(event => {
                const eventDate = new Date(event.date);
                return eventDate.getDate() === day && 
                       eventDate.getMonth() === month && 
                       eventDate.getFullYear() === year;
            });
            
            if (eventsOnDay.length > 0) {
                dayDiv.classList.add('has-events');
                dayDiv.title = `${eventsOnDay.length} evento(s) este día`;
                
                // Add event indicators
                const eventsIndicator = document.createElement('div');
                eventsIndicator.className = 'day-events-indicator';
                for (let i = 0; i < Math.min(eventsOnDay.length, 3); i++) {
                    const eventDot = document.createElement('div');
                    eventDot.className = 'event-dot';
                    eventsIndicator.appendChild(eventDot);
                }
                dayDiv.appendChild(eventsIndicator);
            }
            
            // Check if it's a holiday
            const monthDay = `${String(month + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
            const holiday = holidays.find(h => h.date === monthDay);
            if (holiday) {
                dayDiv.classList.add('holiday');
                dayDiv.title = holiday.name;
                
                const holidayIcon = document.createElement('span');
                holidayIcon.className = 'material-icons-round holiday-icon';
                holidayIcon.textContent = getHolidayIcon(holiday.icon);
                dayDiv.appendChild(holidayIcon);
            }
            
            // Add click event to show day details
            dayDiv.addEventListener('click', () => showDayEvents(day, month, year));
            
            calendarDays.appendChild(dayDiv);
        }
    }
    
    function showDayEvents(day, month, year) {
        const eventsOnDay = events.filter(event => {
            const eventDate = new Date(event.date);
            return eventDate.getDate() === day && 
                   eventDate.getMonth() === month && 
                   eventDate.getFullYear() === year;
        });
        
        if (eventsOnDay.length === 0) {
            showNotification(`No hay eventos programados para el ${day}/${month + 1}/${year}`, 'info');
            return;
        }
        
        // Create modal to show day events
        const modal = document.createElement('div');
        modal.className = 'day-events-modal';
        modal.innerHTML = `
            <div class="day-events-modal-content">
                <div class="day-events-modal-header">
                    <span class="material-icons-round close-modal">close</span>
                    <h2>Eventos del ${day}/${month + 1}/${year}</h2>
                </div>
                <div class="day-events-modal-body">
                    ${eventsOnDay.map(event => `
                        <div class="day-event-item">
                            <div class="event-time">
                                ${new Date(event.date).toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' })}
                            </div>
                            <div class="event-details">
                                <h3>${event.title}</h3>
                                <p>${event.description || 'Sin descripción'}</p>
                                <span class="event-type-badge ${event.type}">${event.type}</span>
                            </div>
                            <div class="event-actions">
                                <button class="btn-icon complete-event" data-id="${event.id}">
                                    <span class="material-icons-round">check_circle</span>
                                </button>
                                <button class="btn-icon delete-event" data-id="${event.id}">
                                    <span class="material-icons-round">delete</span>
                                </button>
                            </div>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
        
        document.body.appendChild(modal);
        
        // Add event listeners
        modal.querySelector('.close-modal').addEventListener('click', () => {
            document.body.removeChild(modal);
        });
        
        modal.querySelectorAll('.complete-event').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const id = parseInt(e.currentTarget.dataset.id);
                completeEvent(id);
                document.body.removeChild(modal);
                showDayEvents(day, month, year); // Refresh
            });
        });
        
        modal.querySelectorAll('.delete-event').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const id = parseInt(e.currentTarget.dataset.id);
                deleteEvent(id);
                document.body.removeChild(modal);
                showDayEvents(day, month, year); // Refresh
            });
        });
    }
    
    function completeEvent(id) {
        events = events.map(event => 
            event.id === id ? {...event, completed: true} : event
        );
        saveEvents();
        renderUpcomingEvents();
        renderCalendar();
        showNotification('Evento marcado como completado', 'success');
    }
    
    function deleteEvent(id) {
        events = events.filter(event => event.id !== id);
        saveEvents();
        renderUpcomingEvents();
        renderCalendar();
        showNotification('Evento eliminado', 'info');
    }
    
    function renderUpcomingEvents() {
        const now = new Date();
        const upcomingEvents = events
            .filter(event => !event.completed && new Date(event.date) > now)
            .sort((a, b) => new Date(a.date) - new Date(b.date))
            .slice(0, 5); // Show next 5 events
        
        if (upcomingEvents.length === 0) {
            upcomingList.innerHTML = `
                <div class="empty-state">
                    <p>No hay eventos próximos. ¡Agrega tu primer evento!</p>
                </div>
            `;
            return;
        }
        
        upcomingList.innerHTML = upcomingEvents.map(event => {
            const eventDate = new Date(event.date);
            const timeDiff = eventDate - now;
            const daysDiff = Math.ceil(timeDiff / (1000 * 60 * 60 * 24));
            
            let timeText = '';
            if (daysDiff > 0) {
                timeText = `En ${daysDiff} día${daysDiff !== 1 ? 's' : ''}`;
            } else {
                timeText = 'Hoy';
            }
            
            return `
                <div class="upcoming-event">
                    <div class="event-time">${timeText}</div>
                    <div class="event-info">
                        <h3>${event.title}</h3>
                        <p>${event.description || 'Sin descripción'}</p>
                        <span class="event-type-badge ${event.type}">${event.type}</span>
                    </div>
                </div>
            `;
        }).join('');
    }
    
    function renderHolidays() {
        const holidaysList = document.getElementById('holidays-list');
        const now = new Date();
        const currentYear = now.getFullYear();
        
        // Calculate dynamic holidays (like Father's Day - third Sunday of June)
        const fathersDay = new Date(currentYear, 5, 1); // June 1st
        fathersDay.setDate(1 + ((0 - fathersDay.getDay() + 7) % 7) + 14); // Third Sunday
        
        const holidayEvents = [
            ...holidays.map(h => ({
                ...h,
                date: new Date(currentYear, parseInt(h.date.split('-')[0]) - 1, parseInt(h.date.split('-')[1]))
            })),
            { name: 'Día del Padre', date: fathersDay, icon: 'family_restroom' }
        ].sort((a, b) => a.date - b.date);
        
        holidaysList.innerHTML = holidayEvents.map(holiday => {
            const isPast = holiday.date < now.setHours(0,0,0,0);
            return `
                <div class="holiday-item ${isPast ? 'past' : ''}">
                    <div class="holiday-icon">
                        <span class="material-icons-round">${getHolidayIcon(holiday.icon)}</span>
                    </div>
                    <div class="holiday-info">
                        <h3>${holiday.name}</h3>
                        <p>${holiday.date.toLocaleDateString('es-ES', { day: 'numeric', month: 'long' })}</p>
                        ${holiday.note ? `<small>${holiday.note}</small>` : ''}
                    </div>
                </div>
            `;
        }).join('');
    }
    
    function getHolidayIcon(iconName) {
        const icons = {
            'card_giftcard': 'card_giftcard',
            'celebration': 'celebration',
            'family_restroom': 'family_restroom',
            'child_friendly': 'child_friendly',
            'flag': 'flag'
        };
        return icons[iconName] || 'event';
    }
    
    function startClock() {
        function updateClock() {
            const now = new Date();
            document.getElementById('live-clock').textContent = now.toLocaleTimeString('es-ES', {
                hour: '2-digit',
                minute: '2-digit',
                second: '2-digit'
            });
        }
        
        updateClock(); // Initial call
        setInterval(updateClock, 1000);
    }
    
    function checkReminders() {
        // Check for events that need reminders (5 days, 2 days, 1 day before) and custom reminders
        const now = new Date();

        events.forEach(event => {
            if (event.completed) return;

            const eventDate = new Date(event.date);
            const timeDiff = eventDate - now;
            if (timeDiff <= 0) return; // past event

            const daysLeft = Math.ceil(timeDiff / (1000 * 60 * 60 * 24));

            // Predefined day reminders: 5, 2, 1 days
            [5, 2, 1].forEach(days => {
                if (daysLeft === days) {
                    const key = `reminder_${event.id}_d${days}`;
                    if (!localStorage.getItem(key)) {
                        showReminderNotification(event.title, days);
                        localStorage.setItem(key, Date.now().toString());
                    }
                }
            });

            // Custom reminder specified in minutes in the form (reminderTime)
            if (event.reminderTime && Number(event.reminderTime) > 0) {
                const minutesBefore = Number(event.reminderTime);
                const msBefore = minutesBefore * 60 * 1000;
                if (timeDiff > 0 && timeDiff <= msBefore) {
                    const key = `reminder_${event.id}_custom_${minutesBefore}`;
                    if (!localStorage.getItem(key)) {
                        // Convert minutes to a friendly label
                        let label = '';
                        if (minutesBefore >= 1440) {
                            label = `${Math.round(minutesBefore/1440)} día(s)`;
                        } else if (minutesBefore >= 60) {
                            label = `${Math.round(minutesBefore/60)} hora(s)`;
                        } else {
                            label = `${minutesBefore} minutos`;
                        }
                        showReminderNotification(event.title, label, 'custom');
                        localStorage.setItem(key, Date.now().toString());
                    }
                }
            }
        });
        
        // Check every hour
        setTimeout(checkReminders, 60 * 60 * 1000);
    }
    
    function showReminderNotification(eventTitle, daysLeft) {
        let message = '';
        if (typeof daysLeft === 'number') {
            if (daysLeft === 1) {
                message = `¡Recuerda! El evento "${eventTitle}" es mañana`;
            } else if (daysLeft === 2) {
                message = `¡Recuerda! El evento "${eventTitle}" es dentro de 2 días`;
            } else {
                message = `¡Recuerda! El evento "${eventTitle}" es dentro de ${daysLeft} días`;
            }
        } else {
            // daysLeft may be a label string for custom reminders
            message = `¡Recordatorio! El evento "${eventTitle}" tiene un recordatorio programado (${daysLeft} antes)`;
        }

        showNotification(message, 'reminder');

        // Integrate with AI chat (simulated)
        integrateWithAIChat(message);
    }
    
    function integrateWithAIChat(message) {
        // In a real implementation, this would send a message to the AI chat
        console.log(`[AI Chat Integration] Enviando recordatorio: ${message}`);
        
        // Simulate sending to AI chat
        const chatNotification = document.createElement('div');
        chatNotification.className = 'ai-chat-notification';
        chatNotification.innerHTML = `
            <div class="ai-chat-notification-content">
                <span class="material-icons-round">auto_awesome</span>
                <div class="ai-chat-notification-text">
                    <p>Asistente IA: ${message}</p>
                </div>
            </div>
        `;
        
        document.body.appendChild(chatNotification);
        
        // Remove after 5 seconds
        setTimeout(() => {
            document.body.removeChild(chatNotification);
        }, 5000);
    }
    
    function showNotification(message, type = 'info') {
        // Remove any existing notifications
        const existingNotifications = document.querySelectorAll('.notification');
        existingNotifications.forEach(notif => notif.remove());
        
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
        
        // Auto remove after 5 seconds (except reminders)
        if (type !== 'reminder') {
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
            'reminder': 'notifications_active',
            'error': 'error'
        };
        return icons[type] || 'info';
    }
    
    function saveEvents() {
        localStorage.setItem('miniAmigixEvents', JSON.stringify(events));
    }
    
    // Initialize original button texts for antires module compatibility
    const gameLaunches = document.querySelectorAll('.game-launch');
    gameLaunches.forEach(button => {
        if (!button.dataset.originalText) {
            button.dataset.originalText = button.textContent;
        }
    });
    
    console.log("📅 Eventos module initialized");
});

// Export functions for use in other modules if needed
window.MiniAmigixEventos = {
    renderCalendar,
    renderUpcomingEvents,
    renderHolidays,
    showNotification
};