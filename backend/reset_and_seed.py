from app.database import SessionLocal, engine
from app.models import Patient, Base, ChatHistory, EmotionLog, Alert

# Ensure tables exist
Base.metadata.create_all(bind=engine)

db = SessionLocal()

# Clear existing data to ensure ONLY these 5 exist
db.query(Alert).delete()
db.query(ChatHistory).delete()
db.query(EmotionLog).delete()
db.query(Patient).delete()
db.commit()

patients = [
    Patient(
        name="Prema", age=72, gender="Female", condition_stage="Moderate",
        preferred_language="Hindi",
        likes="Gardening, Cooking", hobbies="Knitting, listening to bhajans",
        favorite_songs="Lata Mangeshkar old songs", comfort_phrases="सब ठीक हो जाएगा, मैं यहाँ हूँ",
        notes="Gets anxious in the evening (Sundowning). Often forgets names of vegetables but loves talking about her childhood in Lucknow.",
        caregiver_id=1
    ),
    Patient(
        name="Ramesh", age=78, gender="Male", condition_stage="Mild",
        preferred_language="Hindi",
        likes="Reading newspaper, Morning walks", hobbies="Playing chess, listening to old radio shows",
        favorite_songs="Kishore Kumar classics", comfort_phrases="मैं हूँ न आपके साथ, डरिये मत",
        notes="Early stage dementia. Occasionally forgets where he put his glasses. Remembers old cricket matches vividly.",
        caregiver_id=1
    ),
    Patient(
        name="Saroj", age=81, gender="Female", condition_stage="Severe",
        preferred_language="Hindi",
        likes="Looking at old photos, Sweet food", hobbies="Humming old tunes",
        favorite_songs="Asha Bhosle songs", comfort_phrases="आप बिल्कुल सुरक्षित हैं यहाँ",
        notes="Advanced dementia. Needs help with daily activities. Calms down significantly when shown photos of her wedding.",
        caregiver_id=1
    ),
    Patient(
        name="Malti", age=69, gender="Female", condition_stage="Mild",
        preferred_language="Hindi",
        likes="Watching TV serials, Chatting", hobbies="Making pickles, stitching",
        favorite_songs="Old Bollywood romantic songs", comfort_phrases="चिंता मत कीजिये, सब अच्छा होगा",
        notes="Mild Cognitive Impairment. Very social but repeats the same stories every 10 minutes. Loves feeding birds.",
        caregiver_id=1
    ),
    Patient(
        name="Lalita", age=75, gender="Female", condition_stage="Moderate",
        preferred_language="Hindi",
        likes="Flowers, Tea", hobbies="Drawing, listening to religious discourses",
        favorite_songs="Bhajans and Aarti", comfort_phrases="भगवान सब ठीक करेंगे",
        notes="Moderate dementia. Forgets her current location but can recite long prayers perfectly. Enjoys the smell of jasmine.",
        caregiver_id=1
    )
]

db.add_all(patients)
db.commit()
db.close()
print("Database reset! Only 5 Indian patients (Prema, Ramesh, Saroj, Malti, Lalita) are now in the DB.")
