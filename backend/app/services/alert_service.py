from sqlalchemy.orm import Session
from app.models import Alert, Patient
from app.services.notification_service import send_email_alert, send_sms_alert


DANGER_WORDS = [
    "i want to die",
    "kill myself",
    "suicide",
    "end my life",
    "i will die",
    "i want to disappear",
    "nobody loves me",
]


def detect_risk_level(text: str, emotion: str = ""):
    clean = (text or "").lower()

    if any(word in clean for word in DANGER_WORDS):
        return "high", "Emergency self-harm risk detected"

    if emotion.lower() in ["sad", "angry", "fear"]:
        return "medium", "Negative emotion detected"

    return "low", ""


def create_alert(
    db: Session,
    patient_id: int,
    alert_type: str,
    message: str,
    severity: str = "medium",
):
    alert = Alert(
        patient_id=patient_id,
        alert_type=alert_type,
        message=message,
        severity=severity,
        is_read=False,
    )

    db.add(alert)
    db.commit()
    db.refresh(alert)

    patient = db.query(Patient).filter(Patient.id == patient_id).first()

    if patient:
        alert_msg = f"""
Clara AI Alert

Patient: {patient.name}
Severity: {severity}
Alert: {alert_type}

Message:
{message}

Please check on the patient immediately.
"""

        # SMS to family/caregiver/doctor numbers
        send_sms_alert(patient.emergency_contact, alert_msg)
        send_sms_alert(patient.doctor_phone, alert_msg)

        # Email only if you later add family_email / doctor_email fields
        # send_email_alert(patient.family_email, "Clara AI Emergency Alert", alert_msg)

    return alert