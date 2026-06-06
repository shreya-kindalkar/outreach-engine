import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("PROSPEO_API_KEY")

HEADERS = {
    "X-KEY": API_KEY,
    "Content-Type": "application/json"
}

def find_decision_makers(domain):
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

    response = requests.post(
        url,
        json=payload,
        headers=HEADERS
    )

    if response.status_code != 200:
        return []

    data = response.json()

    results = []
    
    for item in data.get("results", []):
        person = item["person"]

        results.append({
            "person_id": person["person_id"],
            "name": person["full_name"],
            "title": person["current_job_title"],
            "linkedin": person["linkedin_url"]
        })
    
    return results
