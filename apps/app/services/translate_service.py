"""
Translate service.

Business logic for translation operations.
"""

import logging
from typing import Optional

from ..api.translator_api import TranslatorAPI
from ..utils import LogHelper

logger = logging.getLogger(__name__)


class TranslateService:
    """Service for translation operations."""
    
    @staticmethod
    def translate_text(text: str, target_language: str, source_language: str = "auto") -> Optional[str]:
        """Translate text to target language."""
        try:
            return TranslatorAPI.translate(text, target_language, source_language)
        except Exception as e:
            LogHelper.log_error(logger, f"Error al traducir: {str(e)}", exc_info=True)
            return None
    
    @staticmethod
    def detect_language(text: str) -> Optional[str]:
        """Detect language of text."""
        try:
            return TranslatorAPI.detect_language(text)
        except Exception as e:
            LogHelper.log_error(logger, f"Error al detectar idioma: {str(e)}", exc_info=True)
            return None
