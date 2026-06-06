from services.ocean import search_companies
from services.prospeo import find_decision_makers
from services.prospeo_enrich import enrich_person
from services.brevo import send_email

# =========================
# CONFIG
# =========================

SEED_DOMAIN = "openai.com"

# Keep FALSE for demo/testing
SEND_EMAILS = False

EMAIL_SUBJECT = "Quick Introduction"

EMAIL_TEMPLATE = """
<h2>Hello {name},</h2>

<p>
I came across {company} and was impressed by what your team is building.
</p>

<p>
I'm currently exploring AI-powered outreach and lead generation systems,
and I'd love to connect and learn more about your work.
</p>

<p>
Looking forward to hearing from you.
</p>

<p>
Best regards,<br>
Shreya Kindalkar
</p>
"""


# =========================
# PIPELINE
# =========================

print(f"\nStarting outreach pipeline for: {SEED_DOMAIN}\n")

companies = search_companies(SEED_DOMAIN)

for company in companies:

    company_name = company.get("name")
    company_domain = company.get("domain")

    print("=" * 60)
    print(f"Company: {company_name}")
    print(f"Domain : {company_domain}")
    print("=" * 60)

    people = find_decision_makers(company_domain)

    if not people:
        print("No decision makers found.\n")
        continue

    leads_found = False

    for person in people[:3]:

        lead = enrich_person(person["person_id"])

        if not lead:
            continue

        email = lead.get("email")

        if not email:
            continue

        leads_found = True

        print(
            f"{lead['name']} | "
            f"{lead['title']} | "
            f"{lead['email']}"
        )

        if SEND_EMAILS:

            email_body = EMAIL_TEMPLATE.format(
                name=lead["name"],
                company=company_name
            )

            send_email(
                to_email=lead["email"],
                to_name=lead["name"],
                subject=EMAIL_SUBJECT,
                content=email_body
            )

            print("Email sent.\n")

        else:

            print(
                f"[DRY RUN] Would send email to "
                f"{lead['email']}\n"
            )

    if not leads_found:
        print("No verified emails found.\n")

print("\nPipeline completed.\n")