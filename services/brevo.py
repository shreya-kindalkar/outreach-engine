import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("BREVO_API_KEY")

HEADERS = {
    "accept": "application/json",
    "api-key": API_KEY,
    "content-type": "application/json"
}


def send_email(to_email, to_name, subject, content):
    url = "https://api.brevo.com/v3/smtp/email"

    payload = {
        "sender": {
            "name": "Shreya",
            "email": "shreyakindalkar7@gmail.com"
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

    response = requests.post(
        url,
        json=payload,
        headers=HEADERS
    )

    print(response.status_code)
    print(response.text)

    return response