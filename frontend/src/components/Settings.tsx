import React, { useState } from 'react';
import './Settings.css';

const Settings: React.FC = () => {
  const [activeTab, setActiveTab] = useState('General');
  const [screenMode, setScreenMode] = useState('Oscuro');
  const [primaryColor, setPrimaryColor] = useState('#667eea');

  const tabs = [
    { id: 'General', icon: '⚙️' },
    { id: 'Mi Perfil', icon: '👤' },
    { id: 'Apariencia', icon: '🎨' },
    { id: 'Personalizar Amigis', icon: '🦆' },
    { id: 'Mi Espacio', icon: '🌌' },
  ];

  const screenModes = [
    { id: 'Oscuro', icon: '🌙', label: 'Oscuro' },
    { id: 'Claro', icon: '🌞', label: 'Claro' },
    { id: 'Sistema', icon: '💻', label: 'Sistema' },
  ];

  const colors = [
    { id: '#667eea', name: 'Purple' },
    { id: '#f093fb', name: 'Pink' },
    { id: '#11998e', name: 'Green' },
    { id: '#f5576c', name: 'Red' },
    { id: '#4facfe', name: 'Blue' },
    { id: '#fa709a', name: 'Rose' },
  ];

  return (
    <div className="settings-container">
      <div className="settings-header">
        <div className="header-title">
          <span className="header-icon">⚙️</span>
          <div>
            <h1>Configuración</h1>
            <p>Personaliza cada aspecto de tu experiencia con Amigis.</p>
          </div>
        </div>
        <div className="header-actions">
          <button className="action-btn secondary">🔄 Restaurar</button>
          <button className="action-btn primary">💾 Guardar Cambios</button>
        </div>
      </div>

      {/* User Info */}
      <div className="user-info-section">
        <div className="user-card">
          <div className="user-avatar">M</div>
          <div className="user-details">
            <h2>mariajosetacoc2005</h2>
            <span className="user-email">mariajosetacoc2005@gmail.com</span>
            <span className="verified-badge">✅ Cuenta verificada</span>
          </div>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="tabs-section">
        <div className="tabs-grid">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              className={`tab-btn ${activeTab === tab.id ? 'active' : ''}`}
              onClick={() => setActiveTab(tab.id)}
            >
              <span className="tab-icon">{tab.icon}</span>
              <span className="tab-label">{tab.id}</span>
            </button>
          ))}
        </div>
      </div>

      {/* Settings Content */}
      <div className="settings-content">
        {activeTab === 'General' && (
          <div className="settings-panel">
            <h3>Configuración de MiniAmigixV</h3>
            
            {/* Screen Mode */}
            <div className="setting-group">
              <label className="setting-label">🌙 Modo de Pantalla</label>
              <div className="screen-modes">
                {screenModes.map((mode) => (
                  <button
                    key={mode.id}
                    className={`mode-btn ${screenMode === mode.id ? 'active' : ''}`}
                    onClick={() => setScreenMode(mode.id)}
                  >
                    <span className="mode-icon">{mode.icon}</span>
                    <span className="mode-label">{mode.label}</span>
                  </button>
                ))}
              </div>
            </div>

            {/* Primary Color */}
            <div className="setting-group">
              <label className="setting-label">🎨 Color Principal</label>
              <div className="color-picker">
                {colors.map((color) => (
                  <button
                    key={color.id}
                    className={`color-btn ${primaryColor === color.id ? 'active' : ''}`}
                    onClick={() => setPrimaryColor(color.id)}
                    style={{ backgroundColor: color.id }}
                    title={color.name}
                  >
                    {primaryColor === color.id && <span className="check-icon">✓</span>}
                  </button>
                ))}
              </div>
            </div>
          </div>
        )}

        {activeTab === 'Mi Perfil' && (
          <div className="settings-panel">
            <div className="profile-header">
              <div className="profile-avatar">📷</div>
              <div className="profile-info">
                <h2>mariajosetacoc2005</h2>
                <span className="profile-email">mariajosetacoc2005@gmail.com</span>
                <span className="verified-badge">✅ Cuenta verificada</span>
              </div>
            </div>

            <h3>👤 Información Personal</h3>
            
            <div className="form-group">
              <label>Nombre de usuario</label>
              <input type="text" defaultValue="mariajosetacoc2005" />
            </div>

            <div className="form-group">
              <label>Correo electrónico</label>
              <input type="email" defaultValue="mariajosetacoc2005@gmail.com" />
            </div>

            <div className="form-group">
              <label>Biografía</label>
              <textarea placeholder="Cuéntanos algo sobre ti..." rows={3} />
            </div>

            <div className="form-group">
              <label>País</label>
              <select defaultValue="Ecuador">
                <option>Ecuador</option>
                <option>Argentina</option>
                <option>Colombia</option>
                <option>México</option>
                <option>España</option>
                <option>Chile</option>
                <option>Perú</option>
                <option>Otro</option>
              </select>
            </div>

            <div className="form-group">
              <label>Fecha de nacimiento</label>
              <input type="date" />
            </div>

            <button className="action-btn primary">💾 Guardar Perfil</button>
          </div>
        )}

        {activeTab === 'Apariencia' && (
          <div className="settings-panel">
            <h3>🎨 Apariencia</h3>
            <p>Personaliza el aspecto visual de MiniAmigixV.</p>
            
            <div className="setting-group">
              <label className="setting-label">🌙 Modo de Pantalla</label>
              <div className="screen-modes">
                {screenModes.map((mode) => (
                  <button
                    key={mode.id}
                    className={`mode-btn ${screenMode === mode.id ? 'active' : ''}`}
                    onClick={() => setScreenMode(mode.id)}
                  >
                    <span className="mode-icon">{mode.icon}</span>
                    <span className="mode-label">{mode.label}</span>
                  </button>
                ))}
              </div>
            </div>

            <div className="setting-group">
              <label className="setting-label">🎨 Color Principal</label>
              <div className="color-picker">
                {colors.map((color) => (
                  <button
                    key={color.id}
                    className={`color-btn ${primaryColor === color.id ? 'active' : ''}`}
                    onClick={() => setPrimaryColor(color.id)}
                    style={{ backgroundColor: color.id }}
                    title={color.name}
                  >
                    {primaryColor === color.id && <span className="check-icon">✓</span>}
                  </button>
                ))}
              </div>
            </div>
          </div>
        )}

        {activeTab === 'Personalizar Amigis' && (
          <div className="settings-panel">
            <h3>🦆 Personalizar Amigis</h3>
            <p>Personaliza tu mascota Amigis con accesorios y colores.</p>
            
            <div className="amigis-preview">
              <span className="amigis-avatar">🦆</span>
              <p>Amigis Nivel 12</p>
            </div>

            <div className="setting-group">
              <label className="setting-label">Accesorios</label>
              <div className="accessories-grid">
                <button className="accessory-btn active">👕 Gorra</button>
                <button className="accessory-btn active">🎧 Audífonos DJ</button>
                <button className="accessory-btn active">🎒 Mochila</button>
                <button className="accessory-btn">👓 Gafas</button>
                <button className="accessory-btn">🎩 Sombrero</button>
                <button className="accessory-btn">🧣 Bufanda</button>
              </div>
            </div>

            <button className="action-btn primary">💾 Guardar Cambios</button>
          </div>
        )}

        {activeTab === 'Mi Espacio' && (
          <div className="settings-panel">
            <h3>🌌 Mi Espacio</h3>
            <p>Configura tu espacio personal en MiniAmigixV.</p>
            
            <div className="setting-group">
              <label className="setting-label">Fondo de Pantalla</label>
              <div className="wallpaper-grid">
                <button className="wallpaper-btn active">🌌 Espacio</button>
                <button className="wallpaper-btn">🌅 Amanecer</button>
                <button className="wallpaper-btn">🌊 Océano</button>
                <button className="wallpaper-btn">🏔️ Montañas</button>
                <button className="wallpaper-btn">🌸 Sakura</button>
                <button className="wallpaper-btn">🎨 Abstracto</button>
              </div>
            </div>

            <button className="action-btn primary">💾 Guardar Cambios</button>
          </div>
        )}
      </div>
    </div>
  );
};

export default Settings;
