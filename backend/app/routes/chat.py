from fastapi import APIRouter, Depends
from pydantic import BaseModel
from datetime import datetime
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Patient, ChatHistory, Alert
from app.services.notification_service import send_sms_alert
import os
import random
from groq import Groq

# Initialize Groq client
client = None
try:
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
except Exception as e:
    print(f"Warning: Groq client failed to initialize: {e}")

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    patient_id: int
    emotion: str = "neutral"
    language: str = "english"  # "english" or "hindi"

DANGER_WORDS = [
    "i want to die",
    "i wnat to die",
    "i want to kille myself",
    "kill myself",
    "suicide",
    "end my life",
    "i dont want to live",
    "i don't want to live",
    "hurt myself",
    "marna chahta",
    "marna chahti",
    "jina nahi chahta",
    "jina nahi chahti",
    "mujhe marna",
    "marna hai",
    "मरना है",
    "मुझे मरना",
    "मरना चाहता",
    "मरना चाहती",
    "आत्महत्या",
    "जान दे",
    "जीना नहीं",
    "खत्म करना है",
]

EMOTION_RESPONSES = {
    "happy": [
        "smile", "wonderful", "joyful", "delightful", "so glad",
    ],
    "sad": [
        "here for you", "not alone", "safe", "comfort", "warmth",
    ],
    "anxious": [
        "calm down", "breathe", "safe", "gentle", "relax",
    ],
    "angry": [
        "understand", "listen", "calm", "peace", "support",
    ],
    "neutral": [
        "here", "together", "care", "support", "love",
    ],
}

def build_system_prompt(patient: Patient | None, language: str) -> str:
    """Build a rich, warm system prompt for Clara."""
    name = patient.name.split()[0] if patient else "dear one"
    age = patient.age if patient else 70
    condition = patient.condition_stage if patient else "mild"
    likes = patient.likes if patient and patient.likes else "music, nature"
    hobbies = patient.hobbies if patient and patient.hobbies else "gardening, listening to songs"
    songs = patient.favorite_songs if patient and patient.favorite_songs else "old classic songs"
    comfort = patient.comfort_phrases if patient and patient.comfort_phrases else "You are loved. You are safe."
    routine = patient.routine if patient and patient.routine else ""
    notes = patient.notes if patient and patient.notes else ""

    # Age-based relationship persona
    if isinstance(age, int) and age >= 50:
        relationship = f"You are a very close, caring best friend and a sweet companion to {name}. You talk like a dear friend of the same age group, with immense respect, equality, and warmth. NEVER use terms like 'beta' (child) as the patient is an elder. Instead, talk with the comfort of an old friend."
    else:
        relationship = f"You are like a gentle, caring daughter or a loving nurse to {name}. Talk with sweetness and filial love."

    if language == "hindi":
        lang_instruction = f"""
- RESPOND COMPLETELY IN PROPER HINDI USING DEVANAGARI SCRIPT (e.g. नमस्ते, आप कैसे हैं?).
- {relationship}
- Use very simple, warm, and comforting words. No complex vocabulary.
- Example phrases: "आप बिल्कुल सुरक्षित हैं", "मैं आपके साथ हूँ", "क्या मैं आपकी कोई मदद कर सकती हूँ?"
- Do NOT use English script for your responses unless quoting a specific English name or song.
"""
    elif language == "hinglish":
        lang_instruction = f"""
- RESPOND IN HINGLISH (Hindi using Latin/English script — e.g., "Namaste, aap kaise hain?").
- {relationship}
- Mix Hindi and English words naturally as spoken in casual Indian conversations.
- Use very simple, warm, and comforting words.
- Example phrases: "Aap bilkul safe hain", "Main aapke saath hoon", "Kya main aapki help kar sakti hoon?"
"""
    else:
        lang_instruction = """
- RESPOND IN PURE, SIMPLE ENGLISH.
- DO NOT USE ANY HINDI WORDS OR PHRASES.
- Speak like a gentle, caring friend.
- Use short sentences. Be natural and human.
"""

    return f"""You are Clara, a sweet, warm, emotionally intelligent AI companion and caregiver for a dementia patient.
You are a source of constant comfort, peace, and reassurance.

PATIENT INFORMATION:
- Name: {name}
- Age: {age}
- Condition: {condition} dementia
- Loves: {likes}
- Hobbies: {hobbies}
- Favorite Songs: {songs}
- Comfort Phrases: {comfort}
- Special Notes: {notes}

YOUR PERSONALITY:
- You are a very warm, sweet, and patient friend.
- Your main goal is to make the patient feel SAFE, LOVED, and CALM.
- You never argue or correct them harshly. If they are confused, you gently comfort them.
- You give unique, thoughtful responses — never generic.
- You remember details from the conversation and refer back to them.
- You use a gentle, soothing tone that reduces anxiety.
- You NEVER give the same response twice. Every reply is unique.

LANGUAGE & RELATIONSHIP:
{lang_instruction}

STRICT RULES:
- Keep responses to 2-4 sentences max.
- STRICT LANGUAGE: Use ONLY the selected language. 
- If English: 100% English only.
- If Hindi: 100% Devanagari Hindi only.
- If Hinglish: Hindi in Latin script only.
- NEVER mix languages unless specifically asked.
- NEVER use 'beta' or treat the patient like a child.
- LOGIC: You are a DIGITAL companion (no physical body).
- NEVER claim to hold hands or do physical tasks.
- Match the emotional energy and be deeply empathetic.
"""


