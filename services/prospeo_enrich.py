import os
from dotenv import load_dotenv
from services.http_client import post_json

load_dotenv()

API_KEY = os.getenv("PROSPEO_API_KEY")

HEADERS = {
    "X-KEY": API_KEY,
    "Content-Type": "application/json"
}


def enrich_person(person_id):
    if not API_KEY:
        print("Missing PROSPEO_API_KEY.")
        return None

    if not person_id:
        return None

    url = "https://api.prospeo.io/enrich-person"

    payload = {
        "only_verified_email": True,
        "data": {
            "person_id": person_id
        }
    }

    data = post_json(url, HEADERS, payload, "Prospeo enrich")
    if not data:
        return None

    person = data.get("person", {})

    email_data = person.get("email", {})
    if not isinstance(email_data, dict):
        email_data = {}

    return {
        "person_id": person.get("person_id"),
        "name": person.get("full_name"),
        "title": person.get("current_job_title"),
        "linkedin": person.get("linkedin_url"),
        "email": email_data.get("email"),
        "email_status": email_data.get("status")
    }
