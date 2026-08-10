// =====================================================
// MINIAMIGIXV — ESTUDIO & APRENDIZAJE v4.0
// JavaScript para funcionalidades interactivas
// =====================================================

// Estado global de la aplicación
const EstadoEstudio = {
    pomodoro: {
        tiempoRestante: 25 * 60, // 25 minutos en segundos
        intervalo: null,
    },
    metas: [],
    notas: [],
    estadisticas: {
        sesionesCompletadas: 0,
        tiempoTotal: 0,
        xp: 0,
        streak: 0
    }
};

// Frases motivacionales para Pomodoro
const frasesMotivacionales = [
    "¡Un Pomodoro más y lo tienes! 🍅",
    "Cada minuto cuenta, ¡sigue así! ⏰",
    "El enfoque es tu superpoder hoy 🎯",
    "Pequeños pasos, grandes resultados 🚀",
    "Tu concentración está en su punto máximo 💪",
    "¡A por el siguiente nivel! ⭐",
    "El éxito se construye sesión a sesión 📈",
    "Mantén el ritmo, ¡lo estás haciendo genial! 🔥",
    "Cada Pomodoro te acerca a tu meta 🎯",
    "La disciplina es el puente entre metas y logros 🌟"
];

// Historial de actividad de ejemplo
const actividadEjemplo = [
    { tipo: 'pomodoro', texto: 'Completaste una sesión Pomodoro', tiempo: 'Hace 20 min' },
    { tipo: 'nota', texto: 'Creaste una nota', tiempo: 'Hace 1 h' },
    { tipo: 'xp', texto: 'Ganaste 50 XP', tiempo: 'Ayer' },
    { tipo: 'streak', texto: 'Mantuviste tu racha', tiempo: 'Ayer' }
];

// =====================================================
// INICIALIZACIÓN
// =====================================================
document.addEventListener('DOMContentLoaded', function() {
    inicializarPomodoro();
    inicializarCalendario();
    inicializarMetas();
    inicializarNotas();
    cargarEstadisticas();
    inicializarEventListeners();
});

function inicializarEventListeners() {
    // Event listeners para modales
    document.getElementById('btn-new-note').addEventListener('click', showNoteModal);
    document.getElementById('btn-add-goal').addEventListener('click', showGoalModal);
    
    // Event listeners para color picker
    document.querySelectorAll('.color-option').forEach(btn => {
        btn.addEventListener('click', function() {
            document.querySelectorAll('.color-option').forEach(b => b.classList.remove('selected'));
            this.classList.add('selected');
        });
    });
    
    // Seleccionar primer color por defecto
    if (document.querySelector('.color-option')) {
        document.querySelector('.color-option').classList.add('selected');
    }
    
    // Inicializar frase motivacional
    actualizarFraseMotivacional();
    
    // Cargar actividad
    cargarActividad();
}

// =====================================================
// POMODORO
// =====================================================
function inicializarPomodoro() {
    const btnStart = document.getElementById('pomodoro-start');
    const btnPause = document.getElementById('pomodoro-pause');
    const btnReset = document.getElementById('pomodoro-reset');
    
    btnStart.addEventListener('click', iniciarPomodoro);
    btnPause.addEventListener('click', pausarPomodoro);
    btnReset.addEventListener('click', reiniciarPomodoro);
    
    // Cargar datos guardados
    cargarDatosPomodoro();
}

function iniciarPomodoro() {
    if (EstadoEstudio.pomodoro.corriendo) return;
    
    EstadoEstudio.pomodoro.corriendo = true;
    document.getElementById('pomodoro-start').style.display = 'none';
    document.getElementById('pomodoro-pause').style.display = 'flex';
    document.querySelector('.pomodoro-card').classList.add('pomodoro-active');
    
    EstadoEstudio.pomodoro.intervalo = setInterval(() => {
        EstadoEstudio.pomodoro.tiempoRestante--;
        
        if (EstadoEstudio.pomodoro.tiempoRestante <= 0) {
            completarPomodoro();
        } else {
            actualizarDisplayPomodoro();
        }
    }, 1000);
}

