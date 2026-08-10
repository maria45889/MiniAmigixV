import logging

logger = logging.getLogger(__name__)


class GeminiAPI:
    
    @staticmethod
    def generate_response(prompt: str, model: str = "gemini-pro") -> str:
        logger.warning("Gemini API not implemented yet")
        return ""
