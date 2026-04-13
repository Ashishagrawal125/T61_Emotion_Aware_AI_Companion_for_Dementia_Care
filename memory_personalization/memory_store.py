import json
from pathlib import Path
from typing import Any, Dict


BASE_DIR = Path(__file__).resolve().parent
MEMORY_FILE = BASE_DIR / "patient_memory.json"


def load_memory() -> Dict[str, Any]:
    """Load patient memory data from JSON file."""
    if not MEMORY_FILE.exists():
        return {"patients": {}}

    with open(MEMORY_FILE, "r", encoding="utf-8") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return {"patients": {}}


def save_memory(data: Dict[str, Any]) -> None:
    """Save patient memory data to JSON file."""
    with open(MEMORY_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)