function pausarPomodoro() {
    if (!EstadoEstudio.pomodoro.corriendo) return;
    
    EstadoEstudio.pomodoro.corriendo = false;
    clearInterval(EstadoEstudio.pomodoro.intervalo);
    
    document.getElementById('pomodoro-start').style.display = 'flex';
    document.getElementById('pomodoro-pause').style.display = 'none';
    document.querySelector('.pomodoro-card').classList.remove('pomodoro-active');
}

function reiniciarPomodoro() {
    pausarPomodoro();
    EstadoEstudio.pomodoro.tiempoRestante = 25 * 60;
    actualizarDisplayPomodoro();
}

function completarPomodoro() {
    pausarPomodoro();
    EstadoEstudio.pomodoro.pomodorosHoy++;
    EstadoEstudio.pomodoro.totalPomodoros++;
    
    // Guardar en servidor
    guardarPomodoroCompletado();
    
    // Mostrar notificación
    mostrarNotificacion('🍅 ¡Pomodoro completado! Bien hecho.', 'success');
    
    // Agregar actividad
    agregarActividad('pomodoro', 'Completaste una sesión Pomodoro');
    
    // Actualizar frase motivacional
    actualizarFraseMotivacional();
    
    // Reiniciar para el siguiente
    reiniciarPomodoro();
    actualizarEstadisticasPomodoro();
}

function actualizarFraseMotivacional() {
    const fraseElement = document.getElementById('timer-motivational');
    if (fraseElement) {
        const fraseAleatoria = frasesMotivacionales[Math.floor(Math.random() * frasesMotivacionales.length)];
        fraseElement.textContent = fraseAleatoria;
    }
}

function cargarActividad() {
    const actividadTimeline = document.getElementById('activity-timeline');
    if (!actividadTimeline) return;
    
    // Usar actividad de ejemplo por ahora
    EstadoEstudio.actividad = actividadEjemplo;
    renderizarActividad();
}

function renderizarActividad() {
    const actividadTimeline = document.getElementById('activity-timeline');
    if (!actividadTimeline) return;
    
    actividadTimeline.innerHTML = '';
    
    EstadoEstudio.actividad.forEach(item => {
        const activityItem = document.createElement('div');
        activityItem.className = 'activity-item';
        
        const iconClass = `activity-${item.tipo}`;
        const iconEmoji = obtenerIconoActividad(item.tipo);
        
        activityItem.innerHTML = `
            <div class="activity-icon ${iconClass}">${iconEmoji}</div>
            <div class="activity-content">
                <span class="activity-text">${item.texto}</span>
                <span class="activity-time">${item.tiempo}</span>
            </div>
        `;
        
        actividadTimeline.appendChild(activityItem);
    });
}

function obtenerIconoActividad(tipo) {
    const iconos = {
        'pomodoro': '🟢',
        'nota': '🟣',
        'xp': '⭐',
        'streak': '🔥',
        'meta': '🎯',
        'nivel': '🏆'
    };
    return iconos[tipo] || '📌';
}

function agregarActividad(tipo, texto) {
    const nuevaActividad = {
        tipo: tipo,
        texto: texto,
        tiempo: 'Ahora mismo'
    };
    
    EstadoEstudio.actividad.unshift(nuevaActividad);
    
    // Mantener solo las últimas 10 actividades
    if (EstadoEstudio.actividad.length > 10) {
        EstadoEstudio.actividad = EstadoEstudio.actividad.slice(0, 10);
    }
    
    renderizarActividad();
}

