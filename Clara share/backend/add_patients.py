from app.database import SessionLocal, engine
from app.models import Patient, Base

# Ensure tables exist
Base.metadata.create_all(bind=engine)

db = SessionLocal()

patients = [
    Patient(
        name="Prema", age=72, gender="Female", condition_stage="Moderate",
        preferred_language="Hindi",
        likes="Gardening, Cooking", hobbies="Knitting, listening to bhajans",
        favorite_songs="Lata Mangeshkar old songs", comfort_phrases="Sab theek ho jayega, main yahan hoon",
        notes="Gets anxious in the evening. Loves talking about her grandchildren.",
        caregiver_id=1
    ),
    Patient(
        name="Ramesh", age=78, gender="Male", condition_stage="Mild",
        preferred_language="Hindi",
        likes="Reading newspaper, Morning walks", hobbies="Playing chess, listening to old radio shows",
        favorite_songs="Kishore Kumar classics", comfort_phrases="Main hoon na aapke saath, dariye mat",
        notes="Forgets names often but remembers faces. Likes strict routine.",
        caregiver_id=1
    ),
    Patient(
        name="Saroj", age=81, gender="Female", condition_stage="Severe",
        preferred_language="Hindi",
        likes="Looking at old photos, Sweet food", hobbies="Humming old tunes",
        favorite_songs="Asha Bhosle songs", comfort_phrases="Aap bilkul safe hain yahan",
        notes="Needs constant reassurance. Can get agitated easily if left alone.",
        caregiver_id=1
    ),
    Patient(
        name="Malti", age=69, gender="Female", condition_stage="Mild",
        preferred_language="Hindi",
        likes="Watching TV serials, Chatting", hobbies="Making pickles, stitching",
        favorite_songs="Old Bollywood romantic songs", comfort_phrases="Chinta mat kijiye, sab achha hoga",
        notes="Very talkative and friendly. Sometimes forgets if she had her meals.",
        caregiver_id=1
    ),
    Patient(
        name="Lalita", age=75, gender="Female", condition_stage="Moderate",
        preferred_language="Hindi",
        likes="Flowers, Tea", hobbies="Drawing, listening to religious discourses",
        favorite_songs="Bhajans and Aarti", comfort_phrases="Bhagwan sab theek karenge",
        notes="Calms down when listening to devotional songs.",
        caregiver_id=1
    )
]

db.add_all(patients)
db.commit()
db.close()
print("5 Indian patients added successfully!")
