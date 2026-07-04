import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))
sys.path.insert(0, str(BASE_DIR / 'apps'))

os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'
import django
django.setup()

from django.conf import settings
import openai

print("PROVING AI CONFIGS...")
print(f"OPENAI_API_KEY: {settings.OPENAI_API_KEY[:15] if settings.OPENAI_API_KEY else None}...")
print(f"GROQ_API_KEY: {settings.GROQ_API_KEY[:15] if settings.GROQ_API_KEY else None}...")
print(f"OLLAMA_API_URL: {settings.OLLAMA_API_URL}")
print(f"OLLAMA_MODEL: {settings.OLLAMA_MODEL}")

messages = [{'role': 'user', 'content': 'Say hello'}]

# Test Groq
if settings.GROQ_API_KEY:
    try:
        print("\nTesting Groq...")
        client = openai.OpenAI(api_key=settings.GROQ_API_KEY, base_url='https://api.groq.com/openai/v1')
        response = client.chat.completions.create(
            model='llama-3.3-70b-versatile',
            messages=messages,
            max_tokens=10,
        )
        print("Groq success:", response.choices[0].message.content)
    except Exception as e:
        print("Groq failed:", e)

# Test OpenAI
if settings.OPENAI_API_KEY:
    try:
        print("\nTesting OpenAI...")
        client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        response = client.chat.completions.create(
            model='gpt-4o-mini',
            messages=messages,
            max_tokens=10,
        )
        print("OpenAI success:", response.choices[0].message.content)
    except Exception as e:
        print("OpenAI failed:", e)

# Test Ollama
if settings.OLLAMA_API_URL:
    try:
        print("\nTesting Ollama (without /v1 suffix)...")
        client = openai.OpenAI(base_url=settings.OLLAMA_API_URL, api_key='ollama')
        response = client.chat.completions.create(
            model=settings.OLLAMA_MODEL,
            messages=messages,
            max_tokens=10,
        )
        print("Ollama success:", response.choices[0].message.content)
    except Exception as e:
        print("Ollama failed:", e)

    try:
        url = settings.OLLAMA_API_URL
        if not url.endswith('/v1') and not url.endswith('/v1/'):
            url = url.rstrip('/') + '/v1'
        print(f"\nTesting Ollama (with /v1 suffix: {url})...")
        client = openai.OpenAI(base_url=url, api_key='ollama')
        response = client.chat.completions.create(
            model=settings.OLLAMA_MODEL,
            messages=messages,
            max_tokens=10,
        )
        print("Ollama with /v1 success:", response.choices[0].message.content)
    except Exception as e:
        print("Ollama with /v1 failed:", e)
