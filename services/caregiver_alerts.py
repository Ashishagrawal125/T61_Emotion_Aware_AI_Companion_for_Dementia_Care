from services.safety_service import assess_text_risk

def should_alert_caregiver(emotion: str, recent_text: str = "") -> bool:
    risky_emotions = {"sad", "fear", "angry", "distress"}
    if emotion.lower() in risky_emotions:
        return True
    return assess_text_risk(recent_text) == "high"
