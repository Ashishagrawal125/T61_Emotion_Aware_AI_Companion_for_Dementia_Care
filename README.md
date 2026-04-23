# 🧠 Clara AI - Emotion Aware Companion for Dementia Care

Clara AI is a Streamlit-based prototype that helps support dementia care using emotion-aware interaction. It combines voice transcription, translation, facial emotion detection, text emotion analysis, supportive AI chat, and basic wellness insights in one interface.

## Features

- Voice recording and speech-to-text transcription
- Multilingual translation to and from English
- Voice emotion analysis using text emotion classification
- Facial emotion detection from uploaded images or live camera
- Supportive AI chat for calm and empathetic responses
- Voice chat with text-to-speech reply generation
- Heart-rate CSV visualization and summary metrics

## Tech Stack

- **Frontend / App:** Streamlit
- **Computer Vision:** OpenCV, DeepFace
- **NLP / Emotion Analysis:** Transformers pipeline, FLAN-T5
- **Speech:** Sarvam STT + TTS APIs
- **Translation:** deep-translator, langdetect
- **Data / Charts:** pandas, plotly

## Project Files

- `app.py` - main Streamlit application
- `Sarvam_STT.py` - speech-to-text helper
- `Google_Translate.py` - translation helper
- `tts_tutorial.py` - text-to-speech helper

## Setup

```bash
git clone <your-repo-url>
cd T61_Emotion_Aware_AI_Companion_for_Dementia_Care
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
pip install -r requirements.txt
```

### Linux / Mac

```bash
source venv/bin/activate
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file or set environment variables in your terminal:

```env
SARVAM_API_KEY=your_sarvam_api_key
```

## Run

```bash
streamlit run app.py
```

## Notes

- The previous version had hardcoded API keys and unstable logic in voice chat, heart-rate handling, and emotion flow. This updated version removes those issues and makes the app safer and easier to run.
- For best facial analysis results, use a clear front-facing image.
- If Sarvam API keys are missing, voice features will not work until you add them.
