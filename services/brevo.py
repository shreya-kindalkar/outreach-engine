import os
from dotenv import load_dotenv
from services.http_client import post

load_dotenv()

API_KEY = os.getenv("BREVO_API_KEY")
SENDER_NAME = os.getenv("BREVO_SENDER_NAME")
SENDER_EMAIL = os.getenv("BREVO_SENDER_EMAIL")

HEADERS = {
    "accept": "application/json",
    "api-key": API_KEY,
    "content-type": "application/json"
}


def send_email(to_email, to_name, subject, content):
    missing_vars = []
    if not API_KEY:
        missing_vars.append("BREVO_API_KEY")
    if not SENDER_NAME:
        missing_vars.append("BREVO_SENDER_NAME")
    if not SENDER_EMAIL:
        missing_vars.append("BREVO_SENDER_EMAIL")

    if missing_vars:
        print("Missing Brevo configuration:")
        for name in missing_vars:
            print(f"- {name}")
        return False

    url = "https://api.brevo.com/v3/smtp/email"

    payload = {
        "sender": {
            "name": SENDER_NAME,
            "email": SENDER_EMAIL
        },
        "replyTo": {
            "email": SENDER_EMAIL,
            "name": SENDER_NAME
        },
        "to": [
            {
                "email": to_email,
                "name": to_name
            }
        ],
        "subject": subject,
        "htmlContent": content
    }

    response = post(url, HEADERS, payload, "Brevo")
    if not response:
        return False

    if response.status_code not in {200, 201, 202}:
        print(f"Brevo send failed ({response.status_code}): {response.text}")
        return False

    return True
