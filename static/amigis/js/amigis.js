/* ==================== AMIGIS - Mascota Patito Programador ==================== */
/* Versión completa con arrastrar, accesorios y animaciones */

class AmigisMascot {
    constructor() {
        this.container = null;
        this.wrapper = null;
        this.image = null;
        this.bubble = null;
        this.accessoriesLayer = null;
        this.currentSection = 'home';
        this.isDragging = false;
        this.dragOffset = { x: 0, y: 0 };
        this.position = { x: 20, y: 20 };
        this.blinkInterval = null;
        this.randomExpressionInterval = null;
        
        this.greetings = [
            '¡Hola! Soy Amigis, tu patito programador 🦆',
            '¡Qué gusto verte! ¿En qué puedo ayudarte?',
            '¡Hola amigo! Estoy listo para ayudarte',
            '¡Bienvenido! Soy Amigis, tu asistente',
            '¡Hey! ¿Listo para comenzar?'
        ];
        
        this.sectionMessages = {
            'home': '¡Bienvenido a MiniAmigixV! 🏠',
            'chat': '¡Escribiendo código con IA! �',
            'musica': '¡Música para programar! 🎵',
            'juegos': '¡A descansar un poco! 🎮',
            'clima': '¡El clima de hoy! ☀️',
            'traductor': '¡Traduciendo código! 🌐',
            'blog': '¡Leyendo artículos! 📝',
            'soporte': '¡Aquí para ayudarte! 💪',
            'eventos': '¡Organizando tu agenda! 📅',
            'entretenimiento': '¡Tiempo de divertirse! 🎬',
            'estudio': '¡A aprender cosas nuevas! 📚',
            'tutorial': '¡Te enseño paso a paso! 🎓'
        };
        
        this.sectionAccessories = {
            'home': null,
            'chat': 'speech-bubble',
            'musica': 'headphones',
            'juegos': 'gamepad',
            'clima': 'umbrella',
            'traductor': 'speech-bubble',
            'blog': 'sunglasses',
            'soporte': 'headphones',
            'eventos': 'speech-bubble',
            'entretenimiento': 'sunglasses',
            'estudio': 'speech-bubble',
            'tutorial': 'speech-bubble'
        };
        
        this.randomExpressions = [
            '¡Qué buen día! ☀️',
            '¿Necesitas ayuda? 🤔',
            '¡Estoy aquí para ti! 💪',
            '¡Vamos a programar! 💻',
            '¡Tú puedes! 🌟',
            '¡Excelente trabajo! ⭐',
            '¡Sigue así! 🚀',
            '¡Genial! 👏'
        ];
        
        this.init();
    }

    init() {
        // Evitar duplicación de instancias
        if (window.amigisInstance) {
            console.log('Amigis ya está inicializado. Reutilizando instancia existente.');
            return window.amigisInstance;
        }
        
        this.loadPosition();
        this.createMascot();
        this.attachEvents();
        this.detectTheme();
        this.detectCurrentSection();
        this.loadUserName();
        this.startBlinking();
        this.startRandomExpressions();
        this.greetOnLoad();
    }

