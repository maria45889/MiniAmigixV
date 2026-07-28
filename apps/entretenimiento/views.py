from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import ContenidoEntretenimiento, CategoriaEntretenimiento, FavoritoEntretenimiento


@login_required
def entretenimiento_view(request):
    """Vista principal del módulo de entretenimiento"""
    
    # Obtener todas las categorías
    categorias = CategoriaEntretenimiento.objects.all()
    
    # Obtener contenido destacado (recomendación del día)
    contenido_destacado = ContenidoEntretenimiento.objects.filter(
        es_destacado=True
    ).first()
    
    # Si no hay contenido destacado, tomar el mejor calificado
    if not contenido_destacado:
        contenido_destacado = ContenidoEntretenimiento.objects.order_by('-calificacion').first()
    
    # Obtener contenidos por tipo
    peliculas = ContenidoEntretenimiento.objects.filter(tipo='pelicula')[:10]
    series = ContenidoEntretenimiento.objects.filter(tipo='serie')[:10]
    anime = ContenidoEntretenimiento.objects.filter(tipo='anime')[:10]
    libros = ContenidoEntretenimiento.objects.filter(tipo='libro')[:10]
    manga = ContenidoEntretenimiento.objects.filter(tipo='manga')[:10]
    musica = ContenidoEntretenimiento.objects.filter(tipo='musica')[:10]
    podcasts = ContenidoEntretenimiento.objects.filter(tipo='podcast')[:10]
    documentales = ContenidoEntretenimiento.objects.filter(tipo='documental')[:10]
    teatro = ContenidoEntretenimiento.objects.filter(tipo='teatro')[:10]
    
    # Obtener favoritos del usuario
    favoritos_ids = FavoritoEntretenimiento.objects.filter(
        usuario=request.user
    ).values_list('contenido_id', flat=True)
    
    # Preparar contexto con recomendaciones
    recomendaciones = {
        'peliculas': peliculas,
        'series': series,
        'anime': anime,
        'libros': libros,
        'manga': manga,
        'musica': musica,
        'podcasts': podcasts,
        'documentales': documentales,
        'teatro': teatro,
    }
    
    # Si hay contenido destacado, usarlo como primera recomendación de películas
    if contenido_destacado and contenido_destacado.tipo == 'pelicula':
        if contenido_destacado not in peliculas:
            recomendaciones['peliculas'] = [contenido_destacado] + list(peliculas[:9])
    
    context = {
        'categorias': categorias,
        'recomendaciones': recomendaciones,
        'contenido_destacado': contenido_destacado,
        'favoritos_ids': list(favoritos_ids),
    }
    
    return render(request, 'entretenimiento.html', context)


@login_required
def toggle_favorito(request):
    """Vista para agregar/quitar favoritos (AJAX)"""
    import json
    from django.http import JsonResponse
    from django.utils.text import slugify
    
    if request.method == 'POST':
        data = json.loads(request.body)
        contenido_id = data.get('contenido_id')
        
        try:
            # Intentar buscar por ID numérico primero
            try:
                contenido = ContenidoEntretenimiento.objects.get(id=contenido_id)
            except (ValueError, ContenidoEntretenimiento.DoesNotExist):
                # Si falla, buscar por slug del título
                contenido = ContenidoEntretenimiento.objects.filter(
                    titulo__icontains=contenido_id.replace('-', ' ')
                ).first()
                if not contenido:
                    return JsonResponse({'status': 'error', 'message': 'Contenido no encontrado'}, status=404)
            
            favorito, created = FavoritoEntretenimiento.objects.get_or_create(
                usuario=request.user,
                contenido=contenido
            )
            
            if not created:
                # Ya existe, eliminar
                favorito.delete()
                return JsonResponse({'status': 'removed', 'message': 'Eliminado de favoritos'})
            else:
                return JsonResponse({'status': 'added', 'message': 'Agregado a favoritos'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)


@login_required
def obtener_recomendacion_ia(request):
    """Vista para obtener recomendación personalizada por IA"""
    import json
    from django.http import JsonResponse
    import random
    
    if request.method == 'POST':
        # Obtener favoritos del usuario para personalizar
        favoritos = FavoritoEntretenimiento.objects.filter(
            usuario=request.user
        ).select_related('contenido')
        
        # Si el usuario tiene favoritos, obtener géneros preferidos
        generos_preferidos = []
        if favoritos.exists():
            generos_preferidos = list(
                favoritos.values_list('contenido__genero', flat=True).distinct()
            )
        
        # Filtrar contenido basado en preferencias o usar todos
        if generos_preferidos:
            contenidos = ContenidoEntretenimiento.objects.filter(
                genero__in=generos_preferidos
            )
        else:
            contenidos = ContenidoEntretenimiento.objects.all()
        
        # Excluir contenido ya visto/favorito
        if favoritos.exists():
            favoritos_ids = favoritos.values_list('contenido_id', flat=True)
            contenidos = contenidos.exclude(id__in=favoritos_ids)
        
        if contenidos.exists():
            contenido = random.choice(contenidos)
            
            return JsonResponse({
                'status': 'success',
                'contenido': {
                    'titulo': contenido.titulo,
                    'tipo': contenido.get_tipo_display(),
                    'genero': contenido.genero,
                    'descripcion': contenido.descripcion,
                    'imagen': contenido.imagen,
                    'calificacion': str(contenido.calificacion),
                    'trailer': contenido.trailer,
                }
            })
    
    return JsonResponse({'status': 'error', 'message': 'No hay contenido disponible'}, status=404)


@login_required
def buscar_contenido(request):
    """Vista para buscar contenido"""
    import json
    from django.http import JsonResponse
    
    if request.method == 'GET':
        query = request.GET.get('q', '')
        tipo = request.GET.get('tipo', '')
        
        contenidos = ContenidoEntretenimiento.objects.all()
        
        if query:
            contenidos = contenidos.filter(
                titulo__icontains=query
            ) | contenidos.filter(
                genero__icontains=query
            ) | contenidos.filter(
                descripcion__icontains=query
            )
        
        if tipo:
            contenidos = contenidos.filter(tipo=tipo)
        
        resultados = []
        for contenido in contenidos[:20]:
            resultados.append({
                'id': contenido.id,
                'titulo': contenido.titulo,
                'tipo': contenido.get_tipo_display(),
                'genero': contenido.genero,
                'descripcion': contenido.descripcion[:200],
                'imagen': contenido.imagen,
                'calificacion': str(contenido.calificacion),
                'anio': contenido.anio,
            })
        
        return JsonResponse({
            'status': 'success',
            'resultados': resultados,
            'total': len(resultados),
        })
    
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)


@login_required
def listar_favoritos(request):
    """Vista para listar favoritos del usuario"""
    import json
    from django.http import JsonResponse
    
    if request.method == 'GET':
        favoritos = FavoritoEntretenimiento.objects.filter(
            usuario=request.user
        ).select_related('contenido')
        
        resultados = []
        for fav in favoritos:
            contenido = fav.contenido
            resultados.append({
                'id': contenido.id,
                'titulo': contenido.titulo,
                'tipo': contenido.get_tipo_display(),
                'genero': contenido.genero,
                'imagen': contenido.imagen,
                'calificacion': str(contenido.calificacion),
                'fecha_agregado': fav.fecha_agregado.strftime('%Y-%m-%d'),
            })
        
        return JsonResponse({
            'status': 'success',
            'favoritos': resultados,
            'total': len(resultados),
        })
    
    return JsonResponse({'status': 'error', 'message': 'Método no permitido'}, status=405)
