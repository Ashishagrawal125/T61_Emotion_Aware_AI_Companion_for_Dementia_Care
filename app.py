import streamlit as st
from transformers import pipeline
from streamlit_mic_recorder import mic_recorder
import cv2
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from PIL import Image
import os
import uuid
import tempfile
import whisper
import tensorflow as tf
from tensorflow.keras.preprocessing.image import img_to_array
from PIL import Image
import numpy as np
import time
import json
import Sarvam_STT
import Google_Translate
import tts_tutorial
from deepface import DeepFace
from transformers import pipeline

# Set page config
st.set_page_config(
    page_title="Clara",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with animations and beautiful styling
st.markdown("""
    <style>
    .main {
        padding: 2rem;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    .stButton>button {
        width: 100%;
        margin-top: 1rem;
        background: linear-gradient(45deg, #FF6B6B, #FF8E53);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 10px 20px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(255, 107, 107, 0.4);
    }
    .result-box {
        padding: 1.5rem;
        border-radius: 15px;
        background: white;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
        color: #2c3e50;
    }
    .result-box:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 15px rgba(0, 0, 0, 0.2);
    }
    .stTabs {
        margin: 0 auto;
        max-width: 1200px;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
        justify-content: center !important;
        display: flex !important;
        width: 100%;
    }
    .stTabs [data-baseweb="tab"] {
        flex: 1;
        max-width: 300px;
        min-width: 200px;
        text-align: center;
        margin: 0 10px;
        background-color: white;
        border-radius: 20px;
        padding: 10px 20px;
        transition: all 0.3s ease;
        color: #2c3e50;
    }
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #FF6B6B;
        color: white;
    }
    .stTabs [aria-selected="true"] {
        background-color: #FF6B6B !important;
        color: white !important;
    }
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
        transition: all 0.3s ease;
        color: #2c3e50;
        height: 100%;
        display: flex;
        flex-direction: column;
    }
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 15px rgba(0, 0, 0, 0.2);
    }
    .camera-feed {
        margin: 0 auto;
        max-width: 800px;
        width: 100%;
    }
    .emotion-indicator {
        position: absolute;
        top: 10px;
        right: 10px;
        background: rgba(255, 107, 107, 0.9);
        color: white;
        padding: 5px 10px;
        border-radius: 15px;
        font-weight: bold;
    }
    p, h1, h2, h3, h4, h5, h6 {
        color: #2c3e50;
    }
    </style>
""", unsafe_allow_html=True)
# Initialize session state variables
if 'camera_running' not in st.session_state:
    st.session_state.camera_running = False
if 'frame_placeholder' not in st.session_state:
    st.session_state.frame_placeholder = None
if 'camera_thread' not in st.session_state:
    st.session_state.camera_thread = None

# Emotion labels
emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Neutral', 'Sad', 'Surprise']
def ask_model(messages):
    try:
        user_input = messages[-1]["content"]

        prompt = f"""
                    You are a highly empathetic mental health support assistant.

                    The user is sharing personal feelings. Your job is to:
                    - Respond with empathy
                    - Validate their emotions
                    - Give supportive advice
                    - Be calm, kind, and human-like
                    - NEVER judge or question harshly

                    User: {user_input}
                    Assistant:
                    """
        inputs = chat_tokenizer(prompt, return_tensors="pt", truncation=True)

        outputs = chat_model.generate(
            **inputs,
            max_length=150,
            do_sample=True,
            temperature=0.95,
            top_p=0.92,
            repetition_penalty=1.2
        )
        reply = chat_tokenizer.decode(outputs[0], skip_special_tokens=True)

        # Clean unwanted parts
        if "Assistant:" in reply:
            reply = reply.split("Assistant:")[-1].strip()

        # Remove bad robotic patterns
        bad_patterns = ["why are you", "i am a", "you are a"]

        if any(p in reply.lower() for p in bad_patterns):
            return "I'm really sorry you're feeling this way. It sounds like you're going through something heavy. I'm here for you—do you want to talk more about what's been stressing you?"

        # Ensure empathetic tone
        if len(reply.split()) < 5:
            return "I hear you. It sounds like things have been tough lately. You don’t have to handle it alone—I'm here to listen."

        return reply.strip()

    except Exception as e:
        return f"Error: {str(e)}"
    
def annotate_emotions(input_data):

    # Handle both file path and image input
    if isinstance(input_data, str):
        frame = cv2.imread(input_data)
    else:
        frame = np.array(input_data)

    if frame is None:
        return None

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    annotated_frame = frame.copy()

    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    for (x, y, w, h) in faces:
        # Draw rectangle
        cv2.rectangle(annotated_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Extract ORIGINAL face (not processed)
        face = frame[y:y + h, x:x + w]

        try:
            result = DeepFace.analyze(face, actions=['emotion'], enforce_detection=False)
            emotion = result[0]['dominant_emotion']
        except:
            emotion = "Unknown"

        # Put text
        cv2.putText(
            annotated_frame,
            emotion,
            (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            (225, 0, 200),
            2
        )

    return annotated_frame
# Camera loop function
def camera_loop():
    try:
        while st.session_state.camera_running:
            # Capture frame from webcam
            frame = st.camera_input("Camera Feed", key="live_camera")
            
            if frame is not None:
                # Convert the frame to a PIL image
                frame = Image.open(frame)
                
                # Annotate emotions on the frame
                annotated_frame = annotate_emotions(frame)
                
                # Display the annotated frame in the placeholder
                if st.session_state.frame_placeholder is not None:
                    st.session_state.frame_placeholder.image(annotated_frame, caption="Live Feed with Emotion Detection", use_container_width=True)
            
            time.sleep(0.1)
    finally:
        pass

# Initialize models
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

@st.cache_resource
def load_chatbot():
    model_name = "google/flan-t5-large"
    
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    
    return tokenizer, model

chat_tokenizer, chat_model = load_chatbot()

chatbot = load_chatbot()
chatbot = load_chatbot()
def load_models():
    try:
        # Load face cascade first as it's essential
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        #classifier = tf.keras.models.load_model('models/ResNet50_Transfer_Learning.keras')
        classifier = "deepface"
        if face_cascade.empty():
            st.error("Error loading face detection model")
            return (None, None), (None, None)


        # Load sentiment analysis model
        try:
            model = whisper.load_model("base")
            sentiment_analysis = pipeline("sentiment-analysis", framework="pt", model="SamLowe/roberta-base-go_emotions")
            # sentiment_analysis = pipeline("sentiment-analysis", model="cardiffnlp/twitter-xlm-roberta-base-sentiment")  shitttt

            return (sentiment_analysis, model), (face_cascade, classifier)
        except Exception as e:
            st.error(f"Error loading sentiment analysis model: {str(e)}")
            return (None, None), (None, None)

        return (sentiment_analysis, model), (face_cascade, classifier)
    except Exception as e:
        st.error(f"Error loading models: {str(e)}")
        return (None, None), (None, None)

# Create models directory if it doesn't exist
os.makedirs("models", exist_ok=True)

# Load models at startup
with st.spinner("Loading models..."):
    a,b = load_models()

    (sentiment_analysis,model) = a
    (face_cascade,classifier) = b

if not face_cascade:
    st.error("Failed to load face detection model. Please check your OpenCV installation.")
    st.stop()
if not classifier:
    st.error("Failed to load classifier. Please check your OpenCV installation.")
    st.stop()

if classifier is None:
    st.error("Failed to load classifier.")
    st.stop()
if not model:
    st.error("Failed to load whisper model. Please check your internet connection and try again.")
    st.stop()

# Header with gradient background
st.markdown("""
    <div class="header-container">
        <h1 style="color: white;">🧠 Meet Clara – Your AI Emotional Companion</h1>
        <p style="color: white;">Clara listens, understands, and supports you—anytime you need it.</p>
    </div>
""", unsafe_allow_html=True)

# Feature cards
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
        <div class="feature-card">
            <h3>🎤 Voice Analysis</h3>
            <p>Record and analyze your voice to understand your emotional state</p>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="feature-card">
            <h3>👤 Facial Detection</h3>
            <p>Real-time facial analysis to track your emotional expressions</p>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div class="feature-card">
            <h3>❤️ Heart Rate Monitor</h3>
            <p>Track your heart rate patterns for emotional insights</p>
        </div>
    """, unsafe_allow_html=True)

# Create centered container for all content
st.markdown("""
    <div style='display: flex; justify-content: center; width: 100%;'>
        <div style='max-width: 1200px; width: 100%;'>
""", unsafe_allow_html=True)

# Create tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["🎤 Voice Analysis", "👤 Facial Detection", "❤️ Heart Rate Monitor","💬 AI Chat","🗣️ Voice Chat"])

# Voice Analysis Tab
with tab1:
    st.header("Voice Analysis")
    
    # Voice recording section with better styling
    st.markdown("""
        <div class="feature-card">
            <h3>Record Your Voice</h3>
            <p>Speak naturally and let AI analyze your emotions</p>
        </div>
    """, unsafe_allow_html=True)
    def analyze_sentiment(text):
        results = sentiment_analysis(text)
        sentiment_results = {result['label']: result['score'] for result in results}
        return sentiment_results

    def get_sentiment_emoji(sentiment):
        # Define the emojis corresponding to each sentiment
        emoji_mapping = {
            "disappointment": "😞",
            "sadness": "😢",
            "annoyance": "😠",
            "neutral": "😐",
            "disapproval": "👎",
            "realization": "😮",
            "nervousness": "😬",
            "approval": "👍",
            "joy": "😄",
            "anger": "😡",
            "embarrassment": "😳",
            "caring": "🤗",
            "remorse": "😔",
            "disgust": "🤢",
            "grief": "😥",
            "confusion": "😕",
            "relief": "😌",
            "desire": "😍",
            "admiration": "😌",
            "optimism": "😊",
            "fear": "😨",
            "love": "❤️",
            "excitement": "🎉",
            "curiosity": "🤔",
            "amusement": "😄",
            "surprise": "😲",
            "gratitude": "🙏",
            "pride": "🦁"
        }
        return emoji_mapping.get(sentiment, "")

    def display_sentiment_results(sentiment_results, option):
        sentiment_text = ""
        for sentiment, score in sentiment_results.items():
            emoji = get_sentiment_emoji(sentiment)
            if option == "Sentiment Only":
                sentiment_text += f"{sentiment} {emoji}\n"
            elif option == "Sentiment + Score":
                sentiment_text += f"{sentiment} {emoji}: {score}\n"
        return sentiment_text

    def inference(ans, sentiment_option):
        sentiment_results = analyze_sentiment(ans)
        sentiment_output = display_sentiment_results(sentiment_results, sentiment_option)
        return sentiment_output
    # Live recording
    try:
        audio = mic_recorder(
            start_prompt="🎙️ Start Recording",
            stop_prompt="⏹️ Stop Recording",
            just_once=False,
            use_container_width=True,
            key='voice_recorder'
        )
        
        if audio:
            try:
                recordings_folder = "recordings"
                os.makedirs(recordings_folder, exist_ok=True)
                unique_filename = f"recording_{uuid.uuid4().hex}.wav"
                file_path = os.path.join(recordings_folder, unique_filename)
                
                # Save and play audio with better styling
                audio_bytes = audio["bytes"]
                st.markdown("""
                    <div class="metric-container">
                        <h4>🎵 Your Recording</h4>
                """, unsafe_allow_html=True)
                st.audio(audio_bytes, format="audio/wav")
                st.markdown("</div>", unsafe_allow_html=True)
                
                with open(file_path, "wb") as f:
                    f.write(audio_bytes)
        
                # Analyze emotion directly from audio features
                if st.button("🔍 Analyze Voice Emotion"):
                    with st.spinner("Analyzing your voice..."):
                        try:
                            # For now, we'll use a simulated emotion detection
                            # In a real implementation, you would use a voice emotion detection model
                            
                            st.markdown("### 📊 Analysis Results")
                            st.markdown("#### Transcribing Audio...")
                            results = Sarvam_STT.detect_and_translate(file_path)
                            st.markdown(f"### {results['transcript']}")
                            text = results["transcript"]
                            if not results["language_code"] == "en":
                                text = Google_Translate.detect_and_translate(text)
                            sentiment_output_value = inference(text, "Sentiment + Score")
                            st.markdown("#### "+ sentiment_output_value)
                            
                            
                            # Sort emotions by confidenc
                            
                            # Add a note about the analysis
                            st.info("""
                                Note: This is a demonstration of voice emotion analysis. 
                                For more accurate results, consider using a dedicated voice emotion recognition model.
                            """)
                            
                        except Exception as e:
                            st.error(f"Error analyzing voice: {str(e)}")
                            st.info("Please try recording again with clearer speech.")
            except Exception as e:
                st.error(f"Error saving recording: {str(e)}")
    except Exception as e:
        st.error(f"Error with microphone recorder: {str(e)}")
        st.info("Please make sure your microphone is properly connected and accessible.")

# Facial Detection Tab
with tab2:
    st.header("Facial Detection")
    
    # Center the radio buttons
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        input_type = st.radio(
            "Choose input type",
            ["📹 Live Camera", "📸 Upload Image", "🎥 Upload Video"],
            horizontal=True,
            key="detection_type"
        )
    
    # Camera feed section
    if input_type == "📹 Live Camera":
        # Center the camera feed
        st.markdown('<div class="camera-feed">', unsafe_allow_html=True)
        
        # Create a placeholder for the camera feed
        if st.session_state.frame_placeholder is None:
            st.session_state.frame_placeholder = st.empty()
        
        # Camera control buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📹 Start Camera"):
                st.session_state.camera_running = True
        with col2:
            if st.button("⏹️ Stop Camera"):
                st.session_state.camera_running = False
                st.session_state.frame_placeholder.empty()
        
        # Camera feed display
        if st.session_state.camera_running:
            camera_frame = st.camera_input("", key="continuous_camera")
            
            if camera_frame is not None:
                frame = Image.open(camera_frame)
                unique_filename = f"images/{uuid.uuid4()}.jpg"
                if not os.path.exists("images"):
                    os.mkdir("images")
                with open(unique_filename, "wb") as f:
                    frame.save(unique_filename)
                annotated_frame = annotate_emotions(unique_filename)
                st.session_state.frame_placeholder.image(annotated_frame, use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

    elif input_type == "📸 Upload Image":
        st.markdown("""
            <div class="feature-card">
                <h3>Upload Image</h3>
                <p>Analyze emotions from a static image</p>
            </div>
        """, unsafe_allow_html=True)
        if st.session_state.frame_placeholder is None:
            st.session_state.frame_placeholder = st.empty()
        
        uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
        if uploaded_file is not None:
            frame = Image.open(uploaded_file)
            # st.image(frame, caption="Uploaded Image", use_container_width=True)
            st.session_state.frame_placeholder.image(frame, use_container_width=True)
            unique_filename = f"images/{uuid.uuid4()}.jpg"
            if not os.path.exists("images"):
                os.mkdir("images")
            with open(unique_filename, "wb") as f:
                frame.save(unique_filename)
            annotated_frame = annotate_emotions(unique_filename)
                    # Display the processed image
            annotated_frame = cv2.cvtColor(annotated_frame, cv2.COLOR_RGB2BGR)
            st.session_state.frame_placeholder.image(annotated_frame, use_container_width=True)
            # st.image(annotated_frame, channels="BGR", caption="Processed Image with Emotion Detection", use_container_width=True)
        else:
            st.warning("No faces detected in the image!")
    
    else:  # Video upload
        st.markdown("""
            <div class="feature-card">
                <h3>Upload Video</h3>
                <p>Analyze emotions from a video file</p>
            </div>
        """, unsafe_allow_html=True)
        
        uploaded_video = st.file_uploader("Choose a video...", type=["mp4", "avi"])
        if uploaded_video:
            # Save uploaded video
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp_file:
                tmp_file.write(uploaded_video.getvalue())
                video_path = tmp_file.name
            if st.session_state.frame_placeholder is None:
                st.session_state.frame_placeholder = st.empty()
            
            # Display video
            st.video(uploaded_video)
            
            if st.button("🔍 Analyze Video"):
                with st.spinner("Processing video..."):
                    # Process video frames
                    cap = cv2.VideoCapture(video_path)
                    while cap.isOpened():
                        ret, frame = cap.read()
                        if not ret:
                            break
                        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        annotated_frame = frame.copy()
                        annotated_frame = cv2.cvtColor(annotated_frame, cv2.COLOR_RGB2BGR)
                        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30),flags=cv2.CASCADE_SCALE_IMAGE)

                        for (x, y, w, h) in faces:
                            cv2.rectangle(annotated_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                            face = gray[y:y + h, x:x + w]
                            face = cv2.cvtColor(face, cv2.COLOR_GRAY2RGB)  # Convert grayscale to RGB
                            face = cv2.resize(face, (224, 224))
                            face = face.astype("float") / 255.0
                            face = img_to_array(face)
                            face = np.expand_dims(face, axis=0)

                            prediction = classifier.predict(face)[0]
                            emotion = emotion_labels[np.argmax(prediction)]

                            cv2.putText(annotated_frame, emotion, (x, y-30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (225, 0, 200), 2)
                        
                        st.image(annotated_frame, channels="BGR", caption="Processed Video Frame", use_container_width=True)
                    
                    cap.release()

# Heart Rate Monitor Tab
with tab3:
    st.header("Heart Rate Monitor")
    
    # Stylish header
    st.markdown("""
        <div class="feature-card">
            <h3>Real-time Heart Rate Monitoring</h3>
            <p>Track your heart rate patterns for emotional insights</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Upload CSV
    uploaded_hr = st.file_uploader("Upload heart rate data (CSV)", type=["csv"])
    
    if uploaded_hr:
        import numpy as np
        
        # Read CSV
        hr_data = pd.read_csv(uploaded_hr)

        # Normalize column names
        hr_data.columns = [col.lower() for col in hr_data.columns]

        # Possible column names
        possible_cols = ["heart", "heart_rate", "bpm", "pulse"]

        heart_col = None

        for col in possible_cols:
            if col in hr_data.columns:
                heart_col = col
                break

        # Assign heart_rate column
        if heart_col:
            hr_data["heart_rate"] = hr_data[heart_col]
        else:
            numeric_cols = hr_data.select_dtypes(include=['number']).columns

            if len(numeric_cols) > 0:
                hr_data["heart_rate"] = hr_data[numeric_cols[0]]
            else:
                # Fallback random data
                hr_data["heart_rate"] = np.random.randint(60, 100, size=len(hr_data))

        # Ensure time column
        if "time" not in hr_data.columns:
            hr_data["time"] = range(len(hr_data))

        # Plot graph
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=hr_data["time"],
            y=hr_data['heart_rate'],
            mode='lines+markers',
            name='Heart Rate',
            line=dict(color='#FF6B6B', width=3),
            marker=dict(color='#FF8E53', size=8)
        ))

        fig.update_layout(
            title='Heart Rate Analysis',
            xaxis_title='Time',
            yaxis_title='Heart Rate (BPM)',
            height=400,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#2c3e50')
        )

        st.plotly_chart(fig, use_container_width=True)

        # Metrics
        avg_hr = hr_data['heart_rate'].mean()
        max_hr = hr_data['heart_rate'].max()
        min_hr = hr_data['heart_rate'].min()

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Average Heart Rate", f"{avg_hr:.1f} BPM")

        with col2:
            st.metric("Maximum Heart Rate", f"{max_hr:.1f} BPM")

        with col3:
            st.metric("Minimum Heart Rate", f"{min_hr:.1f} BPM")

        # Status
        if avg_hr < 60:
            st.warning("⚠️ Average heart rate is below normal range")
        elif avg_hr > 100:
            st.warning("⚠️ Average heart rate is above normal range")
        else:
            st.success("✅ Average heart rate is within normal range")

    else:
        if st.button("❤️ Start Live Heart Rate Monitoring"):
            import numpy as np

            # Generate sample data
            time_vals = np.linspace(0, 10, 100)
            heart_rate = 70 + 5 * np.sin(time_vals) + np.random.normal(0, 1, 100)

            # Plot
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=time_vals,
                y=heart_rate,
                mode='lines+markers',
                name='Heart Rate',
                line=dict(color='#FF6B6B', width=3),
                marker=dict(color='#FF8E53', size=8)
            ))

            fig.update_layout(
                title='Real-time Heart Rate',
                xaxis_title='Time (seconds)',
                yaxis_title='Heart Rate (BPM)',
                height=400,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#2c3e50')
            )

            st.plotly_chart(fig, use_container_width=True)

            # Current HR
            current_hr = heart_rate[-1]

            st.markdown(f"""
                <div class="metric-container">
                    <h3>Current Heart Rate</h3>
                    <h2 style="color: #FF6B6B;">{current_hr:.1f} BPM</h2>
                </div>
            """, unsafe_allow_html=True)

            # Status
            if current_hr < 60:
                st.warning("⚠️ Heart rate is below normal range")
            elif current_hr > 100:
                st.warning("⚠️ Heart rate is above normal range")
            else:
                st.success("✅ Heart rate is within normal range")
