import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OCEAN_API_KEY")

HEADERS = {
    "X-Api-Token": API_KEY,
    "Content-Type": "application/json"
}


def search_companies(domain):
    payload = {
        "size": 5,
        "companiesFilters": {
            "lookalikeDomains": [domain]
        },
        "fields": [
            "name",
            "domain",
            "description",
            "employeeCountOcean"
        ]
    }

    response = requests.post(
        "https://api.ocean.io/v3/search/companies",
        headers=HEADERS,
        json=payload
    )

    print(response.status_code)

    data=response.json()
    companies=[]
    for item in data["companies"]:
        company=item["company"]

        companies.append({
            "name":company.get("name"),
            "domain":company.get("domain"),
            "description":company.get("description"),
            "employees":company.get("employeeCountOcean")
        })

    return companies 