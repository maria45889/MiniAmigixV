from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.utils import timezone
from django.core.cache import cache
from .models import WeatherCache
from datetime import timedelta, datetime
import requests
import logging
import time

logger = logging.getLogger(__name__)


def _get_coordinates_from_city(ciudad):
    """Obtiene coordenadas y metadatos de una ciudad usando Open-Meteo geocoding."""
    geocoding_url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {
        "name": ciudad,
        "count": 1,
        "language": "es",
        "format": "json",
    }
    response = requests.get(geocoding_url, params=params, timeout=5)
    response.raise_for_status()
    geo_data = response.json()

    if not geo_data.get("results"):
        raise ValueError("Ciudad no encontrada")

    result = geo_data["results"][0]
    return (
        float(result["latitude"]),
        float(result["longitude"]),
        result.get("name", ciudad),
        result.get("country", ""),
    )


def _get_city_from_coordinates(lat, lon, fallback_name=None):
    """Obtiene nombre de ciudad y país desde coordenadas usando Open-Meteo reverse geocoding."""
    reverse_url = "https://geocoding-api.open-meteo.com/v1/reverse"
    params = {
        "latitude": lat,
        "longitude": lon,
        "language": "es",
        "format": "json",
    }
    response = requests.get(reverse_url, params=params, timeout=5)
    response.raise_for_status()
    data = response.json()

    results = data.get("results") or []
    if not results:
        return fallback_name or f"Ubicación ({lat}, {lon})", ""

    result = results[0]
    return result.get("name") or fallback_name or f"Ubicación ({lat}, {lon})", result.get("country", "")


def clima_view(request):
    """Vista principal del módulo clima"""
    return render(request, 'clima/clima.html')

