import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / ".env")

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY missing in backend/.env")

client = Groq(api_key=api_key)


def generate_response_stream(message: str, emotion: str = "neutral", memory_context: str = ""):
    prompt = f"""
You are Clara, an emotion-aware AI companion for dementia care.

Patient Memory:
{memory_context}

Current Emotion:
{emotion}

User Message:
{message}

Rules:
- Use simple, warm, short sentences.
- Be calm and supportive.
- Do not give medical diagnosis.
- If user is confused, guide gently.
- If user is sad or scared, comfort them.
- If user asks for songs/music, respond warmly and mention their preferences.
"""

    stream = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.6,
        stream=True,
    )

    for chunk in stream:
        content = chunk.choices[0].delta.content
        if content:
            yield content