function actualizarDisplayPomodoro() {
    const minutos = Math.floor(EstadoEstudio.pomodoro.tiempoRestante / 60);
    const segundos = EstadoEstudio.pomodoro.tiempoRestante % 60;
    const display = `${minutos.toString().padStart(2, '0')}:${segundos.toString().padStart(2, '0')}`;
    
    const displayElement = document.getElementById('pomodoro-display');
    if (displayElement) {
        displayElement.textContent = display;
    }
    document.title = `${display} - Pomodoro`;
    
    // Actualizar barra de progreso de sesión
    const totalTiempo = 25 * 60;
    const progreso = ((totalTiempo - EstadoEstudio.pomodoro.tiempoRestante) / totalTiempo) * 100;
    const sessionFill = document.getElementById('session-progress-fill');
    if (sessionFill) {
        sessionFill.style.width = `${progreso}%`;
    }
}

function actualizarEstadisticasPomodoro() {
    document.getElementById('pomodoros-today').textContent = EstadoEstudio.pomodoro.pomodorosHoy;
    document.getElementById('total-pomodoros').textContent = EstadoEstudio.pomodoro.totalPomodoros;
}

async function guardarPomodoroCompletado() {
    try {
        const response = await fetch('/estudio/api/guardar-pomodoro/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken()
            },
            body: JSON.stringify({
                duracion_minutos: 25,
                tipo: 'trabajo'
            })
        });
        
        if (response.ok) {
            const data = await response.json();
            console.log('Pomodoro guardado:', data);
        }
    } catch (error) {
        console.error('Error al guardar pomodoro:', error);
    }
}

async function cargarDatosPomodoro() {
    try {
        const response = await fetch('/estudio/api/obtener-estadisticas/');
        if (response.ok) {
            const data = await response.json();
            EstadoEstudio.pomodoro.pomodorosHoy = data.pomodoros_hoy || 0;
            EstadoEstudio.pomodoro.totalPomodoros = data.total_pomodoros || 0;
            actualizarEstadisticasPomodoro();
        }
    } catch (error) {
        console.error('Error al cargar datos de pomodoro:', error);
    }
}

// =====================================================
// CALENDARIO
// =====================================================
function inicializarCalendario() {
    generarCalendario();
    
    document.getElementById('calendar-prev').addEventListener('click', () => {
        EstadoEstudio.calendario.fechaMostrada.setMonth(EstadoEstudio.calendario.fechaMostrada.getMonth() - 1);
        generarCalendario();
    });
    
    document.getElementById('calendar-next').addEventListener('click', () => {
        EstadoEstudio.calendario.fechaMostrada.setMonth(EstadoEstudio.calendario.fechaMostrada.getMonth() + 1);
        generarCalendario();
    });
    
    cargarDiasEstudiados();
}

function generarCalendario() {
    const fecha = EstadoEstudio.calendario.fechaMostrada;
    const año = fecha.getFullYear();
    const mes = fecha.getMonth();
    
    // Actualizar título del mes
    const nombresMeses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 
                          'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'];
    document.getElementById('calendar-month').textContent = `${nombresMeses[mes]} ${año}`;
    
    // Obtener primer día del mes y total de días
    const primerDia = new Date(año, mes, 1);
    const ultimoDia = new Date(año, mes + 1, 0);
    const diasEnMes = ultimoDia.getDate();
    const diaSemanaInicio = (primerDia.getDay() + 6) % 7; // Ajustar para que lunes sea 0
    
    // Generar días
    const calendarDays = document.getElementById('calendar-days');
    calendarDays.innerHTML = '';
    
    // Días del mes anterior
    const mesAnterior = new Date(año, mes, 0);
    const diasMesAnterior = mesAnterior.getDate();
    
    for (let i = diaSemanaInicio - 1; i >= 0; i--) {
        const dia = document.createElement('div');
        dia.className = 'calendar-day other-month';
        dia.textContent = diasMesAnterior - i;
        calendarDays.appendChild(dia);
    }
    
    // Días del mes actual
    const hoy = new Date();
    for (let i = 1; i <= diasEnMes; i++) {
        const dia = document.createElement('div');
        dia.className = 'calendar-day';
        dia.textContent = i;
        
        // Marcar hoy
        if (i === hoy.getDate() && mes === hoy.getMonth() && año === hoy.getFullYear()) {
            dia.classList.add('today');
        }
        
        // Marcar días estudiados
        const fechaStr = `${año}-${String(mes + 1).padStart(2, '0')}-${String(i).padStart(2, '0')}`;
        if (EstadoEstudio.calendario.diasEstudiados.includes(fechaStr)) {
            dia.classList.add('studied');
        }
        
        dia.addEventListener('click', () => seleccionarDia(i, mes, año));
        calendarDays.appendChild(dia);
    }
    
    // Días del mes siguiente
    const totalCeldas = calendarDays.children.length;
    const diasSiguientes = 42 - totalCeldas; // 6 filas de 7 días
    
    for (let i = 1; i <= diasSiguientes; i++) {
        const dia = document.createElement('div');
        dia.className = 'calendar-day other-month';
        dia.textContent = i;
        calendarDays.appendChild(dia);
    }
}

