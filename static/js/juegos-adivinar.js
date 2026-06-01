document.addEventListener('DOMContentLoaded', () => {
    const clues = [
        { answer: 'sol', clue: 'Soy una estrella, doy luz y calor y despierto al día.' },
        { answer: 'corazon', clue: 'Late sin parar, simboliza amor y te mantiene vivo.' },
        { answer: 'luna', clue: 'Brillo de noche, cambio de fases y guío las mareas.' },
        { answer: 'arbol', clue: 'Tengo raíces y hojas, doy sombra y limpio el aire.' },
        { answer: 'lluvia', clue: 'Caigo del cielo en gotas y refresco la tierra sofocada.' },
        { answer: 'estrella', clue: 'En el cielo nocturno titilo y parezco una luz lejana.' },
        { answer: 'montana', clue: 'Soy alta, rocosa y mi cima se cubre de nieve.' }
    ];

    const clueElement = document.getElementById('guess-clue');
    const inputElement = document.getElementById('guess-answer');
    const resultElement = document.getElementById('guess-result');
    const submitButton = document.getElementById('guess-submit');
    const newButton = document.getElementById('guess-new');
    let currentPuzzle = null;

    function normalizeText(text) {
        return text
            .toLowerCase()
            .trim()
            .normalize('NFD')
            .replace(/[\u0300-\u036f]/g, '')
            .replace(/[^a-z0-9]/gi, '');
    }

    function chooseNewPuzzle() {
        currentPuzzle = clues[Math.floor(Math.random() * clues.length)];
        clueElement.textContent = currentPuzzle.clue;
        inputElement.value = '';
        resultElement.textContent = '';
        inputElement.focus();
    }

    function checkAnswer(event) {
        event.preventDefault();
        if (!currentPuzzle) {
            resultElement.textContent = 'Presiona "Nueva adivinanza" para comenzar.';
            return;
        }

        const guess = normalizeText(inputElement.value);
        const answer = normalizeText(currentPuzzle.answer);

        if (!guess) {
            resultElement.textContent = 'Escribe tu respuesta antes de probar.';
            return;
        }

        if (guess === answer) {
            resultElement.innerHTML = `<span class="guess-success">¡Correcto! La respuesta es "${currentPuzzle.answer}".</span>`;
        } else {
            resultElement.innerHTML = `<span class="guess-fail">Buena intuición, pero no es correcto. Intenta otra vez.</span>`;
        }
    }

    submitButton.addEventListener('click', checkAnswer);
    newButton.addEventListener('click', (event) => {
        event.preventDefault();
        chooseNewPuzzle();
    });

    chooseNewPuzzle();
});
