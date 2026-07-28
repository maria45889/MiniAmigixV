import React, { useState } from 'react';
import './Files.css';

interface File {
  id: number;
  name: string;
  icon: string;
  type: string;
  size: string;
  date: string;
}

interface Folder {
  id: number;
  name: string;
  icon: string;
  count: string;
}

const Files: React.FC = () => {
  const [searchQuery, setSearchQuery] = useState('');

  const folders: Folder[] = [
    { id: 1, name: 'Estudio', icon: '📚', count: '14 archivos' },
    { id: 2, name: 'Programación', icon: '💻', count: '32 archivos' },
    { id: 3, name: 'Música', icon: '🎵', count: '24 canciones' },
    { id: 4, name: 'Imágenes', icon: '🖼️', count: '18 fotos' },
    { id: 5, name: 'Documentos', icon: '📄', count: '12 PDFs' },
    { id: 6, name: 'Videos', icon: '🎥', count: '5 clips' },
    { id: 7, name: 'Descargas', icon: '📥', count: '8 ítems' },
    { id: 8, name: 'Favoritos', icon: '⭐', count: '6 ítems' },
    { id: 9, name: 'Papelera', icon: '🗑️', count: '3 ítems' },
  ];

  const recentFiles: File[] = [
    {
      id: 1,
      name: 'Proyecto_Django.pdf',
      icon: '📄',
      type: 'Documento PDF',
      size: '4.2 MB',
      date: 'Ayer'
    },
    {
      id: 2,
      name: 'Apuntes_Python.docx',
      icon: '📝',
      type: 'Documento Word',
      size: '1.1 MB',
      date: 'Hoy'
    },
    {
      id: 3,
      name: 'Presentación.pptx',
      icon: '📊',
      type: 'Presentación PowerPoint',
      size: '8.5 MB',
      date: 'Hace 3 días'
    },
    {
      id: 4,
      name: 'Captura.png',
      icon: '📸',
      type: 'Imagen PNG',
      size: '2.4 MB',
      date: 'Hoy'
    },
    {
      id: 5,
      name: 'Música.mp3',
      icon: '🎵',
      type: 'Archivo Audio',
      size: '5.8 MB',
      date: 'Hace 2 días'
    }
  ];

  const aiTools = [
    { id: 1, name: 'Resumir PDF', icon: '📄' },
    { id: 2, name: 'Traducir Doc', icon: '🌍' },
    { id: 3, name: 'Ortografía', icon: '📝' },
    { id: 4, name: 'Explicar Código', icon: '💻' },
    { id: 5, name: 'Resumir PPT', icon: '📊' },
    { id: 6, name: 'Transcribir', icon: '🎧' },
  ];

  const storage = {
    used: 8.5,
    total: 15,
    percentage: 56.6
  };

  const getAIAction = (file: File) => {
    if (file.type.includes('PDF')) return '🤖 Resumir';
    if (file.type.includes('Word')) return '📝 Corregir';
    if (file.type.includes('PowerPoint')) return '📊 Resumir';
    if (file.type.includes('Audio')) return '🎧 Transcribir';
    return '🤖 Analizar';
  };

  return (
    <div className="files-container">
      <div className="files-header">
        <div className="header-title">
          <span className="header-icon">📁</span>
          <div>
            <h1>Mis Archivos & Documentos</h1>
            <p>Todo tu contenido organizado en un solo lugar con inteligencia artificial.</p>
          </div>
        </div>
      </div>

      {/* Search and Actions */}
      <div className="search-section">
        <div className="search-bar">
          <span className="search-icon">🔍</span>
          <input
            type="text"
            placeholder="Buscar archivo..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
          <div className="action-buttons">
            <button className="action-btn primary">Subir Archivo</button>
            <button className="action-btn secondary">Nueva Carpeta</button>
            <button className="action-btn secondary">Sincronizar</button>
          </div>
        </div>
      </div>

      {/* Amigis Files */}
      <div className="amigis-files-section">
        <div className="amigis-files-card">
          <div className="amigis-avatar">🦆</div>
          <div className="amigis-content">
            <h3>Centro Inteligente de Archivos 🦆</h3>
            <p>"¡Hola! Puedo resumir tus PDFs, traducir documentos, corregir ortografía o transcribir audios con un solo clic. 📄✨"</p>
          </div>
        </div>
      </div>

      {/* Upload Area */}
      <div className="upload-section">
        <div className="upload-area">
          <span className="upload-icon ☁️">☁️</span>
          <h3>Arrastra tus archivos aquí o haz clic para examinar</h3>
          <p>Soporta PDF, Word, PPTX, MP3, PNG, JPG, ZIP y más (Máx 100 MB).</p>
        </div>
      </div>

      {/* Folders */}
      <div className="folders-section">
        <div className="section-header">
          <h3>Mis Carpetas</h3>
        </div>
        <div className="folders-grid">
          {folders.map((folder) => (
            <div key={folder.id} className="folder-card">
              <span className="folder-icon">{folder.icon}</span>
              <div className="folder-info">
                <h4>{folder.name}</h4>
                <span className="folder-count">{folder.count}</span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Recent Files */}
      <div className="files-section">
        <div className="section-header">
          <h3>Archivos Recientes</h3>
          <span className="files-count">5 archivos mostrados</span>
        </div>
        <div className="files-list">
          {recentFiles.map((file) => (
            <div key={file.id} className="file-card">
              <span className="file-icon">{file.icon}</span>
              <div className="file-info">
                <h4>{file.name}</h4>
                <div className="file-meta">
                  <span>{file.type}</span>
                  <span>•</span>
                  <span>{file.size}</span>
                  <span>•</span>
                  <span>{file.date}</span>
                </div>
              </div>
              <div className="file-actions">
                <button className="file-action-btn">📤 Compartir</button>
                <button className="file-action-btn ai">{getAIAction(file)}</button>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Storage */}
      <div className="storage-section">
        <div className="storage-card">
          <span className="storage-icon">☁️</span>
          <div className="storage-info">
            <h3>Almacenamiento</h3>
            <div className="storage-progress">
              <div className="progress-bar">
                <div className="progress-fill" style={{ width: `${storage.percentage}%` }}></div>
              </div>
              <span className="storage-text">{storage.used} GB / {storage.total} GB</span>
            </div>
            <p className="storage-message">{storage.percentage}% usado. Espacio suficiente para tus cursos y proyectos.</p>
          </div>
        </div>
      </div>

      {/* AI Tools */}
      <div className="ai-tools-section">
        <div className="section-header">
          <h3>🤖 Herramientas de IA con Amigis</h3>
        </div>
        <div className="ai-tools-grid">
          {aiTools.map((tool) => (
            <div key={tool.id} className="ai-tool-card">
              <span className="tool-icon">{tool.icon}</span>
              <span className="tool-name">{tool.name}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Files;
