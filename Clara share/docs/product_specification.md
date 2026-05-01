# Detailed Product Specification: Emotion-Aware AI Companion for Dementia Care

## 1. Introduction
This document outlines the detailed specifications for a user-centric health support application tailored for dementia patients and their caregivers. The application combines emotion-aware conversational AI, real-time emotion detection, and comprehensive caregiver monitoring to provide a safe, engaging, and supportive environment for the patient while offering actionable insights to caregivers and medical professionals.

---

## 2. User Roles
1. **Patient**: The primary user interacting with the AI companion via text and voice chat.
2. **Caregiver / Family Member**: Secondary users who monitor the patient's emotional well-being, manage settings, and receive alerts.
3. **Doctor / Healthcare Professional**: Authorized personnel with access to historical emotional data and chat logs for medical assessment.

---

## 3. Core Features & Workflows

### 3.1. Authentication and Onboarding
* **First-Time Registration & Login**:
  * Users can register and log in using either an **Email ID** or a **Phone Number** (with OTP verification for simplicity).
  * **Persistent Login**: Secure token-based session management ensures returning users (especially patients who may struggle with remembering credentials) remain logged in automatically upon re-entry.
* **Post-Login Walkthrough (Onboarding)**:
  * A highly visual, step-by-step guided tutorial introduces the application.
  * Uses simple language, large typography, and voice-assisted guidance to explain how to chat, use the voice feature, and navigate the app.

### 3.2. Patient Profile Setup
Before accessing the core companion features, a comprehensive profile must be completed (often assisted by a caregiver):
* **Demographics**: Name, Age, Gender.
* **Emergency Contacts**: Primary family member designated for immediate emergency contact.
* **Care Team**: Additional family members or professional caregivers (including names, roles, and phone numbers).
* **Personal Context**:
  * Likes and dislikes.
  * Hobbies and past professions.
  * Key life events or fond memories to be used by the AI to ground conversations and reduce anxiety.

### 3.3. Multimodal Chat Interface (Text & Voice)
* **Empathetic AI Chat**:
  * The AI persona is designed to be universally calm, supportive, and patient.
  * Responses are dynamically personalized using the patient’s profile data (e.g., asking about their specific hobbies or referencing familiar family members to provide comfort).
* **Voice Chat Integration**:
  * Features a prominent, accessible "Push to Talk" or "Always Listening" voice toggle.
  * Utilizes high-quality, human-like Text-to-Speech (TTS) synthesis to sound natural and reassuring, avoiding robotic tones that might confuse the patient.
* **Visual Interface**:
  * Clutter-free UI with high contrast, large buttons, and soft, calming color palettes.

### 3.4. Emotion Detection & Response Adaptation
* **Real-Time Recognition**: Uses camera and voice inputs to detect real-time emotions such as Sadness, Happiness, Fear, Anger, and Neutral.
* **Dynamic Adaptation**: The AI companion adjusts its conversational tone based on the detected emotion (e.g., speaking softer and more reassuringly if fear or anxiety is detected).

### 3.5. Critical Alert System
* **Distress Monitoring**: The AI continuously scans chat inputs (text and transcribed voice) for critical statements indicating severe distress or self-harm (e.g., "I want to die", "I am lost and scared").
* **Discreet Notifications**:
  * Upon detecting a critical trigger, the system immediately and discreetly dispatches an alert (SMS, push notification, and Email) to the designated emergency contacts, caregivers, and doctors.
  * **Crucial UX Note**: The alert is sent silently in the background. The patient is *not* informed of the alert; instead, the AI seamlessly pivots to a highly comforting, de-escalating conversation script.

### 3.6. Caregiver Dashboard & Data Management
* **Secure Data Storage**: All conversations are stored in a secure, encrypted database, fully compliant with healthcare data privacy standards (e.g., HIPAA/GDPR principles).
* **Authorized Access**: Caregivers and doctors can access these transcripts to review the patient’s day-to-day state of mind.
* **Dashboard Metrics**:
  * **Activity Summary**: Total conversation duration, frequency of interactions.
  * **Emotional Trends**: Date-wise graphs showing the distribution of emotions (e.g., 60% Happy, 30% Neutral, 10% Anxious).
  * **Incident Logging**: A specific log detailing the frequency, dates, and times of panic attacks, severe anxiety episodes, or triggered critical alerts.
  * **General Health Data**: Any other integrated metrics (e.g., if wearable data is added in the future).

---

## 4. User Experience (UX) & Design Guidelines

### For the Patient:
* **Accessibility First**: Large, legible fonts (e.g., Inter, Roboto), high-contrast elements, and minimal cognitive load on each screen.
* **Forgiving Interface**: No complex menus or deep navigation trees. The primary screen should be the companion chat/voice interface.
* **Aesthetics**: Use soft, calming colors (pastels, soft blues, greens) that do not overstimulate.

### For the Caregiver / Doctor:
* **Data-Rich but Intuitive**: Use clear data visualizations (charts, heatmaps) to represent emotional trends over time.
* **Action-Oriented**: Important alerts and recent panic episodes should be highlighted at the very top of the dashboard for immediate visibility.

---

## 5. Security & Privacy Considerations
* **Role-Based Access Control (RBAC)**: Strict segregation between Patient views (strictly interaction) and Caregiver/Doctor views (analytics and settings).
* **Data Encryption**: End-to-end encryption for chat logs and sensitive profile data.
* **Transparency**: Clear consent flows during the onboarding process regarding the recording of voice/video for emotion detection and data sharing with the care team.
