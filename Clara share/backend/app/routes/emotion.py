from fastapi import APIRouter, UploadFile, File, Form, Depends
from datetime import datetime
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import EmotionLog

router = APIRouter()

@router.post("/emotion")
async def detect_emotion(
    file: UploadFile = File(...),
    patient_id: int = Form(...),
    db: Session = Depends(get_db)
):
    contents = await file.read()
    
    try:
        import cv2
        import numpy as np
        from deepface import DeepFace
        
        nparr = np.frombuffer(contents, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # SPEED OPTIMIZATION: Resize image proportionally to prevent distortion
        # Distorting the face by forcing it into a square causes inaccurate emotion detection
        height, width = img.shape[:2]
        max_dim = 300
        if max(height, width) > max_dim:
            scale = max_dim / max(height, width)
            img = cv2.resize(img, (int(width * scale), int(height * scale)))
        
        # Use 'opencv' or 'ssd' for faster face detection
        result = DeepFace.analyze(
            img, 
            actions=['emotion'], 
            enforce_detection=False,
            detector_backend='opencv', # Fast Haar Cascades
            silent=True
        )
        
        if isinstance(result, list):
            result = result[0]
            
        dominant = result['dominant_emotion']
        raw_confidence = float(result['emotion'][dominant])

        # Clinical Mapping for Dementia Care
        # Mapping surprise to Anxious and fear to Panic/Fear
        mapping = {
            "happy": "Happy",
            "sad": "Sad",
            "neutral": "Neutral",
            "fear": "Panic" if raw_confidence > 60 else "Fear",
            "surprise": "Anxious",
            "angry": "Agitated",
            "disgust": "Upset"
        }
        
        emotion = mapping.get(dominant.lower(), dominant.capitalize())
        confidence = raw_confidence
    except Exception as e:
        print(f"DeepFace speed-optimized error: {e}")
        emotion = "Neutral"
        confidence = 0.0

    new_log = EmotionLog(
        patient_id=patient_id,
        emotion=emotion,
        confidence=confidence,
        source="face"
    )
    db.add(new_log)
    db.commit()

    return {
        "emotion": emotion,
        "confidence": confidence
    }