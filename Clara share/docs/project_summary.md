# 🧠 Project Clara: Emotion-Aware AI Companion for Dementia Care

Project Clara is an advanced, multi-modal AI application designed to support dementia patients and their caregivers. It bridges the gap between clinical care and emotional support by providing a compassionate AI companion that understands and responds to the user's emotional state.

---

## 🏗️ Technical Architecture

The project follows a modern **Client-Server Architecture** with a clear separation between the AI processing, data management, and user interface layers.

### 1. Frontend (The User Experience)
*   **Framework**: Next.js 15+ (React 19)
*   **Styling**: Tailwind CSS 4 for a professional, glassmorphic, and responsive UI.
*   **Animations**: Framer Motion for smooth transitions and empathetic micro-interactions.
*   **Key Components**:
    *   `EmotionCamera`: Real-time video feed analysis.
    *   `VoiceAssistant`: Hands-free STT and TTS interaction.
    *   `CaregiverDashboard`: Data visualization and alert monitoring.

### 2. Backend (The Intelligence Hub)
*   **Framework**: FastAPI (Python)
*   **AI Engine**: 
    *   **Conversational AI**: Groq (Llama-3.1-8b) for empathetic text generation.
    *   **Emotion Recognition**: DeepFace + OpenCV for facial expression analysis.
    *   **Speech Processing**: OpenAI Whisper for multilingual STT.

### 3. Database (The Memory Store)
*   **Engine**: SQLite (SQLAlchemy ORM)
*   **Key Tables**: Caregivers, Patients, EmotionLogs, ChatHistory, Alerts.

---

## 🔄 Core Functionality

1.  **Multi-Modal Input**: Captures user's voice, face, and text.
2.  **Emotion-Aware Responses**: AI tone shifts based on detected user emotion (Sad, Anxious, etc.).
3.  **Bilingual Support**: Full support for English, Hindi, and Hinglish.
4.  **Emergency Alert System**: Scans for distress and notifies caregivers via Email/SMS.

---

## 📂 File Structure

*   `frontend/app/`: Next.js pages and routing.
*   `backend/app/routes/`: API endpoints for Chat, Emotion, and Alerts.
*   `backend/app/models.py`: Database structure.