function seleccionarDia(dia, mes, año) {
    const fecha = new Date(año, mes, dia);
    const fechaStr = fecha.toLocaleDateString('es-ES', { 
        weekday: 'long', 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric' 
    });
    
    console.log('Día seleccionado:', fechaStr);
    // Aquí podrías mostrar detalles del día seleccionado
}

async function cargarDiasEstudiados() {
    try {
        const response = await fetch('/estudio/api/obtener-dias-estudiados/');
        if (response.ok) {
            const data = await response.json();
            EstadoEstudio.calendario.diasEstudiados = data.dias || [];
            generarCalendario();
        }
    } catch (error) {
        console.error('Error al cargar días estudiados:', error);
    }
}

// =====================================================
// METAS
// =====================================================
function inicializarMetas() {
    cargarMetas();
}

async function cargarMetas() {
    try {
        const response = await fetch('/estudio/api/obtener-metas/');
        if (response.ok) {
            const data = await response.json();
            EstadoEstudio.metas = data.metas || [];
            renderizarMetas();
        }
    } catch (error) {
        console.error('Error al cargar metas:', error);
        mostrarEstadoVacioMetas();
    }
}

function renderizarMetas() {
    const goalsList = document.getElementById('goals-list');
    const goalsEmpty = document.getElementById('goals-empty');
    
    if (EstadoEstudio.metas.length === 0) {
        goalsList.style.display = 'none';
        goalsEmpty.style.display = 'block';
        return;
    }
    
    goalsList.style.display = 'block';
    goalsEmpty.style.display = 'none';
    
    goalsList.innerHTML = '';
    
    EstadoEstudio.metas.forEach(meta => {
        const goalItem = document.createElement('div');
        goalItem.className = `goal-item ${meta.completada ? 'completed' : ''}`;
        goalItem.innerHTML = `
            <div class="goal-checkbox ${meta.completada ? 'checked' : ''}" 
                 onclick="toggleMeta('${meta.id}')"></div>
            <div class="goal-content">
                <div class="goal-title">${meta.titulo}</div>
                ${meta.descripcion ? `<div class="goal-description">${meta.descripcion}</div>` : ''}
            </div>
            <button class="goal-delete" onclick="eliminarMeta('${meta.id}')">✕</button>
        `;
        goalsList.appendChild(goalItem);
    });
    
    actualizarProgresoMetas();
}

function actualizarProgresoMetas() {
    const total = EstadoEstudio.metas.length;
    const completadas = EstadoEstudio.metas.filter(m => m.completada).length;
    const porcentaje = total > 0 ? (completadas / total) * 100 : 0;
    
    document.getElementById('goals-progress-fill').style.width = `${porcentaje}%`;
    document.getElementById('goals-completed').textContent = completadas;
    document.getElementById('goals-total').textContent = total;
}

