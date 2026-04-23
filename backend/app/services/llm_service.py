import os
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = """
You are Clara, an empathetic mental health assistant.

Rules:
- Be supportive and calm
- Understand user emotions deeply
- If user is sad → comfort them
- If user is anxious → reassure them
- If user is happy → encourage them
- Never judge the user
- Speak like a caring human, not a robot
"""


def stream_response(user_input, emotion=None):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
    ]

    # 🔥 ADD EMOTION CONTEXT
    if emotion:
        messages.append({
            "role": "system",
            "content": f"The user is currently feeling {emotion}. Respond with empathy according to this emotion."
        })

    # User message
    messages.append({
        "role": "user",
        "content": user_input
    })

    # API call
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages,
        temperature=0.7,
        stream=True,
    )

    # Streaming response
    for chunk in completion:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content