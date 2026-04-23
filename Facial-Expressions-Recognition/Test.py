from keras.models import load_model
from keras.preprocessing.image import img_to_array
import cv2
import numpy as np

# Load model
classifier = load_model('Emotion_little_vgg.h5')

# Load face detector
face_classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

if face_classifier.empty():
    print("Error loading cascade file")
    exit()

class_labels = ['Angry','Happy','Neutral','Sad','Surprise']

# Try camera index 0 first
cap = cv2.VideoCapture(1)

if not cap.isOpened():
    print("Cannot access camera")
    exit()

while True:
    ret, frame = cap.read()

    if not ret:
        print("Failed to grab frame")
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

        roi_gray = gray[y:y+h, x:x+w]
        roi_gray = cv2.resize(roi_gray, (48, 48), interpolation=cv2.INTER_AREA)

        roi = roi_gray.astype('float') / 255.0
        roi = img_to_array(roi)
        roi = np.expand_dims(roi, axis=0)

        preds = classifier.predict(roi, verbose=0)[0]
        label = class_labels[preds.argmax()]

        cv2.putText(frame, label, (x, y-10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.9,
                    (0, 255, 0),
                    2)

    cv2.imshow('Emotion Detector', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()