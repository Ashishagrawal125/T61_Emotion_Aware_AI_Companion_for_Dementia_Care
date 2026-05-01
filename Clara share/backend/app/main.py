from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine
from app import models

from app.routes import (
    auth_routes,
    patient_routes,
    chat,
    voice,
    emotion,
    dashboard_routes,
    alerts_routes,
)

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Clara AI Backend", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_routes.router, prefix="/api")
app.include_router(patient_routes.router, prefix="/api")
app.include_router(chat.router, prefix="/api")
app.include_router(voice.router, prefix="/api")
app.include_router(emotion.router, prefix="/api")
app.include_router(dashboard_routes.router, prefix="/api")
app.include_router(alerts_routes.router, prefix="/api")


@app.get("/")
def home():
    return {"message": "Clara AI Backend Running"}