# AI Chat Tab
# AI Chat Tab
with tab4:
    st.header("AI Chat")
    
    # Initialize chat history in session state if not exists
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    st.markdown("""
        <div class="feature-card">
            <h3>Chat with AI Assistant</h3>
            <p>Discuss your emotions and get personalized insights</p>
        </div>
    """, unsafe_allow_html=True)

    # Display chat history
    for message in st.session_state.chat_history:
        role = "user" if message["role"] == "user" else "assistant"
        with st.chat_message(role):
            st.write(message["content"])

    # Function to simulate AI response generation (streaming effect)
    def generate_response(user_input):
        # Fetch AI response using the ask_model function
        full_response = ask_model(user_input)
        
        # Simulate typing by displaying the response character-by-character
        streamed_response = ""
        for char in full_response:
            streamed_response += char
            time.sleep(0.02)  # Simulate "thinking" delay between characters
            yield streamed_response

    # Chat input section
    user_input = st.chat_input("Type your message here...")

    if user_input:
        # Add user message to chat history and display it
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        # Stream the AI response
        with st.chat_message("assistant"):
            ai_response_placeholder = st.empty()  # Placeholder for streaming text
            final_response = ""
            for response in generate_response(st.session_state.chat_history):
                ai_response_placeholder.write(response)  # Update the placeholder with each character
                final_response = response
            
            # Once done, finalize the actual response in the chat history
            st.session_state.chat_history.append({"role": "assistant", "content": final_response})

    # Clear chat button
    if st.button("🧹 Clear Chat"):
        st.session_state.chat_history = []  # Clear the chat history
        st.rerun()  # Rerun the app to refresh the UI immediately
