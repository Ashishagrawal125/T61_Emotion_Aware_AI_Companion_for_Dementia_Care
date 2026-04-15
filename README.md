# 🧠 Emotion-Aware AI Companion for Dementia Care

An AI-powered companion system designed to provide emotional support, cognitive engagement, and caregiver insights for dementia patients using emotion recognition and conversational AI.

---

## 📌 Project Overview

Dementia patients often experience memory loss, confusion, anxiety, and loneliness. Due to limited caregiver availability, continuous emotional support becomes difficult.

This project aims to build an **Emotion-Aware AI Companion** that recognizes emotional states and provides empathetic, personalized interactions.

---

## 🎯 Objectives

- Detect emotions using voice and facial cues
- Provide empathetic AI-based conversations
- Offer daily reminders and cognitive activities
- Enable caregiver monitoring via dashboard
- Ensure ethical and secure data handling

---

## 🚀 Key Features

- ✅ Caregiver Authentication & Login
- ✅ Patient Profile Management
- ✅ Emotion Detection (Voice/Face/Text)
- ✅ Empathetic AI Interaction
- ✅ Daily Reminders
- ✅ Cognitive Engagement Activities
- ✅ Caregiver Dashboard & Analytics
- ✅ Emotion Alerts System

---

## 🛠️ Tech Stack

### Backend
- FastAPI / Node.js
- Python (ML Models)
- REST APIs
- JWT Authentication

### AI & ML
- Emotion Recognition Models
- NLP & LLM Integration
- Sentiment Analysis

### Database
- MySQL
- Object Storage (Images/Audio)

### Frontend
- Web Interface
- HTML / CSS / JavaScript

### Testing
- PyTest
- Jest
- Playwright
- Postman

---

## 📐 System Architecture

Client (Web UI)
↓
Emotion Engine → NLP Module → AI Response
↓
Database → Dashboard → Caregiver


---

## 📊 Performance Targets

| Metric              | Target        |
|---------------------|---------------|
| Emotion Accuracy    | ≥ 80%         |
| Response Time       | ≤ 3 seconds   |
| System Uptime       | ≥ 99%         |
| Error Rate          | ≤ 1%          |

---

## 🔗 API Endpoints (Sample)

| Endpoint                    | Method | Purpose                 |
|-----------------------------|--------|-------------------------|
| /api/auth/login             | POST   | Caregiver Login         |
| /api/patient/create         | POST   | Create Patient Profile |
| /api/emotion/analyze        | POST   | Analyze Emotion         |
| /api/interaction/respond    | POST   | Generate AI Response    |
| /api/dashboard/emotions     | GET    | Get Emotion History     |

---
```
## 📁 Project Structure

emotion-ai-companion/
│
├── backend/
│ ├── auth/
│ ├── api/
│ ├── models/
│ └── services/
│
├── ml/
│ ├── emotion_detection/
│ ├── nlp/
│ └── training/
│
├── frontend/
│ ├── components/
│ ├── pages/
│ └── assets/
│
├── database/
│ └── migrations/
│
├── tests/
│
└── README.md
```

---

## ⚙️ Installation & Setup

### Prerequisites
- Python 3.8+
- Node.js 16+
- MySQL
- Git
---
```
### Clone Repository
git clone https://github.com/your-username/emotion-ai-companion.git
cd emotion-ai-companion

  Backend Setup
cd backend
pip install -r requirements.txt
uvicorn main:app --reload

  Frontend Setup
cd frontend
npm install
npm start
Environment Variables
Create .env file:

DB_HOST=localhost
DB_USER=root
DB_PASS=yourpassword
JWT_SECRET=yourkey
MODEL_API_KEY=yourkey
```
---
🧪 Testing

Run tests using:

pytest

npm test

npx playwright test
---
🔐 Security & Privacy

Role-based authentication

Encrypted credentials

Anonymized patient data

Secure API access

No medical diagnosis
---
📅 Development Timeline

Week 1–2: Requirements & Design

Week 3–4: Backend & Emotion Engine

Week 5–6: AI Integration & Dashboard

Week 7: Testing & Optimization

Week 8: Final Release
---
⚠️ Limitations

Prototype-level deployment

Limited real patient data

No clinical validation

Web-based version only (v1)
---
  👥 Team
Name	    Role
Ashish	Project Lead

Ashish	ML Engineer

Shruti	Backend Developer

Aashi	  QA & Documentation
---
📜 Compliance
Academic Research Project

Institutional Ethics Guidelines

No Third-Party Data Sharing

No Clinical Decision Making
---
📈 Future Enhancements
Mobile App Support

Advanced Emotion Models

Multilingual Support

Wearable Integration
---
Real-time Medical Alerts
⭐ If you find this project useful, please star the repository!


---


