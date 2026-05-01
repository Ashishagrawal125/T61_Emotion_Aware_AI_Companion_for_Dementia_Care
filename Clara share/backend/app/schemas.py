from pydantic import BaseModel, EmailStr
from typing import Optional


class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    phone: str
    role: str = "caregiver"
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class PatientCreate(BaseModel):
    name: str
    age: int
    gender: str = ""
    phone: str = ""
    condition_stage: str = "mild"
    preferred_language: str = "English"
    emergency_contact: Optional[str] = ""
    doctor_phone: Optional[str] = ""
    notes: Optional[str] = ""
    family_members: Optional[str] = ""
    likes: Optional[str] = ""
    dislikes: Optional[str] = ""
    favorite_songs: Optional[str] = ""
    hobbies: Optional[str] = ""
    routine: Optional[str] = ""
    comfort_phrases: Optional[str] = ""


class PatientUpdate(PatientCreate):
    pass


class ChatRequest(BaseModel):
    message: str
    emotion: Optional[str] = "neutral"
    patient_id: Optional[int] = None