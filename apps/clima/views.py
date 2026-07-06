from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.utils import timezone
from .models import WeatherCache
from datetime import timedelta, datetime
import requests
import logging

logger = logging.getLogger(__name__)

def clima_view(request):
    """Vista principal del módulo clima"""
    return render(request, 'clima/clima.html')

@csrf_exempt
def obtener_clima(request):
    """API para obtener el clima actual de una ciudad usando WeatherAPI"""
    try:
        api_key = getattr(settings, 'WEATHERAPI_KEY', None)
        if not api_key:
            return JsonResponse({
                'success': False,
                'error': 'API Key de WeatherAPI no configurada'
            }, status=500)

        ciudad = request.GET.get('ciudad', 'Madrid')
        lat = request.GET.get('lat')
        lon = request.GET.get('lon')
        from_geo = request.GET.get('from_geo', 'false') == 'true'
        
        # Guardar el nombre original de la ciudad buscada
        ciudad_buscada = ciudad
        
        logger.info(f"obtener_clima - ciudad: {ciudad}, lat: {lat}, lon: {lon}, from_geo: {from_geo}")
        
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
                    ciudad=ciudad
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
                    'temp_max': cache.temp_max,
                    'temp_min': cache.temp_min,
                    'visibilidad': cache.visibilidad,
                    'uv_index': cache.uv_index,
                    'probabilidad_lluvia': cache.probabilidad_lluvia,
                    'amanecer': cache.amanecer.strftime('%H:%M') if cache.amanecer else None,
                    'atardecer': cache.atardecer.strftime('%H:%M') if cache.atardecer else None,
                    'pronostico': cache.pronostico,
                    'pronostico_hora': [],
                    'from_cache': True
                }
            })
        
        # Si no hay caché o está expirado, consultar WeatherAPI
        # Construir query para WeatherAPI
        if lat and lon:
            query = f"{lat},{lon}"
        else:
            # Para búsquedas por ciudad, agregar el país para obtener resultados más precisos
            # o usar el parámetro 'q' directamente
            query = ciudad
        
        # Obtener clima actual y pronóstico de 7 días con más datos
        # Agregamos 'lang=es' para español y 'aqi=no' para no incluir calidad del aire
        url = f"https://api.weatherapi.com/v1/forecast.json?key={api_key}&q={query}&days=7&lang=es&aqi=no&alerts=no"
        
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Extraer datos de la respuesta de WeatherAPI
        location = data['location']
        current = data['current']
        forecast = data['forecast']['forecastday']
        
        # Usar el nombre de la ciudad buscada si es una búsqueda por nombre
        # Si la ubicación devuelta es muy específica, usar region o el nombre buscado
        if lat and lon:
            # Para geolocalización, usar el nombre que devuelve WeatherAPI
            ciudad = location['name']
        else:
            # Para búsqueda por nombre, usar el nombre original buscado
            # para mostrar lo que el usuario escribió
            ciudad = ciudad_buscada
        
        pais = location['country']
        lat = location['lat']
        lon = location['lon']
        
        temperatura = current['temp_c']
        sensacion_termica = current['feelslike_c']
        humedad = current['humidity']
        presion = current['pressure_mb']
        viento_velocidad = current['wind_kph'] / 3.6  # Convertir a m/s
        viento_direccion = current['wind_degree']
        descripcion = current['condition']['text']
        icono = "https:" + current['condition']['icon']
        
        # Datos adicionales
        visibilidad = current.get('vis_km', 10)
        uv_index = current.get('uv', 0)
        
        # Datos del primer día para temp_max/min y probabilidad de lluvia
        if forecast:
            day_data = forecast[0]['day']
            temp_max = day_data['maxtemp_c']
            temp_min = day_data['mintemp_c']
            probabilidad_lluvia = day_data.get('daily_chance_of_rain', 0)
            
            # Convertir horas de amanecer/atardecer de string a Time
            try:
                amanecer_str = forecast[0]['astro']['sunrise']
                atardecer_str = forecast[0]['astro']['sunset']
                # WeatherAPI devuelve formato "06:15 AM" o "06:15"
                if amanecer_str:
                    try:
                        amanecer = datetime.strptime(amanecer_str, '%I:%M %p').time()
                    except ValueError:
                        amanecer = datetime.strptime(amanecer_str, '%H:%M').time()
                else:
                    amanecer = None
                    
                if atardecer_str:
                    try:
                        atardecer = datetime.strptime(atardecer_str, '%I:%M %p').time()
                    except ValueError:
                        atardecer = datetime.strptime(atardecer_str, '%H:%M').time()
                else:
                    atardecer = None
            except (ValueError, KeyError):
                amanecer = None
                atardecer = None
        else:
            temp_max = None
            temp_min = None
            probabilidad_lluvia = 0
            amanecer = None
            atardecer = None
        
        # Procesar pronóstico (7 días)
        pronostico_procesado = []
        for day in forecast:
            day_data = day['day']
            pronostico_procesado.append({
                'fecha': day['date'],
                'temperatura_max': day_data['maxtemp_c'],
                'temperatura_min': day_data['mintemp_c'],
                'descripcion': day_data['condition']['text'],
                'icono': "https:" + day_data['condition']['icon']
            })
        
        # Procesar pronóstico por horas (24 horas)
        pronostico_hora_procesado = []
        if forecast and 'hour' in forecast[0]:
            for hour in forecast[0]['hour'][:24]:
                pronostico_hora_procesado.append({
                    'dt': hour['time_epoch'],
                    'temp': hour['temp_c'],
                    'descripcion': hour['condition']['text'],
                    'icono': hour['condition']['icon']
                })
        
        # Guardar en caché
        weather_cache = WeatherCache.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            ciudad=ciudad,
            pais=pais,
            latitud=float(lat) if lat else None,
            longitud=float(lon) if lon else None,
            temperatura=temperatura,
            sensacion_termica=sensacion_termica,
            humedad=humedad,
            presion=presion,
            viento_velocidad=viento_velocidad,
            viento_direccion=viento_direccion,
            descripcion=descripcion,
            icono=icono,
            temp_max=temp_max,
            temp_min=temp_min,
            visibilidad=visibilidad,
            uv_index=uv_index,
            probabilidad_lluvia=probabilidad_lluvia,
            amanecer=amanecer,
            atardecer=atardecer,
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
                'temp_max': weather_cache.temp_max,
                'temp_min': weather_cache.temp_min,
                'visibilidad': weather_cache.visibilidad,
                'uv_index': weather_cache.uv_index,
                'probabilidad_lluvia': weather_cache.probabilidad_lluvia,
                'amanecer': weather_cache.amanecer.strftime('%H:%M') if weather_cache.amanecer else None,
                'atardecer': weather_cache.atardecer.strftime('%H:%M') if weather_cache.atardecer else None,
                'pronostico': weather_cache.pronostico,
                'pronostico_hora': pronostico_hora_procesado,
                'from_cache': False
            }
        })
        
    except requests.RequestException as e:
        logger.error(f"Error consultando WeatherAPI: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': 'Error al consultar el servicio del clima'
        }, status=500)
    except Exception as e:
        logger.error(f"Error inesperado en obtener_clima: {str(e)}", exc_info=True)
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