function mostrarEstadoVacioMetas() {
    document.getElementById('goals-list').style.display = 'none';
    document.getElementById('goals-empty').style.display = 'block';
}

function showGoalModal() {
    document.getElementById('goal-modal').style.display = 'flex';
    document.getElementById('goal-title').value = '';
    document.getElementById('goal-description').value = '';
    document.getElementById('goal-title').focus();
}

function closeGoalModal() {
    document.getElementById('goal-modal').style.display = 'none';
}

async function saveGoal() {
    const titulo = document.getElementById('goal-title').value.trim();
    const descripcion = document.getElementById('goal-description').value.trim();
    
    if (!titulo) {
        mostrarNotificacion('Por favor, ingresa un título para la meta', 'error');
        return;
    }
    
    try {
        const response = await fetch('/estudio/api/guardar-meta/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken()
            },
            body: JSON.stringify({
                titulo: titulo,
                descripcion: descripcion
            })
        });
        
        if (response.ok) {
            const data = await response.json();
            EstadoEstudio.metas.push(data.meta);
            renderizarMetas();
            closeGoalModal();
            mostrarNotificacion('Meta guardada exitosamente', 'success');
        } else {
            mostrarNotificacion('Error al guardar la meta', 'error');
        }
    } catch (error) {
        console.error('Error al guardar meta:', error);
        mostrarNotificacion('Error al guardar la meta', 'error');
    }
}

