document.addEventListener('DOMContentLoaded', () => {
    const supportForm = document.getElementById('soporte-form');
    if (!supportForm) return;

    supportForm.addEventListener('submit', () => {
        const submitButton = supportForm.querySelector('button[type="submit"]');
        if (submitButton) {
            submitButton.disabled = true;
            submitButton.textContent = 'Enviando...';
        }
    });
});
