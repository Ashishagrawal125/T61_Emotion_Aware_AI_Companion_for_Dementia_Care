from typing import Any, Dict, Optional

from memory_personalization.memory_store import load_memory, save_memory


class MemoryService:
    def __init__(self) -> None:
        self.data = load_memory()

    def refresh(self) -> None:
        self.data = load_memory()

    def get_patient(self, patient_id: str) -> Optional[Dict[str, Any]]:
        self.refresh()
        return self.data.get("patients", {}).get(patient_id)

    def update_patient_memory(self, patient_id: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        self.refresh()

        if "patients" not in self.data:
            self.data["patients"] = {}

        if patient_id not in self.data["patients"]:
            self.data["patients"][patient_id] = {}

        self.data["patients"][patient_id].update(updates)
        save_memory(self.data)
        return self.data["patients"][patient_id]

    def build_personalized_context(self, patient_id: str) -> str:
        patient = self.get_patient(patient_id)
        if not patient:
            return "No patient memory found. Speak gently and ask simple reassuring questions."

        name = patient.get("name", "the patient")
        preferred_name = patient.get("preferred_name", name)
        family_members = ", ".join(patient.get("family_members", [])) or "not available"
        favorite_food = patient.get("favorite_food", "not available")
        favorite_song = patient.get("favorite_song", "not available")
        hometown = patient.get("hometown", "not available")
        routine = patient.get("daily_routine", "not available")
        notes = patient.get("important_notes", "not available")
        likes = ", ".join(patient.get("likes", [])) or "not available"
        dislikes = ", ".join(patient.get("dislikes", [])) or "not available"

        context = (
            f"Patient name: {name}. "
            f"Preferred name: {preferred_name}. "
            f"Family members: {family_members}. "
            f"Favorite food: {favorite_food}. "
            f"Favorite song: {favorite_song}. "
            f"Hometown: {hometown}. "
            f"Daily routine: {routine}. "
            f"Likes: {likes}. "
            f"Dislikes: {dislikes}. "
            f"Care notes: {notes}."
        )
        return context

    def generate_personalized_reply(self, patient_id: str, user_message: str) -> str:
        patient = self.get_patient(patient_id)
        if not patient:
            return (
                "I am here with you. You are safe. Let us take a deep breath together. "
                "Would you like to talk about your family or listen to a calming song?"
            )

        preferred_name = patient.get("preferred_name", patient.get("name", "dear"))
        family_members = patient.get("family_members", [])
        favorite_song = patient.get("favorite_song", "your favorite song")
        favorite_food = patient.get("favorite_food", "something you enjoy")
        hometown = patient.get("hometown", "your hometown")

        msg = user_message.lower()
        if "who are you" in msg or "do i know you" in msg:
            fam_text = ", ".join(family_members) if family_members else "your loved ones"
            return (
                f"Hello {preferred_name}, I am your companion and I am here to support you. "
                f"Your family members like {fam_text} care about you very much."
            )

        if "home" in msg or "where am i" in msg:
            return (
                f"It is okay, {preferred_name}. You are in a safe place right now. "
                f"Would you like to talk about {hometown} or remember a happy moment with your family?"
            )

        if "hungry" in msg or "food" in msg:
            return (
                f"You might feel better with something comforting, {preferred_name}. "
                f"I remember you like {favorite_food}."
            )

        if "sad" in msg or "alone" in msg or "lonely" in msg:
            fam_text = family_members[0] if family_members else "your family"
            return (
                f"I am with you, {preferred_name}. You are not alone. "
                f"Would you like me to remind you of {fam_text} or talk about {favorite_song}?"
            )

        return (
            f"I am here with you, {preferred_name}. Let us talk gently. "
            f"We can remember your family, your favorite song {favorite_song}, or something peaceful from {hometown}."
        )