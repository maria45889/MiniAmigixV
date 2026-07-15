"""
Entertainment service.

Business logic for entertainment recommendations.
"""

import logging
from typing import Dict, List

from ..constants.entertainment import ENTERTAINMENT_RECOMMENDATIONS, MOOD_ENTERTAINMENT

logger = logging.getLogger(__name__)


class EntertainmentService:
    """Service for entertainment-related operations."""
    
    @staticmethod
    def get_recommendations(category: str = None, genre: str = None) -> Dict:
        """Get entertainment recommendations."""
        if category and category in ENTERTAINMENT_RECOMMENDATIONS:
            if genre and genre in ENTERTAINMENT_RECOMMENDATIONS[category]:
                return {category: {genre: ENTERTAINMENT_RECOMMENDATIONS[category][genre]}}
            return {category: ENTERTAINMENT_RECOMMENDATIONS[category]}
        return ENTERTAINMENT_RECOMMENDATIONS
    
    @staticmethod
    def get_mood_recommendations(mood: str) -> Dict:
        """Get recommendations based on mood."""
        if mood and mood in MOOD_ENTERTAINMENT:
            return MOOD_ENTERTAINMENT[mood]
        return MOOD_ENTERTAINMENT
