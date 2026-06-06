# Outreach Engine

A command-line outreach pipeline for finding lookalike companies, discovering decision-makers, resolving verified work emails, and optionally sending personalized outreach with Brevo.

## Pipeline

1. Ocean.io finds lookalike companies from a seed domain.
2. Prospeo finds decision-makers at each lookalike company.
3. `services/eazyreach.py` represents the verified email resolution stage.
4. Brevo sends personalized outreach emails.

The assignment names EazyReach for stage 3. This project keeps an EazyReach-compatible adapter, but currently backs it with Prospeo enrichment using `only_verified_email=True` because EazyReach access is unavailable.

## Setup

Create a `.env` file:

```env
OCEAN_API_KEY=your_ocean_key
PROSPEO_API_KEY=your_prospeo_key
BREVO_API_KEY=your_brevo_key
BREVO_SENDER_NAME=Your Name
BREVO_SENDER_EMAIL=you@example.com
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run

Dry run:

```bash
python main.py openai.com
```

Send emails:

```bash
python main.py openai.com --send
```

Emails are never sent by default. Even with `--send`, the program asks you to type `SEND` before sending.

## Reliability Notes

- API requests use timeouts.
- Rate limits and transient server errors are retried with backoff.
- Missing or partial API records are skipped instead of crashing the pipeline.
- Leads are deduplicated by normalized email address.
- Brevo send failures are reported instead of being treated as successful sends.
