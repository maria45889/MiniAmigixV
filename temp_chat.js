document.addEventListener('DOMContentLoaded', () => {
    const chatMessages = document.getElementById('chat-messages');
    const chatHistory = document.getElementById('chat-history');
    const chatWindow = document.getElementById('chat-window');
    const chatForm = document.getElementById('chat-form');
    const messageInput = document.getElementById('message-input');
    const emojiBtn = document.getElementById('emoji-btn');
    const emojiPicker = document.getElementById('emoji-picker');
    const newChatBtn = document.getElementById('new-chat-btn');
    const clearChatBtn = document.getElementById('clear-chat-btn');
    const voiceInputBtn = document.getElementById('voice-input-btn');
    const conversationCount = document.getElementById('conversation-count');
    const chatStats = document.getElementById('chat-stats');
    const helpSearchInput = document.getElementById('help-search-input');
    const helpButtonsContainer = document.getElementById('help-buttons');
    const helpFaqList = document.getElementById('help-faq-list');

    if (!chatMessages || !chatForm || !messageInput) return;

    const storageKey = 'miniamigixv_chat_state';
    const emojis = ['ð','ð','ð','ð','ð','ð','ð','ð','ð¤','ð¥¹','ð­','ð¤','ð´','ð¤¯','ð¥³','ð','ð','ð','ð','ð','ðª','â¨','ð¥','ð','ð¡','ð¯','ð','ðµ','âï¸','ð§ï¸','ð®','ð§','â','â','â ï¸','â­','ð','ð','ð','ð«¶'];
    const welcomeText = 'Hola, soy tu asistente de MiniAmigixV. Puedes escribirme con emojis, copiar mis respuestas o escucharlas con voz.';

    let state = loadState();
    let currentChatId = state.currentChatId;

    renderEmojiPicker();
    renderHistory();
    renderMessages();

    chatForm.addEventListener('submit', (event) => {
        event.preventDefault();
        sendMessage();
    });

    messageInput.addEventListener('input', () => {
        messageInput.style.height = 'auto';
        messageInput.style.height = `${Math.min(messageInput.scrollHeight, 132)}px`;
    });

    messageInput.addEventListener('keydown', (event) => {
        if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault();
            sendMessage();
        }
    });

    emojiBtn.addEventListener('click', () => {
        emojiPicker.classList.toggle('open');
    });

    document.addEventListener('click', (event) => {
        if (!emojiPicker.contains(event.target) && !emojiBtn.contains(event.target)) {
            emojiPicker.classList.remove('open');
        }
    });

    newChatBtn.addEventListener('click', createNewChat);
    clearChatBtn.addEventListener('click', createNewChat);

    voiceInputBtn.addEventListener('click', startVoiceInput);

    chatMessages.addEventListener('click', async (event) => {
        const copyButton = event.target.closest('[data-action="copy"]');
        const speakButton = event.target.closest('[data-action="speak"]');

        if (copyButton) {
            const text = copyButton.closest('.message').querySelector('.bubble p').textContent;
            await copyText(text);
            copyButton.querySelector('.material-icons-round').textContent = 'done';
            setTimeout(() => {
                copyButton.querySelector('.material-icons-round').textContent = 'content_copy';
            }, 1200);
        }

        if (speakButton) {
            const text = speakButton.closest('.message').querySelector('.bubble p').textContent;
            speakText(text, speakButton);
        }
    });

    function loadState() {
        try {
            const saved = JSON.parse(localStorage.getItem(storageKey));
            if (saved && saved.chats && saved.currentChatId) return saved;
        } catch (error) {
            console.warn('No se pudo cargar el historial del chat', error);
        }

        const firstChat = {
            id: createId(),
            title: 'ConversaciÃ³n nueva',
            createdAt: Date.now(),
            messages: [
                { role: 'ai', text: welcomeText, createdAt: Date.now() }
            ]
        };

        return {
            currentChatId: firstChat.id,
            chats: [firstChat]
        };
    }

    const helpTopics = [
        {
            title: 'Inicio / Dashboard',
            keywords: ['inicio', 'dashboard', 'home', 'panel'],
            prompt: 'ExplÃ­came cÃ³mo usar el panel de inicio y las opciones principales de MiniAmigixV.',
            response: 'En el panel de Inicio puedes ver tus accesos directos, el reloj, el clima y las secciones principales. Usa la barra lateral para navegar entre mÃ³dulos como Clima, Eventos, MÃºsica y Configuraciones.'
        },
        {
            title: 'Configuraciones',
            keywords: ['configuraciÃ³n', 'configuraciones', 'ajustes', 'preferencias'],
            prompt: 'Dame una guÃ­a paso a paso para ajustar mi perfil y las configuraciones de la aplicaciÃ³n.',
            response: 'En Configuraciones puedes cambiar la apariencia, administrar notificaciones, privacidad y acceso. Guarda siempre tus cambios y usa el botÃ³n de restablecer si quieres volver a los valores predeterminados.'
        },
        {
            title: 'Perfil',
            keywords: ['perfil', 'foto', 'usuario', 'nombre', 'avatar'],
            prompt: 'Â¿CÃ³mo actualizo mi foto de perfil y mi nombre en MiniAmigixV?',
            response: 'En Perfil puedes subir tu foto, cambiar tu nombre y establecer un nombre personalizado para el asistente IA. AsegÃºrate de guardar los cambios para que se reflejen en toda la aplicaciÃ³n.'
        },
        {
            title: 'Clima',
            keywords: ['clima', 'tiempo', 'pronÃ³stico', 'weather'],
            prompt: 'ExplÃ­came cÃ³mo utilizar la secciÃ³n de Clima para ver el pronÃ³stico y gestionar ciudades.',
            response: 'En Clima puedes buscar tu ciudad, ver informaciÃ³n meteorolÃ³gica y crear alertas. Usa el campo de bÃºsqueda para encontrar ciudades y consulta los detalles de temperatura, humedad y viento.'
        },
        {
            title: 'Eventos',
            keywords: ['evento', 'eventos', 'agenda', 'recordatorio'],
            prompt: 'Â¿CÃ³mo creo un evento y quÃ© debo incluir para que sea Ãºtil?',
            response: 'Para crear eventos, ingresa un tÃ­tulo, fecha, hora y una breve nota. Puedes organizar tus actividades con etiquetas como trabajo, familia o personal y revisar tu historial de eventos en el mÃ³dulo de Eventos.'
        },
        {
            title: 'Estudios',
            keywords: ['estudios', 'tiempo', 'pomodoro', 'temporizador'],
            prompt: 'Â¿CÃ³mo uso el temporizador de estudios y cuÃ¡les son las mejores prÃ¡cticas?',
            response: 'En Estudios puedes iniciar un temporizador de estudio, pausar o reiniciar. Usa intervalos de trabajo y descanso para mejorar tu concentraciÃ³n, y guarda tus sesiones para ver tu progreso.'
        },
        {
            title: 'Traductor',
            keywords: ['traductor', 'traducciÃ³n', 'idioma', 'translate'],
            prompt: 'ExplÃ­came cÃ³mo traducir textos y usar las funciones de copiar y limpiar en Traductor.',
            response: 'Ingresa tu texto, selecciona los idiomas origen y destino y presiona traducir. Puedes copiar el resultado con el icono y limpiar el Ã¡rea de entrada con el botÃ³n correspondiente.'
        },
        {
            title: 'Soporte',
            keywords: ['soporte', 'ticket', 'ayuda', 'consulta'],
            prompt: 'Â¿CÃ³mo envÃ­o una consulta de soporte o un ticket tÃ©cnico?',
            response: 'En Soporte puedes enviar tickets con tÃ­tulo, descripciÃ³n, tipo y prioridad. Describe el problema con detalle para recibir una respuesta mÃ¡s rÃ¡pida y clara del equipo de ayuda.'
        }
    ];

    const faqItems = [
        {
            question: 'Â¿CÃ³mo puedo copiar una respuesta de la IA?',
            answer: 'Presiona el botÃ³n de copiar que aparece junto a cada respuesta de la IA en la conversaciÃ³n.'
        },
        {
            question: 'Â¿Puedo escuchar las respuestas de la IA?',
            answer: 'SÃ­, utiliza el botÃ³n de volumen junto a cada respuesta de la IA para que el navegador la lea en voz alta.'
        },
        {
            question: 'Â¿CÃ³mo creo un nuevo chat?',
            answer: 'Pulsa el botÃ³n "Nuevo chat" para iniciar una conversaciÃ³n fresca y mantener tu historial organizado.'
        },
        {
            question: 'Â¿CÃ³mo restablezco mis configuraciones?',
            answer: 'Ve a Configuraciones y usa el botÃ³n "Restablecer configuraciones" para volver a los valores predeterminados.'
        },
        {
            question: 'Â¿CÃ³mo actualizo mi perfil?',
            answer: 'Ve a la secciÃ³n Perfil para cambiar tu foto, alias y nombre del asistente IA.'
        }
    ];

    function renderHelpPanel() {
        if (!helpButtonsContainer || !helpFaqList) return;

        helpButtonsContainer.innerHTML = '';
        helpTopics.forEach(topic => {
            const button = document.createElement('button');
            button.type = 'button';
            button.className = 'help-button';
            button.innerHTML = `
                <span>${topic.title}</span>
            `;
            button.addEventListener('click', () => askHelpTopic(topic));
            helpButtonsContainer.appendChild(button);
        });

        helpFaqList.innerHTML = '';
        faqItems.forEach(item => {
            const li = document.createElement('li');
            li.className = 'help-faq-item';
            li.innerHTML = `
                <strong>${item.question}</strong>
                <p>${item.answer}</p>
            `;
            helpFaqList.appendChild(li);
        });

        if (helpSearchInput) {
            helpSearchInput.addEventListener('input', filterHelpTopics);
        }
    }

    function filterHelpTopics() {
        if (!helpSearchInput || !helpButtonsContainer) return;

        const query = helpSearchInput.value.trim().toLowerCase();
        helpButtonsContainer.innerHTML = '';

        const filtered = helpTopics.filter(topic => {
            return topic.title.toLowerCase().includes(query) || topic.keywords.some(keyword => keyword.includes(query));
        });

        const list = filtered.length ? filtered : helpTopics;
        list.forEach(topic => {
            const button = document.createElement('button');
            button.type = 'button';
            button.className = 'help-button';
            button.innerHTML = `<span>${topic.title}</span>`;
            button.addEventListener('click', () => askHelpTopic(topic));
            helpButtonsContainer.appendChild(button);
        });
    }

    function askHelpTopic(topic) {
        messageInput.value = topic.prompt;
        messageInput.focus();
        sendMessage();
    }

    function saveState() {
        localStorage.setItem(storageKey, JSON.stringify(state));
    }

    function currentChat() {
        return state.chats.find(chat => chat.id === currentChatId) || state.chats[0];
    }

    function createNewChat() {
        const chat = {
            id: createId(),
            title: 'ConversaciÃ³n nueva',
            createdAt: Date.now(),
            messages: [
                { role: 'ai', text: welcomeText, createdAt: Date.now() }
            ]
        };

        // Ahora que `helpTopics` y `faqItems` estÃ¡n definidos, renderizamos el panel de ayuda
        renderHelpPanel();

        state.chats.unshift(chat);
        currentChatId = chat.id;
        state.currentChatId = chat.id;
        saveState();
        renderHistory();
        renderMessages();
        messageInput.focus();
    }

    function sendMessage() {
        const text = messageInput.value.trim();
        if (!text) return;

        const chat = currentChat();
        chat.messages.push({ role: 'user', text, createdAt: Date.now() });
        chat.title = makeTitle(text);
        messageInput.value = '';
        messageInput.style.height = 'auto';
        emojiPicker.classList.remove('open');

        saveState();
        renderHistory();
        renderMessages();
        showTyping();

        setTimeout(() => {
            removeTyping();
            chat.messages.push({ role: 'ai', text: buildAiReply(text), createdAt: Date.now() });
            saveState();
            renderHistory();
            renderMessages();
        }, 600);
    }

    function renderHistory() {
        chatHistory.innerHTML = '';
        if (conversationCount) {
            conversationCount.textContent = `${state.chats.length} conversaciÃ³n${state.chats.length === 1 ? '' : 'es'}`;
        }

        state.chats.forEach(chat => {
            const lastMessage = chat.messages[chat.messages.length - 1];
            const item = document.createElement('button');
            item.type = 'button';
            item.className = `chat-item ${chat.id === currentChatId ? 'active' : ''}`;
            item.innerHTML = `
                <span class="chat-item-icon"><span class="material-icons-round">forum</span></span>
                <span class="chat-item-info">
                    <span class="chat-item-title">${escapeHtml(chat.title)}</span>
                    <span class="chat-item-preview">${escapeHtml(truncateText(lastMessage?.text || 'Sin mensajes', 46))}</span>
                </span>
            `;
            item.addEventListener('click', () => {
                currentChatId = chat.id;
                state.currentChatId = chat.id;
                saveState();
                renderHistory();
                renderMessages();
            });
            chatHistory.appendChild(item);
        });
    }

    function renderMessages() {
        const chat = currentChat();
        chatMessages.innerHTML = '';

        chat.messages.forEach(message => {
            chatMessages.appendChild(createMessageElement(message));
        });

        if (chatStats) {
            chatStats.textContent = `${escapeHtml(chat.title)} Â· ${chat.messages.length} mensaje${chat.messages.length === 1 ? '' : 's'}`;
        }

        scrollToBottom();
    }

    function createMessageElement(message) {
        const isUser = message.role === 'user';
        const wrapper = document.createElement('article');
        wrapper.className = `message ${isUser ? 'user' : 'ai'}`;
        wrapper.innerHTML = `
            <div class="avatar">
                <span class="material-icons-round">${isUser ? 'person' : 'psychology'}</span>
            </div>
            <div class="bubble">
                <p>${escapeHtml(message.text)}</p>
                <div class="message-meta">
                    <span>${formatTime(message.createdAt)}</span>
                    ${isUser ? '' : `
                    <span class="message-actions">
                        <button type="button" class="message-action" data-action="copy" title="Copiar respuesta" aria-label="Copiar respuesta">
                            <span class="material-icons-round">content_copy</span>
                        </button>
                        <button type="button" class="message-action" data-action="speak" title="Escuchar respuesta" aria-label="Escuchar respuesta">
                            <span class="material-icons-round">volume_up</span>
                        </button>
                    </span>`}
                </div>
            </div>
        `;
        return wrapper;
    }

    function showTyping() {
        const typing = document.createElement('article');
        typing.className = 'message ai';
        typing.dataset.typing = 'true';
        typing.innerHTML = `
            <div class="avatar"><span class="material-icons-round">psychology</span></div>
            <div class="bubble">
                <div class="typing" aria-label="La IA estÃ¡ escribiendo"><span></span><span></span><span></span></div>
            </div>
        `;
        chatMessages.appendChild(typing);
        scrollToBottom();
    }

    function removeTyping() {
        const typing = chatMessages.querySelector('[data-typing="true"]');
        if (typing) typing.remove();
    }

    function renderEmojiPicker() {
        emojiPicker.innerHTML = '';
        emojis.forEach(emoji => {
            const button = document.createElement('button');
            button.type = 'button';
            button.className = 'emoji-choice';
            button.textContent = emoji;
            button.addEventListener('click', () => insertAtCursor(emoji));
            emojiPicker.appendChild(button);
        });
    }

    function insertAtCursor(text) {
        const start = messageInput.selectionStart;
        const end = messageInput.selectionEnd;
        messageInput.value = `${messageInput.value.slice(0, start)}${text}${messageInput.value.slice(end)}`;
        messageInput.focus();
        messageInput.selectionStart = messageInput.selectionEnd = start + text.length;
        messageInput.dispatchEvent(new Event('input'));
    }

    function buildAiReply(text) {
        const lower = text.toLowerCase();

        if (lower.includes('hola') || lower.includes('buenas')) {
            return 'Â¡Hola! Estoy aquÃ­ para ayudarte. Puedes preguntarme sobre cualquier mÃ³dulo de MiniAmigixV o pedirme ideas para organizar tu dÃ­a.';
        }

        if (lower.includes('mÃºsica') || lower.includes('musica')) {
            return 'En MÃºsica puedes organizar canciones y reproducir enlaces. TambiÃ©n puedes guardar nombres con emojis para hacer tu biblioteca mÃ¡s personal.';
        }

        if (lower.includes('clima')) {
            return 'En Clima puedes revisar el estado del tiempo y usar esa informaciÃ³n para planificar eventos o actividades.';
        }

        if (lower.includes('evento')) {
            return 'Para eventos, lo mejor es escribir tÃ­tulo, fecha, hora y una nota breve. AsÃ­ tus recordatorios quedan claros.';
        }

        if (lower.includes('copiar')) {
            return 'Puedes copiar mis respuestas con el botÃ³n de portapapeles que aparece debajo de cada mensaje de IA.';
        }

        if (lower.includes('voz') || lower.includes('audio') || lower.includes('escuchar')) {
            return 'Para escuchar una respuesta, presiona el botÃ³n de volumen debajo del mensaje. El navegador leerÃ¡ el texto en voz alta.';
        }

        for (const topic of helpTopics) {
            if (topic.keywords.some(keyword => lower.includes(keyword))) {
                return topic.response;
            }
        }

        if (lower.includes('ayuda') || lower.includes('soporte') || lower.includes('pregunta')) {
            return 'Puedo ayudarte con cualquier secciÃ³n de MiniAmigixV. Dime si necesitas orientaciÃ³n sobre Perfil, Configuraciones, Clima, Eventos, Estudios, Traductor o Soporte.';
        }

        if (lower.includes('cÃ³mo') || lower.includes('como') || lower.includes('quÃ© hago') || lower.includes('quÃ© puedo')) {
            return 'Puedes pedirme una explicaciÃ³n paso a paso de cualquier mÃ³dulo. Por ejemplo: "Â¿CÃ³mo uso el traductor?" o "ExplÃ­came el panel de Configuraciones".';
        }

        return `Entiendo: "${text}". Puedo ayudarte a convertir eso en una acciÃ³n concreta dentro de MiniAmigixV, explicarlo paso a paso o darte una respuesta mÃ¡s corta si prefieres.`;
    }

    async function copyText(text) {
        if (navigator.clipboard) {
            await navigator.clipboard.writeText(text);
            return;
        }

        const textarea = document.createElement('textarea');
        textarea.value = text;
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand('copy');
        textarea.remove();
    }

    function speakText(text, button) {
        if (!('speechSynthesis' in window)) {
            alert('Tu navegador no tiene reproducciÃ³n por voz disponible.');
            return;
        }

        window.speechSynthesis.cancel();
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = 'es-ES';
        utterance.rate = 1;
        button.querySelector('.material-icons-round').textContent = 'stop';
        utterance.onend = () => {
            button.querySelector('.material-icons-round').textContent = 'volume_up';
        };
        window.speechSynthesis.speak(utterance);
    }

    function startVoiceInput() {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        if (!SpeechRecognition) {
            alert('El dictado por voz no estÃ¡ disponible en este navegador.');
            return;
        }

        const recognition = new SpeechRecognition();
        recognition.lang = 'es-ES';
        recognition.interimResults = false;
        recognition.maxAlternatives = 1;
        voiceInputBtn.classList.add('active');
        recognition.start();
        recognition.onresult = (event) => {
            insertAtCursor(event.results[0][0].transcript);
        };
        recognition.onend = () => {
            voiceInputBtn.classList.remove('active');
        };
    }

    function makeTitle(text) {
        const cleaned = text.trim();
        return cleaned.length > 34 ? `${cleaned.slice(0, 34)}...` : cleaned || 'ConversaciÃ³n nueva';
    }

    function truncateText(text, maxLength) {
        if (!text) return '';
        return text.length > maxLength ? `${text.slice(0, maxLength - 1)}â¦` : text;
    }

    function createId() {
        return `chat-${Date.now()}-${Math.random().toString(16).slice(2)}`;
    }

    function formatTime(timestamp) {
        return new Intl.DateTimeFormat('es', { hour: '2-digit', minute: '2-digit' }).format(new Date(timestamp));
    }

    function scrollToBottom() {
        requestAnimationFrame(() => {
            chatWindow.scrollTop = chatWindow.scrollHeight;
        });
    }

    function escapeHtml(value) {
        return String(value)
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#039;');
    }
});

