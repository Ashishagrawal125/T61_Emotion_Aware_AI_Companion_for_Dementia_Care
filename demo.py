from typing import Any, Dict, Optional

from fastapi import FastAPI
from pydantic import BaseModel, Field

from memory_personalization.memory_service import MemoryService
from safe_response.safe_response_generator import SafeResponseGenerator
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Emotion-Aware AI Companion Demo")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

memory_service = MemoryService()
safe_response_service = SafeResponseGenerator()


class MemoryUpdateRequest(BaseModel):
    patient_id: str = Field(..., example="p001")
    updates: Dict[str, Any]


class PatientMessageRequest(BaseModel):
    patient_id: str = Field(..., example="p001")
    message: str


class SafeResponseRequest(BaseModel):
    message: str


@app.get("/")
def home() -> Dict[str, str]:
    return {"message": "Emotion-Aware AI Companion backend is running."}


@app.get("/api/patient/{patient_id}")
def get_patient_memory(patient_id: str) -> Dict[str, Any]:
    patient = memory_service.get_patient(patient_id)
    if not patient:
        return {"status": "error", "message": "Patient not found."}

    return {
        "status": "success",
        "patient_id": patient_id,
        "memory": patient,
        "personalized_context": memory_service.build_personalized_context(patient_id)
    }


@app.post("/api/patient/update-memory")
def update_patient_memory(payload: MemoryUpdateRequest) -> Dict[str, Any]:
    updated = memory_service.update_patient_memory(payload.patient_id, payload.updates)
    return {
        "status": "success",
        "message": "Patient memory updated successfully.",
        "patient_id": payload.patient_id,
        "updated_memory": updated
    }


@app.post("/api/memory/personalized-response")
def personalized_response(payload: PatientMessageRequest) -> Dict[str, Any]:
    reply = memory_service.generate_personalized_reply(payload.patient_id, payload.message)
    context = memory_service.build_personalized_context(payload.patient_id)

    return {
        "status": "success",
        "patient_id": payload.patient_id,
        "input_message": payload.message,
        "personalized_context": context,
        "reply": reply
    }


@app.post("/api/safe-response/analyze")
def safe_response(payload: SafeResponseRequest) -> Dict[str, Any]:
    result = safe_response_service.generate_safe_response(payload.message)
    return {
        "status": "success",
        "input_message": payload.message,
        "analysis": result
    }


@app.post("/api/interaction/respond")
def combined_interaction(payload: PatientMessageRequest) -> Dict[str, Any]:
    safe_result = safe_response_service.generate_safe_response(payload.message)

    if safe_result["risk_level"] in ["critical", "high"]:
        final_reply = safe_result["response"]
        mode = "safe_response_priority"
    else:
        personalized_reply = memory_service.generate_personalized_reply(payload.patient_id, payload.message)
        final_reply = personalized_reply
        mode = "personalized_support"

    return {
        "status": "success",
        "mode": mode,
         "patient_id": payload.patient_id,
        "input_message": payload.message,
        "safe_analysis": safe_result,
        "final_reply": final_reply
    }