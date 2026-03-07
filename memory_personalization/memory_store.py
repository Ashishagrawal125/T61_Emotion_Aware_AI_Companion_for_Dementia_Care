import json

MEMORY_FILE = "memory_personalization/user_memory.json"

def load_memory():
    try:
        with open(MEMORY_FILE, "r") as file:
            return json.load(file)
    except:
        return {}

def save_memory(memory):
    with open(MEMORY_FILE, "w") as file:
        json.dump(memory, file, indent=4)

def add_memory(key, value):
    memory = load_memory()
    memory[key] = value
    save_memory(memory)

def get_memory(key):
    memory = load_memory()
    return memory.get(key, "Memory not found")
