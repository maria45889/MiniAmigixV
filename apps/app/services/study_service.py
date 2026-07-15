"""
Study service.

Business logic for study operations.
"""

import logging
from typing import Dict

from ..selectors.study_selector import StudySelector
from ..utils import LogHelper

logger = logging.getLogger(__name__)


class StudyService:
    """Service for study-related operations."""
    
    @staticmethod
    def get_study_data(user) -> Dict:
        """Get study data for user."""
        categorias = StudySelector.get_all_categories()
        recursos_usuario = StudySelector.get_resources(user) if user.is_authenticated else []
        progreso_usuario = StudySelector.get_progress(user) if user.is_authenticated else []
        
        return {
            'categorias': categorias,
            'recursos': recursos_usuario,
            'progreso': progreso_usuario
        }
    
    @staticmethod
    def add_resource(user, title: str, url: str, category_id: int):
        """Add a study resource."""
        try:
            resource = StudySelector.create_resource(user, title, url, category_id)
            LogHelper.log_info(logger, f"Recurso agregado: {title}")
            return resource, None
        except Exception as e:
            LogHelper.log_error(logger, f"Error al agregar recurso: {str(e)}", exc_info=True)
            return None, str(e)
