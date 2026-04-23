from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from app.services.llm_service import stream_response

router = APIRouter()


@router.post("/chat")
async def chat(data: dict):
    user_input = data.get("message")
    emotion = data.get("emotion")

    return StreamingResponse(
    stream_response(user_input, emotion),
    media_type="text/plain"
)