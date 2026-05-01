from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/auth", tags=["Auth"])

users = {}


class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str
    role: str = "caregiver"


class LoginRequest(BaseModel):
    email: str
    password: str


@router.post("/register")
def register(data: RegisterRequest):
    users[data.email] = {
        "id": len(users) + 1,
        "name": data.name,
        "email": data.email,
        "password": data.password,
        "role": data.role,
    }

    return {"message": "Registered successfully"}


@router.post("/login")
def login(data: LoginRequest):
    user = users.get(data.email)

    # default test login also allowed
    if data.email == "aashigarg825@gmail.com" and data.password == "123456":
        return {
            "access_token": "demo-token",
            "token_type": "bearer",
            "caregiver": {
                "id": 1,
                "name": "Aashi Garg",
                "email": data.email,
                "role": "family",
            },
        }

    if not user or user["password"] != data.password:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    return {
        "access_token": "demo-token",
        "token_type": "bearer",
        "caregiver": {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"],
            "role": user["role"],
        },
    }