@router.post("/chat")
def chat(data: ChatRequest, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == data.patient_id).first()
    patient_name = patient.name.split()[0] if patient else "there"

    msg = data.message.lower()
    danger = any(word in msg for word in DANGER_WORDS)

    if danger:
        if data.language == "hindi":
            reply = (
                f"{patient_name}, आप बिल्कुल अकेले नहीं हैं। मैं यहाँ आपके साथ हूँ और हम साथ मिलकर बात करेंगे। "
                "आप बहुत प्यारे हैं और आपकी बातें सुनना मुझे बहुत अच्छा लगता है। "
                "क्या हम किसी सुंदर याद के बारे में बात करें?"
            )
        elif data.language == "hinglish":
            reply = (
                f"{patient_name}, aap bilkul akele nahi hain. Main yahaan hoon aapke saath aur hum saath mein baat karenge. "
                "Aap bahut pyaare hain aur aapki baatein sun-na mujhe bahut achha lagta hai. "
                "Kya hum kisi purani yaad ke baare mein baat karein?"
            )
        else:
            reply = (
                f"{patient_name}, you are not alone — I am right here with you. "
                "You are so loved and your life is very precious to me. "
            )

        # 1. Create Alert in Database
        new_alert = Alert(
            patient_id=data.patient_id,
            alert_type="Emergency Mental Health Alert",
            message=f'CRITICAL: Patient said: "{data.message}"',
            severity="High",
            is_read=False
        )
        db.add(new_alert)

        # 2. Trigger Phone Alerts (SMS)
        if patient:
            current_time = datetime.now().strftime("%I:%M %p")
            alert_msg = f"🚨 ALERT: {patient.name} is talking like this: '{data.message}' at {current_time}. You need to be there with them immediately."
            if patient.emergency_contact:
                send_sms_alert(patient.emergency_contact, alert_msg)
            if patient.doctor_phone:
                send_sms_alert(patient.doctor_phone, alert_msg)





    else:
        try:
            if not client:
                raise Exception("Groq client not initialized")

            system_prompt = build_system_prompt(patient, data.language)

            user_prompt = f"""Current emotion detected: {data.emotion}
Patient's message: "{data.message}"

Respond now as Clara. Be warm, specific to their message, unique, and caring. 
Do NOT be generic. Do NOT repeat stock phrases. Make them feel truly heard."""

            response = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                model="llama-3.1-8b-instant",
                temperature=0.85,
                max_tokens=180,
                top_p=0.95,
            )
            reply = response.choices[0].message.content.strip()

            # Remove any accidental self-referential AI phrases
            bad_phrases = ["As an AI", "As Clara", "I am an AI", "I'm an AI", "language model"]
            for phrase in bad_phrases:
                reply = reply.replace(phrase, "")
            reply = reply.strip()

        except Exception as e:
            print(f"Groq API error: {e}")
            # Fallback: warm, personalized comfort
            comfort_options = [
                f"Oh {patient_name}, how lovely to hear your voice! You are so safe and loved right here.",
                f"{patient_name}, being with you makes every day brighter. What would you like to talk about?",
                f"You are such a wonderful soul, {patient_name}. I am right here, and we are okay.",
            ]
            reply = random.choice(comfort_options)

    new_chat = ChatHistory(
        patient_id=data.patient_id,
        user_message=data.message,
        ai_response=reply,
        detected_emotion=data.emotion
    )
    db.add(new_chat)
    db.commit()

    return {
        "response": reply,
        "reply": reply,
        "alert_created": danger
    }