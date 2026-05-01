# 👵 Clara AI: Emotion-Aware AI Companion for Dementia Care
**Team ID: 61 | GLA University | 2025-2026**

Clara AI is a specialized medical companion designed to provide emotional support to dementia patients and actionable insights to caregivers. It uses multimodal emotion detection (Face/Voice) and empathetic AI reasoning.

## 🚀 Getting Started

### 1. Prerequisites
- **Python 3.10+**
- **Node.js 18+**
- **Webcam** (for emotion detection)

### 2. Backend Setup
1. Open a terminal and navigate to the `backend` folder:
   ```bash
   cd backend
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the backend server:
   ```bash
   uvicorn app.main:app --reload
   ```
   *The API will be live at `http://127.0.0.1:8000`*

### 3. Frontend Setup
1. Open a **second** terminal and navigate to the `frontend` folder:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Run the development server:
   ```bash
   npm run dev
   ```
   *The application will be live at `http://localhost:3000`*

---

## 🛠️ Key Features
- **Real-Time Emotion Tracking**: Uses DeepFace to monitor patient mood via webcam.
- **Bilingual Support**: Full English and Devanagari Hindi conversational support.
- **Emergency Safety Radar**: Automatically detects crisis phrases and sends real-time SMS alerts via Twilio.
- **Caregiver Dashboard**: Comprehensive visualization of emotional trends and interaction logs.

## 🏗️ Tech Stack
- **Frontend**: Next.js, React, Tailwind CSS, Recharts.
- **Backend**: FastAPI, SQLAlchemy, SQLite.
- **AI/ML**: DeepFace (vgg-face), Groq (Llama-3-70B), Web Speech API.
- **Messaging**: Twilio SMS API.

---

## 👥 Team Members
1. **Ashish Agrawal** (2315510043)
2. **Shruti Gupta** (2315510200)
3. **Aashi Garg** (2315510003)

**Mentor**: Gourav Bathla
