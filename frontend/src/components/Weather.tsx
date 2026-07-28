import React, { useState } from 'react';
import './Weather.css';

interface WeatherData {
  city: string;
  country: string;
  temperature: number;
  condition: string;
  icon: string;
  humidity: number;
  wind: number;
  visibility: number;
  uvIndex: number;
  sunrise: string;
  sunset: string;
  message: string;
}

interface HourlyForecast {
  time: string;
  icon: string;
  temperature: number;
}

interface DailyForecast {
  day: string;
  icon: string;
  high: number;
  low: number;
}

interface FavoriteCity {
  name: string;
  country: string;
}

const Weather: React.FC = () => {
  const [selectedCity, setSelectedCity] = useState('Quito');
  const [searchQuery, setSearchQuery] = useState('');

  const favoriteCities: FavoriteCity[] = [
    { name: 'Quito', country: 'Ecuador' },
    { name: 'Guayaquil', country: 'Ecuador' },
    { name: 'Cuenca', country: 'Ecuador' },
    { name: 'Loja', country: 'Ecuador' },
    { name: 'Tokio', country: 'Japón' },
    { name: 'Madrid', country: 'España' },
  ];

  const currentWeather: WeatherData = {
    city: 'Quito',
    country: 'Ecuador',
    temperature: 22,
    condition: 'Chubascos ligeros',
    icon: '🌤',
    humidity: 94,
    wind: 7,
    visibility: 10,
    uvIndex: 5,
    sunrise: '06:12',
    sunset: '18:25',
    message: 'Hoy hace 22°C. No necesitas paraguas. 😊'
  };

  const hourlyForecast: HourlyForecast[] = [
    { time: '09:00', icon: '☀️', temperature: 19 },
    { time: '12:00', icon: '🌤', temperature: 22 },
    { time: '15:00', icon: '☁️', temperature: 21 },
    { time: '18:00', icon: '🌙', temperature: 17 },
    { time: '21:00', icon: '🌙', temperature: 15 },
  ];

  const dailyForecast: DailyForecast[] = [
    { day: 'Hoy', icon: '🌦', high: 21, low: 9 },
    { day: 'Lun', icon: '🌦', high: 21, low: 9 },
    { day: 'Mar', icon: '☁️', high: 21, low: 8 },
    { day: 'Mié', icon: '🌦', high: 21, low: 9 },
    { day: 'Jue', icon: '☁️', high: 19, low: 9 },
    { day: 'Vie', icon: '☁️', high: 21, low: 10 },
    { day: 'Sáb', icon: '☁️', high: 20, low: 9 },
  ];

  const handleCitySelect = (city: string) => {
    setSelectedCity(city);
  };

  const handleSearch = () => {
    if (searchQuery.trim()) {
      setSelectedCity(searchQuery);
      setSearchQuery('');
    }
  };

  return (
    <div className="weather-container">
      <div className="weather-header">
        <div className="header-title">
          <span className="header-icon">🌤</span>
          <div>
            <h1>Clima & Atmósfera</h1>
            <p>Pronóstico meteorológico en tiempo real para cualquier ciudad del mundo.</p>
          </div>
        </div>
      </div>

      {/* Search and Favorites */}
      <div className="search-section">
        <div className="search-bar">
          <input
            type="text"
            placeholder="Buscar ciudad..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
          />
          <button className="search-btn" onClick={handleSearch}>Buscar</button>
        </div>
        <div className="favorites-section">
          <span className="favorites-label">⭐ FAVORITAS:</span>
          <div className="favorites-list">
            {favoriteCities.map((city) => (
              <button
                key={city.name}
                className={`favorite-city ${selectedCity === city.name ? 'active' : ''}`}
                onClick={() => handleCitySelect(city.name)}
              >
                📍 {city.name}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Current Weather */}
      <div className="current-weather">
        <div className="weather-main">
          <div className="weather-location">
            <span className="location-icon">📍</span>
            <div>
              <h2>{currentWeather.city}, {currentWeather.country}</h2>
              <p className="current-temp">{currentWeather.temperature}°C</p>
            </div>
          </div>
          <div className="weather-condition">
            <span className="weather-icon-large">{currentWeather.icon}</span>
            <p className="condition-text">{currentWeather.condition}</p>
          </div>
        </div>
        <div className="weather-message">
          <span className="message-icon">🐥</span>
          <p>{currentWeather.message}</p>
        </div>
      </div>

      {/* Weather Details Grid */}
      <div className="weather-details">
        <div className="detail-card">
          <span className="detail-icon">🌡️</span>
          <div className="detail-info">
            <span className="detail-value">{currentWeather.temperature}°C</span>
            <span className="detail-label">Temperatura</span>
          </div>
        </div>
        <div className="detail-card">
          <span className="detail-icon">💧</span>
          <div className="detail-info">
            <span className="detail-value">{currentWeather.humidity}%</span>
            <span className="detail-label">Humedad</span>
          </div>
        </div>
        <div className="detail-card">
          <span className="detail-icon">🌬️</span>
          <div className="detail-info">
            <span className="detail-value">{currentWeather.wind} km/h</span>
            <span className="detail-label">Viento</span>
          </div>
        </div>
        <div className="detail-card">
          <span className="detail-icon">👁️</span>
          <div className="detail-info">
            <span className="detail-value">{currentWeather.visibility} km</span>
            <span className="detail-label">Visibilidad</span>
          </div>
        </div>
        <div className="detail-card">
          <span className="detail-icon">☀️</span>
          <div className="detail-info">
            <span className="detail-value">UV {currentWeather.uvIndex}</span>
            <span className="detail-label">Índice UV</span>
          </div>
        </div>
        <div className="detail-card">
          <span className="detail-icon">🌅</span>
          <div className="detail-info">
            <span className="detail-value">{currentWeather.sunrise}</span>
            <span className="detail-label">Amanecer</span>
          </div>
        </div>
        <div className="detail-card">
          <span className="detail-icon">🌇</span>
          <div className="detail-info">
            <span className="detail-value">{currentWeather.sunset}</span>
            <span className="detail-label">Atardecer</span>
          </div>
        </div>
      </div>

      {/* Hourly Forecast */}
      <div className="forecast-section">
        <div className="section-header">
          <h3>⏰ Pronóstico por Horas</h3>
        </div>
        <div className="hourly-forecast">
          {hourlyForecast.map((hour) => (
            <div key={hour.time} className="hourly-item">
              <span className="hour-time">{hour.time}</span>
              <span className="hour-icon">{hour.icon}</span>
              <span className="hour-temp">{hour.temperature}°</span>
            </div>
          ))}
        </div>
      </div>

      {/* 7-Day Forecast */}
      <div className="forecast-section">
        <div className="section-header">
          <h3>📅 Pronóstico de 7 Días</h3>
        </div>
        <div className="daily-forecast">
          {dailyForecast.map((day) => (
            <div key={day.day} className="daily-item">
              <span className="day-name">{day.day}</span>
              <span className="day-icon">{day.icon}</span>
              <div className="day-temps">
                <span className="day-high">{day.high}°</span>
                <span className="day-low">{day.low}°</span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Environmental Indices */}
      <div className="indices-section">
        <div className="section-header">
          <h3>📊 Índices Ambientales</h3>
        </div>
        <div className="indices-grid">
          <div className="index-card">
            <div className="index-header">
              <span className="index-icon">🌞</span>
              <span className="index-title">Índice UV</span>
            </div>
            <div className="index-value">Moderado (4/11)</div>
            <div className="index-status">Protección</div>
          </div>
          <div className="index-card">
            <div className="index-header">
              <span className="index-icon">🌫</span>
              <span className="index-title">Calidad del Aire</span>
            </div>
            <div className="index-value">32 AQI — Excelente</div>
            <div className="index-status">Excelente</div>
          </div>
          <div className="index-card">
            <div className="index-header">
              <span className="index-icon">⚡</span>
              <span className="index-title">Prob. Tormenta</span>
            </div>
            <div className="index-value">15% esta tarde</div>
            <div className="index-status">Baja</div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Weather;
