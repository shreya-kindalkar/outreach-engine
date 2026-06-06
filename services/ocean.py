import os
from dotenv import load_dotenv
from services.http_client import post_json

load_dotenv()

API_KEY = os.getenv("OCEAN_API_KEY")

HEADERS = {
    "X-Api-Token": API_KEY,
    "Content-Type": "application/json"
}


def search_companies(domain):
    if not API_KEY:
        print("Missing OCEAN_API_KEY.")
        return []

    url = "https://api.ocean.io/v3/search/companies"

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

    data = post_json(url, HEADERS, payload, "Ocean")
    if not data:
        return []

    companies = []
    for item in data.get("companies", []):
        company = item.get("company", {})
        company_domain = company.get("domain")
        if not company_domain:
            continue

        companies.append({
            "name": company.get("name") or company_domain,
            "domain": company_domain,
            "description": company.get("description"),
            "employees": company.get("employeeCountOcean")
        })

    return companies 
