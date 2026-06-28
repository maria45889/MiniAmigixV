from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.utils import timezone
from .models import WeatherCache
from datetime import timedelta
import requests
import logging

logger = logging.getLogger(__name__)

@login_required
def clima_view(request):
    """Vista principal del módulo clima"""
    return render(request, 'clima/clima.html')

@csrf_exempt
def obtener_clima(request):
    """API para obtener el clima actual de una ciudad usando Open-Meteo API"""
    ciudad = request.GET.get('ciudad', 'Madrid')
    pais = request.GET.get('pais', 'ES')
    lat = request.GET.get('lat')
    lon = request.GET.get('lon')
    from_geo = request.GET.get('from_geo', 'false') == 'true'
    
    # Si viene de geolocalización, ignorar caché para obtener datos frescos
    if from_geo:
        cache = None
    else:
        # Verificar si hay caché válido
        if lat and lon:
            cache = WeatherCache.objects.filter(
                latitud=lat, 
                longitud=lon
            ).first()
        else:
            cache = WeatherCache.objects.filter(
                ciudad=ciudad, 
                pais=pais
            ).first()
    
    if cache and not cache.esta_expirado():
        return JsonResponse({
            'success': True,
            'data': {
                'temperatura': cache.temperatura,
                'sensacion_termica': cache.sensacion_termica,
                'humedad': cache.humedad,
                'presion': cache.presion,
                'viento_velocidad': cache.viento_velocidad,
                'viento_direccion': cache.viento_direccion,
                'descripcion': cache.descripcion,
                'icono': cache.icono,
                'ciudad': cache.ciudad,
                'pais': cache.pais,
                'latitud': cache.latitud,
                'longitud': cache.longitud,
                'pronostico': cache.pronostico,
                'from_cache': True
            }
        })
    
    # Si no hay caché o está expirado, consultar Open-Meteo API
    try:
        if lat and lon:
            # Hacer geocoding inverso usando Nominatim (OpenStreetMap) - mejor cobertura
            nominatim_url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}&accept-language=es"
            try:
                logger.info(f"Intentando geocoding inverso con Nominatim para lat={lat}, lon={lon}")
                headers = {'User-Agent': 'MiniAmigixV/1.0'}
                reverse_geo_response = requests.get(nominatim_url, headers=headers, timeout=5)
                reverse_geo_response.raise_for_status()
                reverse_geo_data = reverse_geo_response.json()
                logger.info(f"Respuesta Nominatim: {reverse_geo_data}")
                
                if reverse_geo_data.get('address'):
                    address = reverse_geo_data['address']
                    # Priorizar ciudad, luego town, luego village
                    ciudad = address.get('city') or address.get('town') or address.get('village') or address.get('municipality') or 'Desconocido'
                    # Obtener código de país
                    country_code = address.get('country_code', '').upper()
                    pais = country_code if country_code else 'EC'
                    logger.info(f"Ciudad detectada: {ciudad}, País: {pais}")
                else:
                    ciudad = 'Desconocido'
                    pais = 'EC'
                    logger.warning("No se encontraron resultados en Nominatim")
            except Exception as e:
                logger.error(f"Error en geocoding inverso con Nominatim: {str(e)}")
                ciudad = 'Desconocido'
                pais = 'EC'
            
            # Usar coordenadas directamente
            url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m,wind_direction_10m&daily=weather_code,temperature_2m_max,temperature_2m_min&timezone=auto"
        else:
            # Primero obtener coordenadas de la ciudad usando geocoding de Open-Meteo
            geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={ciudad}&count=1&language=es&format=json"
            geo_response = requests.get(geo_url)
            geo_response.raise_for_status()
            geo_data = geo_response.json()
            
            if not geo_data.get('results'):
                return JsonResponse({
                    'success': False,
                    'error': f'Ciudad "{ciudad}" no encontrada'
                }, status=404)
            
            location = geo_data['results'][0]
            lat = location['latitude']
            lon = location['longitude']
            ciudad = location.get('name', ciudad)
            pais = location.get('country_code', 'ES')
            
            # Ahora obtener clima con las coordenadas
            url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m,wind_direction_10m&daily=weather_code,temperature_2m_max,temperature_2m_min&timezone=auto"
        
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        # Mapear códigos de clima de Open-Meteo a descripciones
        weather_codes = {
            0: 'Cielo despejado',
            1: 'Mayormente despejado',
            2: 'Parcialmente nublado',
            3: 'Nublado',
            45: 'Niebla',
            48: 'Niebla con escarcha',
            51: 'Llovizna ligera',
            53: 'Llovizna moderada',
            55: 'Llovizna densa',
            61: 'Lluvia ligera',
            63: 'Lluvia moderada',
            65: 'Lluvia fuerte',
            71: 'Nieve ligera',
            73: 'Nieve moderada',
            75: 'Nieve fuerte',
            80: 'Chubascos lig eros',
            81: 'Chubascos moderados',
            82: 'Chubascos fuertes',
            95: 'Tormenta eléctrica',
            96: 'Tormenta con granizo ligero',
            99: 'Tormenta con granizo fuerte'
        }
        
        current = data['current']
        daily = data['daily']
        
        # Procesar pronóstico (5 días)
        pronostico_procesado = []
        for i in range(1, min(6, len(daily['time']))):
            weather_code = daily['weather_code'][i]
            pronostico_procesado.append({
                'fecha': daily['time'][i],
                'temperatura_max': daily['temperature_2m_max'][i],
                'temperatura_min': daily['temperature_2m_min'][i],
                'descripcion': weather_codes.get(weather_code, 'Desconocido'),
                'icono': str(weather_code)
            })
        
        # Guardar en caché
        weather_cache = WeatherCache.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            ciudad=ciudad,
            pais=pais,
            latitud=lat,
            longitud=lon,
            temperatura=current['temperature_2m'],
            sensacion_termica=current.get('apparent_temperature'),
            humedad=current['relative_humidity_2m'],
            presion=None,  # Open-Meteo no proporciona presión
            viento_velocidad=current['wind_speed_10m'],
            viento_direccion=current.get('wind_direction_10m'),
            descripcion=weather_codes.get(current['weather_code'], 'Desconocido'),
            icono=str(current['weather_code']),
            pronostico=pronostico_procesado,
            fecha_expiracion=timezone.now() + timedelta(hours=1)
        )
        
        return JsonResponse({
            'success': True,
            'data': {
                'temperatura': weather_cache.temperatura,
                'sensacion_termica': weather_cache.sensacion_termica,
                'humedad': weather_cache.humedad,
                'presion': weather_cache.presion,
                'viento_velocidad': weather_cache.viento_velocidad,
                'viento_direccion': weather_cache.viento_direccion,
                'descripcion': weather_cache.descripcion,
                'icono': weather_cache.icono,
                'ciudad': weather_cache.ciudad,
                'pais': weather_cache.pais,
                'latitud': weather_cache.latitud,
                'longitud': weather_cache.longitud,
                'pronostico': weather_cache.pronostico,
                'from_cache': False
            }
        })
        
    except requests.RequestException as e:
        logger.error(f"Error consultando Open-Meteo API: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': 'Error al consultar el servicio del clima'
        }, status=500)

@csrf_exempt
def geolocalizar(request):
    """API para obtener clima basado en geolocalización del navegador"""
    lat = request.GET.get('lat')
    lon = request.GET.get('lon')
    
    if not lat or not lon:
        return JsonResponse({
            'success': False,
            'error': 'Se requieren coordenadas latitud y longitud'
        }, status=400)
    
    # Reutilizar la función obtener_clima con coordenadas
    request.GET = request.GET.copy()
    request.GET['lat'] = lat
    request.GET['lon'] = lon
    
    return obtener_clima(request)
