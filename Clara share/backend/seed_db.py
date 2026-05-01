import sys
from pathlib import Path

# Add the backend directory to sys.path so we can import app
sys.path.append(str(Path(__file__).resolve().parent))

from app.database import SessionLocal, engine
from app.models import Patient, Base

# Make sure tables exist
Base.metadata.create_all(bind=engine)

def seed_data():
    db = SessionLocal()
    
    # Check if there are already patients in the DB
    if db.query(Patient).count() > 0:
        print("Database already has patients. Skipping seeding.")
        db.close()
        return

    patients_data = [
        Patient(
            name="Margaret Smith",
            age=78,
            gender="Female",
            phone="+1-555-0198",
            condition_stage="moderate",
            preferred_language="English",
            emergency_contact="James Smith (Son) - +1-555-0200",
            doctor_phone="Dr. Adams - +1-555-8833",
            notes="Patient sometimes experiences evening confusion (sundowning). Responds very well to conversations about her cat, Whiskers.",
            family_members="James (Son), Sarah (Daughter), Michael (Grandson)",
            likes="Gardening, drinking chamomile tea, classical music, cats.",
            dislikes="Loud noises, bright flashing lights, being rushed, sudden changes in routine.",
            favorite_songs="Moon River, What a Wonderful World",
            hobbies="Knitting, watching old movies, looking at family photo albums.",
            routine="Wakes up at 7:30 AM, Breakfast at 8:30 AM, Afternoon nap at 2:00 PM, Dinner at 6:00 PM, Bedtime at 9:00 PM.",
            comfort_phrases="You are safe here, Margaret. James is coming to visit soon. Let's have a nice warm cup of tea."
        ),
        Patient(
            name="Robert Johnson",
            age=82,
            gender="Male",
            phone="+1-555-0342",
            condition_stage="mild",
            preferred_language="English",
            emergency_contact="Emily Davis (Daughter) - +1-555-0343",
            doctor_phone="Dr. Chen - +1-555-8844",
            notes="Loves to talk about his time in the Navy. Sometimes forgets what day it is.",
            family_members="Emily (Daughter), David (Son)",
            likes="Black coffee, reading the newspaper, talking about ships, jazz music.",
            dislikes="Being patronized, cold weather, crowded places.",
            favorite_songs="Take Five by Dave Brubeck, In the Mood by Glenn Miller",
            hobbies="Building model ships, reading historical non-fiction, listening to the radio.",
            routine="Wakes up at 6:00 AM, Coffee and news at 6:30 AM, Lunch at 12:00 PM, Walk at 4:00 PM, Bedtime at 8:30 PM.",
            comfort_phrases="You did a great job in the Navy, Robert. You are at home and safe. Let's look at the newspaper."
        ),
        Patient(
            name="Maria Garcia",
            age=75,
            gender="Female",
            phone="+1-555-0551",
            condition_stage="moderate",
            preferred_language="Spanish",
            emergency_contact="Carlos Garcia (Husband) - +1-555-0552",
            doctor_phone="Dr. Ramirez - +1-555-8855",
            notes="Primarily speaks Spanish now as condition progressed. Enjoys cooking shows.",
            family_members="Carlos (Husband), Sofia (Daughter)",
            likes="Cooking shows, telenovelas, traditional Mexican food, bright colors.",
            dislikes="Dark rooms, being alone, loud arguments.",
            favorite_songs="Bésame Mucho, Cielito Lindo",
            hobbies="Watching TV, folding clothes (finds it calming), looking out the window.",
            routine="Wakes up at 8:00 AM, Breakfast at 9:00 AM, TV time at 11:00 AM, Dinner with Carlos at 6:30 PM.",
            comfort_phrases="Carlos ya viene, Maria. Todo está bien. Vamos a ver tu programa favorito."
        ),
        Patient(
            name="William Taylor",
            age=88,
            gender="Male",
            phone="+1-555-0761",
            condition_stage="severe",
            preferred_language="English",
            emergency_contact="Nancy Brown (Caregiver) - +1-555-0762",
            doctor_phone="Dr. Adams - +1-555-8833",
            notes="Requires full-time care. Can become agitated easily. Needs a very calm environment.",
            family_members="None locally. Nancy is primary caregiver.",
            likes="Soft instrumental music, warm blankets, looking at pictures of landscapes.",
            dislikes="Unexpected touches, loud voices, being moved too quickly.",
            favorite_songs="Clair de Lune, Four Seasons",
            hobbies="Listening to music, resting.",
            routine="Wakes up at 9:00 AM, Assisted meals, Music therapy at 2:00 PM, Bedtime at 8:00 PM.",
            comfort_phrases="I am right here with you, William. You are safe. Listen to the beautiful music."
        ),
        Patient(
            name="Linda Anderson",
            age=69,
            gender="Female",
            phone="+1-555-0911",
            condition_stage="early onset",
            preferred_language="English",
            emergency_contact="Mark Anderson (Husband) - +1-555-0912",
            doctor_phone="Dr. Lewis - +1-555-8866",
            notes="Aware of her diagnosis and sometimes gets frustrated or depressed. Needs encouragement.",
            family_members="Mark (Husband), Jennifer (Daughter)",
            likes="Yoga, painting, herbal tea, discussing books.",
            dislikes="Being treated like a child, failing to remember words, violent movies.",
            favorite_songs="Let It Be by The Beatles, Bridge Over Troubled Water",
            hobbies="Watercolor painting, reading simple books, gentle yoga.",
            routine="Wakes up at 7:00 AM, Yoga at 8:00 AM, Painting at 1:00 PM, Evening walk at 5:00 PM.",
            comfort_phrases="It is okay to be frustrated, Linda. You are doing great. Let's do some painting together."
        )
    ]

    for p in patients_data:
        db.add(p)
    
    db.commit()
    print(f"Successfully inserted {len(patients_data)} sample patients into the database.")
    db.close()

if __name__ == "__main__":
    seed_data()
