import sys
import types
import unittest
from types import SimpleNamespace
from unittest.mock import patch

import openai

fake_models = types.ModuleType("apps.app.models")
fake_models.ConversacionChat = type("ConversacionChat", (), {})
fake_models.MensajeChat = type("MensajeChat", (), {})
fake_models.Cancion = type("Cancion", (), {})
fake_models.Playlist = type("Playlist", (), {})
fake_models.Favorite = type("Favorite", (), {})
fake_models.Game = type("Game", (), {})
fake_models.Score = type("Score", (), {})
fake_models.Achievement = type("Achievement", (), {})
fake_models.UserAchievement = type("UserAchievement", (), {})
fake_models.EstadoAnimo = type("EstadoAnimo", (), {})
fake_models.RecomendacionEntretenimiento = type("RecomendacionEntretenimiento", (), {})
sys.modules.setdefault("apps.app.models", fake_models)

from apps.app import views


class AiProviderFallbackTests(unittest.TestCase):
    def test_falls_back_to_openai_when_groq_auth_fails(self):
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
                if self.kwargs.get("base_url") == "https://api.groq.com/openai/v1":
                    raise openai.AuthenticationError("invalid groq key")
                return SimpleNamespace(
                    choices=[SimpleNamespace(message=SimpleNamespace(content="respuesta desde openai"))]
                )

        settings_obj = SimpleNamespace(
            OPENAI_API_KEY="openai-key",
            GROQ_API_KEY="groq-key",
            OLLAMA_API_URL="http://localhost:11434",
            OLLAMA_MODEL="llama3.3",
        )

        with patch.object(views.openai, "OpenAI", side_effect=lambda **kwargs: FakeOpenAIClient(**kwargs)):
            response = views.generate_ai_response(
                messages=[{"role": "user", "content": "hola"}],
                settings_obj=settings_obj,
                imagen=False,
                max_tokens=60,
            )

        self.assertEqual(response, "respuesta desde openai")
