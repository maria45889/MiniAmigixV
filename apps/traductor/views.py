from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import TranslationCache
from datetime import timedelta
from deep_translator import GoogleTranslator
import logging

logger = logging.getLogger(__name__)

@login_required
def traductor_view(request):
    """Vista principal del módulo traductor"""
    return render(request, 'traductor/traductor.html')

@csrf_exempt
def traducir_texto(request):
    """API para traducir texto"""
    texto = request.POST.get('texto', '')
    idioma_destino = request.POST.get('idioma_destino', 'en')
    idioma_origen = request.POST.get('idioma_origen', 'auto')
    
    if not texto:
        return JsonResponse({
            'success': False,
            'error': 'No se proporcionó texto para traducir'
        }, status=400)
    
    # Si idioma_origen es 'auto', intentar detectar
    idioma_detectado = None
    if idioma_origen == 'auto':
        try:
            # Usar GoogleTranslator para detectar idioma
            translator = GoogleTranslator(source='auto', target='en')
            idioma_detectado = translator.detect(texto).lower()
            idioma_origen = idioma_detectado
        except Exception as e:
            logger.error(f"Error detectando idioma: {str(e)}")
            idioma_origen = 'auto'
    
    # Verificar si hay caché válido
    cache = TranslationCache.objects.filter(
        texto_original=texto,
        idioma_origen=idioma_origen,
        idioma_destino=idioma_destino
    ).first()
    
    if cache and not cache.esta_expirado():
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
    
    # Si no hay caché o está expirado, traducir
    try:
        translator = GoogleTranslator(source=idioma_origen if idioma_origen != 'auto' else 'auto', target=idioma_destino)
        texto_traducido = translator.translate(texto)
        
        # Guardar en caché
        translation_cache = TranslationCache.objects.create(
            usuario=request.user if request.user.is_authenticated else None,
            texto_original=texto,
            texto_traducido=texto_traducido,
            idioma_origen=idioma_origen,
            idioma_destino=idioma_destino,
            idioma_detectado=idioma_detectado,
            fecha_expiracion=timezone.now() + timedelta(days=7)
        )
        
        return JsonResponse({
            'success': True,
            'data': {
                'texto_original': translation_cache.texto_original,
                'texto_traducido': translation_cache.texto_traducido,
                'idioma_origen': translation_cache.idioma_origen,
                'idioma_destino': translation_cache.idioma_destino,
                'idioma_detectado': translation_cache.idioma_detectado,
                'from_cache': False
            }
        })
        
    except Exception as e:
        logger.error(f"Error traduciendo texto: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': 'Error al traducir el texto'
        }, status=500)

@csrf_exempt
def detectar_idioma(request):
    """API para detectar el idioma de un texto"""
    texto = request.POST.get('texto', '')
    
    if not texto:
        return JsonResponse({
            'success': False,
            'error': 'No se proporcionó texto'
        }, status=400)
    
    try:
        translator = GoogleTranslator(source='auto', target='en')
        deteccion = translator.detect(texto)
        
        return JsonResponse({
            'success': True,
            'data': {
                'idioma': deteccion.lower(),
                'confianza': 0.95  # GoogleTranslator no proporciona confianza, valor por defecto
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
