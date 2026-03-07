from memory_personalization.memory_store import get_memory
from safe_response.safe_response_generator import generate_safe_response

print("Patient Daughter:", get_memory("daughter_name"))

user_input = input("Patient says: ")

response = generate_safe_response(user_input)

print("AI Companion:", response)
