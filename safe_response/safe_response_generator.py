from typing import Dict, List

from safe_response.keywords import DISTRESS_KEYWORDS


class SafeResponseGenerator:
    def __init__(self) -> None:
        self.keyword_map = DISTRESS_KEYWORDS

    def detect_risk_flags(self, text: str) -> Dict[str, List[str]]:
        text_lower = text.lower().strip()
        found = {}

        for category, keywords in self.keyword_map.items():
            matches = [word for word in keywords if word in text_lower]
            if matches:
                found[category] = matches

        return found

    def generate_safe_response(self, text: str) -> Dict[str, str]:
        flags = self.detect_risk_flags(text)

        if "self_harm" in flags:
            return {
                "risk_level": "critical",
                "response": (
                    "I am really sorry that you are feeling this way. You deserve immediate human support right now. "
                    "Please call a trusted family member, caregiver, or local emergency service immediately. "
                    "Do not stay alone."
                ),
                "action": "alert_caregiver"
            }
        if "medical" in flags:
            return {
                "risk_level": "high",
                "response": (
                    "I am concerned that this may need urgent attention. Please contact a caregiver or doctor immediately. "
                    "If breathing difficulty, severe pain, or collapse is happening, call emergency services now."
                ),
                "action": "urgent_medical_support"
            }

        if "panic" in flags:
            return {
                "risk_level": "medium",
                "response": (
                    "You are safe. I am here with you. Let us take one slow breath in and one slow breath out. "
                    "Would you like me to guide you step by step and notify your caregiver?"
                ),
                "action": "calm_and_monitor"
            }

        if "confusion" in flags:
            return {
                "risk_level": "medium",
                "response": (
                    "It is okay to feel confused. You are safe, and I am here to help. "
                    "Let us take this slowly. Can I remind you where you are and who is with you?"
                ),
                "action": "reorient_patient"
            }

        if "agitation" in flags:
            return {
                "risk_level": "low",
                "response": (
                    "I understand this feels upsetting. I will speak gently and stay with you. "
                    "Let us pause for a moment and try something calming."
                ),
                "action": "de_escalate"
            }
        return {
            "risk_level": "low",
            "response": (
                "I am here with you. You are safe. Let us continue calmly."
            ),
            "action": "normal_support"
        }