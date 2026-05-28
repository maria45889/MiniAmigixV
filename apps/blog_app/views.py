from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.views import View
from .models import Post
import json

def blog_fragment(request):
    # Show both personal and admin posts
    posts = Post.objects.all()
    return render(request, 'blog_app/blog_fragment.html', {'posts': posts})

def personal_blog(request):
    # Show only personal posts
    posts = Post.objects.filter(post_type='personal')
    return render(request, 'blog_app/personal_blog.html', {'posts': posts})

def admin_blog(request):
    # Show only admin posts (news, announcements, etc.)
    posts = Post.objects.filter(post_type='admin')
    return render(request, 'blog_app/admin_blog.html', {'posts': posts})

@csrf_exempt
@require_http_methods(["POST"])
def create_post(request):
    try:
        data = json.loads(request.body)
        titulo = data.get('titulo')
        categoria = data.get('categoria')
        contenido = data.get('contenido')
        autor = data.get('autor', 'Anónimo')
        lectura_min = data.get('lectura_min', 1)
        post_type = data.get('post_type', 'personal')  # Default to personal
        
        if not titulo or not categoria or not contenido:
            return JsonResponse({'success': False, 'error': 'Missing required fields'}, status=400)
        
        post = Post.objects.create(
            titulo=titulo,
            categoria=categoria,
            contenido=contenido,
            autor=autor,
            lectura_min=lectura_min,
            post_type=post_type
        )
        
        return JsonResponse({
            'success': True,
            'post': {
                'id': post.id,
                'titulo': post.titulo,
                'categoria': post.categoria,
                'contenido': post.contenido,
                'autor': post.autor,
                'fecha': post.fecha.strftime('%d/%m/%Y'),
                'lectura_min': post.lectura_min,
                'post_type': post.post_type
            }
        })
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
