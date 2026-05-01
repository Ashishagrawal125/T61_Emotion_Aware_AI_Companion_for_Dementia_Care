from fastapi import APIRouter
from app.store import alerts

router = APIRouter()

@router.get("/alerts/{patient_id}")
def get_alerts(patient_id: int):
    return [a for a in alerts if a["patient_id"] == patient_id][::-1]

@router.put("/alerts/{alert_id}/read")
def mark_read(alert_id: int):
    for alert in alerts:
        if alert["id"] == alert_id:
            alert["is_read"] = True
            return alert
    return {"message": "Alert not found"}