import argparse
import os
import re

from dotenv import load_dotenv

load_dotenv()

from services.ocean import search_companies
from services.prospeo import find_decision_makers
from services.eazyreach import resolve_verified_email
from services.brevo import send_email

# =========================
# EMAIL CONFIG
# =========================

EMAIL_SUBJECT = "Quick question about {company}"

EMAIL_TEMPLATE = """
<p>Hi {name},</p>

<p>
I came across <strong>{company}</strong> while researching companies similar to
<strong>{company_domain}</strong>.
</p>

<p>
Your role as <strong>{title}</strong> stood out because you seem close to the
customer, growth, or partnership conversations this outreach project is meant
to support.
</p>

<p>
I built a small outreach engine for an internship assignment and wanted to send
a relevant note rather than a generic blast. Would you be open to a brief
conversation?
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


def validate_config(send_emails):
    required_vars = ["OCEAN_API_KEY", "PROSPEO_API_KEY"]

    if send_emails:
        required_vars.extend([
            "BREVO_API_KEY",
            "BREVO_SENDER_NAME",
            "BREVO_SENDER_EMAIL",
        ])

    missing_vars = [name for name in required_vars if not os.getenv(name)]

    if missing_vars:
        print("Missing required environment variables:")
        for name in missing_vars:
            print(f"- {name}")
        print("\nCreate a .env file using .env.example as a template.")
        return False

    return True


def render_email_preview(html_content, max_length=140):
    text = re.sub(r"<br\s*/?>", " ", html_content, flags=re.IGNORECASE)
    text = re.sub(r"<[^>]+>", " ", text)
    text = " ".join(text.split())

    if len(text) <= max_length:
        return text

    return text[: max_length - 3].rstrip() + "..."


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
            lead_title = lead.get("title") or "your role"

            print(f"{lead_name} | {lead_title} | {email}")

            company_label = company_name or company_domain
            email_subject = EMAIL_SUBJECT.format(company=company_label)
            email_body = EMAIL_TEMPLATE.format(
                name=lead_name,
                title=lead_title,
                company=company_label,
                company_domain=company_domain or company_label,
            )

            if send_emails:
                sent = send_email(
                    to_email=email,
                    to_name=lead_name,
                    subject=email_subject,
                    content=email_body,
                )

                if sent:
                    print("Email sent.\n")
                else:
                    print("Email failed.\n")

            else:
                print(f"[DRY RUN] Would send email to {email}")
                print(f"Subject: {email_subject}")
                print(f"Preview: {render_email_preview(email_body)}\n")

        if not leads_found:
            print("No verified emails found.\n")

    print("\nPipeline completed.\n")


def main():
    args = parse_args()
    seed_domain = normalize_domain(args.domain)

    if not seed_domain or "." not in seed_domain:
        print("Please provide a valid company domain, for example openai.com.")
        return

    if not validate_config(args.send):
        return

    send_emails = args.send and confirm_send(seed_domain)
    run_pipeline(seed_domain, send_emails=send_emails)


if __name__ == "__main__":
    main()
