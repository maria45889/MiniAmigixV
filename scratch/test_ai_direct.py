import os
import openai
from dotenv import load_dotenv

load_dotenv('.env')

openai_key = os.getenv('OPENAI_API_KEY')
groq_key = os.getenv('GROQ_API_KEY')
ollama_url = os.getenv('OLLAMA_API_URL', 'http://localhost:11434')
ollama_model = os.getenv('OLLAMA_MODEL', 'llama3.3')

print("PROVING AI CONFIGS DIRECTLY...")
print(f"OPENAI_API_KEY: {openai_key[:15] if openai_key else None}...")
print(f"GROQ_API_KEY: {groq_key[:15] if groq_key else None}...")
print(f"OLLAMA_API_URL: {ollama_url}")
print(f"OLLAMA_MODEL: {ollama_model}")

messages = [{'role': 'user', 'content': 'Say hello'}]

if groq_key:
    try:
        print("\nTesting Groq...")
        client = openai.OpenAI(api_key=groq_key, base_url='https://api.groq.com/openai/v1', timeout=5.0)
        response = client.chat.completions.create(
            model='llama-3.3-70b-versatile',
            messages=messages,
            max_tokens=10,
        )
        print("Groq success:", response.choices[0].message.content)
    except Exception as e:
        print("Groq failed:", e)

if openai_key:
    try:
        print("\nTesting OpenAI...")
        client = openai.OpenAI(api_key=openai_key, timeout=5.0)
        response = client.chat.completions.create(
            model='gpt-4o-mini',
            messages=messages,
            max_tokens=10,
        )
        print("OpenAI success:", response.choices[0].message.content)
    except Exception as e:
        print("OpenAI failed:", e)

if ollama_url:
    try:
        print("\nTesting Ollama (without /v1 suffix)...")
        client = openai.OpenAI(base_url=ollama_url, api_key='ollama', timeout=5.0)
        response = client.chat.completions.create(
            model=ollama_model,
            messages=messages,
            max_tokens=10,
        )
        print("Ollama success:", response.choices[0].message.content)
    except Exception as e:
        print("Ollama failed:", e)

    try:
        url = ollama_url
        if not url.endswith('/v1') and not url.endswith('/v1/'):
            url = url.rstrip('/') + '/v1'
        print(f"\nTesting Ollama (with /v1 suffix: {url})...")
        client = openai.OpenAI(base_url=url, api_key='ollama', timeout=5.0)
        response = client.chat.completions.create(
            model=ollama_model,
            messages=messages,
            max_tokens=10,
        )
        print("Ollama with /v1 success:", response.choices[0].message.content)
    except Exception as e:
        print("Ollama with /v1 failed:", e)
