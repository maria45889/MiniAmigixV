from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
import os
import requests

from .models import Nota, Resumen, StudySession, PomodoroSession, DailyStats
from django.utils import timezone
from datetime import datetime, timedelta

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
            color = data.get('color', '#fef08a')
            fijada = data.get('fijada', False)
            
            if not contenido:
                return JsonResponse({'success': False, 'error': 'El contenido no puede estar vacío'})
            
            nota = Nota.objects.create(
                usuario=request.user,
                contenido=contenido,
                color=color,
                fijada=fijada
            )
            
            # Actualizar estadísticas diarias
            hoy = timezone.now().date()
            stats, _ = DailyStats.objects.get_or_create(
                usuario=request.user,
                fecha=hoy,
                defaults={
                    'tiempo_estudiado_segundos': 0,
                    'pomodoros_completados': 0,
                    'notas_creadas': 0,
                    'resumenes_creados': 0,
                    'racha_dias': 0
                }
            )
            stats.notas_creadas += 1
            stats.save()
            
            return JsonResponse({
                'success': True,
                'nota': {
                    'id': str(nota.id),
                    'contenido': nota.contenido,
                    'color': nota.color,
                    'fijada': nota.fijada,
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
                    'color': nota.color,
                    'fijada': nota.fijada,
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

@csrf_exempt
@login_required
def obtener_estadisticas(request):
    if request.method == 'GET':
        try:
            hoy = timezone.now().date()
            inicio_semana = hoy - timedelta(days=hoy.weekday())
            
            # Estadísticas de hoy
            stats_hoy, _ = DailyStats.objects.get_or_create(
                usuario=request.user,
                fecha=hoy,
                defaults={
                    'tiempo_estudiado_segundos': 0,
                    'pomodoros_completados': 0,
                    'notas_creadas': 0,
                    'resumenes_creados': 0,
                    'racha_dias': 0
                }
            )
            
            # Calcular racha
            racha = 0
            fecha_temp = hoy
            while True:
                try:
                    stats_dia = DailyStats.objects.get(usuario=request.user, fecha=fecha_temp)
                    if stats_dia.tiempo_estudiado_segundos > 0 or stats_dia.pomodoros_completados > 0:
                        racha += 1
                        fecha_temp -= timedelta(days=1)
                    else:
                        break
                except DailyStats.DoesNotExist:
                    break
            
            # Estadísticas de la semana
            stats_semana = DailyStats.objects.filter(
                usuario=request.user,
                fecha__gte=inicio_semana
            )
            
            tiempo_total_semana = sum(s.tiempo_estudiado_segundos for s in stats_semana)
            pomodoros_semana = sum(s.pomodoros_completados for s in stats_semana)
            
            # Mejor día
            mejor_dia = DailyStats.objects.filter(
                usuario=request.user,
                tiempo_estudiado_segundos__gt=0
            ).order_by('-tiempo_estudiado_segundos').first()
            
            # Próximo evento del calendario (localStorage)
            # Esto se manejará en el frontend
            
            # Datos semanales para gráfico
            datos_semana = []
            for i in range(7):
                fecha = inicio_semana + timedelta(days=i)
                try:
                    stats = DailyStats.objects.get(usuario=request.user, fecha=fecha)
                    horas = stats.tiempo_estudiado_segundos / 3600
                except DailyStats.DoesNotExist:
                    horas = 0
                datos_semana.append({
                    'dia': fecha.strftime('%a')[0], # Primera letra del día
                    'horas': round(horas, 1)
                })
            
            return JsonResponse({
                'success': True,
                'estadisticas': {
                    'hoy': {
                        'tiempo_segundos': stats_hoy.tiempo_estudiado_segundos,
                        'tiempo_formateado': f"{stats_hoy.tiempo_estudiado_segundos // 3600}h {(stats_hoy.tiempo_estudiado_segundos % 3600) // 60}m",
                        'pomodoros': stats_hoy.pomodoros_completados,
                        'notas': stats_hoy.notas_creadas,
                        'resumenes': stats_hoy.resumenes_creados
                    },
                    'racha': racha,
                    'semana': {
                        'tiempo_total_segundos': tiempo_total_semana,
                        'tiempo_formateado': f"{tiempo_total_semana // 3600}h {(tiempo_total_semana % 3600) // 60}m",
                        'pomodoros': pomodoros_semana
                    },
                    'mejor_dia': {
                        'fecha': mejor_dia.fecha.strftime('%d/%m/%Y') if mejor_dia else None,
                        'tiempo_formateado': f"{mejor_dia.tiempo_estudiado_segundos // 3600}h {(mejor_dia.tiempo_estudiado_segundos % 3600) // 60}m" if mejor_dia else "0h 0m"
                    },
                    'grafico_semana': datos_semana
                }
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Método no permitido'})

@csrf_exempt
@login_required
def guardar_sesion_estudio(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            duracion = data.get('duracion_segundos', 0)
            tipo = data.get('tipo', 'cronometro')
            
            sesion = StudySession.objects.create(
                usuario=request.user,
                duracion_segundos=duracion,
                tipo_sesion=tipo
            )
            
            # Actualizar estadísticas diarias
            hoy = timezone.now().date()
            stats, _ = DailyStats.objects.get_or_create(
                usuario=request.user,
                fecha=hoy,
                defaults={
                    'tiempo_estudiado_segundos': 0,
                    'pomodoros_completados': 0,
                    'notas_creadas': 0,
                    'resumenes_creados': 0,
                    'racha_dias': 0
                }
            )
            stats.tiempo_estudiado_segundos += duracion
            stats.save()
            
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Método no permitido'})

@csrf_exempt
@login_required
def guardar_pomodoro(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            duracion = data.get('duracion_minutos', 25)
            tipo = data.get('tipo', 'trabajo')
            completado = data.get('completado', True)
            
            pomodoro = PomodoroSession.objects.create(
                usuario=request.user,
                duracion_minutos=duracion,
                tipo=tipo,
                completado=completado
            )
            
            if completado and tipo == 'trabajo':
                # Actualizar estadísticas diarias
                hoy = timezone.now().date()
                stats, _ = DailyStats.objects.get_or_create(
                    usuario=request.user,
                    fecha=hoy,
                    defaults={
                        'tiempo_estudiado_segundos': 0,
                        'pomodoros_completados': 0,
                        'notas_creadas': 0,
                        'resumenes_creados': 0,
                        'racha_dias': 0
                    }
                )
                stats.pomodoros_completados += 1
                stats.tiempo_estudiado_segundos += duracion * 60
                stats.save()
            
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Método no permitido'})
