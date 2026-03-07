distress_keywords = [
    "scared",
    "lost",
    "confused",
    "help",
    "panic",
    "angry"
]

def generate_safe_response(user_input):

    for word in distress_keywords:
        if word in user_input.lower():
            return (
                "It's okay. You are safe. "
                "Please stay calm. "
                "A caregiver is nearby to help you."
            )

    return "I am here with you. How are you feeling today?"
