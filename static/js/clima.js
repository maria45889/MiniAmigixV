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
    
    // API Key (in a real app, this would be stored securely on the backend)
    const API_KEY = 'your_openweathermap_api_key_here'; // Replace with actual key or use backend proxy
    
    // Initialize
    weatherResults.style.display = 'none';
    
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
            // Prefer a real API call if API_KEY is provided; otherwise fall back to simulated data
            let weatherData = null;
            if (API_KEY && API_KEY !== 'your_openweathermap_api_key_here') {
                try {
                    weatherData = await fetchWeatherFromOpenWeather(city);
                } catch (e) {
                    console.warn('OpenWeather failed, falling back to simulated data', e);
                    weatherData = await fetchSimulatedWeatherData(city);
                }
            } else {
                weatherData = await fetchSimulatedWeatherData(city);
            }
            
            if (weatherData) {
                displayWeatherData(weatherData);
                displayForecast(weatherData.forecast);
                weatherResults.style.display = 'block';
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

    // Fetch from OpenWeatherMap (requires API_KEY). This function performs geocoding + weather calls.
    async function fetchWeatherFromOpenWeather(query) {
        // 1) Geocoding
        const geoUrl = `https://api.openweathermap.org/geo/1.0/direct?q=${encodeURIComponent(query)}&limit=1&appid=${API_KEY}`;
        const geoResp = await fetch(geoUrl);
        if (!geoResp.ok) throw new Error('Geocoding failed');
        const geoJson = await geoResp.json();
        if (!geoJson || geoJson.length === 0) throw new Error('Location not found');
        const loc = geoJson[0];

        // 2) Current weather
        const weatherUrl = `https://api.openweathermap.org/data/2.5/weather?lat=${loc.lat}&lon=${loc.lon}&units=metric&lang=es&appid=${API_KEY}`;
        const weatherResp = await fetch(weatherUrl);
        if (!weatherResp.ok) throw new Error('Weather fetch failed');
        const w = await weatherResp.json();

        // 3) Forecast (5-day / 3-hour -> simplify to daily 5)
        const forecastUrl = `https://api.openweathermap.org/data/2.5/forecast?lat=${loc.lat}&lon=${loc.lon}&units=metric&lang=es&appid=${API_KEY}`;
        const fResp = await fetch(forecastUrl);
        const fdata = fResp.ok ? await fResp.json() : null;

        // Map to our internal structure
        const data = {
            name: loc.name || query,
            country: loc.country || '--',
            temp: Math.round(w.main.temp),
            feels_like: Math.round(w.main.feels_like),
            humidity: w.main.humidity,
            pressure: w.main.pressure,
            wind_speed: w.wind.speed,
            visibility: w.visibility || 10000,
            description: w.weather[0].description,
            icon: w.weather[0].icon,
            sunrise: w.sys.sunrise,
            sunset: w.sys.sunset,
            alerts: w.alerts || null,
            forecast: []
        };

        if (fdata && fdata.list) {
            // choose one entry per next 5 days roughly
            const byDay = {};
            fdata.list.forEach(item => {
                const day = new Date(item.dt * 1000).toLocaleDateString('es-ES');
                if (!byDay[day]) byDay[day] = [];
                byDay[day].push(item);
            });
            const days = Object.keys(byDay).slice(0, 5);
            data.forecast = days.map(d => {
                const items = byDay[d];
                const temps = items.map(i => i.main.temp);
                const min = Math.floor(Math.min(...temps));
                const max = Math.ceil(Math.max(...temps));
                const desc = items[0].weather[0].description;
                const icon = items[0].weather[0].icon;
                return { day: new Date(items[0].dt * 1000).toLocaleDateString('es-ES', { weekday: 'short' }), date: d, temp_min: min, temp_max: max, description: desc, icon };
            });
        }

        return data;
    }
    
    // Simulated weather data function (replace with actual API call in production)
    async function fetchSimulatedWeatherData(city) {
        // Simulate network delay
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        // Mock data based on common weather patterns
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
            forecast.push({
                day: getDayName(i),
                date: getDateString(i),
                temp_min: Math.floor(dayTemp - 3),
                temp_max: Math.ceil(dayTemp + 3),
                description: getRandomDescription(),
                icon: getRandomIcon()
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
        // Location
        weatherLocation.textContent = `${data.name}, ${data.country}`;
        
        // Temperature
        weatherTemperature.textContent = `${data.temp}°C`;
        
        // Description
        weatherDescription.textContent = capitalizeFirstLetter(data.description);
        
        // Icon
        weatherIcon.innerHTML = getWeatherIconHTML(data.icon, data.description);
        
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
                <div class="forecast-temp">
                    <span>${day.temp_min}°</span>
                    <span>${day.temp_max}°</span>
                </div>
            `;
            
            forecastContainer.appendChild(forecastDay);
        });
    }

    // City suggestions via OpenWeatherMap geocoding (or simulated suggestions)
    async function fetchCitySuggestions(query) {
        citySuggestions.setAttribute('aria-hidden', 'false');
        citySuggestions.innerHTML = '<div class="suggesting">Buscando...</div>';
        if (API_KEY && API_KEY !== 'your_openweathermap_api_key_here') {
            try {
                const url = `https://api.openweathermap.org/geo/1.0/direct?q=${encodeURIComponent(query)}&limit=6&appid=${API_KEY}`;
                const resp = await fetch(url);
                const json = await resp.json();
                renderCitySuggestions(json.map(i => ({ name: i.name, state: i.state, country: i.country })), query);
                return;
            } catch (e) {
                console.warn('Geocoding failed', e);
            }
        }

        // Fallback: create simple matches from common cities and the typed query
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
        loadingIndicator.style.display = 'flex';
        weatherResults.style.display = 'none';
        cityInput.disabled = true;
    }
    
    // Hide loading indicator
    function hideLoading() {
        loadingIndicator.style.display = 'none';
        cityInput.disabled = false;
    }
    
    // Show error message
    function showError(message) {
        recommendationText.textContent = message;
        recommendationText.style.color = '#ff5722';
        // Clear other data
        weatherLocation.textContent = '--';
        weatherTemperature.textContent = '--°C';
        weatherDescription.textContent = '--';
        weatherIcon.innerHTML = '<span class="material-icons-round">error</span>';
        humidityValue.textContent = '--%';
        windValue.textContent = '-- km/h';
        pressureValue.textContent = '-- hPa';
        visibilityValue.textContent = '-- km';
        forecastContainer.innerHTML = '<div class="forecast-placeholder"><p>Error al cargar el pronóstico</p></div>';
        weatherResults.style.display = 'block';
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