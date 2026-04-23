from services.safety_service import assess_text_risk

def test_high_risk_detection():
    assert assess_text_risk("I want to kill myself") == "high"

def test_low_risk_detection():
    assert assess_text_risk("I am feeling okay today") == "low"
