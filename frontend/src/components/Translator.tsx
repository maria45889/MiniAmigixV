import React, { useState } from 'react';
import './Translator.css';

interface TranslationHistory {
  id: number;
  sourceLang: string;
  targetLang: string;
  date: string;
  originalText: string;
  translatedText: string;
  isFavorite: boolean;
}

const Translator: React.FC = () => {
  const [sourceLang, setSourceLang] = useState('es');
  const [targetLang, setTargetLang] = useState('en');
  const [inputText, setInputText] = useState('');
  const [translatedText, setTranslatedText] = useState('');
  const [history, setHistory] = useState<TranslationHistory[]>([
    {
      id: 1,
      sourceLang: 'en',
      targetLang: 'es',
      date: '23/7/2026, 18:39:40',
      originalText: 'hola',
      translatedText: 'hola',
      isFavorite: false
    },
    {
      id: 2,
      sourceLang: 'en',
      targetLang: 'es',
      date: '23/7/2026, 18:39:40',
      originalText: 'hola',
      translatedText: 'hola',
      isFavorite: false
    },
    {
      id: 3,
      sourceLang: 'en',
      targetLang: 'es',
      date: '23/7/2026, 18:39:40',
      originalText: 'hola',
      translatedText: 'hola',
      isFavorite: false
    },
    {
      id: 4,
      sourceLang: 'en',
      targetLang: 'es',
      date: '23/7/2026, 18:39:40',
      originalText: 'hola',
      translatedText: 'hola',
      isFavorite: false
    },
    {
      id: 5,
      sourceLang: 'en',
      targetLang: 'es',
      date: '23/7/2026, 18:39:39',
      originalText: 'hola',
      translatedText: 'hola',
      isFavorite: false
    },
    {
      id: 6,
      sourceLang: 'es',
      targetLang: 'en',
      date: '23/7/2026, 18:39:33',
      originalText: 'hola',
      translatedText: 'hello',
      isFavorite: false
    }
  ]);

  const languages = [
    { code: 'es', name: 'Español', flag: '🇪🇸' },
    { code: 'en', name: 'Inglés', flag: '🇺🇸' },
    { code: 'fr', name: 'Francés', flag: '🇫🇷' },
    { code: 'de', name: 'Alemán', flag: '🇩🇪' },
    { code: 'it', name: 'Italiano', flag: '🇮🇹' },
    { code: 'pt', name: 'Portugués', flag: '🇵🇹' },
    { code: 'ja', name: 'Japonés', flag: '🇯🇵' },
    { code: 'zh', name: 'Chino', flag: '🇨🇳' },
    { code: 'ru', name: 'Ruso', flag: '🇷🇺' },
    { code: 'ar', name: 'Árabe', flag: '🇸🇦' },
  ];

  const handleTranslate = () => {
    // Simulate translation
    const mockTranslations: Record<string, string> = {
      'hola': 'hello',
      'hello': 'hola',
      'buenos días': 'good morning',
      'good morning': 'buenos días',
    };
    
    const translation = mockTranslations[inputText.toLowerCase()] || inputText;
    setTranslatedText(translation);
    
    // Add to history
    const newHistoryItem: TranslationHistory = {
      id: Date.now(),
      sourceLang,
      targetLang,
      date: new Date().toLocaleString('es-ES'),
      originalText: inputText,
      translatedText: translation,
      isFavorite: false
    };
    setHistory([newHistoryItem, ...history]);
  };

  const handleSwapLanguages = () => {
    setSourceLang(targetLang);
    setTargetLang(sourceLang);
  };

  const handleCopyText = (text: string) => {
    navigator.clipboard.writeText(text);
  };

  const handleDeleteHistory = (id: number) => {
    setHistory(history.filter(item => item.id !== id));
  };

  const handleToggleFavorite = (id: number) => {
    setHistory(history.map(item => 
      item.id === id ? { ...item, isFavorite: !item.isFavorite } : item
    ));
  };

  const handleClearInput = () => {
    setInputText('');
    setTranslatedText('');
  };

  const characterCount = inputText.length;
  const maxCharacters = 5000;

  return (
    <div className="translator-container">
      <div className="translator-header">
        <div className="header-title">
          <span className="header-icon">🌍</span>
          <div>
            <h1>Traductor IA</h1>
            <p>MiniAmigixV</p>
          </div>
        </div>
      </div>

      {/* Language Selector */}
      <div className="language-selector">
        <div className="language-select">
          <select 
            value={sourceLang} 
            onChange={(e) => setSourceLang(e.target.value)}
            className="select-dropdown"
          >
            {languages.map(lang => (
              <option key={lang.code} value={lang.code}>
                {lang.flag} {lang.name}
              </option>
            ))}
          </select>
        </div>
        
        <button className="swap-btn" onClick={handleSwapLanguages}>
          ⇄
        </button>
        
        <div className="language-select">
          <select 
            value={targetLang} 
            onChange={(e) => setTargetLang(e.target.value)}
            className="select-dropdown"
          >
            {languages.map(lang => (
              <option key={lang.code} value={lang.code}>
                {lang.flag} {lang.name}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Input Area */}
      <div className="translation-area">
        <div className="input-section">
          <textarea
            className="text-input"
            placeholder="Escribe o pega texto aquí..."
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            maxLength={maxCharacters}
          />
          <div className="input-footer">
            <span className="char-count">{characterCount} / {maxCharacters} caracteres</span>
            <div className="input-actions">
              <button className="action-btn" title="Voz">🎤</button>
              <button className="action-btn" title="Copiar" onClick={() => handleCopyText(inputText)}>📋</button>
              <button className="action-btn" title="Eliminar" onClick={handleClearInput}>🗑️</button>
            </div>
          </div>
        </div>

        {/* Translate Button */}
        <button className="translate-btn" onClick={handleTranslate}>
          ⚡ Traducir
        </button>

        {/* Output Area */}
        <div className="output-section">
          <div className="output-text">
            {translatedText || 'La traducción aparecerá aquí...'}
          </div>
          <div className="output-actions">
            <button className="action-btn" title="Voz">🔊</button>
            <button className="action-btn" title="Copiar" onClick={() => handleCopyText(translatedText)}>📋</button>
            <button className="action-btn" title="Favorito">⭐</button>
          </div>
        </div>
      </div>

      {/* Additional Input Methods */}
      <div className="input-methods">
        <button className="method-btn">
          📷 Imagen
        </button>
        <button className="method-btn">
          📄 Documento
        </button>
        <button className="method-btn">
          📋 Pegar
        </button>
      </div>

      {/* History Section */}
      <div className="history-section">
        <div className="history-header">
          <h2>📚 Historial de traducciones</h2>
          <div className="history-tabs">
            <button className="tab-btn active">Historial</button>
            <button className="tab-btn">⭐ Favoritos</button>
          </div>
        </div>
        
        <div className="history-list">
          {history.map((item) => (
            <div key={item.id} className="history-item">
              <div className="history-header-info">
                <span className="lang-direction">
                  {languages.find(l => l.code === item.sourceLang)?.flag} {languages.find(l => l.code === item.sourceLang)?.name} → {languages.find(l => l.code === item.targetLang)?.flag} {languages.find(l => l.code === item.targetLang)?.name}
                </span>
                <span className="history-date">{item.date}</span>
              </div>
              <div className="history-content">
                <div className="history-original">
                  <span className="text-label">Original:</span>
                  <span className="text-content">{item.originalText}</span>
                </div>
                <div className="history-translated">
                  <span className="text-label">Traducción:</span>
                  <span className="text-content">{item.translatedText}</span>
                </div>
              </div>
              <div className="history-actions">
                <button className="history-action-btn" title="Copiar" onClick={() => handleCopyText(item.translatedText)}>📋</button>
                <button 
                  className={`history-action-btn ${item.isFavorite ? 'favorite' : ''}`} 
                  title="Favorito"
                  onClick={() => handleToggleFavorite(item.id)}
                >
                  ⭐
                </button>
                <button className="history-action-btn" title="Eliminar" onClick={() => handleDeleteHistory(item.id)}>🗑️</button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Translator;