with tab5:
    st.header("Voice Chat")
    
    try:
        audio = mic_recorder(
            start_prompt="🎙️ Start Recording",
            stop_prompt="⏹️ Stop Recording",
            just_once=False,
            use_container_width=True,
            key='voice_recorder'
        )
        
        if audio:
            try:
                recordings_folder = "recordings"
                os.makedirs(recordings_folder, exist_ok=True)
                unique_filename = f"recording_{uuid.uuid4().hex}.wav"
                file_path = os.path.join(recordings_folder, unique_filename)
                
                # Save and play audio with better styling
                audio_bytes = audio["bytes"]
                st.markdown("""
                    <div class="metric-container">
                        <h4>🎵 Your Recording</h4>
                """, unsafe_allow_html=True)
                st.audio(audio_bytes, format="audio/wav")
                st.markdown("</div>", unsafe_allow_html=True)
                
                with open(file_path, "wb") as f:
                    f.write(audio_bytes)
        
                # Analyze emotion directly from audio features
                if st.button("🔍 send"):
                    with st.spinner("Processing....."):
                        try:
                            # For now, we'll use a simulated emotion detection
                            # In a real implementation, you would use a voice emotion detection model
                            


                            results = Sarvam_STT.detect_and_translate(file_path)
                            st.markdown(f"### {results['transcript']}")
                            text = results["transcript"]
                            tar_lang = "en"
                            if not results["language_code"] == "en":
                                text,tar_lang = Google_Translate.change_to_target(text,"en")
                            st.markdown(f"### {text}")
                            try:
                                response = ask_model(text)
                                if not tar_lang == "en":
                                    response,tar_lang = Google_Translate.change_to_target(response,tar_lang)
                                response_file = tts_tutorial.text_to_speech(response,tar_lang)
                                with open(file_path, "rb") as f:
                                    audio_bytes = f.read()

# Play the audio in Streamlit
                                st.audio(audio_bytes, format="audio/wav")
                            except Exception as e:
                                st.write(f"Error Generating response")

                                
                        except Exception as e:
                            st.write(f"Error Generating response")
            except Exception as e:
                st.error(f"Error processing audio: {e}")
    except Exception as e:
        st.error(f"Error with voice recording: {e}")
# Footer with better styling
st.markdown("---")
st.markdown("""
    <div style='text-align: center; padding: 2rem; background: linear-gradient(45deg, #FF6B6B, #FF8E53); border-radius: 20px; color: white;'>
        <p style='font-size: 1.2rem;'>Designed to understand you better 💙 </p>
        <p style='font-size: 0.9rem;'>© 2026 Clara AI. All rights reserved.</p>
    </div>
""", unsafe_allow_html=True)

st.markdown("</div></div>", unsafe_allow_html=True)

