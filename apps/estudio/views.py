from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
import os
from openai import OpenAI

from .models import Nota, Resumen

# Inicializar cliente de OpenAI
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

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
            
            # Usar OpenAI para generar el resumen
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Eres un asistente que genera resúmenes concisos y claros de textos. Genera un resumen en español del texto proporcionado."},
                    {"role": "user", "content": f"Por favor, genera un resumen conciso del siguiente texto:\n\n{texto}"}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            resumen = response.choices[0].message.content
            
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
