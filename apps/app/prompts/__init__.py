"""
Prompts module.

Contains AI system prompts for different functionalities.
"""

from .chat import CHAT_SYSTEM_PROMPT
from .translator import TRANSLATOR_SYSTEM_PROMPT
from .study import STUDY_SYSTEM_PROMPT
from .entertainment import ENTERTAINMENT_SYSTEM_PROMPT

__all__ = [
    'CHAT_SYSTEM_PROMPT',
    'TRANSLATOR_SYSTEM_PROMPT',
    'STUDY_SYSTEM_PROMPT',
    'ENTERTAINMENT_SYSTEM_PROMPT'
]
