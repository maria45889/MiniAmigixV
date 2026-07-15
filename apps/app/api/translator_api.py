"""
Translator API integration.
"""

import logging
import requests

logger = logging.getLogger(__name__)


class TranslatorAPI:
    """Service for translation API interactions."""
    
    @staticmethod
    def translate(text: str, target_language: str, source_language: str = "auto") -> str:
        """
        Translate text to target language.
        
        Args:
            text: Text to translate
            target_language: Target language code
            source_language: Source language code (auto for auto-detect)
            
        Returns:
            Translated text
        """
        from django.conf import settings
        
        api_key = getattr(settings, 'GOOGLE_TRANSLATE_API_KEY', None)
        if not api_key:
            # Fallback to simple placeholder
            logger.warning("Google Translate API key not configured, using placeholder")
            return f"[Translated to {target_language}]: {text}"
        
        try:
            url = f"https://translation.googleapis.com/language/translate/v2"
            params = {
                'key': api_key,
                'q': text,
                'target': target_language,
                'source': source_language if source_language != 'auto' else None
            }
            
            response = requests.post(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            return data['data']['translations'][0]['translatedText']
            
        except Exception as e:
            logger.error(f"Error translating text: {e}")
            raise
    
    @staticmethod
    def detect_language(text: str) -> str:
        """
        Detect language of text.
        
        Args:
            text: Text to analyze
            
        Returns:
            Language code
        """
        from django.conf import settings
        
        api_key = getattr(settings, 'GOOGLE_TRANSLATE_API_KEY', None)
        if not api_key:
            # Fallback to simple placeholder
            logger.warning("Google Translate API key not configured, using placeholder")
            return "auto"
        
        try:
            url = f"https://translation.googleapis.com/language/translate/v2/detect"
            params = {
                'key': api_key,
                'q': text
            }
            
            response = requests.post(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            return data['data']['detections'][0][0]['language']
            
        except Exception as e:
            logger.error(f"Error detecting language: {e}")
            raise
