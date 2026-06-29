from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Post, Category, Comment


def blog(request):
    noticias_globales = Post.objects.filter(
        es_oficial=True,
        publicado=True
    )
    if not request.user.is_staff:
        noticias_globales = noticias_globales.filter(visible_para_todos=True)
    
    mis_publicaciones = []
    if request.user.is_authenticated:
        mis_publicaciones = Post.objects.filter(
            usuario=request.user,
            publicado=True,
            es_oficial=False
        )
    
    categorias = Category.objects.all()
    
    for publicacion in noticias_globales:
        publicacion.comentarios_lista = publicacion.comentarios.all()[:5]
    
    for publicacion in mis_publicaciones:
        publicacion.comentarios_lista = publicacion.comentarios.all()[:5]
    
    return render(request, 'blog/blog.html', {
        'noticias_globales': noticias_globales,
        'mis_publicaciones': mis_publicaciones,
        'categorias': categorias
    })


@login_required
def crear_publicacion(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo', '').strip()
        contenido = request.POST.get('contenido', '').strip()
        categoria = request.POST.get('categoria', 'personal')
        imagen = request.FILES.get('imagen')
        
        # Debug: imprimir datos recibidos
        print(f"DEBUG - Título: '{titulo}' (len: {len(titulo)})")
        print(f"DEBUG - Contenido: '{contenido[:50]}...' (len: {len(contenido)})")
        print(f"DEBUG - Categoría: {categoria}")
        print(f"DEBUG - Usuario: {request.user.username}")
        print(f"DEBUG - POST keys: {list(request.POST.keys())}")
        
        if not titulo or not contenido:
            print("ERROR: Título o contenido vacío")
            from django.contrib import messages
            messages.error(request, 'El título y el contenido son obligatorios')
            return redirect('blog')
        
        es_oficial = False
        fijado = False
        visible_para_todos = request.POST.get('visible_para_todos') == 'on'
        
        if request.user.is_staff:
            es_oficial = request.POST.get('es_oficial') == 'on'
            fijado = request.POST.get('fijado') == 'on'
        else:
            if categoria in ['mantenimiento', 'actualizaciones', 'avisos_urgentes']:
                categoria = 'personal'
        
        try:
            post = Post.objects.create(
                usuario=request.user,
                titulo=titulo,
                contenido=contenido,
                imagen=imagen,
                categoria=categoria,
                es_oficial=es_oficial,
                fijado=fijado,
                visible_para_todos=visible_para_todos
            )
            print(f"SUCCESS: Post creado con ID {post.id}")
            from django.contrib import messages
            messages.success(request, 'Publicación creada exitosamente')
            return redirect('blog')
        except Exception as e:
            print(f"ERROR al crear post: {str(e)}")
            import traceback
            traceback.print_exc()
            from django.contrib import messages
            messages.error(request, f'Error al crear la publicación: {str(e)}')
            return redirect('blog')
    
    return redirect('blog')


@login_required
def eliminar_publicacion(request, post_id):
    if request.method == 'POST':
        try:
            publicacion = Post.objects.get(id=post_id, usuario=request.user)
            publicacion.delete()
        except Post.DoesNotExist:
            pass
    return redirect('blog')


@require_http_methods(["DELETE"])
@login_required
def delete_publicacion_api(request, post_id):
    try:
        publicacion = Post.objects.get(id=post_id, usuario=request.user)
        publicacion.delete()
        return JsonResponse({'success': True})
    except Post.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Publicación no encontrada'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@require_http_methods(["POST"])
@login_required
def crear_comentario(request):
    try:
        data = json.loads(request.body)
        post_id = data.get('post_id')
        contenido = data.get('contenido', '').strip()
        padre_id = data.get('padre_id', None)
        
        if not contenido:
            return JsonResponse({'error': 'El contenido es requerido'}, status=400)
        
        post = Post.objects.get(id=post_id, publicado=True)
        
        comentario = Comment.objects.create(
            post=post,
            usuario=request.user,
            contenido=contenido
        )
        
        if padre_id:
            comentario.padre = Comment.objects.get(id=padre_id)
            comentario.save()
        
        return JsonResponse({
            'success': True,
            'comentario_id': comentario.id,
            'usuario': request.user.username,
            'contenido': contenido,
            'fecha': comentario.fecha_creacion.strftime('%d/%m/%Y %H:%M')
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(["POST"])
@login_required
def crear_categoria(request):
    if not request.user.is_staff:
        return JsonResponse({'error': 'No autorizado'}, status=403)
    
    try:
        data = json.loads(request.body)
        nombre = data.get('nombre', '').strip()
        icono = data.get('icono', '📁')
        descripcion = data.get('descripcion', '').strip()
        
        if not nombre:
            return JsonResponse({'error': 'El nombre es requerido'}, status=400)
        
        categoria = Category.objects.create(
            nombre=nombre,
            icono=icono,
            descripcion=descripcion
        )
        
        return JsonResponse({
            'success': True,
            'categoria_id': categoria.id,
            'nombre': categoria.nombre,
            'icono': categoria.icono
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(["DELETE"])
@login_required
def eliminar_categoria(request, categoria_id):
    if not request.user.is_staff:
        return JsonResponse({'error': 'No autorizado'}, status=403)
    
    try:
        categoria = Category.objects.get(id=categoria_id)
        categoria.delete()
        return JsonResponse({'success': True})
    except Category.DoesNotExist:
        return JsonResponse({'error': 'Categoría no encontrada'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