@csrf_exempt
def obtener_clima(request):
    """API para obtener el clima actual usando Open-Meteo (gratis, sin API key)"""
    start_time = time.time()
    try:
        ciudad = request.GET.get('ciudad')
        lat = request.GET.get('lat')
        lon = request.GET.get('lon')
        from_geo = request.GET.get('from_geo', 'false') == 'true'

        ciudad_buscada = ciudad
        logger.info(f"obtener_clima - ciudad: {ciudad}, lat: {lat}, lon: {lon}")

        # Si no hay coordenadas, usar geocodificación para obtenerlas
        if not lat or not lon:
            if ciudad:
                # Usar caché para geocodificación
                cache_key = f"geo_{ciudad.lower()}"
                cached_coords = cache.get(cache_key)

                if cached_coords:
                    if len(cached_coords) == 4:
                        lat, lon, ciudad, _ = cached_coords
                    else:
                        lat, lon, ciudad = cached_coords
                    logger.info(f"Usando caché de geocodificación para {ciudad}")
                else:
                    # Geocodificar la ciudad para obtener coordenadas
                    try:
                        lat, lon, ciudad, pais = _get_coordinates_from_city(ciudad)
                        cache.set(cache_key, (lat, lon, ciudad, pais), 86400)
                    except ValueError:
                        return JsonResponse({
                            'success': False,
                            'error': 'Ciudad no encontrada'
                        }, status=404)
                    except requests.RequestException as e:
                        logger.error(f"Error geocodificando ciudad: {str(e)}")
                        return JsonResponse({
                            'success': False,
                            'error': 'Error al buscar la ciudad'
                        }, status=500)
            else:
                return JsonResponse({
                    'success': False,
                    'error': 'Se requiere una ciudad o coordenadas'
                }, status=400)
        else:
            # Obtener nombre de la ciudad a partir de lat/lon usando Nominatim
            cache_key = f"reverse_geo_{lat}_{lon}"
            cached_city = cache.get(cache_key)

            if cached_city:
                ciudad, pais = cached_city
                logger.info(f"Usando caché de geocodificación inversa para {lat}, {lon}")
            else:
                try:
                    ciudad, pais = _get_city_from_coordinates(float(lat), float(lon), fallback_name=ciudad_buscada)
                    cache.set(cache_key, (ciudad, pais), 86400)
                except requests.RequestException as e:
                    logger.error(f"Error consultando geocodificación inversa: {str(e)}")
                    ciudad = ciudad_buscada or f"Ubicación ({lat}, {lon})"
                    pais = ""

        # Asegurar que ciudad siempre tenga un valor
        if not ciudad:
            ciudad = f"Ubicación ({lat}, {lon})"

        # Verificar caché en base de datos
        weather_cache_key = f"weather_{lat}_{lon}"
        cached_weather = cache.get(weather_cache_key)

        if cached_weather:
            logger.info(f"Usando caché de clima para {lat}, {lon}")
            elapsed = time.time() - start_time
            logger.info(f"Tiempo de respuesta (caché): {elapsed:.2f}s")
            return JsonResponse({
                'success': True,
                'data': cached_weather,
                'from_cache': True
            })

        # Si no está en caché, buscar en base de datos
        db_cache = WeatherCache.objects.filter(
            latitud=lat,
            longitud=lon
        ).first()

        if db_cache and not db_cache.esta_expirado():
            # Agregar etiquetas de días al pronóstico del caché
            dias_semana = ['Dom', 'Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb']
            hoy = datetime.now().weekday()
            pronostico_con_dias = []
            for i, item in enumerate(db_cache.pronostico):
                if i == 0:
                    dia_label = "Hoy"
                else:
                    dia_index = (hoy + i) % 7
                    dia_label = dias_semana[dia_index]
                pronostico_con_dias.append({
                    **item,
                    'dia': dia_label
                })

            weather_data = {
                'temperatura': db_cache.temperatura,
                'sensacion_termica': db_cache.sensacion_termica,
                'humedad': db_cache.humedad,
                'presion': db_cache.presion,
                'viento_velocidad': db_cache.viento_velocidad,
                'viento_direccion': db_cache.viento_direccion,
                'descripcion': db_cache.descripcion,
                'icono': db_cache.icono,
                'ciudad': db_cache.ciudad,
                'pais': db_cache.pais,
                'latitud': db_cache.latitud,
                'longitud': db_cache.longitud,
                'temp_max': db_cache.temp_max,
                'temp_min': db_cache.temp_min,
                'visibilidad': db_cache.visibilidad,
                'uv_index': db_cache.uv_index,
                'probabilidad_lluvia': db_cache.probabilidad_lluvia,
                'amanecer': db_cache.amanecer.strftime('%H:%M') if db_cache.amanecer else None,
                'atardecer': db_cache.atardecer.strftime('%H:%M') if db_cache.atardecer else None,
                'pronostico': pronostico_con_dias,
                'pronostico_hora': [],
            }

            # Guardar en caché de Django por 55 minutos (menos que la expiración de BD)
            cache.set(weather_cache_key, weather_data, 3300)

            elapsed = time.time() - start_time
            logger.info(f"Tiempo de respuesta (caché BD): {elapsed:.2f}s")

            return JsonResponse({
                'success': True,
                'data': weather_data,
                'from_cache': True
            })

        # Consultar Open-Meteo API (gratis, sin API key)
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m,pressure_msl&daily=weather_code,temperature_2m_max,temperature_2m_min,sunrise,sunset,precipitation_probability_max&timezone=auto&forecast_days=7"

        response = requests.get(url, timeout=5)  # Reducido de 10 a 5 segundos
        response.raise_for_status()
        data = response.json()
        
        # Extraer datos actuales
        current = data['current']
        daily = data['daily']
        
        temperatura = current['temperature_2m']
        sensacion_termica = current['apparent_temperature']
        humedad = current['relative_humidity_2m']
        presion = current['pressure_msl']
        viento_velocidad = current['wind_speed_10m']
        weather_code = current['weather_code']
        
        # Mapear código del tiempo a descripción e icono
        weather_descriptions = {
            0: ("Despejado", "01d"),
            1: ("Mayormente despejado", "02d"),
            2: ("Parcialmente nublado", "03d"),
            3: ("Nublado", "04d"),
            45: ("Niebla", "50d"),
            48: ("Niebla con escarcha", "50d"),
            51: ("Llovizna ligera", "10d"),
            53: ("Llovizna moderada", "10d"),
            55: ("Llovizna densa", "10d"),
            61: ("Lluvia ligera", "10d"),
            63: ("Lluvia moderada", "10d"),
            65: ("Lluvia fuerte", "10d"),
            71: ("Nieve ligera", "13d"),
            73: ("Nieve moderada", "13d"),
            75: ("Nieve fuerte", "13d"),
            80: ("Chubascos ligeros", "09d"),
            81: ("Chubascos moderados", "09d"),
            82: ("Chubascos violentos", "09d"),
            95: ("Tormenta", "11d"),
            96: ("Tormenta con granizo ligero", "11d"),
            99: ("Tormenta con granizo fuerte", "11d"),
        }
        
        descripcion, icon_code = weather_descriptions.get(weather_code, ("Desconocido", "01d"))
        icono = f"https://openweathermap.org/img/wn/{icon_code}@2x.png"
        
        # Datos del primer día
        temp_max = daily['temperature_2m_max'][0]
        temp_min = daily['temperature_2m_min'][0]
        probabilidad_lluvia = daily['precipitation_probability_max'][0] if 'precipitation_probability_max' in daily else 0
        
        # Amanecer y atardecer
        try:
            amanecer_str = daily['sunrise'][0]
            atardecer_str = daily['sunset'][0]
            amanecer = datetime.fromisoformat(amanecer_str.replace('Z', '+00:00')).time()
            atardecer = datetime.fromisoformat(atardecer_str.replace('Z', '+00:00')).time()
        except:
            amanecer = None
            atardecer = None
        
        # Procesar pronóstico (7 días)
        pronostico_procesado = []
        dias_semana = ['Dom', 'Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb']
        hoy = datetime.now().weekday()
        
        for i in range(len(daily['time'])):
            day_code = daily['weather_code'][i]
            day_desc, day_icon = weather_descriptions.get(day_code, ("Desconocido", "01d"))
            
            # Calcular el día de la semana correcto
            if i == 0:
                dia_label = "Hoy"
            else:
                dia_index = (hoy + i) % 7
                dia_label = dias_semana[dia_index]
            
            pronostico_procesado.append({
                'fecha': daily['time'][i],
                'dia': dia_label,
                'temperatura_max': daily['temperature_2m_max'][i],
                'temperatura_min': daily['temperature_2m_min'][i],
                'descripcion': day_desc,
                'icono': f"https://openweathermap.org/img/wn/{day_icon}@2x.png"
            })
        
        # Guardar en caché
        weather_cache = WeatherCache.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            ciudad=ciudad,
            pais=pais if pais else "Desconocido",
            latitud=float(lat),
            longitud=float(lon),
            temperatura=temperatura,
            sensacion_termica=sensacion_termica,
            humedad=humedad,
            presion=presion,
            viento_velocidad=viento_velocidad,
            viento_direccion=0,
            descripcion=descripcion,
            icono=icono,
            temp_max=temp_max,
            temp_min=temp_min,
            visibilidad=10000,  # 10km en metros
            uv_index=0,
            probabilidad_lluvia=probabilidad_lluvia,
            amanecer=amanecer,
            atardecer=atardecer,
            pronostico=pronostico_procesado,
            fecha_expiracion=timezone.now() + timedelta(hours=1)
        )

        weather_data = {
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
            'temp_max': weather_cache.temp_max,
            'temp_min': weather_cache.temp_min,
            'visibilidad': weather_cache.visibilidad,
            'uv_index': weather_cache.uv_index,
            'probabilidad_lluvia': weather_cache.probabilidad_lluvia,
            'amanecer': weather_cache.amanecer.strftime('%H:%M') if weather_cache.amanecer else None,
            'atardecer': weather_cache.atardecer.strftime('%H:%M') if weather_cache.atardecer else None,
            'pronostico': weather_cache.pronostico,
            'pronostico_hora': [],
        }

        # Guardar en caché de Django por 55 minutos
        cache.set(weather_cache_key, weather_data, 3300)

        elapsed = time.time() - start_time
        logger.info(f"Tiempo de respuesta (API): {elapsed:.2f}s")

        return JsonResponse({
            'success': True,
            'data': weather_data,
            'from_cache': False
        })

    except requests.RequestException as e:
        elapsed = time.time() - start_time
        logger.error(f"Error consultando Open-Meteo: {str(e)} - Tiempo: {elapsed:.2f}s")
        return JsonResponse({
            'success': False,
            'error': 'Error al consultar el servicio del clima'
        }, status=500)
    except Exception as e:
        elapsed = time.time() - start_time
        logger.error(f"Error inesperado en obtener_clima: {str(e)} - Tiempo: {elapsed:.2f}s", exc_info=True)
        return JsonResponse({
            'success': False,
            'error': f'Error inesperado: {str(e)}'
        }, status=500)

@csrf_exempt
def geolocalizar(request):
    """API para obtener clima basado en geolocalización del navegador"""
    lat = request.GET.get('lat')
    lon = request.GET.get('lon')
    
    logger.info(f"Geolocalización recibida - lat: {lat}, lon: {lon}")
    
    if not lat or not lon:
        return JsonResponse({
            'success': False,
            'error': 'Se requieren coordenadas latitud y longitud'
        }, status=400)
    
    # Reutilizar la función obtener_clima con coordenadas
    request.GET = request.GET.copy()
    request.GET['lat'] = lat
    request.GET['lon'] = lon
    request.GET['from_geo'] = 'true'
    
    return obtener_clima(request)
