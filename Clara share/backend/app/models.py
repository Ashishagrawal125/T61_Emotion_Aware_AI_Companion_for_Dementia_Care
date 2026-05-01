from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Caregiver(Base):
    __tablename__ = "caregivers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    email = Column(String(150), unique=True, index=True)
    phone = Column(String(30), default="")
    role = Column(String(30), default="caregiver")
    password_hash = Column(String(255))
    created_at = Column(DateTime, default=datetime.now)

    patients = relationship("Patient", back_populates="caregiver")


class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    caregiver_id = Column(Integer, ForeignKey("caregivers.id"), nullable=True)

    name = Column(String(100))
    age = Column(Integer)
    gender = Column(String(30), default="")
    phone = Column(String(30), default="")
    condition_stage = Column(String(50), default="mild")
    preferred_language = Column(String(30), default="English")
    emergency_contact = Column(String(100), default="")
    doctor_phone = Column(String(30), default="")
    notes = Column(Text, default="")
    family_members = Column(Text, default="")
    likes = Column(Text, default="")
    dislikes = Column(Text, default="")
    favorite_songs = Column(Text, default="")
    hobbies = Column(Text, default="")
    routine = Column(Text, default="")
    comfort_phrases = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.now)

    caregiver = relationship("Caregiver", back_populates="patients")
    emotions = relationship("EmotionLog", back_populates="patient")
    chats = relationship("ChatHistory", back_populates="patient")
    alerts = relationship("Alert", back_populates="patient")


class EmotionLog(Base):
    __tablename__ = "emotion_logs"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=True)
    emotion = Column(String(50))
    confidence = Column(Float, default=0.0)
    source = Column(String(30), default="face")
    created_at = Column(DateTime, default=datetime.now)

    patient = relationship("Patient", back_populates="emotions")


class ChatHistory(Base):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=True)
    user_message = Column(Text)
    ai_response = Column(Text)
    detected_emotion = Column(String(50), default="neutral")
    created_at = Column(DateTime, default=datetime.now)

    patient = relationship("Patient", back_populates="chats")


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=True)
    alert_type = Column(String(100))
    message = Column(Text)
    severity = Column(String(30), default="medium")
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)

    patient = relationship("Patient", back_populates="alerts")