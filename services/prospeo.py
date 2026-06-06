import os
from dotenv import load_dotenv
from services.http_client import post_json

load_dotenv()

API_KEY = os.getenv("PROSPEO_API_KEY")

HEADERS = {
    "X-KEY": API_KEY,
    "Content-Type": "application/json"
}

def find_decision_makers(domain):
    if not API_KEY:
        print("Missing PROSPEO_API_KEY.")
        return []

    if not domain:
        return []

    url = "https://api.prospeo.io/search-person"

    payload = {
        "page": 1,
        "filters": {
            "company": {
                "websites": {
                    "include": [domain]
                }
            },
            "person_seniority": {
                "include": [
                    "Founder/Owner",
                    "C-Suite",
                    "Director"
                ]
            }
        }
    }

    data = post_json(url, HEADERS, payload, "Prospeo search")
    if not data:
        return []

    results = []
    
    for item in data.get("results", []):
        person = item.get("person", {})
        person_id = person.get("person_id")
        if not person_id:
            continue

        results.append({
            "person_id": person_id,
            "name": person.get("full_name") or "Unknown",
            "title": person.get("current_job_title"),
            "linkedin": person.get("linkedin_url")
        })
    
    return results
