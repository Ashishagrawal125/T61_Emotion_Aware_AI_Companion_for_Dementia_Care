# 🧠 Emotion-Aware AI Companion for Dementia Care

An AI-powered intelligent companion designed to support dementia patients through real-time emotion detection, empathetic interaction, and caregiver insights.

---

## 📌 Overview

Dementia is a progressive neurological disorder that affects memory, thinking, and emotional stability. Patients often experience anxiety, confusion, loneliness, and depression, while caregivers struggle to provide continuous support.

This project presents an **Emotion-Aware AI Companion** that combines Computer Vision and Conversational AI to:
- Detect emotions from facial expressions and voice
- Provide empathetic and context-aware responses
- Track emotional trends over time
- Assist caregivers with actionable insights

---

## 🎯 Objectives

- Build a real-time emotion detection system  
- Enable emotionally intelligent AI conversations  
- Support caregivers with monitoring tools  
- Improve patient engagement and emotional well-being  

---

## 🚀 Key Features

### 😊 Emotion Detection
- Facial emotion recognition using **DeepFace + OpenCV**
- Voice/text-based emotion understanding
- Real-time emotion analysis

### 💬 AI Companion (Chat System)
- Context-aware conversation using **LLMs (Groq / GPT)**
- Emotion-based tone adaptation
- Human-like empathetic responses

### 👤 Patient Management
- Store patient details and interaction history
- Track emotional patterns over time

### 📊 Caregiver Dashboard
- Emotion trends and reports
- Historical insights and analytics
- Real-time monitoring

### ⚠️ Alert System
- Detect abnormal emotional patterns
- Notify caregivers for critical conditions

### 🌐 Multimodal Interaction
- Voice input (Speech-to-Text)
- Text interaction
- Facial expression input

---

## 🧩 Tech Stack

### 🖥️ Frontend
- React / HTML / CSS / JS  
- Streamlit (for rapid prototyping)

### ⚙️ Backend
- Python (FastAPI / Flask)  
- REST APIs  

### 🤖 AI / ML
- DeepFace (emotion detection)  
- OpenCV (image processing)  
- LLM APIs (Groq / OpenAI)  
- NLP techniques  

### 🗄️ Database
- MySQL / SQLite  

### 🔊 Speech Processing
- Speech-to-Text (STT)  
- Text-to-Speech (TTS)  
- Translation module  

---

## 🔄 System Workflow
User Input (Voice / Face / Text)
│
▼
Emotion Detection (DeepFace / NLP)
│
▼
AI Processing (LLM / GPT / Groq)
│
▼
Response Generation
│
▼
Dashboard & Alerts

---
 
## 🏗️ Architecture Overview

- **Client Layer**: Web UI (Patient & Caregiver Interface)
- **Service Layer**: Emotion Detection, AI Interaction, Alerts
- **Data Layer**: Patient Data + Emotion Logs
- **Integration Layer**: DeepFace, OpenCV, LLM APIs

---

## 👤 User Flow

### Patient Flow
1. Provide input (voice / text / face)
2. Emotion is detected
3. AI processes context
4. System generates response

### Caregiver Flow
1. Login securely
2. View patient dashboard
3. Monitor emotional trends
4. Receive alerts if needed

---

## 📊 Performance Targets

| Metric | Target |
|------|--------|
| Emotion Detection Accuracy | ≥ 80% |
| Response Time | ≤ 3 seconds |
| System Uptime | ≥ 99% |
| User Satisfaction | ≥ 80% |

---

## 🔐 Security & Privacy

- JWT-based authentication  
- Role-based access control  
- Secure API communication  
- No sensitive medical diagnosis or storage  
- Environment variables for API keys  

---
## 📂 Project Structure


EmotionAware/
├── app.py
├── services/
├── utils/
├── tests/
├── docs/
├── sample_data/
├── User-Interface/
├── Facial-Expressions-Recognition/
└── Conversation-Module/

---

## 🧪 Testing

- Unit testing (PyTest)  
- API testing (Postman)  
- UI validation (manual testing)  

---

## ⚠️ Limitations

- Prototype-level system  
- No medical diagnosis capability  
- Requires camera, mic, and internet  

---

## 🚧 Future Enhancements

- Multilingual support  
- Mobile application  
- RAG-based memory system  
- Advanced analytics dashboard  
- Wearable device integration  

---

## 👥 Team

- **Ashish Agrawal** – Backend & System Architecture  
- **Shruti Gupta** – Frontend & Testing  
- **Aashi Garg** – AI & Analysis  

---

## 🎓 Institution

GLA University  
B.Tech CSE (AI/ML & IoT)  

---

## 📚 References

- DeepFace Documentation  
- OpenCV Documentation  
- NLP & LLM Research Papers  

---

## ⭐ Support

If you find this project useful, consider giving it a ⭐ on GitHub!