async function toggleMeta(metaId) {
    try {
        const response = await fetch(`/estudio/api/toggle-meta/${metaId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken()
            }
        });
        
        if (response.ok) {
            const meta = EstadoEstudio.metas.find(m => m.id === metaId);
            if (meta) {
                meta.completada = !meta.completada;
                renderizarMetas();
            }
        }
    } catch (error) {
        console.error('Error al cambiar estado de meta:', error);
    }
}

async function eliminarMeta(metaId) {
    if (!confirm('¿Estás seguro de eliminar esta meta?')) return;
    
    try {
        const response = await fetch(`/estudio/api/eliminar-meta/${metaId}/`, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': getCsrfToken()
            }
        });
        
        if (response.ok) {
            EstadoEstudio.metas = EstadoEstudio.metas.filter(m => m.id !== metaId);
            renderizarMetas();
            mostrarNotificacion('Meta eliminada', 'success');
        }
    } catch (error) {
        console.error('Error al eliminar meta:', error);
        mostrarNotificacion('Error al eliminar la meta', 'error');
    }
}

// =====================================================
// NOTAS
// =====================================================
function inicializarNotas() {
    cargarNotas();
}

async function cargarNotas() {
    try {
        const response = await fetch('/estudio/api/obtener-notas/');
        if (response.ok) {
            const data = await response.json();
            EstadoEstudio.notas = data.notas || [];
            renderizarNotas();
        }
    } catch (error) {
        console.error('Error al cargar notas:', error);
        mostrarEstadoVacioNotas();
    }
}

function renderizarNotas() {
    const notesGrid = document.getElementById('notes-grid');
    const notesEmpty = document.getElementById('notes-empty');
    
    if (EstadoEstudio.notas.length === 0) {
        if (notesGrid) notesGrid.style.display = 'none';
        if (notesEmpty) notesEmpty.style.display = 'block';
        return;
    }
    
    if (notesGrid) notesGrid.style.display = 'grid';
    if (notesEmpty) notesEmpty.style.display = 'none';
    
    if (notesGrid) {
        notesGrid.innerHTML = '';
        
        // Mostrar solo las últimas 6 notas
        const notasRecientes = EstadoEstudio.notas.slice(0, 6);
        
        notasRecientes.forEach(nota => {
            const noteCard = document.createElement('div');
            noteCard.className = 'note-card';
            noteCard.style.setProperty('--note-color', nota.color || '#fef08a');
            
            // Generar icono de categoría basado en el color
            const categoriaIcon = obtenerIconoCategoria(nota.color);
            const categoriaNombre = obtenerNombreCategoria(nota.color);
            
            noteCard.innerHTML = `
                <div class="note-card-header">
                    <span class="note-category-icon">${categoriaIcon}</span>
                    <h3 class="note-title">${nota.titulo || 'Sin título'}</h3>
                </div>
                <p class="note-preview">${nota.contenido || ''}</p>
                <div class="note-meta">
                    <span class="note-date">📅 ${nota.fecha_creacion || ''}</span>
                    <span class="note-category">${categoriaNombre}</span>
                </div>
            `;
            noteCard.addEventListener('click', () => abrirNota(nota));
            notesGrid.appendChild(noteCard);
        });
    }
}

function obtenerIconoCategoria(color) {
    // Asignar iconos basados en colores
    const iconosPorColor = {
        '#fef08a': '💡', // Amarillo - Ideas
        '#bbf7d0': '📚', // Verde - Estudio
        '#a5f3fc': '💻', // Cyan - Tecnología
        '#fecaca': '❤️', // Rojo - Personal
        '#e9d5ff': '🎨'  // Púrpura - Creatividad
    };
    return iconosPorColor[color] || '📝';
}

function obtenerNombreCategoria(color) {
    const nombresPorColor = {
        '#fef08a': 'Ideas',
        '#bbf7d0': 'Estudio',
        '#a5f3fc': 'Tecnología',
        '#fecaca': 'Personal',
        '#e9d5ff': 'Creatividad'
    };
    return nombresPorColor[color] || 'General';
}

function mostrarEstadoVacioNotas() {
    document.getElementById('notes-grid').style.display = 'none';
    document.getElementById('notes-empty').style.display = 'block';
}

function showNoteModal() {
    document.getElementById('note-modal').style.display = 'flex';
    document.getElementById('note-title').value = '';
    document.getElementById('note-content').value = '';
    document.getElementById('note-title').focus();
}

function closeNoteModal() {
    document.getElementById('note-modal').style.display = 'none';
}

async function saveNote() {
    const titulo = document.getElementById('note-title').value.trim();
    const contenido = document.getElementById('note-content').value.trim();
    const color = document.querySelector('.color-option.selected')?.dataset.color || '#fef08a';
    
    if (!contenido) {
        mostrarNotificacion('Por favor, escribe el contenido de la nota', 'error');
        return;
    }
    
    try {
        const response = await fetch('/estudio/api/guardar-nota/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken()
            },
            body: JSON.stringify({
                titulo: titulo,
                contenido: contenido,
                color: color
            })
        });
        
        if (response.ok) {
            const data = await response.json();
            EstadoEstudio.notas.unshift(data.nota);
            renderizarNotas();
            closeNoteModal();
            mostrarNotificacion('Nota guardada exitosamente', 'success');
        } else {
            mostrarNotificacion('Error al guardar la nota', 'error');
        }
    } catch (error) {
        console.error('Error al guardar nota:', error);
        mostrarNotificacion('Error al guardar la nota', 'error');
    }
}

function abrirNota(nota) {
    // Aquí podrías implementar la visualización completa de la nota
    console.log('Abrir nota:', nota);
    mostrarNotificacion('Funcionalidad de ver nota completa próximamente', 'info');
}

async function eliminarNota(notaId) {
    if (!confirm('¿Estás seguro de eliminar esta nota?')) return;
    
    try {
        const response = await fetch(`/estudio/api/eliminar-nota/${notaId}/`, {
            method: 'DELETE',
            headers: {
                'X-CSRFToken': getCsrfToken()
            }
        });
        
        if (response.ok) {
            EstadoEstudio.notas = EstadoEstudio.notas.filter(n => n.id !== notaId);
            renderizarNotas();
            mostrarNotificacion('Nota eliminada', 'success');
        }
    } catch (error) {
        console.error('Error al eliminar nota:', error);
        mostrarNotificacion('Error al eliminar la nota', 'error');
    }
}

// =====================================================
// ESTADÍSTICAS
// =====================================================
async function cargarEstadisticas() {
    try {
        const response = await fetch('/estudio/api/obtener-estadisticas/');
        if (response.ok) {
            const data = await response.json();
            
            EstadoEstudio.estadisticas = {
                horasEstudiadas: data.horas_estudiadas || 0,
                racha: data.racha || 0,
                nivel: data.nivel || 1,
                xp: data.xp || 0,
                progresoSemanal: data.progreso_semanal || 0
            };
            
            actualizarEstadisticasUI();
        }
    } catch (error) {
        console.error('Error al cargar estadísticas:', error);
    }
}

function actualizarEstadisticasUI() {
    const stats = EstadoEstudio.estadisticas;
    
    document.getElementById('study-hours').textContent = `${stats.horasEstudiadas}h`;
    document.getElementById('study-streak').textContent = `${stats.racha} días`;
    document.getElementById('study-level').textContent = `Nivel ${stats.nivel}`;
    document.getElementById('weekly-progress').textContent = `+${stats.progresoSemanal}%`;
    
    // Calcular progreso de XP
    const xpParaNivel = stats.nivel * 100;
    const progresoXP = (stats.xp / xpParaNivel) * 100;
    
    // Actualizar barra de progreso lineal (si existe)
    const xpProgress = document.getElementById('xp-progress');
    if (xpProgress) {
        xpProgress.style.width = `${progresoXP}%`;
    }
    
    // Actualizar progreso circular
    const xpRing = document.getElementById('xp-ring');
    if (xpRing) {
        const circumference = 2 * Math.PI * 32; // r = 32
        const offset = circumference - (progresoXP / 100) * circumference;
        xpRing.style.strokeDashoffset = offset;
    }
    
    // Actualizar texto de XP
    const currentXp = document.getElementById('current-xp');
    if (currentXp) {
        currentXp.textContent = stats.xp;
    }
    
    const nextLevel = document.getElementById('next-level');
    if (nextLevel) {
        nextLevel.textContent = `Siguiente nivel: ${xpParaNivel} XP`;
    }
}

// =====================================================
// UTILIDADES
// =====================================================
function getCsrfToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]')?.value || 
           document.cookie.split('; ').find(row => row.startsWith('csrftoken='))?.split('=')[1] || '';
}

function mostrarNotificacion(mensaje, tipo = 'info') {
    // Crear elemento de notificación
    const notificacion = document.createElement('div');
    notificacion.className = `notificacion notificacion-${tipo}`;
    notificacion.textContent = mensaje;
    
    // Estilos
    notificacion.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 16px 24px;
        background: ${tipo === 'success' ? 'linear-gradient(135deg, #10b981, #059669)' : 
                   tipo === 'error' ? 'linear-gradient(135deg, #f43f5e, #e11d48)' : 
                   'linear-gradient(135deg, #7c3aed, #6d28d9)'};
        color: white;
        border-radius: 12px;
        font-size: 14px;
        font-weight: 500;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        z-index: 10000;
        animation: slideInRight 0.3s ease;
        backdrop-filter: blur(10px);
    `;
    
    document.body.appendChild(notificacion);
    
    // Eliminar después de 3 segundos
    setTimeout(() => {
        notificacion.style.animation = 'slideOutRight 0.3s ease';
        setTimeout(() => notificacion.remove(), 300);
    }, 3000);
}

// Agregar animaciones CSS dinámicamente
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(100px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes slideOutRight {
        from {
            opacity: 1;
            transform: translateX(0);
        }
        to {
            opacity: 0;
            transform: translateX(100px);
        }
    }
`;
document.head.appendChild(style);
