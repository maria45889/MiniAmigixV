from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q, Count
from django.core.paginator import Paginator
from .models import Category, Tutorial, Step, TutorialProgress, FAQ


def tutorial_home(request):
    """Página principal de tutoriales"""
    categories = Category.objects.all()
    featured_tutorials = Tutorial.objects.filter(featured=True, is_active=True)
    recent_tutorials = Tutorial.objects.filter(is_active=True)[:6]
    
    context = {
        'categories': categories,
        'featured_tutorials': featured_tutorials,
        'recent_tutorials': recent_tutorials,
    }
    return render(request, 'tutorial/home.html', context)


def tutorial_list(request):
    """Lista de todos los tutoriales con filtros"""
    tutorials = Tutorial.objects.filter(is_active=True)
    categories = Category.objects.all()
    
    # Filtros
    category_slug = request.GET.get('category')
    difficulty = request.GET.get('difficulty')
    search = request.GET.get('search')
    
    if category_slug:
        tutorials = tutorials.filter(category__name=category_slug)
    
    if difficulty:
        tutorials = tutorials.filter(difficulty=difficulty)
    
    if search:
        tutorials = tutorials.filter(
            Q(title__icontains=search) | Q(description__icontains=search)
        )
    
    # Paginación
    paginator = Paginator(tutorials, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'selected_category': category_slug,
        'selected_difficulty': difficulty,
        'search_query': search,
    }
    return render(request, 'tutorial/list.html', context)


def tutorial_detail(request, tutorial_id):
    """Detalle de un tutorial específico"""
    tutorial = get_object_or_404(Tutorial, id=tutorial_id, is_active=True)
    steps = tutorial.steps.all()
    
    # Incrementar vistas
    tutorial.views += 1
    tutorial.save()
    
    # Obtener progreso del usuario si está autenticado
    user_progress = None
    if request.user.is_authenticated:
        user_progress, created = TutorialProgress.objects.get_or_create(
            user=request.user,
            tutorial=tutorial,
            defaults={'current_step': steps.first() if steps else None}
        )
    
    context = {
        'tutorial': tutorial,
        'steps': steps,
        'user_progress': user_progress,
    }
    return render(request, 'tutorial/detail.html', context)


@login_required
def tutorial_step(request, tutorial_id, step_order):
    """Ver un paso específico del tutorial"""
    tutorial = get_object_or_404(Tutorial, id=tutorial_id, is_active=True)
    step = get_object_or_404(Step, tutorial=tutorial, order=step_order)
    
    # Obtener o crear progreso
    progress, created = TutorialProgress.objects.get_or_create(
        user=request.user,
        tutorial=tutorial,
        defaults={'current_step': step}
    )
    
    # Actualizar paso actual
    progress.current_step = step
    progress.save()
    
    # Obtener pasos anterior y siguiente
    prev_step = Step.objects.filter(tutorial=tutorial, order=step_order - 1).first()
    next_step = Step.objects.filter(tutorial=tutorial, order=step_order + 1).first()
    
    context = {
        'tutorial': tutorial,
        'step': step,
        'progress': progress,
        'prev_step': prev_step,
        'next_step': next_step,
    }
    return render(request, 'tutorial/step.html', context)


@login_required
def complete_step(request, tutorial_id, step_order):
    """Marcar un paso como completado"""
    if request.method == 'POST':
        tutorial = get_object_or_404(Tutorial, id=tutorial_id, is_active=True)
        step = get_object_or_404(Step, tutorial=tutorial, order=step_order)
        
        progress = get_object_or_404(TutorialProgress, user=request.user, tutorial=tutorial)
        
        # Mover al siguiente paso
        next_step = Step.objects.filter(tutorial=tutorial, order=step_order + 1).first()
        
        if next_step:
            progress.current_step = next_step
        else:
            # Tutorial completado
            progress.completed = True
            progress.completed_at = timezone.now()
        
        progress.save()
        
        return JsonResponse({
            'success': True,
            'next_step_id': next_step.id if next_step else None,
            'tutorial_completed': progress.completed
        })
    
    return JsonResponse({'success': False}, status=400)


@login_required
def rate_tutorial(request, tutorial_id):
    """Calificar un tutorial"""
    if request.method == 'POST':
        tutorial = get_object_or_404(Tutorial, id=tutorial_id, is_active=True)
        rating = int(request.POST.get('rating', 0))
        
        if 1 <= rating <= 5:
            progress, created = TutorialProgress.objects.get_or_create(
                user=request.user,
                tutorial=tutorial
            )
            progress.rating = rating
            progress.save()
            
            return JsonResponse({'success': True, 'average_rating': tutorial.average_rating})
    
    return JsonResponse({'success': False}, status=400)


@login_required
def save_notes(request, tutorial_id):
    """Guardar notas personales del tutorial"""
    if request.method == 'POST':
        tutorial = get_object_or_404(Tutorial, id=tutorial_id, is_active=True)
        notes = request.POST.get('notes', '')
        
        progress, created = TutorialProgress.objects.get_or_create(
            user=request.user,
            tutorial=tutorial
        )
        progress.notes = notes
        progress.save()
        
        return JsonResponse({'success': True})
    
    return JsonResponse({'success': False}, status=400)


@login_required
def my_tutorials(request):
    """Tutoriales del usuario"""
    progress_list = TutorialProgress.objects.filter(user=request.user).select_related('tutorial')
    
    # Filtros
    status = request.GET.get('status')  # 'in_progress', 'completed', 'all'
    
    if status == 'in_progress':
        progress_list = progress_list.filter(completed=False)
    elif status == 'completed':
        progress_list = progress_list.filter(completed=True)
    
    context = {
        'progress_list': progress_list,
        'selected_status': status,
    }
    return render(request, 'tutorial/my_tutorials.html', context)


def category_tutorials(request, category_id):
    """Tutoriales por categoría"""
    category = get_object_or_404(Category, id=category_id)
    tutorials = Tutorial.objects.filter(category=category, is_active=True)
    
    context = {
        'category': category,
        'tutorials': tutorials,
    }
    return render(request, 'tutorial/category.html', context)


def faq_list(request):
    """Lista de FAQs"""
    faqs = FAQ.objects.all()
    categories = Category.objects.all()
    
    category_id = request.GET.get('category')
    if category_id:
        faqs = faqs.filter(category_id=category_id)
    
    context = {
        'faqs': faqs,
        'categories': categories,
        'selected_category': category_id,
    }
    return render(request, 'tutorial/faq.html', context)


def faq_helpful(request, faq_id):
    """Marcar FAQ como útil/no útil"""
    if request.method == 'POST':
        faq = get_object_or_404(FAQ, id=faq_id)
        helpful = request.POST.get('helpful') == 'true'
        
        if helpful:
            faq.helpful_count += 1
        else:
            faq.not_helpful_count += 1
        
        faq.save()
        
        return JsonResponse({'success': True})
    
    return JsonResponse({'success': False}, status=400)