    createMascot() {
        // Verificar si ya existe un contenedor de Amigis
        const existingContainer = document.querySelector('.amigis-container');
        if (existingContainer) {
            console.log('Amigis container ya existe. Reutilizando.');
            this.container = existingContainer;
            this.wrapper = document.getElementById('amigis-wrapper');
            this.image = document.getElementById('amigis-image');
            this.bubble = document.getElementById('amigis-bubble');
            this.accessoriesLayer = document.getElementById('amigis-accessories');
            return;
        }
        
        // Crear contenedor principal
        this.container = document.createElement('div');
        this.container.className = 'amigis-container';
        this.container.style.left = this.position.x + 'px';
        this.container.style.bottom = this.position.y + 'px';
        this.container.style.right = 'auto';
        
        this.container.innerHTML = `
            <div class="amigis-bubble" id="amigis-bubble"></div>
            <div class="amigis-wrapper" id="amigis-wrapper">
                <img 
                    id="amigis-image" 
                    class="amigis-image" 
                    src="/static/amigis/amigis-light.svg" 
                    alt="Amigis - Mascota Patito Programador"
                />
                <div class="amigis-accessories" id="amigis-accessories">
                    <img class="amigis-accessory" id="acc-headphones" src="/static/amigis/accessories/headphones.svg" alt="Audífonos" />
                    <img class="amigis-accessory" id="acc-gamepad" src="/static/amigis/accessories/gamepad.svg" alt="Control" />
                    <img class="amigis-accessory" id="acc-umbrella" src="/static/amigis/accessories/umbrella.svg" alt="Paraguas" />
                    <img class="amigis-accessory" id="acc-sunglasses" src="/static/amigis/accessories/sunglasses.svg" alt="Gafas" />
                    <img class="amigis-accessory" id="acc-speech-bubble" src="/static/amigis/accessories/speech-bubble.svg" alt="Globo" />
                </div>
            </div>
        `;

        document.body.appendChild(this.container);
        
        // Referencias a elementos
        this.wrapper = document.getElementById('amigis-wrapper');
        this.image = document.getElementById('amigis-image');
        this.bubble = document.getElementById('amigis-bubble');
        this.accessoriesLayer = document.getElementById('amigis-accessories');
    }

