// Traductor Module JavaScript
document.addEventListener('DOMContentLoaded', () => {
    console.log("🌐 MiniAmigixV Traductor: Online");
    
    // DOM Elements
    const sourceText = document.getElementById('source-text');
    const targetText = document.getElementById('target-text');
    const sourceLanguage = document.getElementById('source-language');
    const targetLanguage = document.getElementById('target-language');
    const translateBtn = document.getElementById('translate-btn');
    const swapLanguages = document.getElementById('swap-languages');
    const clearSource = document.getElementById('clear-source');
    const clearTarget = document.getElementById('clear-target');
    const copySource = document.getElementById('copy-source');
    const copyTarget = document.getElementById('copy-target');
    const languageInfo = document.getElementById('language-info');
    const exampleItems = document.querySelectorAll('.example-item');
    
    // State
    let isTranslating = false;
    
    // Initialize
    setupEventListeners();
    loadExamples();
    
    // Functions
    function setupEventListeners() {
        // Translate button
        translateBtn.addEventListener('click', translateText);
        
        // Enter key in source text
        sourceText.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && e.ctrlKey) {
                e.preventDefault();
                translateText();
            }
        });
        
        // Swap languages
        swapLanguages.addEventListener('click', swapLanguagesFunc);
        
        // Clear buttons
        clearSource.addEventListener('click', () => {
            sourceText.value = '';
            targetText.value = '';
            languageInfo.textContent = '';
        });
        
        clearTarget.addEventListener('click', () => {
            targetText.value = '';
        });
        
        // Copy buttons
        copySource.addEventListener('click', () => {
            navigator.clipboard.writeText(sourceText.value).then(() => {
                showNotification('Texto copiado al portapapeles', 'success');
            });
        });
        
        copyTarget.addEventListener('click', () => {
            navigator.clipboard.writeText(targetText.value).then(() => {
                showNotification('Traducción copiada al portapapeles', 'success');
            });
        });
        
        // Example items
        exampleItems.forEach(item => {
            item.addEventListener('click', () => {
                const sourceLang = sourceLanguage.value === 'auto' ? 'es' : sourceLanguage.value;
                const targetLang = targetLanguage.value;
                
                const sourceTextValue = item.getAttribute(`data-${sourceLang}`) || 
                                      item.getAttribute('data-es') || 
                                      item.getAttribute('data-en') || 
                                      item.textContent;
                                      
                const targetTextValue = item.getAttribute(`data-${targetLang}`) || 
                                       item.getAttribute('data-es') || 
                                       item.getAttribute('data-en') || 
                                       item.textContent;
                
                sourceText.value = sourceTextValue;
                targetText.value = targetTextValue;
                
                // Set languages if not auto
                if (sourceLanguage.value === 'auto') {
                    sourceLanguage.value = 'es';
                }
                
                // Translate automatically
                translateText();
            });
        });
    }
    
    function loadExamples() {
        // Examples are already loaded from HTML data attributes
        console.log("Examples loaded");
    }
    
    function translateText() {
        if (isTranslating) return;
        
        const text = sourceText.value.trim();
        if (!text) {
            showNotification('Por favor ingresa un texto para traducir', 'warning');
            return;
        }
        
        isTranslating = true;
        translateBtn.textContent = 'Traduciendo...';
        translateBtn.disabled = true;
        
        // Show loading state
        targetText.value = 'Traduciendo...';
        languageInfo.textContent = '';
        
        const sourceLang = sourceLanguage.value;
        const targetLang = targetLanguage.value;
        
        // Simulate API call delay
        setTimeout(() => {
            // Try to use the backend translation API
            fetch('/traductor/translate/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({
                    text: text,
                    source: sourceLang,
                    target: targetLang
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    targetText.value = data.translated_text || text;
                    
                    // Show language detection info
                    if (data.source && data.source !== 'auto') {
                        const langNames = {
                            'af': 'afrikaans', 'sq': 'albanés', 'am': 'amárico', 'ar': 'árabe',
                            'hy': 'armenio', 'az': 'azerí', 'eu': 'vasco', 'be': 'bielorruso',
                            'bn': 'bengalí', 'bs': 'bosnio', 'bg': 'búlgaro', 'ca': 'catalán',
                            'ceb': 'cebuano', 'ny': 'chichewa', 'zh': 'chino (simplificado)',
                            'zh-tw': 'chino (tradicional)', 'co': 'corso', 'hr': 'croata',
                            'cs': 'checo', 'da': 'danés', 'nl': 'holandés', 'en': 'inglés',
                            'eo': 'esperanto', 'et': 'estonio', 'tl': 'filipino', 'fi': 'finlandés',
                            'fr': 'francés', 'fy': 'frisón', 'gl': 'gallego', 'ka': 'georgiano',
                            'de': 'alemán', 'el': 'griego', 'gu': 'gujarati', 'ht': 'criollo haitiano',
                            'ha': 'hausa', 'haw': 'hawaiano', 'iw': 'hebreo', 'hi': 'hindi',
                            'hmn': 'hmong', 'hu': 'húngaro', 'is': 'islandés', 'ig': 'igbo',
                            'id': 'indonesio', 'ga': 'irlandés', 'it': 'italiano', 'ja': 'japonés',
                            'jw': 'javanés', 'kn': 'kannada', 'kk': 'kazajo', 'km': 'jemer',
                            'ko': 'coreano', 'ku': 'kurdo (kurmanjí)', 'ky': 'kirguís', 'lo': 'laosiano',
                            'la': 'latín', 'lv': 'letón', 'lt': 'lituano', 'lb': 'luxemburgués',
                            'mk': 'macedonio', 'mg': 'malgache', 'ms': 'malayo', 'ml': 'malayalam',
                            'mt': 'maltés', 'mi': 'maorí', 'mr': 'maratí', 'mn': 'mongol',
                            'my': 'birmano', 'ne': 'nepali', 'no': 'noruego', 'ps': 'pachto',
                            'fa': 'persa', 'pl': 'polaco', 'pt': 'portugués', 'pa': 'punjabi',
                            'ro': 'rumano', 'ru': 'ruso', 'sm': 'samoano', 'gd': 'gaélico escocés',
                            'sr': 'serbio', 'st': 'sesoto', 'sn': 'shona', 'sd': 'sindhi',
                            'si': 'cingalés', 'sk': 'eslovaco', 'sl': 'esloveno', 'so': 'somali',
                            'es': 'español', 'su': 'sundanés', 'sw': 'suahili', 'sv': 'sueco',
                            'tg': 'tayiko', 'ta': 'tamil', 'te': 'telugu', 'th': 'tailandés',
                            'tr': 'turco', 'uk': 'ucraniano', 'ur': 'urdú', 'uz': 'uzbeko',
                            'vi': 'vietnamita', 'cy': 'galés', 'xh': 'xhosa', 'yi': 'yidis',
                            'yo': 'yoruba', 'zu': 'zulú'
                        };
                        
                        const sourceName = langNames[data.source] || data.source;
                        const targetName = langNames[targetLang] || targetLang;
                        
                        languageInfo.textContent = `Detectado: ${sourceName} → ${targetName}`;
                        
                        if (data.mock) {
                            languageInfo.textContent += ' (traducción simulada)';
                            languageInfo.style.color = '#ff9800';
                        } else {
                            languageInfo.style.color = var(--neon-pink);
                        }
                    } else {
                        languageInfo.textContent = `Traducción completada`;
                        languageInfo.style.color = var(--neon-pink);
                    }
                    
                    showNotification('Traducción completada', 'success');
                } else {
                    throw new Error(data.error || 'Error en la traducción');
                }
            })
            .catch(error => {
                console.error('Translation error:', error);
                // Fallback to mock translation
                targetText.value = mockTranslate(text, sourceLang, targetLang);
                languageInfo.textContent = 'Traducción simulada (servicio no disponible)';
                languageInfo.style.color = '#ff9800';
                showNotification('Usando traducción simulada', 'warning');
            })
            .finally(() => {
                isTranslating = false;
                translateBtn.textContent = 'Traducir';
                translateBtn.disabled = false;
            });
        }, 500); // Simulate network delay
    }
    
    function swapLanguagesFunc() {
        const sourceValue = sourceLanguage.value;
        const targetValue = targetLanguage.value;
        
        // Don't swap if source is auto
        if (sourceValue === 'auto') {
            // Swap target to source and set source to detect
            sourceLanguage.value = targetValue;
            targetLanguage.value = 'auto';
        } else {
            // Normal swap
            sourceLanguage.value = targetValue;
            targetLanguage.value = sourceValue;
        }
        
        // Swap text areas
        const sourceTextValue = sourceText.value;
        const targetTextValue = targetText.value;
        
        sourceText.value = targetTextValue;
        targetText.value = sourceTextValue;
        
        // Clear info
        languageInfo.textContent = '';
    }
    
    function mockTranslate(text, source, target) {
        """Mock translation function for demo purposes"""
        // Simple mock: just return the text with language markers
        if (source === target) {
            return text;
        }
        
        const langNames = {
            'es': 'Español', 'en': 'Inglés', 'fr': 'Francés', 'de': 'Alemán',
            'it': 'Italiano', 'pt': 'Portugués', 'ru': 'Ruso', 'zh': 'Chino',
            'ja': 'Japonés', 'ko': 'Coreano', 'ar': 'Árabe'
        };
        
        const sourceName = langNames[source] || source.toUpperCase();
        const targetName = langNames[target] || target.toUpperCase();
        
        return `[Traducción de ${sourceName} a ${targetName}]\n\n${text}`;
    }
    
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
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
    
    console.log("🌐 Traductor module initialized");
});

// Export functions for use in other modules if needed
window.MiniAmigixTraductor = {
    translateText,
    swapLanguages: swapLanguagesFunc
};