import cv2
import numpy as np
from deepface import DeepFace
import os

def test_deepface():
    # Create a blank image
    img = np.zeros((480, 640, 3), dtype=np.uint8)
    # Draw a simple face-like shape or just use the blank image
    cv2.putText(img, "Test", (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    try:
        print("Testing DeepFace analyze...")
        result = DeepFace.analyze(img, actions=['emotion'], enforce_detection=False)
        print("Result:", result)
        print("SUCCESS: DeepFace is working.")
    except Exception as e:
        print("ERROR: DeepFace failed.")
        print(f"Exception: {e}")

if __name__ == "__main__":
    test_deepface()