    attachEvents() {
        // Eventos de arrastrar
        this.wrapper.addEventListener('mousedown', (e) => this.startDrag(e));
        document.addEventListener('mousemove', (e) => this.drag(e));
        document.addEventListener('mouseup', () => this.stopDrag());
        
        // Eventos táctiles para móviles
        this.wrapper.addEventListener('touchstart', (e) => this.startDrag(e.touches[0]));
        document.addEventListener('touchmove', (e) => this.drag(e.touches[0]));
        document.addEventListener('touchend', () => this.stopDrag());
        
        // Click en la mascota (si no está arrastrando)
        this.wrapper.addEventListener('click', (e) => {
            if (!this.isDragging) {
                this.showRandomMessage();
                this.setHappy();
            }
        });

        // Detectar cambios de tema
        const observer = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                if (mutation.attributeName === 'class') {
                    this.updateTheme();
                }
            });
        });

        observer.observe(document.body, {
            attributes: true,
            attributeFilter: ['class']
        });
        
        // Detectar cambios de sección
        window.addEventListener('popstate', () => this.detectCurrentSection());
        
        // Adaptar al redimensionar ventana
        window.addEventListener('resize', () => this.constrainPosition());
    }

    // ==================== ARRASTRAR ====================

    startDrag(e) {
        this.isDragging = true;
        const rect = this.container.getBoundingClientRect();
        this.dragOffset.x = e.clientX - rect.left;
        this.dragOffset.y = e.clientY - rect.top;
        this.wrapper.style.cursor = 'grabbing';
    }

    drag(e) {
        if (!this.isDragging) return;
        
        const windowWidth = window.innerWidth;
        const windowHeight = window.innerHeight;
        const containerWidth = this.container.offsetWidth;
        const containerHeight = this.container.offsetHeight;
        
        let newX = e.clientX - this.dragOffset.x;
        let newY = windowHeight - e.clientY - this.dragOffset.y;
        
        // Restringir a los bordes de la ventana
        newX = Math.max(0, Math.min(newX, windowWidth - containerWidth));
        newY = Math.max(0, Math.min(newY, windowHeight - containerHeight));
        
        this.container.style.right = 'auto';
        this.container.style.left = newX + 'px';
        this.container.style.bottom = newY + 'px';
        
        this.position.x = newX;
        this.position.y = newY;
    }

    stopDrag() {
        if (this.isDragging) {
            this.isDragging = false;
            this.wrapper.style.cursor = 'grab';
            this.savePosition();
        }
    }

    constrainPosition() {
        const windowWidth = window.innerWidth;
        const windowHeight = window.innerHeight;
        const containerWidth = this.container.offsetWidth;
        const containerHeight = this.container.offsetHeight;
        
        let newX = Math.max(0, Math.min(this.position.x, windowWidth - containerWidth));
        let newY = Math.max(0, Math.min(this.position.y, windowHeight - containerHeight));
        
        this.container.style.left = newX + 'px';
        this.container.style.bottom = newY + 'px';
        
        this.position.x = newX;
        this.position.y = newY;
        this.savePosition();
    }

    loadPosition() {
        const saved = localStorage.getItem('amigis-position');
        if (saved) {
            try {
                const pos = JSON.parse(saved);
                this.position = pos;
                // Aplicar posición inmediatamente después de crear el contenedor
                if (this.container) {
                    this.container.style.left = this.position.x + 'px';
                    this.container.style.bottom = this.position.y + 'px';
                    this.container.style.right = 'auto';
                }
            } catch (e) {
                console.error('Error al cargar posición de Amigis:', e);
                this.position = { x: 20, y: 20 };
            }
        }
    }

    savePosition() {
        localStorage.setItem('amigis-position', JSON.stringify(this.position));
    }

    // ==================== TEMA ====================

    detectTheme() {
        this.updateTheme();
    }

    loadUserName() {
        if (window.amigisConfig && window.amigisConfig.userName) {
            this.userName = window.amigisConfig.userName;
            this.isAuthenticated = window.amigisConfig.isAuthenticated;
            
            // Actualizar saludos con el nombre del usuario
            this.greetings = [
                `¡Hola ${this.userName}! Soy Amigis, tu compañero de MiniAmigixV 🦆`,
                `¡Qué gusto verte, ${this.userName}! ¿En qué puedo ayudarte?`,
                `¡Hola ${this.userName}! Estoy listo para ayudarte`,
                `¡Bienvenido ${this.userName}! Soy Amigis, tu asistente`,
                `¡Hey ${this.userName}! ¿Listo para comenzar?`
            ];
        }
    }

    updateTheme() {
        const isLight = document.body.classList.contains('light');
        const imagePath = isLight ? '/static/amigis/amigis-light.svg' : '/static/amigis/amigis-dark.svg';
        
        if (this.image) {
            this.image.src = imagePath;
        }
    }

    // ==================== SECCIÓN Y ACCESORIOS ====================

    detectCurrentSection() {
        const path = window.location.pathname;
        let section = 'home';
        
        if (path.includes('/chat')) section = 'chat';
        else if (path.includes('/musica')) section = 'musica';
        else if (path.includes('/juegos')) section = 'juegos';
        else if (path.includes('/clima')) section = 'clima';
        else if (path.includes('/traductor')) section = 'traductor';
        else if (path.includes('/blog')) section = 'blog';
        else if (path.includes('/soporte')) section = 'soporte';
        else if (path.includes('/eventos')) section = 'eventos';
        else if (path.includes('/entretenimiento')) section = 'entretenimiento';
        else if (path.includes('/estudio')) section = 'estudio';
        else if (path.includes('/tutorial')) section = 'tutorial';
        
        this.onSectionChange(section);
    }

    onSectionChange(section) {
        if (this.currentSection === section) return;
        
        this.currentSection = section;
        const message = this.sectionMessages[section] || '¡Nueva sección!';
        this.showMessage(message);
        this.setHappy();
        this.updateAccessory(section);
        
        // Animación especial según sección
        if (section === 'home') {
            this.setWave();
        }
    }

    updateAccessory(section) {
        // Ocultar todos los accesorios
        const accessories = this.accessoriesLayer.querySelectorAll('.amigis-accessory');
        accessories.forEach(acc => acc.classList.remove('active'));
        
        // Mostrar accesorio correspondiente
        const accessoryName = this.sectionAccessories[section];
        if (accessoryName) {
            const accessory = document.getElementById('acc-' + accessoryName);
            if (accessory) {
                accessory.classList.add('active');
            }
        }
    }

    // ==================== MENSAJES ====================

    showMessage(message, duration = 4000) {
        if (!this.bubble) return;
        
        this.bubble.textContent = message;
        this.bubble.classList.add('show');
        
        setTimeout(() => {
            this.bubble.classList.remove('show');
        }, duration);
    }

    showRandomMessage() {
        const randomMessage = this.greetings[Math.floor(Math.random() * this.greetings.length)];
        this.showMessage(randomMessage);
    }

    greetOnLoad() {
        setTimeout(() => {
            const randomGreeting = this.greetings[Math.floor(Math.random() * this.greetings.length)];
            this.showMessage(randomGreeting);
            this.setWave();
        }, 1500);
    }

    // ==================== ANIMACIONES ====================

    setHappy() {
        if (this.wrapper) {
            this.wrapper.classList.add('happy');
            setTimeout(() => {
                this.wrapper.classList.remove('happy');
            }, 600);
        }
    }

    setWave() {
        if (this.wrapper) {
            this.wrapper.classList.add('waving');
            setTimeout(() => {
                this.wrapper.classList.remove('waving');
            }, 800);
        }
    }

    setTyping(isTyping) {
        if (this.wrapper) {
            if (isTyping) {
                this.wrapper.classList.add('typing');
                this.showMessage('Escribiendo... 💻');
            } else {
                this.wrapper.classList.remove('typing');
                this.bubble.classList.remove('show');
            }
        }
    }

    setThinking(isThinking) {
        if (this.wrapper) {
            if (isThinking) {
                this.wrapper.classList.add('thinking');
                this.showMessage('Pensando... 🤔');
            } else {
                this.wrapper.classList.remove('thinking');
                this.bubble.classList.remove('show');
            }
        }
    }

    setSmile() {
        if (this.wrapper) {
            this.wrapper.classList.add('smiling');
            setTimeout(() => {
                this.wrapper.classList.remove('smiling');
            }, 500);
        }
    }

    setCelebrate() {
        if (this.wrapper) {
            this.wrapper.classList.add('celebrating');
            setTimeout(() => {
                this.wrapper.classList.remove('celebrating');
            }, 1000);
        }
    }

    setBlink() {
        if (this.wrapper) {
            this.wrapper.classList.add('blinking');
            setTimeout(() => {
                this.wrapper.classList.remove('blinking');
            }, 300);
        }
    }

    // ==================== EXPRESIONES AUTOMÁTICAS ====================

    startBlinking() {
        // Parpadear cada 3-6 segundos
        this.blinkInterval = setInterval(() => {
            this.setBlink();
        }, Math.random() * 3000 + 3000);
    }

    startRandomExpressions() {
        // Mostrar expresiones aleatorias cada 15-30 segundos
        this.randomExpressionInterval = setInterval(() => {
            const randomExpr = this.randomExpressions[Math.floor(Math.random() * this.randomExpressions.length)];
            this.showMessage(randomExpr, 3000);
            this.setSmile();
        }, Math.random() * 15000 + 15000);
    }

    // ==================== REACCIONES A EVENTOS ====================

    onAIWriting() {
        this.setTyping(true);
    }

    onAIFinished() {
        this.setTyping(false);
        this.setCelebrate();
        this.showMessage('¡Listo! 🎉');
    }

    // ==================== MÉTODOS PÚBLICOS ====================

    static getInstance() {
        if (!window.amigisInstance) {
            window.amigisInstance = new AmigisMascot();
        }
        return window.amigisInstance;
    }
}

// Inicializar cuando el DOM esté listo
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        if (!window.amigisInstance) {
            window.amigisInstance = new AmigisMascot();
        }
    });
} else {
    if (!window.amigisInstance) {
        window.amigisInstance = new AmigisMascot();
    }
}

// Exponer instancia globalmente
window.Amigis = AmigisMascot.getInstance();
