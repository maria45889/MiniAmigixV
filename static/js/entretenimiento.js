// Entretenimiento Module JavaScript
document.addEventListener('DOMContentLoaded', () => {
    console.log("🎪 MiniAmigixV Entretenimiento: Online");
    
    // DOM Elements
    const entertainmentLaunches = document.querySelectorAll('.entertainment-launch');
    const notificationContainer = document.getElementById('notification-container');
    
    // State
    let riddlesIndex = 0;
    let fortunesIndex = 0;
    let quotesIndex = 0;
    let challengesIndex = 0;
    let curiositiesIndex = 0;
    
    // Data arrays
    const riddles = [
        { question: "¿Qué tiene llaves pero no abre puertas, tiene espacio pero no es una habitación y puedes entrar pero no salir?", answer: "Un teclado" },
        { question: "¿Qué sube y baja pero nunca se mueve?", answer: "Las escaleras" },
        { question: "¿Qué tiene muchas agujas pero no coser?", answer: "Un pino" },
        { question: "¿Qué tiene un cuello pero no cabeza?", answer: "Una botella" },
        { question: "¿Qué moja mientras más seca?", answer: "Una toalla" },
        { question: "¿Qué tiene ojos pero no puede ver?", answer: "Una patata" },
        { question: "¿Qué tiene un pulgar y cuatro dedos pero no es una mano?", answer: "Un guante" },
        { question: "¿Qué tiene cabeza y cola pero no cuerpo?", answer: "Una moneda" }
    ];
    
    const wheelFortuneOptions = [
        "¡Gana un deseo! (Funcionalidad simulada)",
        "Recibe 100 puntos de experiencia",
        "Descubre un secreto personal",
        "Haz un reto divertido",
        "Recibe un mensaje motivacional",
        "Gana un día de descanso mental",
        "Descubre tu número de la suerte",
        "Recibe un abrazo virtual",
        "Pierdes un turno (suerte la próxima)",
        "Gana el derecho a saltar una tarea",
        "Descubre una curiosidad asombrosa",
        "Recibe un cumplido inesperado"
    ];
    
    const fortuneCookies = [
        "Una oportunidad emocionante se acerca a ti.",
        "Tu paciencia será recompensada pronto.",
        "Alguien en tu vida necesita tu consejo.",
        "Un viaje inesperado traerá alegría.",
        "Tu trabajo duro dará sus frutos.",
        "Nuevas amistades están en el horizonte.",
        "Confía en tu intuición hoy.",
        "Un antiguo problema encontrará solución.",
        "Tu creatividad inspirará a otros.",
        "Un mensaje importante llegará pronto.",
        "La suerte favorece a los valientes.",
        "Hoy es un buen día para empezar algo nuevo."
    ];
    
    const zodiacSigns = [
        { name: "Aries", dates: "21 Mar - 19 Abr", traits: ["Valiente", "Enérgico", "Pionero"], compatibility: "Leo, Sagitario" },
        { name: "Tauro", dates: "20 Abr - 20 May", traits: ["Paciente", "Confiable", "Práctico"], compatibility: "Virgo, Capricornio" },
        { name: "Géminis", dates: "21 May - 20 Jun", traits: ["Curioso", "Adaptable", "Comunicativo"], compatibility: "Libra, Acuario" },
        { name: "Cáncer", dates: "21 Jun - 22 Jul", traits: ["Leal", "Emocional", "Intuitivo"], compatibility: "Escorpio, Piscis" },
        { name: "Leo", dates: "23 Jul - 22 Ago", traits: ["Generoso", "Cálido", "Autoritario"], compatibility: "Aries, Sagitario" },
        { name: "Virgo", dates: "23 Ago - 22 Sep", traits: ["Analítico", "Trabajador", "Práctico"], compatibility: "Tauro, Capricornio" },
        { name: "Libra", dates: "23 Sep - 22 Oct", traits: ["Justo", "Social", "Romántico"], compatibility: "Géminis, Acuario" },
        { name: "Escorpio", dates: "23 Oct - 21 Nov", traits: ["Pasional", "Recurso", "Determinado"], compatibility: "Cáncer, Piscis" },
        { name: "Sagitario", dates: "22 Nov - 21 Dic", traits: ["Optimista", "Aventurero", "Filósofo"], compatibility: "Aries, Leo" },
        { name: "Capricornio", dates: "22 Dic - 19 Ene", traits: ["Disciplinado", "Responsable", "Ambicioso"], compatibility: "Tauro, Virgo" },
        { name: "Acuario", dates: "20 Ene - 18 Feb", traits: ["Original", "Independente", "Humanitario"], compatibility: "Géminis, Libra" },
        { name: "Piscis", dates: "19 Feb - 20 Mar", traits: ["Compasivo", "Artístico", "Sabio"], compatibility: "Cáncer, Escorpio" }
    ];
    
    const curiosities = [
        "Los pulpos tienen tres corazones.",
        "Una nube promedio pesa más de un millón de libras.",
        "Los plátanos son ligeramente radiactivos.",
        "Marte tiene puesta de sol azul.",
        "Una ráfaga de viento puede viajar más rápido que un guepardo.",
        "La miel nunca se echa a perder.",
        "Los pingüinos pueden saltar hasta 2 metros de altura.",
        "El corazón de una ballena azul es tan grande como un auto pequeño.",
        "Hay más estrellas en el universo que granos de arena en todas las playas de la Tierra.",
        "Un rayo contiene suficiente energía para toastear 100,000 rebanadas de pan."
    ];
    
    const randomQuotes = [
        "La vida es lo que pasa mientras estás ocupado haciendo otros planes. - John Lennon",
        "El único modo de hacer un gran trabajo es amar lo que haces. - Steve Jobs",
        "La felicidad no es algo listo. Viene de tus propias acciones. - Dalai Lama",
        "No importa cuán lento vayas siempre que no te detengas. - Confucio",
        "La mejor manera de predecir el futuro es creándolo. - Peter Drucker",
        "No es cuánto tenemos, sino cuánto disfrutamos, lo que hace la felicidad. - Charles Spurgeon",
        "El éxito no es final, el fracaso no es fatal: es el coraje de continuar lo que cuenta. - Winston Churchill",
        "En medio de la dificultad yace la oportunidad. - Albert Einstein",
        "La única limitación para nuestro logro del mañana será nuestras dudas de hoy. - Franklin D. Roosevelt",
        "No esperes el momento perfecto, toma el momento y hazlo perfecto. - Desconocido"
    ];
    
    const funChallenges = [
        "Habla en rimas durante los próximos 10 minutos",
        "Haz 20 sentadillas mientras cuentas hacia atrás desde 100",
        "Escucha una canción y baila como si nadie te estuviera viendo",
        "Escribe una carta de agradecimiento a tu futuro yo",
        "Haz una lista de 10 cosas por las que estás agradecido",
        "Toma una foto de algo que te haga feliz y ponla como fondo de pantalla",
        "Aprende y usa una nueva palabra en una conversación hoy",
        "Bebe un vaso de agua y nota cómo te sientes",
        "Haz estiramientos durante 5 minutos al despertar",
        "Sonríe a un extraño y observa su reacción",
        "Escribe una poesía corta sobre tu día",
        "Organiza tu escritorio o espacio de trabajo en 10 minutos"
    ];
    
    const rpsOptions = ["piedra", "papel", "tijera"];
    
    const hangmanWords = {
        "Animales": ["PERRO", "GATO", "ELEFANTE", "JIRAFA", "PINGÜINO"],
        "Países": ["ESPAÑA", "JAPÓN", "BRASIL", "CANADÁ", "AUSTRALIA"],
        "Comida": ["PIZZA", "SUSHI", "TACO", "PAELLA", "HAMBURGUESA"],
        "Películas": ["TITANIC", "INCEPTION", "GLADIADOR", "MATRIZ", "AVATAR"]
    };
    
    const sudokuPuzzles = [
        // Easy puzzle 1
        [
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9]
        ]
    ];
    
    // Initialize entertainment launches
    entertainmentLaunches.forEach(button => {
        button.addEventListener('click', (e) => {
            e.preventDefault();
            const activity = button.closest('.entertainment-card').dataset.activity;
            launchEntertainment(activity, button);
        });
    });
    
    function launchEntertainment(activity, button) {
        // Visual feedback
        const originalText = button.textContent;
        button.textContent = 'Cargando...';
        button.disabled = true;
        
        setTimeout(() => {
            switch(activity) {
                case 'riddles':
                    showRiddle();
                    break;
                case 'wheel-fortune':
                    spinWheel();
                    break;
                case 'fortune-cookie':
                    crackFortuneCookie();
                    break;
                case 'zodiac':
                    showZodiacInfo();
                    break;
                case 'curiosities':
                    showCuriosity();
                    break;
                case 'random-quotes':
                    showRandomQuote();
                    break;
                case 'fun-challenges':
                    showFunChallenge();
                    break;
                case 'rps':
                    playRockPaperScissors();
                    break;
                case 'hangman':
                    startHangman();
                    break;
                case 'sudoku':
                    startSudoku();
                    break;
                default:
                    alert(`Actividad ${activity} no implementada aún`);
            }
            
            button.textContent = originalText;
            button.disabled = false;
        }, 500);
    }
    
    function showRiddle() {
        const riddle = riddles[riddlesIndex];
        riddlesIndex = (riddlesIndex + 1) % riddles.length;

        const answer = prompt(`${riddle.question}\n\n¿Cuál crees que es la respuesta?\n\nEscribe 'respuesta' para verla.`);
        if (answer === null) return; // user cancelled

        const ansLower = answer.trim().toLowerCase();
        if (ansLower === 'respuesta') {
            alert(`¡La respuesta es: ${riddle.answer}!`);
        } else if (ansLower.length > 0) {
            if (ansLower === String(riddle.answer).toLowerCase()) {
                alert("¡Correcto! 🎉");
            } else {
                alert(`Incorrecto. La respuesta correcta es: ${riddle.answer}`);
            }
        }
    }
    
    function spinWheel() {
        const result = wheelFortuneOptions[Math.floor(Math.random() * wheelFortuneOptions.length)];
        alert(`🎡 La ruleta ha girado y obtenido:\n\n${result}`);
        showNotification(`Ruleta: ${result}`, 'success');
    }
    
    function crackFortuneCookie() {
        const fortune = fortuneCookies[Math.floor(Math.random() * fortuneCookies.length)];
        alert(`🍪 ¡Has roto tu galleta de la fortuna!\n\n${fortune}`);
        showNotification(`Galleta de la fortuna: ${fortune.substring(0, 50)}...`, 'info');
    }
    
    function showZodiacInfo() {
        const birthDate = prompt("Ingresa tu fecha de nacimiento (DD/MM/AAAA):");
        if (!birthDate) return;
        
        // Simple zodiac calculation (simplified)
        const [day, month, year] = birthDate.split('/').map(Number);
        if (isNaN(day) || isNaN(month) || isNaN(year)) {
            alert("Fecha inválida. Por favor usa el formato DD/MM/AAAA");
            return;
        }
        
        let signIndex = 0;
        if ((month === 3 && day >= 21) || (month === 4 && day <= 19)) signIndex = 0; // Aries
        else if ((month === 4 && day >= 20) || (month === 5 && day <= 20)) signIndex = 1; // Tauro
        else if ((month === 5 && day >= 21) || (month === 6 && day <= 20)) signIndex = 2; // Géminis
        else if ((month === 6 && day >= 21) || (month === 7 && day <= 22)) signIndex = 3; // Cáncer
        else if ((month === 7 && day >= 23) || (month === 8 && day <= 22)) signIndex = 4; // Leo
        else if ((month === 8 && day >= 23) || (month === 9 && day <= 22)) signIndex = 5; // Virgo
        else if ((month === 9 && day >= 23) || (month === 10 && day <= 22)) signIndex = 6; // Libra
        else if ((month === 10 && day >= 23) || (month === 11 && day <= 21)) signIndex = 7; // Escorpio
        else if ((month === 11 && day >= 22) || (month === 12 && day <= 21)) signIndex = 8; // Sagitario
        else if ((month === 12 && day >= 22) || (month === 1 && day <= 19)) signIndex = 9; // Capricornio
        else if ((month === 1 && day >= 20) || (month === 2 && day <= 18)) signIndex = 10; // Acuario
        else signIndex = 11; // Piscis
        
        const sign = zodiacSigns[signIndex];
        alert(`♐ Tu signo zodiacal es: ${sign.name}\n\nFechas: ${sign.dates}\n\nCaracterísticas: ${sign.traits.join(', ')}\n\nCompatibilidad: ${sign.compatibility}`);
    }
    
    function showCuriosity() {
        const curiosity = curiosities[Math.floor(Math.random() * curiosities.length)];
        alert(`💡 Curiosidad del día:\n\n${curiosity}`);
        showNotification(`Curiosidad: ${curiosity.substring(0, 50)}...`, 'info');
    }
    
    function showRandomQuote() {
        const quote = randomQuotes[Math.floor(Math.random() * randomQuotes.length)];
        alert(`💭 Frase aleatoria:\n\n${quote}`);
        showNotification(`Frase: ${quote.substring(0, 50)}...`, 'success');
    }
    
    function showFunChallenge() {
        const challenge = funChallenges[Math.floor(Math.random() * funChallenges.length)];
        alert(`🎯 Tu reto divertido:\n\n${challenge}\n\n¿Aceptas el desafío?`);
        showNotification(`Reto: ${challenge.substring(0, 50)}...`, 'warning');
    }
    
    function playRockPaperScissors() {
        const raw = prompt("Elige: piedra, papel o tijera");
        if (!raw) return;
        const userChoice = raw.toLowerCase().trim();
        if (!rpsOptions.includes(userChoice)) {
            alert("Opción inválida. Por favor elige piedra, papel o tijera.");
            return;
        }
        
        const computerChoice = rpsOptions[Math.floor(Math.random() * rpsOptions.length)];
        let result = "";
        
        if (userChoice === computerChoice) {
            result = "¡Empate!";
        } else if (
            (userChoice === "piedra" && computerChoice === "tijera") ||
            (userChoice === "papel" && computerChoice === "piedra") ||
            (userChoice === "tijera" && computerChoice === "papel")
        ) {
            result = "¡Ganaste! 🎉";
        } else {
            result = "Perdiste. ¡Inténtalo de nuevo! 😊";
        }
        
        alert(`Tú elegiste: ${userChoice}\nLa IA eligió: ${computerChoice}\n\n${result}`);
        showNotification(`RPS: Tú ${userChoice} vs IA ${computerChoice} - ${result}`, 'info');
    }
    
    function startHangman() {
        const categories = Object.keys(hangmanWords);
        const category = categories[Math.floor(Math.random() * categories.length)];
        const word = hangmanWords[category][Math.floor(Math.random() * hangmanWords[category].length)];
        
        let guessedLetters = [];
        let wrongGuesses = 0;
        const maxWrongGuesses = 6;
        
        while (wrongGuesses < maxWrongGuesses) {
            // Show current state
            const displayWord = word.split('').map(letter => 
                guessedLetters.includes(letter) ? letter : '_'
            ).join(' ');
            
            const rawGuess = prompt(
                `Categoría: ${category}\n\nPalabra: ${displayWord}\n\n` +
                `Letras intentadas: ${guessedLetters.join(', ') || 'Ninguna'}\n\n` +
                `Errores: ${wrongGuesses}/${maxWrongGuesses}\n\n` +
                `Ingresa una letra o 'solucionar' para intentar adivinar la palabra completa:`
            ).trim();
            if (rawGuess === null) return; // cancelled
            const guess = rawGuess.toUpperCase();

            if (guess === 'SOLUCIONAR') {
                const fullGuessRaw = prompt("¿Cuál crees que es la palabra completa?");
                if (fullGuessRaw === null) return;
                const fullGuess = fullGuessRaw.toUpperCase().trim();
                if (fullGuess === word) {
                    alert(`¡Correcto! La palabra era: ${word}`);
                    showNotification(`Ahorcado: ¡Adivinaste "${word}"!`, 'success');
                    return;
                } else {
                    alert(`Incorrecto. La palabra era: ${word}`);
                    showNotification(`Ahorcado: Fallaste. La palabra era "${word}"`, 'error');
                    return;
                }
            }

            if (guess.length !== 1 || !/[A-Z]/.test(guess)) {
                alert("Por favor ingresa una sola letra.");
                continue;
            }

            if (guessedLetters.includes(guess)) {
                alert("Ya intentaste esa letra. Prueba con otra.");
                continue;
            }

            guessedLetters.push(guess);
            
            if (word.includes(guess)) {
                // Check if won
                if (word.split('').every(letter => guessedLetters.includes(letter))) {
                    alert(`¡Felicitaciones! Adivinaste la palabra: ${word}`);
                    showNotification(`Ahorcado: ¡Adivinaste "${word}"!`, 'success');
                    return;
                }
            } else {
                wrongGuesses++;
                if (wrongGuesses >= maxWrongGuesses) {
                    alert(`¡Has perdido! La palabra era: ${word}`);
                    showNotification(`Ahorcado: Has perdido. La palabra era "${word}"`, 'error');
                    return;
                }
            }
        }
    }
    
    function startSudoku() {
        const puzzle = sudokuPuzzles[0]; // Take first puzzle for now
        alert(`🎯 Sudoku Fácil\n\n${puzzle.map(row => row.join(' ')).join('\n')}\n\nNota: Esta es una versión simplificada. En una implementación completa, tendrías una interfaz interactiva para resolver el sudoku.`);
        showNotification(`Sudoku: Puzzle cargado (versión básica)`, 'info');
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
    
    console.log("🎪 Entretenimiento module initialized");

    // Export functions for use in other modules if needed
    window.MiniAmigixEntretenimiento = {
        launchEntertainment,
        showNotification
    };
});