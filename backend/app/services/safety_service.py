RISK_WORDS = [
    "suicide", "kill myself", "die", "hurt myself",
    "medicine overdose", "blood", "self harm"
]


def detect_risk(text: str) -> bool:
    lower_text = text.lower()
    return any(word in lower_text for word in RISK_WORDS)


def safe_prefix():
    return """
Safety rules:
- You are not a doctor.
- Do not diagnose dementia or any medical condition.
- Do not suggest medicine dosage.
- If user seems unsafe, advise contacting caregiver or emergency support.
- Keep responses calm, short, simple, and reassuring.
"""