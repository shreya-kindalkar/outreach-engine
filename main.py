import argparse

from services.ocean import search_companies
from services.prospeo import find_decision_makers
from services.eazyreach import resolve_verified_email
from services.brevo import send_email

# =========================
# EMAIL CONFIG
# =========================

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

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("domain", help="Seed company domain, for example openai.com")
    parser.add_argument(
        "--send",
        action="store_true",
        help="Send emails after the safety checkpoint",
    )
    return parser.parse_args()


def normalize_domain(domain):
    return (
        domain.strip()
        .lower()
        .removeprefix("https://")
        .removeprefix("http://")
        .removeprefix("www.")
        .split("/")[0]
    )


def confirm_send(seed_domain):
    confirm = input(
        f"Send outreach emails to verified leads for {seed_domain}? Type SEND: "
    )

    if confirm != "SEND":
        print("\nEmail sending cancelled.")
        print("Running in DRY RUN mode.\n")
        return False

    return True


def run_pipeline(seed_domain, send_emails=False):
    print(f"\nStarting outreach pipeline for: {seed_domain}\n")

    companies = search_companies(seed_domain)
    if not companies:
        print("No lookalike companies found or Ocean search failed.")

    seen_emails = set()

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
            lead = resolve_verified_email(person)

            if not lead:
                continue

            email = lead.get("email")

            if not email:
                continue

            normalized_email = email.lower()
            if normalized_email in seen_emails:
                print(f"Skipping duplicate lead: {email}")
                continue
            seen_emails.add(normalized_email)

            leads_found = True

            lead_name = lead.get("name") or "there"
            lead_title = lead.get("title") or "Unknown title"

            print(f"{lead_name} | {lead_title} | {email}")

            if send_emails:
                email_body = EMAIL_TEMPLATE.format(
                    name=lead_name,
                    company=company_name or company_domain,
                )

                sent = send_email(
                    to_email=email,
                    to_name=lead_name,
                    subject=EMAIL_SUBJECT,
                    content=email_body,
                )

                if sent:
                    print("Email sent.\n")
                else:
                    print("Email failed.\n")

            else:
                print(f"[DRY RUN] Would send email to {email}\n")

        if not leads_found:
            print("No verified emails found.\n")

    print("\nPipeline completed.\n")


def main():
    args = parse_args()
    seed_domain = normalize_domain(args.domain)

    if not seed_domain or "." not in seed_domain:
        print("Please provide a valid company domain, for example openai.com.")
        return

    send_emails = args.send and confirm_send(seed_domain)
    run_pipeline(seed_domain, send_emails=send_emails)


if __name__ == "__main__":
    main()
