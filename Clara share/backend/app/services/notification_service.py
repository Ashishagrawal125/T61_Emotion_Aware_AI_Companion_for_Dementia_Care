import os
import smtplib
from email.message import EmailMessage
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()


def send_email_alert(to_email: str, subject: str, body: str):
    sender = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASS")

    if not sender or not password or not to_email:
        print("Email alert skipped: missing EMAIL_USER / EMAIL_PASS / receiver email")
        return False

    msg = EmailMessage()
    msg["From"] = sender
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(body)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(sender, password)
        smtp.send_message(msg)

    return True


def send_sms_alert(phone: str, message: str):
    """
    Sends an SMS alert using Twilio or Textbelt.
    Priority: Twilio > Textbelt > Console Log
    """
    if not phone:
        print("[WARNING] SMS skipped: No phone number provided")
        return False

    # Normalize phone number for India if no country code is provided
    # If it's 10 digits and doesn't start with '+', add '+91'
    clean_phone = str(phone).strip().replace(" ", "").replace("-", "")
    if len(clean_phone) == 10 and not clean_phone.startswith('+'):
        clean_phone = f"+91{clean_phone}"
    elif len(clean_phone) == 12 and clean_phone.startswith('91'):
        clean_phone = f"+{clean_phone}"
    
    phone = clean_phone

    # 1. Try Twilio
    twilio_sid = os.getenv("TWILIO_ACCOUNT_SID")
    twilio_auth = os.getenv("TWILIO_AUTH_TOKEN")
    twilio_from = os.getenv("TWILIO_PHONE_NUMBER")

    if twilio_sid and twilio_auth and twilio_from:
        try:
            from twilio.rest import Client
            client = Client(twilio_sid, twilio_auth)
            # Remove spaces from the Twilio 'from' number
            clean_from = twilio_from.strip().replace(" ", "").replace("-", "")
            client.messages.create(
                body=message,
                from_=clean_from,
                to=phone
            )
            print(f"[SUCCESS] Twilio SMS sent to {phone} from {clean_from}")
            return True
        except Exception as e:
            print(f"[ERROR] Twilio Error: {e}")

    # 2. Try Textbelt (Fallback)
    try:
        import requests
        resp = requests.post('https://textbelt.com/text', {
            'phone': phone,
            'message': message,
            'key': os.getenv("TEXTBELT_API_KEY", "textbelt"),
        }, timeout=5)
        res_json = resp.json()
        if res_json.get("success"):
            print(f"[SUCCESS] Textbelt SMS sent to {phone}")
            return True
        else:
            print(f"[ERROR] Textbelt failed: {res_json.get('error')}")
    except Exception as e:
        print(f"[ERROR] Textbelt Error: {e}")

    # 3. Last Resort: Log to file/console
    print(f"[SMS LOG ONLY] TO {phone}: {message}")
    with open("sms_alerts.log", "a", encoding="utf-8") as f:
        f.write(f"{datetime.now()}: TO {phone} - {message}\n")

    
    return False