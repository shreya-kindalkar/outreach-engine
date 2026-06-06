from services.ocean import search_companies
from services.prospeo import find_decision_makers
from services.prospeo_enrich import enrich_person

companies = search_companies("openai.com")

for company in companies[:3]:
    print(f"\nCompany: {company['name']}")

    people = find_decision_makers(company["domain"])

    for person in people[:3]:
        lead = enrich_person(person["person_id"])

        if lead:
            print(
                f"{lead['name']} | "
                f"{lead['title']} | "
                f"{lead['email']}"
            )

from services.brevo import send_email

send_email(
    to_email="shreyakindalkar7@gmail.com",
    to_name="Shreya",
    subject="Brevo Test",
    content="<h1>Hello from Outreach Engine!</h1>"
)