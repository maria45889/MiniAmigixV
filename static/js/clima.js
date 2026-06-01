document.addEventListener('DOMContentLoaded', () => {
    console.log("🌤️ MiniAmigixV Clima: Online");
    
    // DOM Elements
    const weatherForm = document.getElementById('weather-search-form');
    const cityInput = document.getElementById('city-input');
    const loadingIndicator = document.getElementById('loading-indicator');
    const weatherResults = document.getElementById('weather-results');
    const weatherLocation = document.getElementById('weather-location');
    const weatherIcon = document.getElementById('weather-icon');
    const weatherTemperature = document.getElementById('weather-temperature');
    const weatherDescription = document.getElementById('weather-description');
    const humidityValue = document.getElementById('humidity-value');
    const windValue = document.getElementById('wind-value');
    const pressureValue = document.getElementById('pressure-value');
    const visibilityValue = document.getElementById('visibility-value');
    const recommendationText = document.getElementById('recommendation-text');
    const forecastContainer = document.getElementById('forecast-container');
    const citySuggestions = document.getElementById('city-suggestions');
    const weatherAlertsContainer = document.getElementById('weather-alerts');
    const radarVisual = document.getElementById('radar-visual');
    const radarStatus = document.getElementById('radar-status');
    const radarInfo = document.getElementById('radar-info');
    const WEATHER_PROXY_URL = '/api/clima/';

    // Simulated data definitions for offline demo mode
    const mockData = {
        'quito': {
            name: 'Quito',
            country: 'EC',
            temp: 15,
            feels_like: 14,
            humidity: 78,
            pressure: 1015,
            wind_speed: 3.2,
            visibility: 10000,
            description: 'parcialmente nublado',
            icon: '02d',
            sunrise: 1622505600,
            sunset: 1622548800
        },
        'guayaquil': {
            name: 'Guayaquil',
            country: 'EC',
            temp: 28,
            feels_like: 31,
            humidity: 82,
            pressure: 1010,
            wind_speed: 4.5,
            visibility: 8000,
            description: 'lluvioso',
            icon: '09d',
            sunrise: 1622505600,
            sunset: 1622548800
        },
        'madrid': {
            name: 'Madrid',
            country: 'ES',
            temp: 24,
            feels_like: 25,
            humidity: 45,
            pressure: 1018,
            wind_speed: 2.1,
            visibility: 15000,
            description: 'despejado',
            icon: '01d',
            sunrise: 1622505600,
            sunset: 1622548800
        },
        'london': {
            name: 'London',
            country: 'GB',
            temp: 18,
            feels_like: 17,
            humidity: 72,
            pressure: 1012,
            wind_speed: 5.3,
            visibility: 12000,
            description: 'nublado',
            icon: '04d',
            sunrise: 1622505600,
            sunset: 1622548800
        }
    };

    // Initialize
    if (weatherResults) {
        weatherResults.style.display = 'none';
    }
    
    // Event Listeners
    weatherForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const city = cityInput.value.trim();
        if (city) {
            fetchWeatherData(city);
        }
    });
    
    // Allow Enter key to submit
    cityInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            e.preventDefault();
            weatherForm.dispatchEvent(new Event('submit'));
        }
    });

    // Autocomplete / suggestions (debounced)
    let suggestTimer = null;
    cityInput.addEventListener('input', (e) => {
        const q = e.target.value.trim();
        if (suggestTimer) clearTimeout(suggestTimer);
        if (!q) {
            citySuggestions.innerHTML = '';
            citySuggestions.setAttribute('aria-hidden', 'true');
            return;
        }
        suggestTimer = setTimeout(() => {
            fetchCitySuggestions(q);
        }, 300);
    });
    
    // Fetch weather data from API
    async function fetchWeatherData(city) {
        showLoading();
        
        try {
            let weatherData = null;
            try {
                weatherData = await fetchWeatherProxy(city);
            } catch (e) {
                console.warn('Proxy weather fetch failed, falling back to simulated data', e);
                weatherData = await fetchSimulatedWeatherData(city);
            }
            
            if (weatherData) {
                displayWeatherData(weatherData);
                displayForecast(weatherData.forecast);
                if (weatherResults) {
                    weatherResults.style.display = 'block';
                }
            } else {
                showError('No se pudo obtener el clima para esa ubicación. Por favor, inténtelo de nuevo.');
            }
        } catch (error) {
            console.error('Error fetching weather data:', error);
            showError('Error al conectar con el servicio del clima. Por favor, inténtelo de nuevo más tarde.');
        } finally {
            hideLoading();
        }
    }

    async function fetchWeatherProxy(query) {
        const url = `${WEATHER_PROXY_URL}?q=${encodeURIComponent(query)}`;
        const response = await fetch(url);
        if (!response.ok) {
            const body = await response.json().catch(() => ({}));
            throw new Error(body.error || 'Proxy request failed');
        }
        const data = await response.json();
        if (data.error) {
            throw new Error(data.error);
        }
        return data;
    }

    // Simulated weather data function (replace with actual API call in production)
    async function fetchSimulatedWeatherData(city) {
        // Simulate network delay
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        // Try to find exact match first
        const cityKey = city.toLowerCase().trim();
        if (mockData[cityKey]) {
            return {
                ...mockData[cityKey],
                forecast: generateForecastData(cityKey)
            };
        }
        
        // If not found, generate generic data based on the city name
        return generateGenericWeatherData(city);
    }
    
    // Generate forecast data
    function generateForecastData(cityKey) {
        const forecast = [];
        const baseTemp = mockData[cityKey] ? mockData[cityKey].temp : 20;
        
        for (let i = 0; i < 5; i++) {
            const dayTemp = baseTemp + (Math.random() - 0.5) * 5; // ±2.5°C variation
            const description = getRandomDescription();
            forecast.push({
                day: getDayName(i),
                date: getDateString(i),
                temp_min: Math.floor(dayTemp - 3),
                temp_max: Math.ceil(dayTemp + 3),
                description,
                icon: getRandomIcon(),
                rain: description.includes('lluv') || description.includes('tormenta') ? Math.floor(Math.random() * 15) + 5 : 0
            });
        }
        return forecast;
    }
    
    // Generate generic weather data for unknown cities
    function generateGenericWeatherData(city) {
        const temp = Math.floor(Math.random() * 20) + 10; // 10-30°C
        const descriptions = ['despejado', 'parcialmente nublado', 'nublado', 'lluvioso', 'tormenta'];
        const description = descriptions[Math.floor(Math.random() * descriptions.length)];
        
        return {
            name: city,
            country: '??',
            temp: temp,
            feels_like: temp + Math.floor(Math.random() * 4) - 2,
            humidity: Math.floor(Math.random() * 50) + 40, // 40-90%
            pressure: Math.floor(Math.random() * 30) + 1000, // 1000-1030 hPa
            wind_speed: Math.floor(Math.random() * 10) + 1, // 1-10 km/h
            visibility: Math.floor(Math.random() * 10) + 5, // 5-15 km * 1000
            description: description,
            icon: getIconFromDescription(description),
            rain: description.includes('lluv') || description.includes('tormenta') ? Math.floor(Math.random() * 15) + 5 : 0,
            sunrise: Date.now() / 1000 - 3600,
            sunset: Date.now() / 1000 + 3600,
            forecast: generateForecastData('')
        };
    }
    
    // Helper functions
    function getDayName(offset) {
        const days = ['Dom', 'Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb'];
        const today = new Date().getDay();
        return days[(today + offset) % 7];
    }
    
    function getDateString(offset) {
        const date = new Date();
        date.setDate(date.getDate() + offset);
        return date.toLocaleDateString('es-ES', { month: 'short', day: 'numeric' });
    }
    
    function getRandomDescription() {
        const descriptions = ['despejado', 'parcialmente nublado', 'nublado', 'lluvioso', 'tormenta'];
        return descriptions[Math.floor(Math.random() * descriptions.length)];
    }
    
    function getRandomIcon() {
        const icons = ['01d', '02d', '03d', '04d', '09d', '10d', '11d', '13d', '50d'];
        return icons[Math.floor(Math.random() * icons.length)];
    }
    
    function getIconFromDescription(description) {
        const iconMap = {
            'despejado': '01d',
            'parcialmente nublado': '02d',
            'nublado': '04d',
            'lluvioso': '09d',
            'tormenta': '11d'
        };
        return iconMap[description] || '01d';
    }
    
    // Display weather data
    function displayWeatherData(data) {
        // Reset any previous error style
        if (recommendationText) {
            recommendationText.style.color = '';
        }

        // Location
        weatherLocation.textContent = `${data.name}, ${data.country}`;
        
        // Temperature
        weatherTemperature.textContent = `${data.temp}°C`;
        
        // Description
        weatherDescription.textContent = capitalizeFirstLetter(data.description);
        
        // Icon
        weatherIcon.innerHTML = getWeatherIconHTML(data.icon, data.description);

        updateRadar(data);
        
        // Details
        humidityValue.textContent = `${data.humidity}%`;
        windValue.textContent = `${Math.round(data.wind_speed * 3.6)} km/h`; // Convert m/s to km/h
        pressureValue.textContent = `${data.pressure} hPa`;
        visibilityValue.textContent = `${data.visibility / 1000} km`;
        
        // Recommendations
        displayRecommendations(data);
    }
    
    // Display forecast
    function displayForecast(forecastData) {
        forecastContainer.innerHTML = '';
        
        forecastData.forEach(day => {
            const forecastDay = document.createElement('div');
            forecastDay.className = 'forecast-day';
            
            forecastDay.innerHTML = `
                <div class="day-name">${day.day}</div>
                <div class="day-date">${day.date}</div>
                <div class="forecast-icon">${getWeatherIconHTML(day.icon, day.description)}</div>
                <div class="forecast-desc">${capitalizeFirstLetter(day.description)}</div>
                <div class="forecast-temp">
                    <span>${day.temp_min}°</span>
                    <span>${day.temp_max}°</span>
                </div>
            `;
            
            forecastContainer.appendChild(forecastDay);
        });
    }

    // Update simulated radar values based on current weather
    function updateRadar(data) {
        if (!radarStatus || !radarInfo) return;

        const anomaly = calculateAnomalyScore(data);
        radarStatus.textContent = `${anomaly.toFixed(2)}%`;

        if (anomaly > 0.12) {
            radarInfo.textContent = 'Riesgo alto: lluvia y tormentas en el pronóstico';
        } else if (anomaly > 0.08) {
            radarInfo.textContent = 'Anomalía detectada: condiciones inestables';
        } else {
            radarInfo.textContent = 'Sistema estable';
        }

        if (radarVisual) {
            radarVisual.classList.toggle('radar-alert', anomaly > 0.08);
        }
    }

    function calculateAnomalyScore(data) {
        if (!data) return 0.04;

        let score = 0.03;
        if (data.temp >= 30) score += 0.02;
        if (data.humidity >= 70) score += 0.015;
        if (data.wind_speed >= 6) score += 0.01;
        if (/(lluv|tormenta|nublado|nieve)/i.test(data.description)) score += 0.02;
        if (data.rain > 0) score += Math.min(0.02, data.rain / 10);

        const forecast = data.forecast || [];
        forecast.forEach(day => {
            if (day.rain > 0) {
                score += 0.015 + Math.min(0.02, day.rain / 10);
            }
            if (/(lluv|tormenta|nieve)/i.test(day.description)) {
                score += 0.01;
            }
            if (day.temp_max >= 30) {
                score += 0.008;
            }
        });

        score += Math.random() * 0.01;
        return Math.min(0.25, Math.max(0.03, score));
    }

    // City suggestions via simple common cities fallback
    async function fetchCitySuggestions(query) {
        citySuggestions.setAttribute('aria-hidden', 'false');
        citySuggestions.innerHTML = '<div class="suggesting">Buscando...</div>';

        const common = ['Quito, EC','Guayaquil, EC','Cuenca, EC','Madrid, ES','Paris, FR','London, GB','New York, US','Tokyo, JP','Sydney, AU'];
        const filtered = common.filter(c => c.toLowerCase().includes(query.toLowerCase())).slice(0,6);
        renderCitySuggestions(filtered.map(c => ({ name: c.split(',')[0], country: c.split(',')[1] })), query);
    }

    function renderCitySuggestions(items, query) {
        if (!items || items.length === 0) {
            citySuggestions.innerHTML = '<div class="no-suggestions">Sin resultados</div>';
            return;
        }
        citySuggestions.innerHTML = items.map(it => {
            const label = it.state ? `${it.name}, ${it.state}, ${it.country || ''}` : `${it.name}${it.country ? ', '+it.country : ''}`;
            return `<button type="button" class="suggestion-item">${label}</button>`;
        }).join('');

        // add click handlers
        citySuggestions.querySelectorAll('.suggestion-item').forEach(btn => {
            btn.addEventListener('click', () => {
                cityInput.value = btn.textContent;
                citySuggestions.innerHTML = '';
                citySuggestions.setAttribute('aria-hidden', 'true');
                weatherForm.dispatchEvent(new Event('submit'));
            });
        });
    }
    
    // Get weather icon HTML
    function getWeatherIconHTML(iconCode, description) {
        // In a real app, we would use the OpenWeatherMap icon URL:
        // return `<img src="https://openweathermap.org/img/wn/${iconCode}@2x.png" alt="${description}">`;
        
        // For this demo, we'll use material icons with color coding
        const iconMap = {
            '01d': { icon: 'wb_sunny', color: '#ffeb3b' }, // clear sky day
            '01n': { icon: 'wb_sunny', color: '#ffeb3b' }, // clear sky night
            '02d': { icon: 'white_balance_sunny', color: '#ffeb3b' }, // few clouds day
            '02n': { icon: 'white_balance_sunny', color: '#ffeb3b' }, // few clouds night
            '03d': { icon: 'cloud', color: '#90a4ae' }, // scattered clouds
            '04d': { icon: 'cloud', color: '#90a4ae' }, // broken clouds
            '09d': { icon: 'grain', color: '#4fc3f7' }, // shower rain
            '10d': { icon: 'umbrella', color: '#4fc3f7' }, // rain day
            '10n': { icon: 'umbrella', color: '#4fc3f7' }, // rain night
            '11d': { icon: 'flash_on', color: '#ff9800' }, // thunderstorm
            '13d': { icon: 'ac_unit', color: '#ffffff' }, // snow
            '50d': { icon: 'opacity', color: '#90a4ae' } // mist
        };
        
        const iconData = iconMap[iconCode] || { icon: 'wb_sunny', color: '#ffeb3b' };
        return `<span class="material-icons-round" style="color: ${iconData.color}; font-size: 2rem;">${iconData.icon}</span>`;
    }
    
    // Display recommendations based on weather
    function displayRecommendations(data) {
        let recommendations = [];
        
        // Temperature-based recommendations
        if (data.temp >= 30) {
            recommendations.push('Usa protector solar y mantén hidratación adecuada');
            recommendations.push('Evita la exposición prolongada al sol directo');
        } else if (data.temp >= 25) {
            recommendations.push('El clima está cálido, considera usar protector solar ligero');
        } else if (data.temp <= 5) {
            recommendations.push('Abrígate bien, hace mucho frío');
            recommendations.push('Considera usar gorro, guantes y bufanda');
        } else if (data.temp <= 10) {
            recommendations.push('Hace frío, usa ropa abrigada');
        }
        
        // Precipitation-based recommendations
        if (data.description.includes('lluvia') || data.description.includes('lluvioso') || 
            data.description.includes('tormenta')) {
            recommendations.push('Lleva un paraguas o impermeable');
            recommendations.push('Evita actividades al aire libre si es posible');
            recommendations.push('Conduce con precaución, las calles pueden estar resbaladizas');
        }
        
        // Wind-based recommendations
        if (data.wind_speed > 8) { // > 8 m/s (~29 km/h)
            recommendations.push('Hay viento fuerte, asegura objetos sueltos al aire libre');
        }
        
        // UV index simulation (based on time of day and temperature)
        const hour = new Date().getHours();
        if (hour >= 10 && hour <= 16 && data.temp >= 20) {
            recommendations.push('El índice UV es alto, usa protector solar incluso en días nublados');
        }
        
        // Humidity recommendations
        if (data.humidity > 80) {
            recommendations.push('La humedad es alta, puede sensación de bochorno');
        } else if (data.humidity < 30) {
            recommendations.push('El aire está seco, considera usar humidificador si estás en interiores');
        }
        
        // Display recommendations
        if (recommendations.length > 0) {
            recommendationText.innerHTML = recommendations.map(rec => `• ${rec}`).join('<br>');
        } else {
            recommendationText.textContent = 'Las condiciones son óptimas para actividades al aire libre';
        }
    }
    
    // Show loading indicator
    function showLoading() {
        if (loadingIndicator) {
            loadingIndicator.style.display = 'flex';
        }
        if (weatherResults) {
            weatherResults.style.display = 'none';
        }
        if (cityInput) {
            cityInput.disabled = true;
        }
    }
    
    // Hide loading indicator
    function hideLoading() {
        if (loadingIndicator) {
            loadingIndicator.style.display = 'none';
        }
        if (cityInput) {
            cityInput.disabled = false;
        }
    }
    
    // Show error message
    function showError(message) {
        if (recommendationText) {
            recommendationText.textContent = message;
            recommendationText.style.color = '#ff5722';
        }
        // Clear other data
        if (weatherLocation) weatherLocation.textContent = '--';
        if (weatherTemperature) weatherTemperature.textContent = '--°C';
        if (weatherDescription) weatherDescription.textContent = '--';
        if (weatherIcon) weatherIcon.innerHTML = '<span class="material-icons-round">error</span>';
        if (humidityValue) humidityValue.textContent = '--%';
        if (windValue) windValue.textContent = '-- km/h';
        if (pressureValue) pressureValue.textContent = '-- hPa';
        if (visibilityValue) visibilityValue.textContent = '-- km';
        if (forecastContainer) forecastContainer.innerHTML = '<div class="forecast-placeholder"><p>Error al cargar el pronóstico</p></div>';
        if (weatherResults) {
            weatherResults.style.display = 'block';
        }

        updateRadar(null);
    }
    
    // Helper function to capitalize first letter
    function capitalizeFirstLetter(string) {
        return string.charAt(0).toUpperCase() + string.slice(1);
    }
    
    // Add some visual flair to the input on focus
    cityInput.addEventListener('focus', () => {
        cityInput.style.boxShadow = '0 0 0 2px rgba(0, 240, 255, 0.2)';
    });
    
    cityInput.addEventListener('blur', () => {
        cityInput.style.boxShadow = 'none';
    });
    
    console.log("🌤️ Clima module initialized");
});