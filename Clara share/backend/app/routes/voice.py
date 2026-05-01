from fastapi import APIRouter, UploadFile, File
from fastapi.responses import StreamingResponse
import uuid
import os

from app.services.stt_service import speech_to_text
from app.services.llm_service import generate_response_stream

router = APIRouter()


@router.post("/voice")
async def voice_chat(file: UploadFile = File(...)):
    filename = f"temp_{uuid.uuid4()}.wav"

    with open(filename, "wb") as f:
        f.write(await file.read())

    text = speech_to_text(filename)

    def generator():
        yield f"User: {text}\n\nAI: "
        for chunk in generate_response_stream(
            message=text,
            emotion="neutral",
            memory_context="",
        ):
            yield chunk

    response = StreamingResponse(generator(), media_type="text/plain")

    if os.path.exists(filename):
        os.remove(filename)

    return response