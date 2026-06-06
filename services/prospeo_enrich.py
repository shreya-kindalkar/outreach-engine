import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("PROSPEO_API_KEY")

HEADERS = {
    "X-KEY": API_KEY,
    "Content-Type": "application/json"
}


def enrich_person(person_id):
    url = "https://api.prospeo.io/enrich-person"

    payload = {
        "only_verified_email": True,
        "data": {
            "person_id": person_id
        }
    }

    response = requests.post(
        url,
        json=payload,
        headers=HEADERS
    )

    if response.status_code != 200:
        return None

    data = response.json()

    person = data.get("person", {})

    email_data = person.get("email", {})

    return {
        "person_id": person.get("person_id"),
        "name": person.get("full_name"),
        "title": person.get("current_job_title"),
        "linkedin": person.get("linkedin_url"),
        "email": email_data.get("email"),
        "email_status": email_data.get("status")
    }