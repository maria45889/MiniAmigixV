from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
import os
import requests

from .models import Nota, Resumen

@login_required
def estudio(request):
    notas = Nota.objects.filter(usuario=request.user)
    resumenes = Resumen.objects.filter(usuario=request.user)
    
    return render(request, 'estudio.html', {
        'notas': notas,
        'resumenes': resumenes
    })

@csrf_exempt
@login_required
def guardar_nota(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            contenido = data.get('contenido', '')
            
            if not contenido:
                return JsonResponse({'success': False, 'error': 'El contenido no puede estar vacío'})
            
            nota = Nota.objects.create(
                usuario=request.user,
                contenido=contenido
            )
            
            return JsonResponse({
                'success': True,
                'nota': {
                    'id': str(nota.id),
                    'contenido': nota.contenido,
                    'fecha_creacion': nota.fecha_creacion.strftime('%d/%m/%Y %H:%M')
                }
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Método no permitido'})

@csrf_exempt
@login_required
def eliminar_nota(request, nota_id):
    if request.method == 'DELETE':
        try:
            nota = Nota.objects.get(id=nota_id, usuario=request.user)
            nota.delete()
            return JsonResponse({'success': True})
        except Nota.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Nota no encontrada'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Método no permitido'})

@csrf_exempt
@login_required
def resumir_texto(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            texto = data.get('texto', '')
            
            if not texto:
                return JsonResponse({'success': False, 'error': 'El texto no puede estar vacío'})
            
            # Algoritmo de resumen local (sin dependencias externas)
            resumen = generar_resumen_local(texto)
            
            # Guardar el resumen en la base de datos
            resumen_obj = Resumen.objects.create(
                usuario=request.user,
                texto_original=texto,
                resumen=resumen
            )
            
            return JsonResponse({
                'success': True,
                'resumen': resumen,
                'resumen_id': str(resumen_obj.id)
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Método no permitido'})

def generar_resumen_local(texto):
    """
    Genera un resumen usando algoritmo de extracción local.
    No requiere conexión a internet ni APIs externas.
    """
    import re
    
    # Dividir texto en oraciones
    oraciones = re.split(r'[.!?]+', texto)
    oraciones = [o.strip() for o in oraciones if o.strip()]
    
    if len(oraciones) <= 3:
        return texto  # Texto muy corto, devolver original
    
    # Calcular puntuación de cada oración
    puntuaciones = []
    for i, oracion in enumerate(oraciones):
        score = 0
        
        # Longitud ideal (entre 10 y 50 palabras)
        palabras = oracion.split()
        longitud = len(palabras)
        if 10 <= longitud <= 50:
            score += 3
        elif 5 <= longitud < 10:
            score += 1
        elif longitud > 50:
            score -= 1
        
        # Posición en el texto (primeras oraciones más importantes)
        if i < 2:
            score += 2
        elif i < 5:
            score += 1
        
        # Palabras clave importantes
        palabras_clave = ['importante', 'principal', 'clave', 'esencial', 'fundamental', 
                         'crucial', 'significativo', 'destacado', 'principalmente', 'básicamente']
        for palabra in palabras_clave:
            if palabra.lower() in oracion.lower():
                score += 2
        
        # Evitar oraciones muy cortas o con poca información
        if longitud < 3:
            score -= 2
            
        puntuaciones.append((score, oracion))
    
    # Ordenar por puntuación y seleccionar las mejores
    puntuaciones.sort(key=lambda x: x[0], reverse=True)
    
    # Seleccionar oraciones (máximo 3 o 40% del total)
    num_oraciones = min(3, max(1, len(oraciones) // 3))
    mejores_oraciones = [oracion for score, oracion in puntuaciones[:num_oraciones]]
    
    # Mantener orden original
    resumen_oraciones = []
    for oracion in oraciones:
        if oracion in mejores_oraciones:
            resumen_oraciones.append(oracion)
    
    resumen = '. '.join(resumen_oraciones) + '.'
    
    # Si el resumen es muy largo, acortarlo
    if len(resumen) > 500:
        resumen = resumen[:497] + '...'
    
    return resumen

@csrf_exempt
@login_required
def obtener_notas(request):
    if request.method == 'GET':
        try:
            notas = Nota.objects.filter(usuario=request.user)
            notas_data = [
                {
                    'id': str(nota.id),
                    'contenido': nota.contenido,
                    'fecha_creacion': nota.fecha_creacion.strftime('%d/%m/%Y %H:%M')
                }
                for nota in notas
            ]
            return JsonResponse({'success': True, 'notas': notas_data})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Método no permitido'})

@csrf_exempt
@login_required
def obtener_resumenes(request):
    if request.method == 'GET':
        try:
            resumenes = Resumen.objects.filter(usuario=request.user)
            resumenes_data = [
                {
                    'id': str(resumen.id),
                    'texto_original': resumen.texto_original[:100] + '...' if len(resumen.texto_original) > 100 else resumen.texto_original,
                    'resumen': resumen.resumen,
                    'fecha_creacion': resumen.fecha_creacion.strftime('%d/%m/%Y %H:%M')
                }
                for resumen in resumenes
            ]
            return JsonResponse({'success': True, 'resumenes': resumenes_data})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Método no permitido'})

@csrf_exempt
@login_required
def eliminar_resumen(request, resumen_id):
    if request.method == 'DELETE':
        try:
            resumen = Resumen.objects.get(id=resumen_id, usuario=request.user)
            resumen.delete()
            return JsonResponse({'success': True})
        except Resumen.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Resumen no encontrado'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Método no permitido'})
