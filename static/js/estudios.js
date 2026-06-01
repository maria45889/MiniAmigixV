// Estudios Module JavaScript
document.addEventListener('DOMContentLoaded', () => {
    console.log("📚 MiniAmigixV Estudios: Online");
    
    // DOM Elements
    const timerDisplay = document.getElementById('timer-display');
    const startTimerBtn = document.getElementById('start-timer');
    const pauseTimerBtn = document.getElementById('pause-timer');
    const resetTimerBtn = document.getElementById('reset-timer');
    const modeToggleBtn = document.getElementById('mode-toggle');
    const modeLabel = document.getElementById('mode-label');
    const modeIndicator = document.getElementById('mode-indicator');
    const sessionsToday = document.getElementById('sessions-today');
    const totalTime = document.getElementById('total-time');
    const addTaskForm = document.getElementById('add-task-form');
    const tasksList = document.getElementById('tasks-list');
    const taskProgressBar = document.getElementById('task-progress-bar');
    const taskProgressText = document.getElementById('task-progress-text');
    const calendarDaysStudy = document.getElementById('calendar-days-study');
    const currentMonthYearStudy = document.getElementById('current-month-year-study');
    const prevMonthStudyBtn = document.getElementById('prev-month-study');
    const nextMonthStudyBtn = document.getElementById('next-month-study');
    const calendarEventsStudy = document.getElementById('calendar-events-study');
    const notesContent = document.getElementById('notes-content');
    const addNoteBtn = document.getElementById('add-note');
    const clearNotesBtn = document.getElementById('clear-notes');
    const studyGameClue = document.getElementById('study-game-clue');
    const studyGameAnswerInput = document.getElementById('study-game-answer');
    const studyGameCheckBtn = document.getElementById('study-game-check');
    const studyGameNewBtn = document.getElementById('study-game-new');
    const studyGameFeedback = document.getElementById('study-game-feedback');
    
    // State
    let timerInterval = null;
    let currentGameQuestion = null;
    let timeLeft = 25 * 60; // 25 minutes in seconds
    let isTimerRunning = false;
    let currentMode = 'focus'; // focus or relax
    let focusTime = 25 * 60; // 25 minutes
    let relaxTime = 5 * 60; // 5 minutes
    let sessionsCompletedToday = 0;
    let totalStudyTime = 0; // in seconds
    let tasks = JSON.parse(localStorage.getItem('miniAmigixTasks') || '[]');
    let studyEvents = JSON.parse(localStorage.getItem('miniAmigixStudyEvents') || '[]');
    let notes = JSON.parse(localStorage.getItem('miniAmigixNotes') || '[]');
    let currentDate = new Date();
    let displayDate = new Date(currentDate.getFullYear(), currentDate.getMonth(), 1);
    
    // Initialize
    updateTimerDisplay();
    updateModeUI();
    loadTasks();
    updateTaskProgress();
    loadNotes();
    renderStudyCalendar();
    startClock();
    loadStudyGame();
    
    // Event Listeners
    startTimerBtn.addEventListener('click', startTimer);
    pauseTimerBtn.addEventListener('click', pauseTimer);
    resetTimerBtn.addEventListener('click', resetTimer);
    modeToggleBtn.addEventListener('click', toggleMode);
    addTaskForm.addEventListener('submit', handleAddTask);
    prevMonthStudyBtn.addEventListener('click', () => {
        displayDate = new Date(displayDate.getFullYear(), displayDate.getMonth() - 1, 1);
        renderStudyCalendar();
    });
    nextMonthStudyBtn.addEventListener('click', () => {
        displayDate = new Date(displayDate.getFullYear(), displayDate.getMonth() + 1, 1);
        renderStudyCalendar();
    });
    addNoteBtn.addEventListener('click', addNote);
    clearNotesBtn.addEventListener('click', clearNotes);
    studyGameCheckBtn.addEventListener('click', checkStudyAnswer);
    studyGameNewBtn.addEventListener('click', chooseStudyQuestion);
    
    // Functions
    function startTimer() {
        if (isTimerRunning) return;
        
        isTimerRunning = true;
        startTimerBtn.disabled = true;
        pauseTimerBtn.disabled = false;
        
        timerInterval = setInterval(() => {
            timeLeft--;
            updateTimerDisplay();
            
            if (timeLeft <= 0) {
                clearInterval(timerInterval);
                isTimerRunning = false;
                startTimerBtn.disabled = false;
                pauseTimerBtn.disabled = true;
                
                if (currentMode === 'focus') {
                    sessionsCompletedToday++;
                    totalStudyTime += focusTime;
                    sessionsToday.textContent = sessionsCompletedToday;
                    totalTime.textContent = formatTime(totalStudyTime);
                    saveStats();
                    showNotification('¡Sesión de enfoque completada! Tiempo de relajación.', 'success');
                    
                    // Automatically switch to relax mode
                    setTimeout(() => {
                        currentMode = 'relax';
                        timeLeft = relaxTime;
                        updateTimerDisplay();
                        updateModeUI();
                        startTimer();
                    }, 1000);
                } else {
                    totalStudyTime += relaxTime;
                    totalTime.textContent = formatTime(totalStudyTime);
                    saveStats();
                    showNotification('¡Sesión de relajación completada! Listo para enfocarte nuevamente.', 'success');
                    
                    // Automatically switch to focus mode
                    setTimeout(() => {
                        currentMode = 'focus';
                        timeLeft = focusTime;
                        updateTimerDisplay();
                        updateModeUI();
                    }, 1000);
                }
            }
        }, 1000);
    }
    
    function pauseTimer() {
        if (!isTimerRunning) return;
        
        clearInterval(timerInterval);
        isTimerRunning = false;
        startTimerBtn.disabled = false;
        pauseTimerBtn.disabled = true;
    }
    
    function resetTimer() {
        clearInterval(timerInterval);
        isTimerRunning = false;
        startTimerBtn.disabled = false;
        pauseTimerBtn.disabled = true;
        
        timeLeft = currentMode === 'focus' ? focusTime : relaxTime;
        updateTimerDisplay();
    }
    
    function toggleMode() {
        if (isTimerRunning) {
            showNotification('Detén el temporizador antes de cambiar el modo', 'warning');
            return;
        }
        
        currentMode = currentMode === 'focus' ? 'relax' : 'focus';
        timeLeft = currentMode === 'focus' ? focusTime : relaxTime;
        updateTimerDisplay();
        updateModeUI();
    }
    
    function updateTimerDisplay() {
        const minutes = Math.floor(timeLeft / 60);
        const seconds = timeLeft % 60;
        timerDisplay.textContent = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
    }
    
    function updateModeUI() {
        modeLabel.textContent = currentMode === 'focus' ? 'Modo Enfoque' : 'Modo Relajación';
        modeIndicator.className = `mode-indicator ${currentMode}`;
        modeToggleBtn.textContent = currentMode === 'focus' ? 'Modo: Enfoque' : 'Modo: Relajación';
    }
    
    function handleAddTask(e) {
        e.preventDefault();
        
        const taskInput = document.getElementById('task-input');
        const taskText = taskInput.value.trim();
        
        if (!taskText) return;
        
        const newTask = {
            id: Date.now() + Math.random(),
            text: taskText,
            completed: false,
            createdAt: new Date().toISOString()
        };
        
        tasks.push(newTask);
        saveTasks();
        renderTasks();
        updateTaskProgress();
        
        // Reset input
        taskInput.value = '';
        taskInput.focus();
        
        showNotification('Tarea agregada exitosamente', 'success');
    }
    
    function renderTasks() {
        if (tasks.length === 0) {
            tasksList.innerHTML = `
                <div class="empty-state">
                    <p>No tienes tareas aún. ¡Agrega tu primera tarea!</p>
                </div>
            `;
            return;
        }
        
        tasksList.innerHTML = tasks.map(task => `
            <div class="task-item">
                <div class="task-checkbox">
                    <input type="checkbox" ${task.completed ? 'checked' : ''} data-id="${task.id}">
                    <span class="task-text ${task.completed ? 'completed' : ''}">${task.text}</span>
                </div>
                <button class="btn-icon delete-task" data-id="${task.id}">
                    <span class="material-icons-round">delete</span>
                </button>
            </div>
        `).join('');
        
        // Add event listeners to checkboxes and delete buttons
        document.querySelectorAll('.task-checkbox input').forEach(checkbox => {
            checkbox.addEventListener('change', (e) => {
                const id = parseInt(e.target.dataset.id);
                toggleTaskCompletion(id);
            });
        });
        
        document.querySelectorAll('.delete-task').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const id = parseInt(e.target.dataset.id);
                deleteTask(id);
            });
        });
    }
    
    function toggleTaskCompletion(id) {
        tasks = tasks.map(task => 
            task.id === id ? {...task, completed: !task.completed} : task
        );
        saveTasks();
        renderTasks();
        updateTaskProgress();
        
        const task = tasks.find(t => t.id === id);
        showNotification(
            task.completed ? `Tarea completada: "${task.text}"` : `Tarea reactivada: "${task.text}"`,
            task.completed ? 'success' : 'info'
        );
    }
    
    function deleteTask(id) {
        tasks = tasks.filter(task => task.id !== id);
        saveTasks();
        renderTasks();
        updateTaskProgress();
        showNotification('Tarea eliminada', 'info');
    }
    
    function updateTaskProgress() {
        const totalTasks = tasks.length;
        const completedTasks = tasks.filter(task => task.completed).length;
        const progress = totalTasks > 0 ? (completedTasks / totalTasks) * 100 : 0;
        
        taskProgressBar.style.width = `${progress}%`;
        taskProgressText.textContent = `${Math.round(progress)}%`;
        
        // Update progress bar color based on progress
        if (progress >= 80) {
            taskProgressBar.style.background = 'var(--neon-pink)';
        } else if (progress >= 60) {
            taskProgressBar.style.background = 'var(--neon-cyan)';
        } else if (progress >= 40) {
            taskProgressBar.style.background = '#ff9800';
        } else {
            taskProgressBar.style.background = '#9c27b0';
        }
    }
    
    function saveTasks() {
        localStorage.setItem('miniAmigixTasks', JSON.stringify(tasks));
    }
    
    function loadTasks() {
        tasks = JSON.parse(localStorage.getItem('miniAmigixTasks') || '[]');
        renderTasks();
        updateTaskProgress();
    }
    
    function addNote() {
        const noteContent = prompt('Escribe tu nota de estudio:');
        if (noteContent === null || noteContent.trim() === '') return;
        
        const newNote = {
            id: Date.now() + Math.random(),
            content: noteContent.trim(),
            createdAt: new Date().toISOString()
        };
        
        notes = [...notes, newNote];
        saveNotes();
        renderNotes();
        
        showNotification('Nota agregada exitosamente', 'success');
    }
    
    function renderNotes() {
        if (notes.length === 0) {
            notesContent.innerHTML = `
                <div class="notes-placeholder">
                    <p>Tus notas de estudio aparecerán aquí</p>
                    <p>Usa el botón de arriba para crear una nueva nota</p>
                </div>
            `;
            return;
        }
        
        notesContent.innerHTML = notes.map(note => `
            <div class="note-item">
                <div class="note-content">
                    <p>${note.content}</p>
                </div>
                <div class="note-meta">
                    <small>${new Date(note.createdAt).toLocaleString('es-ES')}</small>
                    <button class="btn-icon delete-note" data-id="${note.id}">
                        <span class="material-icons-round">delete</span>
                    </button>
                </div>
            </div>
        `).join('');
        
        // Add event listeners to delete buttons
        document.querySelectorAll('.delete-note').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const id = parseInt(e.target.dataset.id);
                deleteNote(id);
            });
        });
    }
    
    function deleteNote(id) {
        notes = notes.filter(note => note.id !== id);
        saveNotes();
        renderNotes();
        showNotification('Nota eliminada', 'info');
    }
    
    function clearNotes() {
        if (notes.length === 0) return;
        
        if (confirm('¿Estás seguro de que quieres eliminar todas las notas?')) {
            notes = [];
            saveNotes();
            renderNotes();
            showNotification('Todas las notas han sido eliminadas', 'info');
        }
    }
    
    function saveNotes() {
        localStorage.setItem('miniAmigixNotes', JSON.stringify(notes));
    }
    
    function loadNotes() {
        notes = JSON.parse(localStorage.getItem('miniAmigixNotes') || '[]');
        renderNotes();
    }
    
    const studyQuestions = [
        {
            clue: '¿Qué técnica de estudio usa períodos cortos de trabajo con pausas frecuentes?',
            answer: 'pomodoro'
        },
        {
            clue: '¿Cómo se llama la técnica de repasar información usando tarjetas con preguntas y respuestas?',
            answer: 'flashcards'
        },
        {
            clue: '¿Qué palabra describe un esquema que agrupa ideas principales y secundarias de un tema?',
            answer: 'mapa mental'
        },
        {
            clue: '¿Qué herramienta te ayuda a memorizar conceptos haciendo preguntas en voz alta?',
            answer: 'autoevaluación'
        },
        {
            clue: '¿Qué práctica consiste en explicar el material con tus propias palabras?',
            answer: 'enseñar'
        }
    ];
    
    function normalizeText(text) {
        return text.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase().trim();
    }
    
    function chooseStudyQuestion() {
        currentGameQuestion = studyQuestions[Math.floor(Math.random() * studyQuestions.length)];
        studyGameClue.textContent = currentGameQuestion.clue;
        studyGameAnswerInput.value = '';
        studyGameFeedback.textContent = '';
        studyGameFeedback.className = 'game-feedback';
        studyGameAnswerInput.focus();
    }
    
    function checkStudyAnswer() {
        if (!currentGameQuestion) {
            showNotification('Presiona "Nueva pregunta" para iniciar el reto.', 'warning');
            return;
        }

        const userAnswer = normalizeText(studyGameAnswerInput.value);
        const expectedAnswer = normalizeText(currentGameQuestion.answer);

        if (userAnswer === expectedAnswer) {
            studyGameFeedback.textContent = '¡Correcto! Excelente memoria de estudio.';
            studyGameFeedback.className = 'game-feedback success';
            showNotification('Respuesta correcta. ¡Buen trabajo!', 'success');
        } else {
            studyGameFeedback.textContent = `La respuesta correcta era: ${currentGameQuestion.answer}`;
            studyGameFeedback.className = 'game-feedback error';
            showNotification('Sigue intentando. ¡Puedes con ello!', 'info');
        }
    }
    
    function loadStudyGame() {
        chooseStudyQuestion();
    }
    
    function renderStudyCalendar() {
        const year = displayDate.getFullYear();
        const month = displayDate.getMonth();
        
        currentMonthYearStudy.textContent = new Date(year, month).toLocaleDateString('es-ES', { 
            year: 'numeric', 
            month: 'long' 
        });
        
        // Clear previous days
        calendarDaysStudy.innerHTML = '';
        calendarEventsStudy.innerHTML = '';
        
        // Get first day of month and number of days
        const firstDay = new Date(year, month, 1);
        const daysInMonth = new Date(year, month + 1, 0).getDate();
        
        // Add empty cells for days before the 1st
        const startingDay = firstDay.getDay(); // 0 = Sunday, 1 = Monday, etc.
        for (let i = 0; i < startingDay; i++) {
            const emptyDiv = document.createElement('div');
            emptyDiv.className = 'calendar-day empty';
            calendarDaysStudy.appendChild(emptyDiv);
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
            
            // Check if there are study events on this day
            const eventsOnDay = studyEvents.filter(event => {
                const eventDate = new Date(event.date);
                return eventDate.getDate() === day && 
                       eventDate.getMonth() === month && 
                       eventDate.getFullYear() === year;
            });
            
            if (eventsOnDay.length > 0) {
                dayDiv.classList.add('has-events');
                dayDiv.title = `${eventsOnDay.length} evento(s) académico(s) este día`;
                
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
            
            // Add click event to show day details
            dayDiv.addEventListener('click', () => showStudyDayEvents(day, month, year));
            
            calendarDaysStudy.appendChild(dayDiv);
        }
        
        // Show events for current month in the events section
        renderStudyMonthEvents();
    }
    
    function showStudyDayEvents(day, month, year) {
        const eventsOnDay = studyEvents.filter(event => {
            const eventDate = new Date(event.date);
            return eventDate.getDate() === day && 
                   eventDate.getMonth() === month && 
                   eventDate.getFullYear() === year;
        });
        
        if (eventsOnDay.length === 0) {
            showNotification(`No hay eventos académicos programados para el ${day}/${month + 1}/${year}`, 'info');
            return;
        }
        
        // Create modal to show day events
        const modal = document.createElement('div');
        modal.className = 'day-events-modal';
        modal.innerHTML = `
            <div class="day-events-modal-content">
                <div class="day-events-modal-header">
                    <span class="material-icons-round close-modal">close</span>
                    <h2>Eventos Académicos del ${day}/${month + 1}/${year}</h2>
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
                completeStudyEvent(id);
                document.body.removeChild(modal);
                showStudyDayEvents(day, month, year); // Refresh
            });
        });
        
        modal.querySelectorAll('.delete-event').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const id = parseInt(e.currentTarget.dataset.id);
                deleteStudyEvent(id);
                document.body.removeChild(modal);
                showStudyDayEvents(day, month, year); // Refresh
            });
        });
    }
    
    function renderStudyMonthEvents() {
        const year = displayDate.getFullYear();
        const month = displayDate.getMonth();
        
        const eventsInMonth = studyEvents.filter(event => {
            const eventDate = new Date(event.date);
            return eventDate.getMonth() === month && 
                   eventDate.getFullYear() === year;
        });
        
        if (eventsInMonth.length === 0) {
            calendarEventsStudy.innerHTML = `
                <div class="empty-state">
                    <p>No hay eventos académicos este mes</p>
                </div>
            `;
            return;
        }
        
        calendarEventsStudy.innerHTML = eventsInMonth.map(event => {
            const eventDate = new Date(event.date);
            return `
                <div class="study-event-item">
                    <div class="event-date">
                        ${eventDate.getDate()} de ${eventDate.toLocaleString('es-ES', { month: 'long' })}
                    </div>
                    <div class="event-info">
                        <h4>${event.title}</h4>
                        <p>${event.description || 'Sin descripción'}</p>
                    </div>
                </div>
            `;
        }).join('');
    }
    
    function completeStudyEvent(id) {
        studyEvents = studyEvents.map(event => 
            event.id === id ? {...event, completed: true} : event
        );
        saveStudyEvents();
        renderStudyCalendar();
        showNotification('Evento académico marcado como completado', 'success');
    }
    
    function deleteStudyEvent(id) {
        studyEvents = studyEvents.filter(event => event.id !== id);
        saveStudyEvents();
        renderStudyCalendar();
        showNotification('Evento académico eliminado', 'info');
    }
    
    function saveStudyEvents() {
        localStorage.setItem('miniAmigixStudyEvents', JSON.stringify(studyEvents));
    }
    
    function loadStudyEvents() {
        studyEvents = JSON.parse(localStorage.getItem('miniAmigixStudyEvents') || '[]');
        renderStudyCalendar();
    }
    
    function startClock() {
        function updateClock() {
            const now = new Date();
            // Update the main clock in the header (already handled by base.html)
            // We could add additional clocks here if needed
        }
        
        updateClock(); // Initial call
        setInterval(updateClock, 1000);
    }
    
    function formatTime(seconds) {
        const hours = Math.floor(seconds / 3600);
        const minutes = Math.floor((seconds % 3600) / 60);
        const remainingSeconds = seconds % 60;
        
        const parts = [];
        if (hours > 0) parts.push(`${hours}h`);
        if (minutes > 0 || hours > 0) parts.push(`${minutes}m`);
        parts.push(`${remainingSeconds}s`);
        
        return parts.join(' ');
    }
    
    function saveStats() {
        localStorage.setItem('miniAmigixSessionsToday', sessionsCompletedToday.toString());
        localStorage.setItem('miniAmigixTotalStudyTime', totalStudyTime.toString());
    }
    
    function loadStats() {
        sessionsCompletedToday = parseInt(localStorage.getItem('miniAmigixSessionsToday') || '0');
        totalStudyTime = parseInt(localStorage.getItem('miniAmigixTotalStudyTime') || '0');
        sessionsToday.textContent = sessionsCompletedToday;
        totalTime.textContent = formatTime(totalStudyTime);
    }
    
    function showNotification(message, type = 'info') {
        // Import the notification function from eventos.js if available, or create a simple version
        if (typeof window.MiniAmigixEventos !== 'undefined' && window.MiniAmigixEventos.showNotification) {
            window.MiniAmigixEventos.showNotification(message, type);
        } else {
            // Simple fallback notification
            console.log(`[${type}] ${message}`);
            alert(message);
        }
    }
    
    // Initialize stats
    loadStats();
    
    // Export functions for use in other modules if needed
    window.MiniAmigixEstudios = {
        startTimer,
        pauseTimer,
        resetTimer,
        toggleMode,
        renderTasks,
        updateTaskProgress,
        addNote,
        renderStudyCalendar
    };
    
    console.log("📚 Estudios module initialized");
});