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
            this.lastDetectedPath = window.location.pathname;
            
            this.translations = {
                'es': {
                    greetings: [
                        '¡Hola! Soy Amigis, tu patito programador 🦆',
                        '¡Qué gusto verte! ¿En qué puedo ayudarte?',
                        '¡Hola amigo! Estoy listo para ayudarte',
                        '¡Bienvenido! Soy Amigis, tu asistente',
                        '¡Hey! ¿Listo para comenzar?'
                    ],
                    sectionMessages: {
                        'home': '¡Bienvenido a MiniAmigixV! 🏠',
                        'chat': '¡Escribiendo código con IA! 💻',
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
                    },
                    randomExpressions: [
                        '¡Qué buen día! ☀️',
                        '¿Necesitas ayuda? 🤔',
                        '¡Estoy aquí para ti! 💪',
                        '¡Vamos a programar! 💻',
                        '¡Tú puedes! 🌟',
                        '¡Excelente trabajo! ⭐',
                        '¡Sigue así! 🚀',
                        '¡Genial! 👏'
                    ],
                    typing: 'Escribiendo... 💻',
                    thinking: 'Pensando... 🤔',
                    done: '¡Listo! 🎉'
                },
                'en': {
                    greetings: [
                        'Hello! I\'m Amigis, your programmer duck 🦆',
                        'Nice to see you! How can I help you?',
                        'Hi friend! I\'m ready to help you',
                        'Welcome! I\'m Amigis, your assistant',
                        'Hey! Ready to start?'
                    ],
                    sectionMessages: {
                        'home': 'Welcome to MiniAmigixV! 🏠',
                        'chat': 'Writing code with AI! 💻',
                        'musica': 'Music to program! 🎵',
                        'juegos': 'Time to relax! 🎮',
                        'clima': 'Today\'s weather! ☀️',
                        'traductor': 'Translating code! 🌐',
                        'blog': 'Reading articles! 📝',
                        'soporte': 'Here to help! 💪',
                        'eventos': 'Organizing your agenda! 📅',
                        'entretenimiento': 'Time to have fun! 🎬',
                        'estudio': 'Learning new things! 📚',
                        'tutorial': 'I\'ll teach you step by step! 🎓'
                    },
                    randomExpressions: [
                        'What a great day! ☀️',
                        'Need help? 🤔',
                        'I\'m here for you! 💪',
                        'Let\'s code! 💻',
                        'You can do it! 🌟',
                        'Excellent job! ⭐',
                        'Keep it up! 🚀',
                        'Great! 👏'
                    ],
                    typing: 'Typing... 💻',
                    thinking: 'Thinking... 🤔',
                    done: 'Done! 🎉'
                },
                'fr': {
                    greetings: [
                        'Bonjour! Je suis Amigis, votre canard programmeur 🦆',
                        'Ravi de vous voir! Comment puis-je vous aider?',
                        'Salut ami! Je suis prêt à vous aider',
                        'Bienvenue! Je suis Amigis, votre assistant',
                        'Hey! Prêt à commencer?'
                    ],
                    sectionMessages: {
                        'home': 'Bienvenue sur MiniAmigixV! 🏠',
                        'chat': 'Écrire du code avec l\'IA! 💻',
                        'musica': 'Musique pour programmer! 🎵',
                        'juegos': 'Temps de se détendre! 🎮',
                        'clima': 'La météo d\'aujourd\'hui! ☀️',
                        'traductor': 'Traduire du code! 🌐',
                        'blog': 'Lire des articles! 📝',
                        'soporte': 'Ici pour aider! 💪',
                        'eventos': 'Organiser votre agenda! 📅',
                        'entretenimiento': 'Temps de s\'amuser! 🎬',
                        'estudio': 'Apprendre de nouvelles choses! 📚',
                        'tutorial': 'Je vous enseigne étape par étape! 🎓'
                    },
                    randomExpressions: [
                        'Quelle belle journée! ☀️',
                        'Besoin d\'aide? 🤔',
                        'Je suis là pour vous! 💪',
                        'Programmons! 💻',
                        'Vous pouvez le faire! 🌟',
                        'Excellent travail! ⭐',
                        'Continuez comme ça! 🚀',
                        'Génial! 👏'
                    ],
                    typing: 'En train d\'écrire... 💻',
                    thinking: 'En train de réfléchir... 🤔',
                    done: 'Terminé! 🎉'
                },
                'de': {
                    greetings: [
                        'Hallo! Ich bin Amigis, dein Programmier-Ente 🦆',
                        'Schön dich zu sehen! Wie kann ich dir helfen?',
                        'Hallo Freund! Ich bin bereit zu helfen',
                        'Willkommen! Ich bin Amigis, dein Assistent',
                        'Hey! Bereit anzufangen?'
                    ],
                    sectionMessages: {
                        'home': 'Willkommen bei MiniAmigixV! 🏠',
                        'chat': 'Code mit KI schreiben! 💻',
                        'musica': 'Musik zum Programmieren! 🎵',
                        'juegos': 'Zeit zum Entspannen! 🎮',
                        'clima': 'Das Wetter heute! ☀️',
                        'traductor': 'Code übersetzen! 🌐',
                        'blog': 'Artikel lesen! 📝',
                        'soporte': 'Hier um zu helfen! 💪',
                        'eventos': 'Termine organisieren! 📅',
                        'entretenimiento': 'Zeit zum Spaß haben! 🎬',
                        'estudio': 'Neues lernen! 📚',
                        'tutorial': 'Ich unterrichte dich Schritt für Schritt! 🎓'
                    },
                    randomExpressions: [
                        'Was für ein schöner Tag! ☀️',
                        'Brauchst du Hilfe? 🤔',
                        'Ich bin für dich da! 💪',
                        'Lass uns programmieren! 💻',
                        'Du kannst es! 🌟',
                        'Ausgezeichnete Arbeit! ⭐',
                        'Mach weiter so! 🚀',
                        'Toll! 👏'
                    ],
                    typing: 'Schreibe... 💻',
                    thinking: 'Denke nach... 🤔',
                    done: 'Fertig! 🎉'
                },
                'pt': {
                    greetings: [
                        'Olá! Sou Amigis, seu pato programador 🦆',
                        'Que bom te ver! Como posso te ajudar?',
                        'Olá amigo! Estou pronto para te ajudar',
                        'Bem-vindo! Sou Amigis, seu assistente',
                        'Ei! Pronto para começar?'
                    ],
                    sectionMessages: {
                        'home': 'Bem-vindo ao MiniAmigixV! 🏠',
                        'chat': 'Escrevendo código com IA! 💻',
                        'musica': 'Música para programar! 🎵',
                        'juegos': 'Hora de relax! 🎮',
                        'clima': 'O clima de hoje! ☀️',
                        'traductor': 'Traduzindo código! 🌐',
                        'blog': 'Lendo artigos! 📝',
                        'soporte': 'Aqui para ajudar! 💪',
                        'eventos': 'Organizando sua agenda! 📅',
                        'entretenimiento': 'Hora de se divertir! 🎬',
                        'estudio': 'Aprender coisas novas! 📚',
                        'tutorial': 'Te ensino passo a passo! 🎓'
                    },
                    randomExpressions: [
                        'Que bom dia! ☀️',
                        'Precisa de ajuda? 🤔',
                        'Estou aqui para você! 💪',
                        'Vamos programar! 💻',
                        'Você consegue! 🌟',
                        'Excelente trabalho! ⭐',
                        'Continue assim! 🚀',
                        'Genial! 👏'
                    ],
                    typing: 'Escrevendo... 💻',
                    thinking: 'Pensando... 🤔',
                    done: 'Pronto! 🎉'
                },
                'it': {
                    greetings: [
                        'Ciao! Sono Amigis, la tua papera programmatrice 🦆',
                        'Piacere di vederti! Come posso aiutarti?',
                        'Ciao amico! Sono pronto ad aiutarti',
                        'Benvenuto! Sono Amigis, il tuo assistente',
                        'Ehi! Pronto a iniziare?'
                    ],
                    sectionMessages: {
                        'home': 'Benvenuto su MiniAmigixV! 🏠',
                        'chat': 'Scrivendo codice con IA! 💻',
                        'musica': 'Musica per programmare! 🎵',
                        'juegos': 'Tempo di relax! 🎮',
                        'clima': 'Il meteo di oggi! ☀️',
                        'traductor': 'Traducendo codice! 🌐',
                        'blog': 'Leggendo articoli! 📝',
                        'soporte': 'Qui per aiutare! 💪',
                        'eventos': 'Organizzando la tua agenda! 📅',
                        'entretenimiento': 'Tempo di divertirsi! 🎬',
                        'estudio': 'Imparare cose nuove! 📚',
                        'tutorial': 'Ti insegno passo passo! 🎓'
                    },
                    randomExpressions: [
                        'Che bella giornata! ☀️',
                        'Hai bisogno di aiuto? 🤔',
                        'Sono qui per te! 💪',
                        'Programmiamo! 💻',
                        'Puoi farlo! 🌟',
                        'Ottimo lavoro! ⭐',
                        'Continua così! 🚀',
                        'Geniale! 👏'
                    ],
                    typing: 'Scrivendo... 💻',
                    thinking: 'Pensando... 🤔',
                    done: 'Fatto! 🎉'
                },
                'ja': {
                    greetings: [
                        'こんにちは！アミギス、プログラマーアヒルです🦆',
                        'お会いできて嬉しいです！何かお手伝いしましょうか？',
                        'こんにちは友達！お手伝いする準備ができました',
                        'ようこそ！アミギス、あなたのアシスタントです',
                        'へい！始める準備はできましたか？'
                    ],
                    sectionMessages: {
                        'home': 'MiniAmigixVへようこそ！🏠',
                        'chat': 'AIでコードを書いています！💻',
                        'musica': 'プログラミング音楽！🎵',
                        'juegos': 'リラックスする時間！🎮',
                        'clima': '今日の天気！☀️',
                        'traductor': 'コードを翻訳中！🌐',
                        'blog': '記事を読んでいます！📝',
                        'soporte': 'お手伝いするためにここにいます！💪',
                        'eventos': '予定を整理しています！📅',
                        'entretenimiento': '楽しむ時間！🎬',
                        'estudio': '新しいことを学ぶ！📚',
                        'tutorial': '段階的に教えます！🎓'
                    },
                    randomExpressions: [
                        '素晴らしい日ですね！☀️',
                        '助けが必要ですか？🤔',
                        'あなたのためにここにいます！💪',
                        'プログラミングしましょう！💻',
                        'あなたならできます！🌟',
                        '素晴らしい仕事！⭐',
                        'その調子で！🚀',
                        '素晴らしい！👏'
                    ],
                    typing: '入力中...💻',
                    thinking: '考え中...🤔',
                    done: '完了！🎉'
                },
                'ko': {
                    greetings: [
                        '안녕하세요! 아미기스, 프로그래머 오리입니다🦆',
                        '만나서 반가워요! 어떻게 도와드릴까요?',
                        '안녕 친구! 도와드릴 준비가 되었어요',
                        '환영합니다! 아미기스, 당신의 어시스턴트입니다',
                        '이이! 시작할 준비가 되셨나요?'
                    ],
                    sectionMessages: {
                        'home': 'MiniAmigixV에 오신 것을 환영합니다!🏠',
                        'chat': 'AI로 코드 작성 중!💻',
                        'musica': '프로그래밍 음악!🎵',
                        'juegos': '휴식 시간!🎮',
                        'clima': '오늘의 날씨!☀️',
                        'traductor': '코드 번역 중!🌐',
                        'blog': '기사 읽기!📝',
                        'soporte': '도와드리기 위해 여기 있습니다!💪',
                        'eventos': '일정 정리 중!📅',
                        'entretenimiento': '즐거운 시간!🎬',
                        'estudio': '새로운 것 배우기!📚',
                        'tutorial': '단계별로 가르쳐 드립니다!🎓'
                    },
                    randomExpressions: [
                        '좋은 날이네요!☀️',
                        '도움이 필요하신가요?🤔',
                        '당신을 위해 여기 있습니다!💪',
                        '프로그래밍 해요!💻',
                        '당신은 할 수 있어요!🌟',
                        '훌륭한 작업입니다!⭐',
                        '계속하세요!🚀',
                        '멋지네요!👏'
                    ],
                    typing: '입력 중...💻',
                    thinking: '생각 중...🤔',
                    done: '완료!🎉'
                },
                'zh': {
                    greetings: [
                        '你好！我是阿米吉斯，你的程序员鸭子🦆',
                        '很高兴见到你！我能帮你什么？',
                        '你好朋友！我准备好帮你了',
                        '欢迎！我是阿米吉斯，你的助手',
                        '嘿！准备好开始了吗？'
                    ],
                    sectionMessages: {
                        'home': '欢迎来到MiniAmigixV！🏠',
                        'chat': '用AI写代码！💻',
                        'musica': '编程音乐！🎵',
                        'juegos': '放松时间！🎮',
                        'clima': '今天的天气！☀️',
                        'traductor': '翻译代码！🌐',
                        'blog': '阅读文章！📝',
                        'soporte': '在这里帮助你！💪',
                        'eventos': '整理你的日程！📅',
                        'entretenimiento': '娱乐时间！🎬',
                        'estudio': '学习新事物！📚',
                        'tutorial': '我一步步教你！🎓'
                    },
                    randomExpressions: [
                        '美好的一天！☀️',
                        '需要帮助吗？🤔',
                        '我在这里为你！💪',
                        '让我们编程吧！💻',
                        '你可以做到！🌟',
                        '出色的工作！⭐',
                        '继续加油！🚀',
                        '太棒了！👏'
                    ],
                    typing: '输入中...💻',
                    thinking: '思考中...🤔',
                    done: '完成！🎉'
                },
                'ru': {
                    greetings: [
                        'Привет! Я Амигис, твоя утка-программист 🦆',
                        'Рад тебя видеть! Чем могу помочь?',
                        'Привет друг! Я готов помочь',
                        'Добро пожаловать! Я Амигис, твой помощник',
                        'Эй! Готов начать?'
                    ],
                    sectionMessages: {
                        'home': 'Добро пожаловать в MiniAmigixV! 🏠',
                        'chat': 'Пишу код с ИИ! 💻',
                        'musica': 'Музыка для программирования! 🎵',
                        'juegos': 'Время отдохнуть! 🎮',
                        'clima': 'Погода сегодня! ☀️',
                        'traductor': 'Перевожу код! 🌐',
                        'blog': 'Читаю статьи! 📝',
                        'soporte': 'Здесь чтобы помочь! 💪',
                        'eventos': 'Организую расписание! 📅',
                        'entretenimiento': 'Время повеселиться! 🎬',
                        'estudio': 'Учиться новому! 📚',
                        'tutorial': 'Научу пошагово! 🎓'
                    },
                    randomExpressions: [
                        'Какой хороший день! ☀️',
                        'Нужна помощь? 🤔',
                        'Я здесь для тебя! 💪',
                        'Давайте программировать! 💻',
                        'Ты можешь! 🌟',
                        'Отличная работа! ⭐',
                        'Продолжай так! 🚀',
                        'Гениально! 👏'
                    ],
                    typing: 'Пишу... 💻',
                    thinking: 'Думаю... 🤔',
                    done: 'Готово! 🎉'
                },
                'ar': {
                    greetings: [
                        'مرحباً! أنا أميجيس، بطة المبرمج 🦆',
                        'سعيد برؤيتك! كيف يمكنني مساعدتك؟',
                        'مرحباً صديقي! أنا مستعد للمساعدة',
                        'مرحباً! أنا أميجيس، مساعدك',
                        'هي! هل أنت مستعد للبدء؟'
                    ],
                    sectionMessages: {
                        'home': 'مرحباً بك في MiniAmigixV! 🏠',
                        'chat': 'كتابة الكود بالذكاء الاصطناعي! 💻',
                        'musica': 'موسيقى للبرمجة! 🎵',
                        'juegos': 'وقت الاسترخاء! 🎮',
                        'clima': 'طقس اليوم! ☀️',
                        'traductor': 'ترجمة الكود! 🌐',
                        'blog': 'قراءة المقالات! 📝',
                        'soporte': 'هنا للمساعدة! 💪',
                        'eventos': 'تنظيم جدولك! 📅',
                        'entretenimiento': 'وقت الترفيه! 🎬',
                        'estudio': 'تعلم أشياء جديدة! 📚',
                        'tutorial': 'أعلمك خطوة بخطوة! 🎓'
                    },
                    randomExpressions: [
                        'ما يوم جميل! ☀️',
                        'تحتاج مساعدة؟ 🤔',
                        'أنا هنا من أجلك! 💪',
                        'لنبرمج! 💻',
                        'يمكنك فعل ذلك! 🌟',
                        'عمل ممتاز! ⭐',
                        'استمر! 🚀',
                        'رائع! 👏'
                    ],
                    typing: 'كتابة... 💻',
                    thinking: 'تفكير... 🤔',
                    done: 'تم! 🎉'
                }
            };
            
            this.currentLang = 'es';
            this.greetings = this.translations['es'].greetings;
            this.sectionMessages = this.translations['es'].sectionMessages;
            this.randomExpressions = this.translations['es'].randomExpressions;
            
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
            this.detectLanguage();
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
            
            // Detectar cambios de sección (popstate y carga inicial)
            window.addEventListener('popstate', () => this.detectCurrentSection());
            
            // Detectar cambios de sección al navegar (para SPA o cambios de URL)
            setInterval(() => {
                const currentPath = window.location.pathname;
                if (currentPath !== this.lastDetectedPath) {
                    this.lastDetectedPath = currentPath;
                    this.detectCurrentSection();
                }
            }, 500);
            
            // Adaptar al redimensionar ventana
            window.addEventListener('resize', () => this.constrainPosition());
            
            // Detectar cambios de idioma en localStorage
            window.addEventListener('storage', (e) => {
                if (e.key === 'idioma' && e.newValue !== e.oldValue) {
                    this.setLanguage(e.newValue);
                }
            });
            
            // También detectar cambios de idioma en la misma página (para SPA)
            const originalSetItem = localStorage.setItem;
            localStorage.setItem = function(key, value) {
                originalSetItem.call(this, key, value);
                if (key === 'idioma' && window.amigisInstance) {
                    window.amigisInstance.setLanguage(value);
                }
            };
        }

        // ==================== ARRASTRAR ====================

        startDrag(e) {
            this.isDragging = true;
            this.dragPointerId = e.pointerId;
            this.wrapper.setPointerCapture(e.pointerId);
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
                
                // Obtener nombre personalizado de Amigis
                this.amigisName = window.amigisConfig.amigisName || 'Amigis';
                
                // Actualizar saludos con el nombre del usuario y el nombre de Amigis
                this.updateGreetings();
            }
            
            // Aplicar personalización del patito
            this.applyCustomization();
        }

        applyCustomization() {
            if (!window.amigisConfig) return;
            
            const config = window.amigisConfig;
            
            // Aplicar ropa
            this.setClothing(config.patitoRopa || 'hoodie');
            
            // Aplicar color de ropa
            this.setClothingColor(config.patitoColorRopa || 'purple');
            
            // Aplicar accesorio
            this.setAccessory(config.patitoAccesorio || 'none');
            
            // Aplicar color del cuerpo
            this.setBodyColor(config.patitoColorCuerpo || 'yellow');
            
            // Aplicar estilo
            this.setStyle(config.patitoEstilo || 'normal');
        }

        setClothing(type) {
            // Ocultar toda la ropa
            const clothingItems = document.querySelectorAll('.clothing-item');
            clothingItems.forEach(item => item.style.display = 'none');
            
            // Mostrar la ropa seleccionada
            if (type !== 'none') {
                const selectedItem = document.getElementById(type);
                if (selectedItem) {
                    selectedItem.style.display = 'block';
                }
            }
        }

        setClothingColor(color) {
            const colorMap = {
                'purple': '#C8A2C8',
                'blue': '#87CEEB',
                'green': '#90EE90',
                'red': '#FF6B6B',
                'black': '#333333',
                'white': '#FFFFFF'
            };
            
            const hoodie = document.querySelector('#hoodie ellipse');
            const shirt = document.querySelector('#shirt rect');
            
            if (hoodie) {
                hoodie.setAttribute('fill', colorMap[color] || colorMap['purple']);
            }
            if (shirt) {
                shirt.setAttribute('fill', colorMap[color] || colorMap['white']);
            }
        }

        setAccessory(type) {
            // Ocultar todos los accesorios
            const accessories = document.querySelectorAll('.accessory-item');
            accessories.forEach(item => item.style.display = 'none');
            
            // Mostrar el accesorio seleccionado
            if (type !== 'none') {
                const selectedItem = document.getElementById(`accessory-${type}`);
                if (selectedItem) {
                    selectedItem.style.display = 'block';
                }
            }
        }

        setBodyColor(color) {
            const gradientMap = {
                'yellow': 'url(#bodyGradient)',
                'orange': 'url(#bodyGradientOrange)',
                'white': 'url(#bodyGradientWhite)',
                'pink': 'url(#bodyGradientPink)'
            };
            
            const body = document.querySelector('#body ellipse');
            const head = document.querySelector('#head circle');
            
            if (body) {
                body.setAttribute('fill', gradientMap[color] || gradientMap['yellow']);
            }
            if (head) {
                head.setAttribute('fill', gradientMap[color] || gradientMap['yellow']);
            }
        }

        setStyle(style) {
            const wrapper = document.getElementById('amigis-wrapper');
            if (!wrapper) return;
            
            // Remover clases de estilo anteriores
            wrapper.classList.remove('style-neon', 'style-gradient');
            
            // Aplicar nuevo estilo
            if (style === 'neon') {
                wrapper.classList.add('style-neon');
            } else if (style === 'gradient') {
                wrapper.classList.add('style-gradient');
            }
        }

        detectLanguage() {
            // Detectar idioma del localStorage o usar español por defecto
            const savedLang = localStorage.getItem('idioma') || 'es';
            this.setLanguage(savedLang);
        }

        setLanguage(lang) {
            // Verificar si el idioma está disponible
            if (!this.translations[lang]) {
                console.warn(`Idioma ${lang} no disponible, usando español`);
                lang = 'es';
            }
            
            this.currentLang = lang;
            
            // Actualizar mensajes con el nuevo idioma
            const langData = this.translations[lang];
            this.greetings = langData.greetings;
            this.sectionMessages = langData.sectionMessages;
            this.randomExpressions = langData.randomExpressions;
            
            // Actualizar saludos con el nombre del usuario si está disponible
            this.updateGreetings();
            
            console.log(`Amigis idioma cambiado a: ${lang}`);
        }

        updateGreetings() {
            if (this.userName && this.amigisName) {
                const langData = this.translations[this.currentLang];
                const greetingTemplates = langData.greetings;
                
                // Reemplazar placeholders con el nombre del usuario y de Amigis
                this.greetings = greetingTemplates.map(greeting => {
                    return greeting
                        .replace('{userName}', this.userName)
                        .replace('{amigisName}', this.amigisName);
                });
            }
        }

        updateTheme() {
            const isLight = document.body.classList.contains('light');
            const imagePath = isLight ? '/static/amigis/amigis-light.svg' : '/static/amigis/amigis-dark.svg';
            
            if (this.image) {
                // Solo cambiar el src de la imagen existente, no recrear la mascota
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
                    const langData = this.translations[this.currentLang];
                    this.showMessage(langData.typing);
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
                    const langData = this.translations[this.currentLang];
                    this.showMessage(langData.thinking);
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
            const langData = this.translations[this.currentLang];
            this.showMessage(langData.done);
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
