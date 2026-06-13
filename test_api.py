import os
import json
import requests
import openai
from dotenv import load_dotenv

load_dotenv()

youtube_key = os.getenv("YOUTUBE_API_KEY")
groq_key = os.getenv("GROQ_API_KEY")

print(f"YOUTUBE_API_KEY present: {bool(youtube_key)}")
print(f"GROQ_API_KEY present: {bool(groq_key)}")

# Test YouTube
if youtube_key:
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        'part': 'snippet',
        'q': 'tráilers películas 2025 2026',
        'type': 'video',
        'maxResults': 4,
        'key': youtube_key,
        'regionCode': 'ES',
        'relevanceLanguage': 'es'
    }
    headers = {'Referer': 'http://localhost:8000/'}
    resp = requests.get(url, params=params, headers=headers, timeout=10)
    print(f"YouTube status code: {resp.status_code}")
    if resp.status_code != 200:
        print(f"YouTube error response: {resp.text}")

# Test Groq
if groq_key:
    try:
        client = openai.OpenAI(api_key=groq_key, base_url="https://api.groq.com/openai/v1")
        prompt = "Recomienda 4 libros populares en español de diferentes géneros. Devuelve SOLO JSON con formato: [{\"titulo\": \"...\", \"autor\": \"...\", \"descripcion\": \"...\"}]. Sin markdown ni explicaciones."
        response = client.chat.completions.create(model="llama-3.3-70b-versatile", messages=[{"role": "user", "content": prompt}], max_tokens=500)
        print("Groq success:")
        print(response.choices[0].message.content)
    except Exception as e:
        print(f"Groq exception: {e}")
