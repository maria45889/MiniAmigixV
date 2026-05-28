// Sugerencias Module JavaScript
document.addEventListener('DOMContentLoaded', () => {
    console.log("💡 MiniAmigixV Sugerencias: Online");
    
    // DOM Elements
    const sugerenciaForm = document.getElementById('send-sugerencia-form');
    const sugerenciasList = document.getElementById('sugerencias-list');
    const notificationContainer = document.getElementById('notification-container');
    
    // Initialize
    setupEventListeners();
    loadSugerencias();
    
    // Functions
    function setupEventListeners() {
        // Form submission
        if (sugerenciaForm) {
            sugerenciaForm.addEventListener('submit', enviarSugerencia);
        }
    }
    
    function loadSugerencias() {
        // In a real app, this would fetch from the server
        // For demo, we'll simulate with some sample data
        const sampleSugerencias = [
            {
                id: 1,
                titulo: 'Modo oscuro mejorado',
                descripcion: 'Sería genial tener más opciones de personalización para el modo oscuro, como diferentes tonos de azul y púrpura.',
                tipo: 'mejora',
                creado_en: '2026-05-20',
                estado: 'pendiente'
            },
            {
                id: 2,
                titulo: 'Problema con el traductor',
                descripcion: 'El traductor no funciona bien con textos muy largos, se corta a la mitad.',
                tipo: 'reporte',
                creado_en: '2026-05-18',
                estado: 'en_revision'
            },
            {
                id: 3,
                titulo: '¡Me encanta la app!',
                descripcion: 'Quería decir que esta aplicación me ha ayudado mucho a organizar mi tiempo y reducir el estrés. ¡Gracias por crear algo tan útil!',
                tipo: 'elogio',
                creado_en: '2026-05-15',
                estado: 'respuesta',
                respuesta: '¡Gracias por tus amables palabras! Nos alegra mucho saber que MiniAmigixV está teniendo un impacto positivo en tu vida.'
            }
        ];
        
        renderSugerencias(sampleSugerencias);
    }
    
    function enviarSugerencia(e) {
        e.preventDefault();
        
        const titulo = document.getElementById('sugerencia-titulo').value.trim();
        const descripcion = document.getElementById('sugerencia-descripcion').value.trim();
        const tipo = document.getElementById('sugerencia-tipo').value;
        
        if (!titulo || !descripcion) {
            showNotification('Por favor completa todos los campos', 'warning');
            return;
        }
        
        // Show loading state
        const submitBtn = sugerenciaForm.querySelector('button[type="submit"]');
        const originalText = submitBtn.textContent;
        submitBtn.textContent = 'Enviando...';
        submitBtn.disabled = true;
        
        // Simulate API call
        setTimeout(() => {
            // In a real app, this would send to /sugerencias/crear/
            const nuevaSugerencia = {
                id: Date.now(), // Temporary ID
                titulo: titulo,
                descripcion: descripcion,
                tipo: tipo,
                creado_en: new Date().toISOString().split('T')[0],
                estado: 'pendiente'
            };
            
            // Add to list (in real app, would come from server response)
            renderSugerencias([nuevaSugerencia, ...getExistingSugerencias()]);
            
            // Reset form
            sugerenciaForm.reset();
            
            // Reset button
            submitBtn.textContent = originalText;
            submitBtn.disabled = false;
            
            showNotification('¡Tu sugerencia ha sido enviada correctamente! Nuestro equipo la revisará pronto.', 'success');
            
            // In a real app, this would trigger an email to admin
            console.log('[Email Simulation] Sending suggestion to admin:', {
                titulo: titulo,
                descripcion: descripcion,
                tipo: tipo,
                timestamp: new Date().toISOString()
            });
        }, 1000);
    }
    
    function getExistingSugerencias() {
        // Get existing suggestions from the DOM
        const sugerencias = [];
        const items = sugerenciasList.querySelectorAll('.sugerencia-item');
        items.forEach(item => {
            const titulo = item.querySelector('h3')?.textContent || '';
            const descripcion = item.querySelector('.sugerencia-content p')?.textContent || '';
            const tipo = item.className.match(/sugerencia-(\w+)/)?.[1] || 'idea';
            const estado = item.className.match(/estado-(\w+)/)?.[1] || 'pendiente';
            const creado_en = item.querySelector('.sugerencia-meta small')?.textContent || '';
            
            sugerencias.push({
                titulo: titulo,
                descripcion: descripcion,
                tipo: tipo,
                estado: estado,
                creado_en: creado_en
            });
        });
        return sugerencias;
    }
    
    function renderSugerencias(sugerencias) {
        if (!sugerenciasList) return;
        
        if (sugerencias.length === 0) {
            sugerenciasList.innerHTML = `
                <div class="empty-state">
                    <span class="material-icons-round">lightbulb_outline</span>
                    <h2>Aún no tienes sugerencias</h2>
                    <p>¡Sé el primero en enviar una sugerencia para ayudar a mejorar MiniAmigixV!</p>
                </div>
            `;
            return;
        }
        
        sugerenciasList.innerHTML = sugerencias.map(sugerencia => {
            const tipoIcon = getSugerenciaIcon(sugerencia.tipo);
            const estadoClass = `estado-${sugerencia.estado}`;
            const estadoText = getEstadoText(sugerencia.estado);
            
            let respuestaHTML = '';
            if (sugerencia.respuesta) {
                respuestaHTML = `
                    <div class="sugerencia-respuesta">
                        <div class="respuesta-header">
                            <span class="material-icons-round">reply</span>
                            <h4>Respuesta del equipo:</h4>
                        </div>
                        <div class="respuesta-content">
                            <p>${sugerencia.respuesta}</p>
                        </div>
                        <div class="respuesta-footer">
                            <small>Respondido el ${sugerencia.respondido_en || 'Recién'} por ${sugerencia.respondido_por || 'Equipo'}</small>
                        </div>
                    </div>
                `;
            }
            
            return `
                <div class="sugerencia-item sugerencia-${sugerencia.tipo} estado-${sugerencia.estado}">
                    <div class="sugerencia-header">
                        <div class="sugerencia-icon">
                            <span class="material-icons-round">${tipoIcon}</span>
                        </div>
                        <div class="sugerencia-content">
                            <h3>${sugerencia.titulo}</h3>
                            <p>${sugerencia.descripcion}</p>
                        </div>
                        <div class="sugerencia-meta">
                            <span class="tipo-tag">${sugerencia.tipo.charAt(0).toUpperCase() + sugerencia.tipo.slice(1)}</span>
                            <span class="estado-tag ${estadoClass}">${estadoText}</span>
                            <small>${sugerencia.creado_en}</small>
                        </div>
                    </div>
                    ${respuestaHTML}
                </div>
            `;
        }).join('');
    }
    
    function getSugerenciaIcon(tipo) {
        const icons = {
            'idea': 'lightbulb',
            'mejora': 'build',
            'reporte': 'bug_report',
            'pregunta': 'question_answer',
            'elogio': 'sentiment_satisfied',
            'otro': 'horizontal_rule'
        };
        return icons[tipo] || 'lightbulb';
    }
    
    function getEstadoText(estado) {
        const estados = {
            'pendiente': 'Pendiente',
            'en_revision': 'En Revisión',
            'respuesta': 'Respondida',
            'resuelta': 'Resuelta'
        };
        return estados[estado] || estado;
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
    
    console.log("💡 Sugerencias module initialized");
});

// Export functions for use in other modules if needed
window.MiniAmigixSugerencias = {
    enviarSugerencia,
    loadSugerencias
};