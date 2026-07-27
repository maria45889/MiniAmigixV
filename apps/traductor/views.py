from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.conf import settings
from .models import TranslationCache
from datetime import timedelta
import logging
import requests

logger = logging.getLogger(__name__)

def traductor_view(request):
    """Vista principal del módulo traductor"""
    return render(request, 'traductor/traductor.html')

@csrf_exempt
def traducir_texto(request):
    """API para traducir texto usando MyMemory API"""
    texto = request.POST.get('texto', '')
    idioma_destino = request.POST.get('idioma_destino', 'en')
    idioma_origen = request.POST.get('idioma_origen', 'auto')
    
    logger.info(f"Traduciendo texto: '{texto[:50]}...' de {idioma_origen} a {idioma_destino}")
    
    if not texto:
        return JsonResponse({
            'success': False,
            'error': 'No se proporcionó texto para traducir'
        }, status=400)
    
    # Verificar si hay caché válido
    try:
        cache = TranslationCache.objects.filter(
            texto_original=texto,
            idioma_origen=idioma_origen,
            idioma_destino=idioma_destino
        ).first()
        
        if cache and not cache.esta_expirado():
            logger.info("Usando traducción desde caché")
            return JsonResponse({
                'success': True,
                'data': {
                    'texto_original': cache.texto_original,
                    'texto_traducido': cache.texto_traducido,
                    'idioma_origen': cache.idioma_origen,
                    'idioma_destino': cache.idioma_destino,
                    'idioma_detectado': cache.idioma_detectado,
                    'from_cache': True
                }
            })
    except Exception as e:
        logger.error(f"Error buscando caché: {str(e)}")
    
    # Si no hay caché o está expirado, traducir usando MyMemory
    try:
        import urllib.parse
        lang_pair = f"{idioma_origen}|{idioma_destino}"
        texto_encoded = urllib.parse.quote(texto)
        url = f"https://api.mymemory.translated.net/get?q={texto_encoded}&langpair={lang_pair}"
        
        logger.info(f"Llamando a MyMemory API: {url}")
        logger.info(f"Parámetros - origen: {idioma_origen}, destino: {idioma_destino}, texto: '{texto[:50]}...'")
        
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        logger.info(f"Respuesta API: {data}")
        
        if data['responseStatus'] == 200:
            texto_traducido = data['responseData']['translatedText']
            idioma_detectado = data.get('responseData', {}).get('detectedLanguage', idioma_origen)
            logger.info(f"Traducción exitosa: '{texto[:30]}...' -> '{texto_traducido[:30]}...'")
        else:
            # Si hay error en la respuesta, devolver el texto original
            texto_traducido = texto
            idioma_detectado = idioma_origen
            logger.warning(f"API respondió con status {data['responseStatus']}, usando texto original. Respuesta completa: {data}")
        
        # Guardar en caché
        try:
            translation_cache = TranslationCache.objects.create(
                usuario=request.user if request.user.is_authenticated else None,
                texto_original=texto,
                texto_traducido=texto_traducido,
                idioma_origen=idioma_origen,
                idioma_destino=idioma_destino,
                idioma_detectado=idioma_detectado,
                fecha_expiracion=timezone.now() + timedelta(days=7)
            )
            logger.info("Traducción guardada en caché")
        except Exception as cache_error:
            logger.error(f"Error guardando en caché: {str(cache_error)}")
        
        return JsonResponse({
            'success': True,
            'data': {
                'texto_original': texto,
                'texto_traducido': texto_traducido,
                'idioma_origen': idioma_origen,
                'idioma_destino': idioma_destino,
                'idioma_detectado': idioma_detectado,
                'from_cache': False
            }
        })
        
    except requests.exceptions.Timeout:
        logger.error("Timeout al llamar a MyMemory API")
        return JsonResponse({
            'success': False,
            'error': 'El servicio de traducción tardó demasiado en responder. Por favor intenta de nuevo.'
        }, status=504)
    except requests.exceptions.RequestException as e:
        logger.error(f"Error de red al llamar a MyMemory API: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': 'Error de conexión con el servicio de traducción. Por favor verifica tu conexión a internet.'
        }, status=503)
    except Exception as e:
        logger.error(f"Error traduciendo texto: {str(e)}", exc_info=True)
        return JsonResponse({
            'success': False,
            'error': 'Error al traducir el texto. Por favor intenta de nuevo.'
        }, status=500)

@csrf_exempt
def detectar_idioma(request):
    """API para detectar el idioma de un texto usando MyMemory"""
    texto = request.POST.get('texto', '')
    
    if not texto:
        return JsonResponse({
            'success': False,
            'error': 'No se proporcionó texto'
        }, status=400)
    
    try:
        # Usar MyMemory para detección de idioma
        url = f"https://api.mymemory.translated.net/get?q={texto}&langpair=autodetect|en"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        idioma_detectado = data.get('responseData', {}).get('detectedLanguage', 'en')
        
        return JsonResponse({
            'success': True,
            'data': {
                'idioma': idioma_detectado,
                'confianza': 0.95  # MyMemory no proporciona confianza, valor por defecto
            }
        })
        
    except Exception as e:
        logger.error(f"Error detectando idioma: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': 'Error al detectar el idioma'
        }, status=500)

