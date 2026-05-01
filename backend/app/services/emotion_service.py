from deepface import DeepFace
import cv2
import numpy as np

def detect_emotion_from_image(file):
    contents = file.file.read()
    np_arr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    result = DeepFace.analyze(img, actions=["emotion"], enforce_detection=False)

    emotion = result[0]["dominant_emotion"]
    confidence = max(result[0]["emotion"].values())

    return emotion, confidence