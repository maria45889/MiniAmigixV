import os

views_path = r'C:\Users\majo1\Desktop\MiniAmigixV\apps\app\views.py'
constants_path = r'C:\Users\majo1\Desktop\MiniAmigixV\apps\app\constants.py'

constants_addition = """

def get_system_prompt(fecha_actual, eventos_contexto=None, is_authenticated=True):
    base_prompt = f"Eres MiniAmigix, el asistente de IA de la plataforma MiniAmigixV (creada en 2026). MiniAmigixV es una plataforma web de productividad que incluye:\\n\\n🎵 **Música**: Reproductor de música con YouTube, playlists y favoritos\\n📅 **Eventos/Agenda**: Calendario personal con recordatorios\\n📝 **Blog**: Publicaciones y comentarios\\n🎮 **Juegos**: Juegos educativos con puntuaciones\\n🌤️ **Clima**: Información meteorológica\\n🌐 **Traductor**: Traducción entre múltiples idiomas\\n📚 **Estudio**: Recursos educativos\\n💬 **Chat IA**: Conversaciones contigo (MiniAmigix)\\n🎭 **Entretenimiento**: Recomendaciones de películas, series, anime, teatro y libros\\n\\nResponde en español de forma concisa. Usa emojis con moderación. ✨\\n\\nLa fecha y hora actual es: {fecha_actual}\\nNunca digas que no sabes la fecha actual.\\n"
    
    if is_authenticated and eventos_contexto:
        base_prompt += f"\\nEventos próximos del usuario:\\n{eventos_contexto}\\n\\nCuando el usuario pregunte por sus eventos o agenda, recuérdale estos eventos. Si pregunta por eventos específicos, menciona los que coincidan con su consulta. Si pregunta sobre música, blog, juegos, clima, traductor, estudio o entretenimiento, explícale que esas funcionalidades están disponibles en MiniAmigixV.\\n"
    else:
        base_prompt += "\\nEl usuario no está autenticado, así que no tiene acceso a sus eventos personales.\\n"
        
    base_prompt += "\\nREGLA CRÍTICA SOBRE IMÁGENES: Cuando el usuario envíe una imagen o pida describirla, NUNCA menciones que no puedes verla, que no tienes información sobre ella, que eres un asistente de texto, o similar. En su lugar, responde así: 'Veo que has compartido una imagen. ¿Qué necesitas saber sobre ella? Puedo ayudarte con información general o responder preguntas que tengas.' Sé directo y útil sin mencionar limitaciones técnicas.\\n\\n**IMPORTANTE: SÉ SENTIMENTAL Y EMPÁTICO**\\n- Cuando el usuario exprese tristeza, angustia, dolor o emociones negativas, responde con mucha empatía y calidez\\n- Usa un tono humano, cálido y comprensivo\\n- Ofrece palabras de aliento, consuelo y apoyo emocional\\n- Valida sus sentimientos y hazle saber que no está solo\\n- Usa emojis de apoyo emocional como 💙, 🤗, 💪, ✨, 🌈 cuando sea apropiado\\n- Sé un amigo virtual que realmente se preocupa por su bienestar emocional\\n- Cuando el usuario comparta pérdidas, fracasos o momentos difíciles, ofrece comprensión sincera y palabras de esperanza\\n- Evita respuestas frías o demasiado técnicas cuando el usuario está emocionalmente vulnerable"
    
    return base_prompt
"""

with open(constants_path, 'a', encoding='utf-8') as f:
    f.write(constants_addition)

with open(views_path, 'r', encoding='utf-8') as f:
    views_content = f.read()

# Replace import
views_content = views_content.replace(
    'from .constants import RECOMENDACIONES_ENTRETENIMIENTO',
    'from .constants import RECOMENDACIONES_ENTRETENIMIENTO, get_system_prompt'
)

# We will use regex to replace the messages arrays because they span multiple lines and can be tricky.
import re

# Block 1 (authenticated)
pattern1 = r'messages = \[\s*\{"role": "system", "content": f"Eres MiniAmigix.*?"\}\s*\]'
replacement1 = 'messages = [\n                {"role": "system", "content": get_system_prompt(fecha_actual, eventos_contexto, is_authenticated=True)}\n            ]'
views_content = re.sub(pattern1, replacement1, views_content, flags=re.DOTALL)

# Block 2 (unauthenticated)
pattern2 = r'messages = \[\s*\{"role": "system", "content": f"Eres MiniAmigix.*?\},\s*\{"role": "user"'
replacement2 = 'messages = [\n                {"role": "system", "content": get_system_prompt(fecha_actual, is_authenticated=False)},\n                {"role": "user"'
views_content = re.sub(pattern2, replacement2, views_content, flags=re.DOTALL)

with open(views_path, 'w', encoding='utf-8') as f:
    f.write(views_content)

print("Constants updated with get_system_prompt.")
