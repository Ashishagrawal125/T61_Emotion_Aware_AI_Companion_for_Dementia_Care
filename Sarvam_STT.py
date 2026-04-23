import os
import requests

SARVAM_STT_URL = "https://api.sarvam.ai/speech-to-text"


def detect_and_translate(file_path: str):
    api_key = os.getenv("SARVAM_API_KEY")
    if not api_key:
        return {
            "transcript": "",
            "language_code": "unknown",
            "error": "SARVAM_API_KEY not set in environment variables.",
        }

    headers = {"api-subscription-key": api_key}
    payload = {
        "with_timestamps": "false",
        "with_diarization": "false",
        "model": "saarika:v2",
        "language_code": "unknown",
    }

    with open(file_path, "rb") as audio_file:
        files = {"file": (os.path.basename(file_path), audio_file, "audio/wav")}
        response = requests.post(SARVAM_STT_URL, headers=headers, data=payload, files=files, timeout=60)

    try:
        response.raise_for_status()
        data = response.json()
        return {
            "transcript": data.get("transcript", ""),
            "language_code": data.get("language_code", "unknown"),
            "raw": data,
        }
    except Exception:
        try:
            data = response.json()
        except Exception:
            data = {"message": response.text}
        return {
            "transcript": "",
            "language_code": "unknown",
            "error": data,
        }
