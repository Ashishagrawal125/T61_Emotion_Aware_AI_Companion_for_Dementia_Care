HIGH_RISK_KEYWORDS = {
    "suicide", "kill myself", "end my life", "self harm", "hurt myself"
}

def assess_text_risk(text: str) -> str:
    lowered = text.lower()
    if any(keyword in lowered for keyword in HIGH_RISK_KEYWORDS):
        return "high"
    if any(word in lowered for word in ["hopeless", "panic", "helpless", "crying"]):
        return "medium"
    return "low"


def safe_companion_reply(text: str) -> str:
    risk = assess_text_risk(text)
    if risk == "high":
        return (
            "I am really sorry you are feeling this way. Please reach out to a trusted person or local emergency help right now. "
            "You deserve immediate support and should not handle this alone."
        )
    if risk == "medium":
        return "I am here with you. Try taking slow breaths and tell me what happened step by step."
    return "I am here for you. Tell me more, and we can talk through it together."
