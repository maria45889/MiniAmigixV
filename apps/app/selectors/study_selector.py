"""
Study selector.

Database queries for study operations.
"""

from apps.estudio.models import StudyResource, StudyCategory, StudyProgress


class StudySelector:
    """Selector for study-related queries."""
    
    @staticmethod
    def get_all_categories():
        """Get all study categories."""
        return StudyCategory.objects.all()
    
    @staticmethod
    def get_resources(user):
        """Get resources for user."""
        return StudyResource.objects.filter(usuario=user).select_related('categoria')
    
    @staticmethod
    def get_progress(user):
        """Get study progress for user."""
        return StudyProgress.objects.filter(usuario=user).select_related('recurso')
    
    @staticmethod
    def create_resource(user, title: str, url: str, category_id: int):
        """Create a study resource."""
        return StudyResource.objects.create(
            usuario=user,
            titulo=title,
            url=url,
            categoria_id=category_id
        )
