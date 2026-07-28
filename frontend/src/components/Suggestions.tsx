import React, { useState } from 'react';
import './Suggestions.css';

const Suggestions: React.FC = () => {
  const [activeFilter, setActiveFilter] = useState('Todas');
  const [searchQuery, setSearchQuery] = useState('');

  const filters = [
    { id: 'Todas', label: 'Todas' },
    { id: 'Pendientes', label: 'Pendientes' },
    { id: 'En Revisión', label: 'En Revisión' },
    { id: 'Aprobadas', label: 'Aprobadas' },
    { id: 'Rechazadas', label: 'Rechazadas' },
  ];

  const stats = [
    { icon: '📊', label: 'Total', value: 0 },
    { icon: '⏳', label: 'Pendientes', value: 0 },
    { icon: '✅', label: 'Aprobadas', value: 0 },
  ];

  return (
    <div className="suggestions-container">
      <div className="suggestions-header">
        <div className="header-title">
          <span className="header-icon">💬</span>
          <div>
            <h1>Sugerencias</h1>
            <p>Comparte tus ideas para mejorar MiniAmigixV</p>
          </div>
        </div>
        <button className="action-btn primary">Nueva Sugerencia</button>
      </div>

      {/* Permission Message */}
      <div className="permission-message">
        <span className="permission-icon">ℹ️</span>
        <p>Solo puedes ver tus propias sugerencias. El administrador puede ver todas las sugerencias.</p>
      </div>

      {/* Stats */}
      <div className="stats-grid">
        {stats.map((stat) => (
          <div key={stat.label} className="stat-card">
            <span className="stat-icon">{stat.icon}</span>
            <div className="stat-info">
              <span className="stat-value">{stat.value}</span>
              <span className="stat-label">{stat.label}</span>
            </div>
          </div>
        ))}
      </div>

      {/* Filters */}
      <div className="filters-section">
        <div className="filters-grid">
          {filters.map((filter) => (
            <button
              key={filter.id}
              className={`filter-btn ${activeFilter === filter.id ? 'active' : ''}`}
              onClick={() => setActiveFilter(filter.id)}
            >
              {filter.label}
            </button>
          ))}
        </div>
      </div>

      {/* Search */}
      <div className="search-section">
        <div className="search-bar">
          <span className="search-icon">🔍</span>
          <input
            type="text"
            placeholder="Buscar sugerencias..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
        </div>
      </div>

      {/* Empty State */}
      <div className="empty-state">
        <span className="empty-icon">💬</span>
        <h3>No tienes sugerencias creadas</h3>
        <p>¡Comparte tus ideas para mejorar MiniAmigixV! Como usuario normal, solo puedes ver tus propias sugerencias.</p>
        <button className="action-btn primary">Crear mi primera sugerencia</button>
      </div>
    </div>
  );
};

export default Suggestions;
