from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import ChatHistory, Alert, EmotionLog

router = APIRouter()

@router.get("/dashboard/{patient_id}")
def dashboard(patient_id: int, db: Session = Depends(get_db)):
    patient_chats = db.query(ChatHistory).filter(ChatHistory.patient_id == patient_id).order_by(ChatHistory.created_at.desc()).limit(10).all()
    patient_alerts = db.query(Alert).filter(Alert.patient_id == patient_id).order_by(Alert.created_at.desc()).all()
    patient_emotions = db.query(EmotionLog).filter(EmotionLog.patient_id == patient_id).order_by(EmotionLog.created_at.desc()).limit(10).all()

    total_chats = db.query(ChatHistory).filter(ChatHistory.patient_id == patient_id).count()
    total_alerts = db.query(Alert).filter(Alert.patient_id == patient_id).count()
    
    dominant_emotion = patient_emotions[0].emotion if patient_emotions else "Neutral"

    return {
        "total_chats": total_chats,
        "total_alerts": total_alerts,
        "dominant_emotion": dominant_emotion,
        "conversations": patient_chats,
        "alerts": patient_alerts,
        "emotion_trend": patient_emotions[::-1],
    }