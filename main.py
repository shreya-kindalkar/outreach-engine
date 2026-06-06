from services.ocean import search_companies
from services.prospeo import find_decision_makers
from services.prospeo_enrich import enrich_person

SEND_EMAILS = False

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

if SEND_EMAILS:
    send_email(
        to_email=lead["email"],
        to_name=lead["name"],
        subject="AI Outreach",
        content="<h1>Hello!</h1>"
    )
else:
    print(f"[DRY RUN] Would send email to {lead['email']}")