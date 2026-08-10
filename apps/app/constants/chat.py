"""
Chat constants.
"""

CHAT_CONFIG = {
    'max_history_messages': 3,
    'max_tokens': 150,
    'default_conversation_title': 'Chat Principal',
    'image_upload_path': 'chat_images/',
    'notification_title': '💬 Nueva respuesta del Chat IA',
    'notification_message_prefix': 'MiniAmigix ha respondido: "',
    'notification_message_suffix': '..."',
    'notification_link': '/chat/'
}

EVENT_CONFIG = {
    'upcoming_days': 5,
    'clock_widget_days': 3,
    'clock_widget_limit': 3
}

DEFAULT_IMAGE_MESSAGE = "Por favor, describe lo que ves en esta imagen o dime qué necesitas saber sobre ella."
