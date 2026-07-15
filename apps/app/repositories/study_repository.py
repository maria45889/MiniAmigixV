"""
Study repository.

Data access layer for study operations.
"""

from estudio.models import StudyResource, StudyProgress


class StudyRepository:
    """Repository for study data access."""
    
    @staticmethod
    def save_resource(resource):
        """Save resource to database."""
        resource.save()
        return resource
    
    @staticmethod
    def save_progress(progress):
        """Save progress to database."""
        progress.save()
        return progress
