import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
import django
django.setup()

from unittest.mock import patch
import openai
from apps.app.views import generate_ai_response

class FakeOpenAIClient:
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    @property
    def chat(self):
        return self

    @property
    def completions(self):
        return self

    def create(self, **kwargs):
        if self.kwargs.get('base_url') == 'https://api.groq.com/openai/v1':
            raise openai.AuthenticationError('invalid groq key')
        return type('Resp', (), {'choices': [type('Choice', (), {'message': type('Message', (), {'content': 'respuesta desde openai'})()})()]})()

class SettingsStub:
    OPENAI_API_KEY = 'openai-key'
    GROQ_API_KEY = 'groq-key'
    OLLAMA_API_URL = 'http://localhost:11434'
    OLLAMA_MODEL = 'llama3.3'

with patch('apps.app.views.openai.OpenAI', side_effect=lambda **kwargs: FakeOpenAIClient(**kwargs)):
    result = generate_ai_response(
        messages=[{'role': 'user', 'content': 'hola'}],
        settings_obj=SettingsStub(),
        imagen=False,
        max_tokens=20,
    )
    print(result)
