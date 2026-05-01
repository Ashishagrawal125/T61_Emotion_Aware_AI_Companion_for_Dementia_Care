from app.database import SessionLocal, engine
from app.models import Patient, Base, Caregiver
from sqlalchemy.orm import Session

# Ensure tables exist
Base.metadata.create_all(bind=engine)

def seed_patients():
    db: Session = SessionLocal()
    
    # Ensure at least one caregiver exists
    caregiver = db.query(Caregiver).first()
    if not caregiver:
        caregiver = Caregiver(name="Primary Caregiver", email="care@clara.ai", password_hash="hashed_pw")
        db.add(caregiver)
        db.commit()
        db.refresh(caregiver)
    
    # Clear existing patients to avoid duplicates if preferred, 
    # but here we just add the new ones.
    
    patients_data = [
        {
            "name": "Meera Sharma",
            "age": 72,
            "gender": "Female",
            "condition_stage": "Mild",
            "preferred_language": "Hindi",
            "emergency_contact": "9876543210",
            "doctor_phone": "9123456780",
            "family_members": "Riya (Daughter), Amit (Son)",
            "likes": "Roses, calm music, morning sunlight",
            "hobbies": "Gardening, listening to bhajans, watching old Hindi movies",
            "routine": "Wakes up at 6 AM, spends time in garden",
            "notes": "Widow, lives with daughter. Mild memory loss, occasional confusion. Feels lonely in evenings. Responds well to familiar topics like family and gardening. Favorite food: Khichdi, tea.",
            "caregiver_id": caregiver.id,
            "comfort_phrases": "Aap bilkul safe hain, Meera ji. Riya bindiya aapke saath hai.",
            "favorite_songs": "Old Hindi movie songs and Bhajans"
        },
        {
            "name": "Ramesh Verma",
            "age": 78,
            "gender": "Male",
            "condition_stage": "Mild",
            "preferred_language": "Hindi",
            "emergency_contact": "9812345678",
            "doctor_phone": "9098765432",
            "family_members": "Sunita (Wife), Rohit (Son)",
            "likes": "Morning tea, newspapers",
            "hobbies": "Walking, reading news",
            "routine": "Follows strict morning schedule. Sits in balcony.",
            "notes": "Gets confused about time and date. Prefers routine and becomes anxious if disrupted. Generally calm but needs reminders. Favorite food: Paratha, chai.",
            "caregiver_id": caregiver.id,
            "comfort_phrases": "Ramesh ji, chai taiyar hai. Sab theek hai.",
            "favorite_songs": "Kishore Kumar classics"
        },
        {
            "name": "Prema Devi",
            "age": 76,
            "gender": "Female",
            "condition_stage": "Moderate",
            "preferred_language": "Hindi",
            "emergency_contact": "9898989898",
            "doctor_phone": "9012345678",
            "family_members": "Kavita (Daughter)",
            "likes": "Old songs, temple visits",
            "hobbies": "Singing, cooking",
            "routine": "Spends time indoors mostly.",
            "notes": "Repeats questions frequently. Moderate memory loss. Feels anxious when left alone. Needs emotional reassurance and engagement. Favorite food: Dal rice.",
            "caregiver_id": caregiver.id,
            "comfort_phrases": "Prema ji, main aapke paas hoon. Kavita jaldi aayegi.",
            "favorite_songs": "Devotional songs and old classics"
        },
        {
            "name": "Abdul Rahman",
            "age": 80,
            "gender": "Male",
            "condition_stage": "Severe",
            "preferred_language": "Hindi",
            "emergency_contact": "9871234560",
            "doctor_phone": "9123987654",
            "family_members": "Ayesha (Daughter), Imran (Son)",
            "likes": "Quiet environment, spiritual recitations",
            "hobbies": "Listening to prayers",
            "routine": "Needs assistance throughout day. Sits quietly.",
            "notes": "Severe dementia, requires constant supervision. Limited communication ability. Gets agitated in noisy environments. Favorite food: Soft food, soup.",
            "caregiver_id": caregiver.id,
            "comfort_phrases": "Abdul ji, shanti rakhiye. Hum sab yahan hain.",
            "favorite_songs": "Spiritual recitations and prayers"
        },
        {
            "name": "Saroj Gupta",
            "age": 70,
            "gender": "Female",
            "condition_stage": "Mild",
            "preferred_language": "English",
            "emergency_contact": "9001122334",
            "doctor_phone": "9112233445",
            "family_members": "Neha (Daughter), Rajesh (Husband)",
            "likes": "Family conversations, TV serials",
            "hobbies": "Knitting, watching TV",
            "routine": "Watches TV in evening.",
            "notes": "Experiences anxiety at night. Mild memory loss. Feels better when engaged in conversations. Needs emotional support and reassurance. Favorite food: Home-cooked meals.",
            "caregiver_id": caregiver.id,
            "comfort_phrases": "Saroj, you are doing great. Neha is just in the other room.",
            "favorite_songs": "Old Bollywood romantic songs"
        }
    ]
    
    for p_data in patients_data:
        patient = Patient(**p_data)
        db.add(patient)
    
    db.commit()
    db.close()
    print(f"Successfully stored {len(patients_data)} patients in the database.")

if __name__ == "__main__":
    seed_patients()