@csrf_exempt
def obtener_idiomas_soportados(request):
    """API para obtener la lista de idiomas soportados"""
    idiomas_comunes = {
        'es': 'Español',
        'en': 'Inglés',
        'fr': 'Francés',
        'de': 'Alemán',
        'it': 'Italiano',
        'pt': 'Portugués',
        'ru': 'Ruso',
        'ja': 'Japonés',
        'ko': 'Coreano',
        'zh': 'Chino',
        'ar': 'Árabe',
        'hi': 'Hindi',
        'nl': 'Holandés',
        'pl': 'Polaco',
        'tr': 'Turco',
        'sv': 'Sueco',
        'da': 'Danés',
        'fi': 'Finlandés',
        'no': 'Noruego',
        'el': 'Griego',
        'he': 'Hebreo',
        'th': 'Tailandés',
        'vi': 'Vietnamita',
        'id': 'Indonesio',
        'ms': 'Malayo',
        'uk': 'Ucraniano',
        'cs': 'Checo',
        'ro': 'Rumano',
        'hu': 'Húngaro',
        'bg': 'Búlgaro',
        'sk': 'Eslovaco',
        'sl': 'Esloveno',
        'hr': 'Croata',
        'sr': 'Serbio',
        'mt': 'Maltés',
        'lv': 'Letón',
        'lt': 'Lituano',
        'et': 'Estonio',
        'is': 'Islandés',
        'ga': 'Irlandés',
        'cy': 'Galés',
        'sq': 'Albanés',
        'mk': 'Macedonio',
        'be': 'Bielorruso',
        'ka': 'Georgiano',
        'hy': 'Armenio',
        'az': 'Azerbaiyano',
        'kk': 'Kazajo',
        'ky': 'Kirguís',
        'uz': 'Uzbeko',
        'tg': 'Tayiko',
        'mn': 'Mongol',
        'km': 'Jemer',
        'my': 'Birmano',
        'ne': 'Nepalí',
        'si': 'Cingalés',
        'ta': 'Tamil',
        'te': 'Telugu',
        'kn': 'Canarés',
        'ml': 'Malayalam',
        'bn': 'Bengalí',
        'gu': 'Gujarati',
        'pa': 'Punjabi',
        'ur': 'Urdu',
        'fa': 'Persa',
        'ps': 'Pastún',
        'sd': 'Sindhi',
        'ku': 'Kurdo',
        'af': 'Afrikáans',
        'sw': 'Swahili',
        'zu': 'Zulú',
        'xh': 'Xhosa',
        'yo': 'Yoruba',
        'ig': 'Igbo',
        'ha': 'Hausa',
        'so': 'Somalí',
        'am': 'Amárico',
        'ti': 'Tigrinya',
        'om': 'Oromo',
    }
    
    return JsonResponse({
        'success': True,
        'data': idiomas_comunes
    })

@csrf_exempt
def traducir_imagen(request):
    """API para traducir texto de una imagen (funcionalidad deshabilitada temporalmente)"""
    return JsonResponse({
        'success': False,
        'error': 'Funcionalidad de traducción de imagen temporalmente deshabilitada. Por favor usa la traducción de texto.'
    }, status=503)

@csrf_exempt
def traducir_documento(request):
    """API para traducir texto de un documento"""
    if request.method != 'POST':
        return JsonResponse({
            'success': False,
            'error': 'Método no permitido'
        }, status=405)
    
    documento = request.FILES.get('documento')
    idioma_destino = request.POST.get('idioma_destino', 'en')
    
    if not documento:
        return JsonResponse({
            'success': False,
            'error': 'No se proporcionó documento'
        }, status=400)
    
    try:
        # Leer documento (solo TXT por ahora)
        contenido = documento.read()
        
        try:
            texto_extraido = contenido.decode('utf-8')
        except UnicodeDecodeError:
            texto_extraido = contenido.decode('latin-1')
        
        if not texto_extraido.strip():
            return JsonResponse({
                'success': False,
                'error': 'El documento está vacío o no se pudo leer'
            }, status=400)
        
        # Traducir el texto extraído usando MyMemory
        lang_pair = f"auto|{idioma_destino}"
        url = f"https://api.mymemory.translated.net/get?q={texto_extraido}&langpair={lang_pair}"
        
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if data['responseStatus'] == 200:
            texto_traducido = data['responseData']['translatedText']
        else:
            texto_traducido = texto_extraido
        
        # Guardar en caché
        translation_cache = TranslationCache.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            texto_original=texto_extraido,
            texto_traducido=texto_traducido,
            idioma_origen='auto',
            idioma_destino=idioma_destino,
            idioma_detectado='auto',
            fecha_expiracion=timezone.now() + timedelta(days=7)
        )
        
        return JsonResponse({
            'success': True,
            'data': {
                'texto_original': texto_extraido,
                'texto_traducido': texto_traducido,
                'idioma_destino': idioma_destino,
                'from_cache': False
            }
        })
        
    except Exception as e:
        logger.error(f"Error traduciendo documento: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': f'Error al procesar el documento: {str(e)}'
        }, status=500)
