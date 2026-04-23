import os
import base64
import wave
import requests

SARVAM_TTS_URL = "https://api.sarvam.ai/text-to-speech"
LANG_MAP = {
    "hi": "hi-IN",
    "bn": "bn-IN",
    "kn": "kn-IN",
    "ml": "ml-IN",
    "mr": "mr-IN",
    "od": "od-IN",
    "pa": "pa-IN",
    "ta": "ta-IN",
    "te": "te-IN",
    "en": "en-IN",
    "gu": "gu-IN",
}


def text_to_speech(text: str, language: str = "en"):
    api_key = os.getenv("SARVAM_API_KEY")
    if not api_key:
        raise RuntimeError("SARVAM_API_KEY not set in environment variables.")
    if not text or not text.strip():
        raise ValueError("Text is empty.")

    lang = language.lower().split("-")[0]
    target_code = LANG_MAP.get(lang, "en-IN")

    payload = {
        "inputs": [text[:500]],
        "target_language_code": target_code,
        "speaker": "neel",
        "model": "bulbul:v1",
        "pitch": 0,
        "pace": 1.0,
        "loudness": 1.0,
        "enable_preprocessing": True,
    }
    headers = {
        "Content-Type": "application/json",
        "api-subscription-key": api_key,
    }

    response = requests.post(SARVAM_TTS_URL, json=payload, headers=headers, timeout=60)
    response.raise_for_status()
    audio_b64 = response.json()["audios"][0]
    audio = base64.b64decode(audio_b64)

    out_file = f"output_{lang}.wav"
    with wave.open(out_file, "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(22050)
        wav_file.writeframes(audio)
    return out_file
