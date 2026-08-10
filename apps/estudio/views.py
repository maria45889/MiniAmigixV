from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
import os
import requests

from .models import Nota, Resumen, StudySession, PomodoroSession, DailyStats, UserProfile, Mision, MisionCompletada, LeccionRapida, Insignia, InsigniaUsuario, Accesorio, AccesorioUsuario, MetaDiaria
from django.utils import timezone
from datetime import datetime, timedelta
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import (
    UserProfileSerializer, MisionSerializer, MisionCompletadaSerializer,
    LeccionRapidaSerializer, InsigniaSerializer, InsigniaUsuarioSerializer,
    AccesorioSerializer, AccesorioUsuarioSerializer
)

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
            titulo = data.get('titulo', '')
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
                    'titulo': titulo,
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
            
            resumen = generar_resumen_local(texto)
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
    import re
    
    oraciones = re.split(r'[.!?]+', texto)
    oraciones = [o.strip() for o in oraciones if o.strip()]
    
    if len(oraciones) <= 3:
        return texto
    
    puntuaciones = []
    for i, oracion in enumerate(oraciones):
        score = 0
        
        palabras = oracion.split()
        longitud = len(palabras)
        if 10 <= longitud <= 50:
            score += 3
        elif 5 <= longitud < 10:
            score += 1
        elif longitud > 50:
            score -= 1
        
        if i < 2:
            score += 2
        elif i < 5:
            score += 1
        
        palabras_clave = ['importante', 'principal', 'clave', 'esencial', 'fundamental', 
                         'crucial', 'significativo', 'destacado', 'principalmente', 'básicamente']
        for palabra in palabras_clave:
            if palabra.lower() in oracion.lower():
                score += 2
        
        if longitud < 3:
            score -= 2
            
        puntuaciones.append((score, oracion))
    
    puntuaciones.sort(key=lambda x: x[0], reverse=True)
    
    num_oraciones = min(3, max(1, len(oraciones) // 3))
    mejores_oraciones = [oracion for score, oracion in puntuaciones[:num_oraciones]]
    
    resumen_oraciones = []
    for oracion in oraciones:
        if oracion in mejores_oraciones:
            resumen_oraciones.append(oracion)
    
    resumen = '. '.join(resumen_oraciones) + '.'
    
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
                    'titulo': nota.contenido[:50] if len(nota.contenido) > 50 else nota.contenido,
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
            profile, _ = UserProfile.objects.get_or_create(usuario=request.user)
            
            # Calcular horas estudiadas (últimos 7 días)
            hace_7_dias = timezone.now().date() - timedelta(days=7)
            stats_semana = DailyStats.objects.filter(
                usuario=request.user,
                fecha__gte=hace_7_dias
            )
            
            horas_estudiadas = sum(
                stat.tiempo_estudiado_segundos / 3600 
                for stat in stats_semana
            )
            
            # Pomodoros hoy y total
            hoy = timezone.now().date()
            pomodoros_hoy = PomodoroSession.objects.filter(
                usuario=request.user,
                fecha__date=hoy,
                completado=True
            ).count()
            
            total_pomodoros = PomodoroSession.objects.filter(
                usuario=request.user,
                completado=True
            ).count()
            
            # Calcular progreso semanal (comparación con semana anterior)
            hace_14_dias = timezone.now().date() - timedelta(days=14)
            stats_semana_pasada = DailyStats.objects.filter(
                usuario=request.user,
                fecha__gte=hace_14_dias,
                fecha__lt=hace_7_dias
            )
            
            horas_semana_actual = sum(
                stat.tiempo_estudiado_segundos / 3600 
                for stat in stats_semana
            )
            
            horas_semana_pasada = sum(
                stat.tiempo_estudiado_segundos / 3600 
                for stat in stats_semana_pasada
            ) if stats_semana_pasada.exists() else 0
            
            progreso_semanal = 0
            if horas_semana_pasada > 0:
                progreso_semanal = int(((horas_semana_actual - horas_semana_pasada) / horas_semana_pasada) * 100)
            elif horas_semana_actual > 0:
                progreso_semanal = 100
            
            return JsonResponse({
                'success': True,
                'horas_estudiadas': round(horas_estudiadas, 1),
                'racha': profile.racha_actual,
                'nivel': profile.nivel,
                'xp': profile.xp,
                'progreso_semanal': progreso_semanal,
                'pomodoros_hoy': pomodoros_hoy,
                'total_pomodoros': total_pomodoros
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

class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return UserProfile.objects.filter(usuario=self.request.user)
    
    def get_object(self):
        profile, created = UserProfile.objects.get_or_create(
            usuario=self.request.user,
            defaults={
                'xp': 0,
                'nivel': 1,
                'monedas': 100,
                'racha_actual': 0,
                'racha_maxima': 0,
                'misiones_completadas': 0
            }
        )
        return profile
    
    @action(detail=False, methods=['post'])
    def agregar_xp(self, request):
        profile = self.get_object()
        cantidad = request.data.get('cantidad', 0)
        try:
            cantidad = int(cantidad)
            profile.agregar_xp(cantidad)
            return Response({'success': True, 'xp_actual': profile.xp, 'nivel': profile.nivel})
        except (ValueError, TypeError):
            return Response({'success': False, 'error': 'Cantidad inválida'}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def agregar_monedas(self, request):
        profile = self.get_object()
        cantidad = request.data.get('cantidad', 0)
        try:
            cantidad = int(cantidad)
            profile.agregar_monedas(cantidad)
            return Response({'success': True, 'monedas_actuales': profile.monedas})
        except (ValueError, TypeError):
            return Response({'success': False, 'error': 'Cantidad inválida'}, status=status.HTTP_400_BAD_REQUEST)

class MisionViewSet(viewsets.ModelViewSet):
    serializer_class = MisionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Mision.objects.filter(activa=True)
    
    @action(detail=True, methods=['post'])
    def completar(self, request, pk=None):
        mision = self.get_object()
        profile, _ = UserProfile.objects.get_or_create(usuario=request.user)
        
        if MisionCompletada.objects.filter(usuario=request.user, mision=mision).exists():
            return Response({'success': False, 'error': 'Misión ya completada'}, status=status.HTTP_400_BAD_REQUEST)
        
        mision_completada = MisionCompletada.objects.create(
            usuario=request.user,
            mision=mision,
            xp_ganado=mision.xp_recompensa,
            monedas_ganadas=mision.monedas_recompensa
        )
        
        profile.agregar_xp(mision.xp_recompensa)
        profile.agregar_monedas(mision.monedas_recompensa)
        profile.misiones_completadas += 1
        profile.save()
        
        return Response({
            'success': True,
            'xp_ganado': mision.xp_recompensa,
            'monedas_ganadas': mision.monedas_recompensa,
            'xp_total': profile.xp,
            'nivel': profile.nivel,
            'monedas_totales': profile.monedas
        })

class MisionCompletadaViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = MisionCompletadaSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return MisionCompletada.objects.filter(usuario=self.request.user)

class LeccionRapidaViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = LeccionRapidaSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return LeccionRapida.objects.filter(activa=True)

class InsigniaViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = InsigniaSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Insignia.objects.all()

class InsigniaUsuarioViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = InsigniaUsuarioSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return InsigniaUsuario.objects.filter(usuario=self.request.user)

class AccesorioViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AccesorioSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Accesorio.objects.all()
    
    @action(detail=True, methods=['post'])
    def comprar(self, request, pk=None):
        accesorio = self.get_object()
        profile, _ = UserProfile.objects.get_or_create(usuario=request.user)
        
        if AccesorioUsuario.objects.filter(usuario=request.user, accesorio=accesorio).exists():
            return Response({'success': False, 'error': 'Accesorio ya comprado'}, status=status.HTTP_400_BAD_REQUEST)
        
        if profile.monedas < accesorio.precio:
            return Response({'success': False, 'error': 'Monedas insuficientes'}, status=status.HTTP_400_BAD_REQUEST)
        
        if profile.xp < accesorio.xp_requerido:
            return Response({'success': False, 'error': 'XP insuficiente'}, status=status.HTTP_400_BAD_REQUEST)
        
        if accesorio.limitado and accesorio.stock <= 0:
            return Response({'success': False, 'error': 'Sin stock'}, status=status.HTTP_400_BAD_REQUEST)
        
        profile.agregar_monedas(-accesorio.precio)
        accesorio_usuario = AccesorioUsuario.objects.create(
            usuario=request.user,
            accesorio=accesorio
        )
        
        if accesorio.limitado:
            accesorio.stock -= 1
            accesorio.save()
        
        return Response({
            'success': True,
            'monedas_restantes': profile.monedas,
            'accesorio': AccesorioUsuarioSerializer(accesorio_usuario).data
        })

class AccesorioUsuarioViewSet(viewsets.ModelViewSet):
    serializer_class = AccesorioUsuarioSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return AccesorioUsuario.objects.filter(usuario=self.request.user)
    
    @action(detail=True, methods=['post'])
    def equipar(self, request, pk=None):
        accesorio_usuario = self.get_object()
        
        categoria = accesorio_usuario.accesorio.categoria
        AccesorioUsuario.objects.filter(
            usuario=request.user,
            accesorio__categoria=categoria
        ).update(equipado=False)
        
        accesorio_usuario.equipado = True
        accesorio_usuario.save()

# =====================================================
# NUEVAS FUNCIONES PARA EL REDISEÑO
# =====================================================

@csrf_exempt
@login_required
def obtener_metas(request):
    if request.method == 'GET':
        try:
            hoy = timezone.now().date()
            metas = MetaDiaria.objects.filter(usuario=request.user, fecha=hoy)
            metas_data = [
                {
                    'id': str(meta.id),
                    'titulo': meta.titulo,
                    'descripcion': meta.descripcion,
                    'completada': meta.completada,
                    'fecha': meta.fecha.strftime('%d/%m/%Y')
                }
                for meta in metas
            ]
            return JsonResponse({'success': True, 'metas': metas_data})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Método no permitido'})

@csrf_exempt
@login_required
def guardar_meta(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            titulo = data.get('titulo', '')
            descripcion = data.get('descripcion', '')
            
            if not titulo:
                return JsonResponse({'success': False, 'error': 'El título es obligatorio'})
            
            hoy = timezone.now().date()
            ultima_meta = MetaDiaria.objects.filter(usuario=request.user).order_by('-orden').first()
            nuevo_orden = (ultima_meta.orden + 1) if ultima_meta else 0
            
            meta = MetaDiaria.objects.create(
                usuario=request.user,
                titulo=titulo,
                descripcion=descripcion,
                fecha=hoy,
                orden=nuevo_orden
            )
            
            return JsonResponse({
                'success': True,
                'meta': {
                    'id': str(meta.id),
                    'titulo': meta.titulo,
                    'descripcion': meta.descripcion,
                    'completada': meta.completada,
                    'fecha': meta.fecha.strftime('%d/%m/%Y')
                }
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Método no permitido'})

@csrf_exempt
@login_required
def toggle_meta(request, meta_id):
    if request.method == 'POST':
        try:
            meta = MetaDiaria.objects.get(id=meta_id, usuario=request.user)
            meta.completada = not meta.completada
            meta.save()
            return JsonResponse({'success': True, 'completada': meta.completada})
        except MetaDiaria.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Meta no encontrada'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Método no permitido'})

@csrf_exempt
@login_required
def eliminar_meta(request, meta_id):
    if request.method == 'DELETE':
        try:
            meta = MetaDiaria.objects.get(id=meta_id, usuario=request.user)
            meta.delete()
            return JsonResponse({'success': True})
        except MetaDiaria.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Meta no encontrada'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Método no permitido'})

@csrf_exempt
@login_required
def obtener_dias_estudiados(request):
    if request.method == 'GET':
        try:
            # Obtener días con actividad en los últimos 30 días
            hace_30_dias = timezone.now().date() - timedelta(days=30)
            dias_con_actividad = DailyStats.objects.filter(
                usuario=request.user,
                fecha__gte=hace_30_dias,
                tiempo_estudiado_segundos__gt=0
            ).values_list('fecha', flat=True)
            
            dias_formato = [fecha.strftime('%Y-%m-%d') for fecha in dias_con_actividad]
            return JsonResponse({'success': True, 'dias': dias_formato})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Método no permitido'})
