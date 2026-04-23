from fastapi import APIRouter, UploadFile, File
import numpy as np
import cv2
from deepface import DeepFace

router = APIRouter()

from collections import Counter

@router.post("/emotion")
async def detect_emotion(file: UploadFile = File(...)):
    try:
        contents = await file.read()

        np_arr = np.frombuffer(contents, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        if img is None:
            return {"emotion": "neutral"}

        # 🔥 Run multiple detections (3 times)
        emotions = []

        for _ in range(3):
            result = DeepFace.analyze(
                img,
                actions=['emotion'],
                enforce_detection=False
            )

            emotions.append(result[0]["dominant_emotion"])

        # 🎯 Majority voting
        final_emotion = Counter(emotions).most_common(1)[0][0]

        return {"emotion": final_emotion}

    except Exception as e:
        print("ERROR:", e)
        return {"emotion": "neutral"}