"""
Study views.
"""

from django.shortcuts import render

from apps.app.services import StudyService


def estudio(request):
    """Render study page."""
    study_data = StudyService.get_study_data(request.user)
    
    return render(request, 'estudio.html', {
        'categorias': study_data['categorias'],
        'recursos': study_data['recursos'],
        'progreso': study_data['progreso']
    })
