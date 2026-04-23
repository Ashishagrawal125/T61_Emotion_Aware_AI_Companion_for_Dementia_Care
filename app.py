# Clara AI Enhancement: Improved logging and response handling
import os
import uuid
import time
import tempfile
from pathlib import Path

import cv2
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from PIL import Image
import streamlit as st
from transformers import pipeline
from streamlit_mic_recorder import mic_recorder
from deepface import DeepFace

import Google_Translate
import Sarvam_STT
import tts_tutorial

APP_TITLE = "Clara AI - Emotion Aware Companion"
RECORDINGS_DIR = Path("recordings")
IMAGES_DIR = Path("images")
RECORDINGS_DIR.mkdir(exist_ok=True)
IMAGES_DIR.mkdir(exist_ok=True)

st.set_page_config(
    page_title="Clara AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .main {background: linear-gradient(135deg, #f7f8fc 0%, #eef2ff 100%);} 
    .stButton>button {
        width: 100%; border-radius: 16px; border: none; padding: 0.7rem 1rem;
        background: linear-gradient(90deg, #6d5efc 0%, #ff6b8a 100%);
        color: white; font-weight: 600;
    }
    .card {
        background: white; padding: 1.2rem; border-radius: 18px; 
        box-shadow: 0 8px 24px rgba(0,0,0,0.08); margin-bottom: 1rem;
    }
    .hero {
        background: linear-gradient(90deg, #6d5efc 0%, #9d7cff 50%, #ff6b8a 100%);
        color: white; padding: 1.5rem; border-radius: 20px; margin-bottom: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def init_state() -> None:
    defaults = {
        "chat_history": [],
        "voice_chat_history": [],
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


init_state()


@st.cache_resource(show_spinner=False)
def get_face_detector():
    cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    if cascade.empty():
        raise RuntimeError("Failed to load Haar cascade for face detection.")
    return cascade


@st.cache_resource(show_spinner=False)
def get_sentiment_model():
    return pipeline(
        "text-classification",
        model="SamLowe/roberta-base-go_emotions",
        top_k=5,
        truncation=True,
    )


@st.cache_resource(show_spinner=False)
def get_chatbot():
    return pipeline(
        "text2text-generation",
        model="google/flan-t5-base",
        max_new_tokens=120,
    )


face_cascade = get_face_detector()
sentiment_model = get_sentiment_model()
chatbot = get_chatbot()


def analyze_face_emotions(image_bgr: np.ndarray):
    gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(40, 40))
    annotated = image_bgr.copy()
    detections = []

    for (x, y, w, h) in faces:
        face = image_bgr[y : y + h, x : x + w]
        try:
            result = DeepFace.analyze(face, actions=["emotion"], enforce_detection=False)
            if isinstance(result, list):
                result = result[0]
            emotion = result.get("dominant_emotion", "unknown")
            score = result.get("emotion", {}).get(emotion, 0.0)
        except Exception:
            emotion = "unknown"
            score = 0.0

        detections.append({"emotion": emotion, "score": score})
        cv2.rectangle(annotated, (x, y), (x + w, y + h), (80, 200, 120), 2)
        cv2.putText(
            annotated,
            f"{emotion}",
            (x, max(25, y - 10)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2,
        )

    return annotated, detections


EMOJI_MAP = {
    "joy": "😄",
    "sadness": "😢",
    "anger": "😠",
    "fear": "😨",
    "surprise": "😮",
    "love": "❤️",
    "caring": "🤗",
    "gratitude": "🙏",
    "nervousness": "😬",
    "confusion": "😕",
    "neutral": "😐",
    "optimism": "😊",
    "disappointment": "😞",
}


def analyze_text_emotion(text: str):
    results = sentiment_model(text)
    if results and isinstance(results[0], list):
        results = results[0]
    cleaned = sorted(results, key=lambda x: x["score"], reverse=True)
    return cleaned[:5]


SAFE_RESPONSE_FALLBACK = (
    "I am here with you. It sounds like things feel heavy right now. "
    "Take one slow breath with me. You can tell me what happened, and we can go one step at a time."
)


def build_supportive_reply(user_text: str) -> str:
    prompt = (
        "You are Clara, a calm and empathetic companion for dementia care support. "
        "Reply in simple, warm, non-judgmental language. Keep the answer short, supportive, and safe. "
        "Do not claim to diagnose medical issues. User message: "
        + user_text
    )
    try:
        output = chatbot(prompt)[0]["generated_text"].strip()
        return output if len(output.split()) >= 6 else SAFE_RESPONSE_FALLBACK
    except Exception:
        return SAFE_RESPONSE_FALLBACK



def render_sentiment_block(text: str):
    sentiments = analyze_text_emotion(text)
    if not sentiments:
        st.warning("No sentiment result generated.")
        return

    top = sentiments[0]
    emoji = EMOJI_MAP.get(top["label"], "🙂")
    st.success(f"Top emotion from voice text: {top['label'].title()} {emoji} ({top['score']:.2f})")

    lines = []
    for item in sentiments:
        emoji = EMOJI_MAP.get(item["label"], "🙂")
        lines.append(f"- {item['label'].title()} {emoji}: {item['score']:.2f}")
    st.markdown("\n".join(lines))



def save_audio_bytes(audio_bytes: bytes) -> str:
    file_path = RECORDINGS_DIR / f"recording_{uuid.uuid4().hex}.wav"
    with open(file_path, "wb") as f:
        f.write(audio_bytes)
    return str(file_path)


st.markdown(
    f"""
    <div class="hero">
        <h1>🧠 {APP_TITLE}</h1>
        <p>Emotion detection, empathetic chat, multilingual voice support, and simple wellness insights.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

c1, c2, c3 = st.columns(3)
with c1:
    st.markdown('<div class="card"><h3>🎤 Voice Analysis</h3><p>Record speech, transcribe it, translate if needed, and detect emotional tone.</p></div>', unsafe_allow_html=True)
with c2:
    st.markdown('<div class="card"><h3>📷 Facial Detection</h3><p>Upload images or use the camera to identify visible facial emotions.</p></div>', unsafe_allow_html=True)
with c3:
    st.markdown('<div class="card"><h3>💬 Supportive Chat</h3><p>Get calm, simple, human-like responses designed for emotional support.</p></div>', unsafe_allow_html=True)


tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🎤 Voice Analysis",
    "📷 Facial Detection",
    "❤️ Heart Rate",
    "💬 AI Chat",
    "🗣️ Voice Chat",
])

with tab1:
    st.subheader("Voice Analysis")
    st.info("Record audio, then transcribe and analyze the emotional tone from text.")

    audio = mic_recorder(
        start_prompt="🎙️ Start Recording",
        stop_prompt="⏹️ Stop Recording",
        just_once=False,
        use_container_width=True,
        key="voice_analysis_recorder",
    )

    if audio:
        audio_bytes = audio["bytes"]
        st.audio(audio_bytes, format="audio/wav")
        file_path = save_audio_bytes(audio_bytes)

        if st.button("Analyze Voice Emotion", key="analyze_voice_btn"):
            with st.spinner("Transcribing and analyzing..."):
                result = Sarvam_STT.detect_and_translate(file_path)
                transcript = result.get("transcript", "")
                source_lang = result.get("language_code", "unknown")

                if not transcript:
                    st.error("No transcript returned from speech-to-text.")
                else:
                    st.markdown(f"**Transcript:** {transcript}")
                    translated = transcript
                    if source_lang and not source_lang.lower().startswith("en"):
                        translated = Google_Translate.detect_and_translate(transcript)
                        st.markdown(f"**Translated to English:** {translated}")

                    render_sentiment_block(translated)

with tab2:
    st.subheader("Facial Detection")
    mode = st.radio(
        "Choose input",
        ["📸 Upload Image", "📹 Live Camera"],
        horizontal=True,
        key="face_mode",
    )

    image_bgr = None
    if mode == "📸 Upload Image":
        uploaded = st.file_uploader("Upload a face image", type=["jpg", "jpeg", "png"], key="face_upload")
        if uploaded is not None:
            image = Image.open(uploaded).convert("RGB")
            image_bgr = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    else:
        camera_file = st.camera_input("Capture photo", key="face_camera")
        if camera_file is not None:
            image = Image.open(camera_file).convert("RGB")
            image_bgr = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    if image_bgr is not None:
        annotated, detections = analyze_face_emotions(image_bgr)
        st.image(cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB), use_container_width=True)
        if detections:
            df = pd.DataFrame(detections)
            st.dataframe(df, use_container_width=True)
            top_emotion = df["emotion"].value_counts().idxmax()
            st.success(f"Detected primary facial emotion: {top_emotion.title()}")
        else:
            st.warning("No face detected. Try a clearer image with a visible face.")

with tab3:
    st.subheader("Heart Rate Monitor")
    st.info("Upload a CSV file with heart rate values. Supported columns: heart, heart_rate, bpm, pulse.")
    uploaded_csv = st.file_uploader("Upload heart rate CSV", type=["csv"], key="hr_csv")

    if uploaded_csv is not None:
        hr_data = pd.read_csv(uploaded_csv)
        hr_data.columns = [c.strip().lower() for c in hr_data.columns]
        heart_col = None
        for col in ["heart_rate", "heart", "bpm", "pulse"]:
            if col in hr_data.columns:
                heart_col = col
                break
        if heart_col is None:
            st.error("Could not find a heart rate column.")
        else:
            hr_data["heart_rate"] = pd.to_numeric(hr_data[heart_col], errors="coerce")
            hr_data = hr_data.dropna(subset=["heart_rate"]).reset_index(drop=True)
            if "time" not in hr_data.columns:
                hr_data["time"] = np.arange(len(hr_data))

            fig = go.Figure()
            fig.add_trace(
                go.Scatter(
                    x=hr_data["time"],
                    y=hr_data["heart_rate"],
                    mode="lines+markers",
                    name="Heart Rate",
                )
            )
            fig.update_layout(title="Heart Rate Trend", xaxis_title="Time", yaxis_title="BPM", height=420)
            st.plotly_chart(fig, use_container_width=True)

            avg_hr = hr_data["heart_rate"].mean()
            max_hr = hr_data["heart_rate"].max()
            min_hr = hr_data["heart_rate"].min()
            m1, m2, m3 = st.columns(3)
            m1.metric("Average", f"{avg_hr:.1f} BPM")
            m2.metric("Maximum", f"{max_hr:.1f} BPM")
            m3.metric("Minimum", f"{min_hr:.1f} BPM")

            if avg_hr < 60:
                st.warning("Average heart rate is below the normal resting range.")
            elif avg_hr > 100:
                st.warning("Average heart rate is above the normal resting range.")
            else:
                st.success("Average heart rate is within the normal resting range.")
    else:
        st.caption("No CSV uploaded yet.")

with tab4:
    st.subheader("AI Chat")
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    prompt = st.chat_input("Type how you are feeling...", key="ai_chat_input")
    if prompt:
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        reply = build_supportive_reply(prompt)
        with st.chat_message("assistant"):
            placeholder = st.empty()
            current = ""
            for ch in reply:
                current += ch
                placeholder.write(current)
                time.sleep(0.01)
        st.session_state.chat_history.append({"role": "assistant", "content": reply})

    if st.button("Clear Chat", key="clear_ai_chat"):
        st.session_state.chat_history = []
        st.rerun()

with tab5:
    st.subheader("Voice Chat")
    voice_audio = mic_recorder(
        start_prompt="🎙️ Start Voice Chat",
        stop_prompt="⏹️ Stop Recording",
        just_once=False,
        use_container_width=True,
        key="voice_chat_recorder",
    )

    if voice_audio:
        voice_bytes = voice_audio["bytes"]
        st.audio(voice_bytes, format="audio/wav")
        voice_path = save_audio_bytes(voice_bytes)

        if st.button("Send Voice Message", key="send_voice_msg"):
            with st.spinner("Listening and replying..."):
                result = Sarvam_STT.detect_and_translate(voice_path)
                transcript = result.get("transcript", "")
                source_lang = result.get("language_code", "en")

                if not transcript:
                    st.error("Could not transcribe the voice input.")
                else:
                    english_text = transcript
                    target_lang = "en"
                    if source_lang and not source_lang.lower().startswith("en"):
                        english_text, target_lang = Google_Translate.change_to_target(transcript, "en")
                    st.markdown(f"**You said:** {transcript}")

                    reply_en = build_supportive_reply(english_text)
                    final_text = reply_en
                    output_lang = "en"
                    if source_lang and not source_lang.lower().startswith("en"):
                        final_text, output_lang = Google_Translate.change_to_target(reply_en, target_lang)

                    st.markdown(f"**Clara:** {final_text}")
                    try:
                        audio_file = tts_tutorial.text_to_speech(final_text, output_lang)
                        if audio_file and os.path.exists(audio_file):
                            with open(audio_file, "rb") as f:
                                st.audio(f.read(), format="audio/wav")
                    except Exception as exc:
                        st.warning(f"Reply text generated, but text-to-speech failed: {exc}")

st.markdown("---")
st.markdown(
    "<div class='card'><b>Clara AI</b><br/>Emotion-aware support for conversation, facial analysis, and multilingual voice interaction.</div>",
    unsafe_allow_html=True,
)
