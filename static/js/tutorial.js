document.addEventListener('DOMContentLoaded', () => {
    console.log('📘 MiniAmigixV Tutorial: Iniciado');

    const skipBtn = document.getElementById('skip-tutorial');
    const startFullBtn = document.getElementById('start-full-tutorial');
    const tutorialStarts = document.querySelectorAll('.tutorial-start');
    const tutorialMenu = document.querySelector('.tutorial-menu');
    const tutorialSteps = document.querySelector('.tutorial-steps');
    const stepTitle = document.getElementById('tutorial-step-title');
    const stepContent = document.getElementById('tutorial-step-content');
    const nextBtn = document.getElementById('tutorial-next-btn');
    const prevBtn = document.getElementById('tutorial-prev-btn');
    const closeBtn = document.getElementById('tutorial-close-btn');
    const backBtn = document.getElementById('tutorial-back-btn');
    const resetTutorialBtn = document.getElementById('reset-tutorial');

    const TUTORIAL_SKIP_KEY = 'miniAmigixTutorialSkipped';
    const TUTORIAL_STATE_KEY = 'miniAmigixTutorialState';

    // Simple step data for modules
    const MODULE_STEPS = {
        chat: [
            { title: 'Bienvenido al Chat IA', content: '<p>El Chat IA te permite conversar con nuestro asistente inteligente. Escribe tu mensaje en la caja de texto y presiona enviar.</p>' },
            { title: 'Usos comunes', content: '<ul><li>Pide resúmenes</li><li>Solicita ayuda para tareas</li><li>Pídele ideas creativas</li></ul>' },
            { title: 'Consejos', content: '<p>Usa mensajes claros y provee contexto para mejores respuestas.</p>' }
        ],
        musica: [
            { title: 'Música: Reproducción', content: '<p>En el módulo Música puedes añadir canciones, crear playlists y reproducir en el mini-player flotante.</p>' },
            { title: 'Controles básicos', content: '<p>Usa los botones Play/Pausa, controla el volumen y cambia de canción desde la lista.</p>' }
        ],
        clima: [
            { title: 'Clima: Buscar ciudad', content: '<p>Busca por ciudad o usa el auto-complete. Si tienes API KEY activa el sistema mostrará pronósticos reales.</p>' },
            { title: 'Recomendaciones', content: '<p>El módulo muestra alertas y recomendaciones basadas en las condiciones actuales.</p>' }
        ],
        eventos: [
            { title: 'Eventos: Crear evento', content: '<p>Usa el formulario para agregar título, descripción, fecha y recordatorios.</p>' },
            { title: 'Recordatorios', content: '<p>El sistema enviará recordatorios locales en las fechas programadas (si el navegador lo permite).</p>' }
        ],
        juegos: [
            { title: 'Juegos: Explorar', content: '<p>Encuentra juegos en la lista y ábrelos desde las tarjetas. Cada juego busca relajar o entretener.</p>' }
        ],
        estudios: [
            { title: 'Estudios: Temporizador', content: '<p>El temporizador tiene modos Enfoque y Relajación para ayudarte a organizar sesiones de estudio.</p>' },
            { title: 'Tareas y progreso', content: '<p>Agrega tareas, completa y elimina; el progreso se calcula automáticamente.</p>' }
        ],
        entretenimiento: [
            { title: 'Entretenimiento: Actividades', content: '<p>Accede a adivinanzas, ruleta, galleta de la fortuna, retos y más para distraerte y relajarte.</p>' }
        ],
        traductor: [
            { title: 'Traductor', content: '<p>Traduce textos entre idiomas de forma rápida y guarda traducciones frecuentes.</p>' }
        ]
    };

    // Utility: save state
    function saveState(state) {
        localStorage.setItem(TUTORIAL_STATE_KEY, JSON.stringify(state));
    }
    function loadState() {
        try { return JSON.parse(localStorage.getItem(TUTORIAL_STATE_KEY) || 'null'); } catch(e){ return null; }
    }

    // If skipped previously, offer quick skip (hide menu)
    if (localStorage.getItem(TUTORIAL_SKIP_KEY) === 'true') {
        const skipNotice = document.createElement('div');
        skipNotice.className = 'tutorial-skip-notice';
        skipNotice.innerHTML = '<p>Has omitido el tutorial previamente. Puedes reiniciarlo desde esta página.</p><button class="btn-neon-sm" id="restart-tutorial">Reiniciar Tutorial</button>';
        tutorialMenu.prepend(skipNotice);
        document.getElementById('restart-tutorial').addEventListener('click', () => {
            localStorage.removeItem(TUTORIAL_SKIP_KEY);
            location.reload();
        });
    }

    // Skip button
    if (skipBtn) skipBtn.addEventListener('click', () => {
        localStorage.setItem(TUTORIAL_SKIP_KEY, 'true');
        // redirect to home
        window.location.href = '/';
    });

    // Reset tutorial button (in completed view)
    if (resetTutorialBtn) resetTutorialBtn.addEventListener('click', () => {
        localStorage.removeItem(TUTORIAL_STATE_KEY);
        localStorage.removeItem(TUTORIAL_SKIP_KEY);
        alert('El tutorial ha sido reiniciado.');
        location.reload();
    });

    // Start full tutorial
    if (startFullBtn) startFullBtn.addEventListener('click', () => {
        startModuleTutorial('full');
    });

    // Module start buttons
    tutorialStarts.forEach(btn => {
        btn.addEventListener('click', (e) => {
            const module = btn.closest('.tutorial-card').dataset.module;
            startModuleTutorial(module);
        });
    });

    // Start tutorial for a module (or full)
    function startModuleTutorial(module) {
        tutorialMenu.style.display = 'none';
        tutorialSteps.style.display = 'block';

        // Build steps
        let steps = [];
        if (module === 'full') {
            // concatenate all modules in order
            for (const key of Object.keys(MODULE_STEPS)) {
                const modSteps = MODULE_STEPS[key].map(s => ({ module: key, ...s }));
                steps = steps.concat(modSteps);
            }
        } else {
            steps = MODULE_STEPS[module].map(s => ({ module, ...s }));
        }

        let state = { module: module, steps, index: 0 };
        const saved = loadState();
        if (saved && saved.module === module) state = saved; // resume
        saveState(state);

        renderStep(state);

        // Attach navigation handlers
        nextBtn.onclick = () => {
            state.index = Math.min(state.steps.length - 1, state.index + 1);
            saveState(state);
            renderStep(state);
        };
        prevBtn.onclick = () => {
            state.index = Math.max(0, state.index - 1);
            saveState(state);
            renderStep(state);
        };
        closeBtn.onclick = () => {
            endTutorial();
        };
        backBtn.onclick = () => {
            // go back to menu
            tutorialSteps.style.display = 'none';
            tutorialMenu.style.display = 'block';
            localStorage.removeItem(TUTORIAL_STATE_KEY);
        };
    }

    function renderStep(state) {
        const step = state.steps[state.index];
        stepTitle.innerHTML = `Paso ${state.index + 1} / ${state.steps.length}: ${step.title}`;
        stepContent.innerHTML = step.content + `<div style="margin-top:12px;color:var(--muted)"><small>Módulo: ${step.module}</small></div>`;

        prevBtn.style.display = state.index === 0 ? 'none' : 'inline-block';
        nextBtn.textContent = state.index === state.steps.length - 1 ? 'Finalizar' : 'Siguiente';

        if (state.index === state.steps.length - 1) {
            nextBtn.onclick = () => { finishTutorial(); };
        }
    }

    function finishTutorial() {
        localStorage.setItem(TUTORIAL_SKIP_KEY, 'true');
        localStorage.removeItem(TUTORIAL_STATE_KEY);
        alert('¡Has completado el tutorial! Se omitirá automáticamente la próxima vez.');
        window.location.href = '/';
    }

    function endTutorial() {
        if (confirm('¿Deseas salir del tutorial? Tu progreso se guardará para continuar luego.')) {
            const state = loadState();
            // state already saved periodically
            tutorialSteps.style.display = 'none';
            tutorialMenu.style.display = 'block';
        }
    }

    // If there's a saved state show a resume option
    const saved = loadState();
    if (saved && saved.steps && saved.steps.length > 0) {
        const resumeNotice = document.createElement('div');
        resumeNotice.className = 'tutorial-resume-notice';
        resumeNotice.innerHTML = `<p>Hay un tutorial en curso. <button class="btn-neon-sm" id="resume-tutorial">Continuar</button> o <button class="btn-neon-outline" id="discard-tutorial">Descartar</button></p>`;
        tutorialMenu.prepend(resumeNotice);
        document.getElementById('resume-tutorial').addEventListener('click', () => {
            startModuleTutorial(saved.module);
            // restore index from saved
            const state = loadState();
            renderStep(state);
        });
        document.getElementById('discard-tutorial').addEventListener('click', () => {
            localStorage.removeItem(TUTORIAL_STATE_KEY);
            resumeNotice.remove();
        });
    }

});
