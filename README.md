# Outreach Engine

## Overview

Outreach Engine is a command-line outreach automation pipeline built for the Subspace internship assignment. Given a seed company domain, the application finds similar companies, identifies relevant decision-makers, resolves verified work emails, and prepares or sends personalized outreach emails.

The implementation is designed as a small production-style integration project: external API clients are separated by responsibility, HTTP behavior is centralized, sending is guarded by explicit safety controls, and partial data failures are handled without stopping the entire pipeline.

## Architecture

```text
Seed Domain
    |
    v
Ocean.io
    |
    v
Lookalike Companies
    |
    v
Prospeo Search Person
    |
    v
Decision Makers
    |
    v
Email Resolution
EazyReach-compatible interface backed by Prospeo enrichment
    |
    v
Brevo
    |
    v
Outreach Email
```

## Features

- Finds lookalike companies from a seed domain using Ocean.io.
- Searches for decision-makers at each company using Prospeo.
- Enriches contacts using Prospeo's person enrichment API.
- Preserves an EazyReach-compatible email resolution abstraction.
- Sends outreach emails through Brevo.
- Uses a shared HTTP client with retries, timeouts, and rate-limit handling.
- Provides a CLI interface for running the full pipeline.
- Runs in dry-run mode by default.
- Requires an explicit `SEND` confirmation before live email delivery.
- Deduplicates leads before sending.
- Handles missing data, failed records, and partial API failures gracefully.

## Project Structure

```text
outreach-engine/
|-- main.py
|-- services/
|   |-- ocean.py
|   |-- prospeo.py
|   |-- prospeo_enrich.py
|   |-- eazyreach.py
|   |-- brevo.py
|   `-- http_client.py
|-- requirements.txt
|-- README.md
|-- .env.example
`-- .env
```

- `main.py` contains the CLI entry point and orchestrates the outreach workflow.
- `services/ocean.py` integrates with Ocean.io to find lookalike companies.
- `services/prospeo.py` searches for decision-makers at target companies.
- `services/prospeo_enrich.py` enriches person records and resolves verified work emails.
- `services/eazyreach.py` exposes an EazyReach-compatible email resolution layer.
- `services/brevo.py` sends outreach emails through Brevo.
- `services/http_client.py` centralizes outbound HTTP behavior, including retries, timeouts, and rate-limit handling.
- `requirements.txt` lists Python dependencies.
- `.env.example` documents the required local environment variables.
- `.env` stores local API credentials and sender configuration.

## API Integrations

### Ocean.io

Ocean.io is used at the top of the pipeline. The application takes the input seed domain and requests similar or lookalike companies that can be used as outreach targets.

### Prospeo

Prospeo is used for two parts of the pipeline:

- Searching for decision-makers associated with each target company.
- Enriching selected people to retrieve verified work email data.

### EazyReach Abstraction

The original assignment referenced EazyReach for email resolution. Subspace later informed applicants that EazyReach credits were unavailable and instructed applicants to use Prospeo as a replacement.

To keep the design aligned with the original assignment, this project keeps an EazyReach-compatible abstraction layer in `services/eazyreach.py` while using Prospeo enrichment underneath. This keeps the rest of the pipeline independent from the specific enrichment provider.

### Brevo

Brevo is used as the outbound email provider. After leads are discovered, enriched, deduplicated, and approved for sending, the Brevo service sends the final outreach emails.

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure environment variables

Create a `.env` file in the project root using `.env.example` as a template.

```env
OCEAN_API_KEY=
PROSPEO_API_KEY=
BREVO_API_KEY=
BREVO_SENDER_NAME=
BREVO_SENDER_EMAIL=
```

The Brevo sender email should be a verified sender in your Brevo account.

## Usage

Run the pipeline in dry-run mode:

```bash
python main.py openai.com
```

Dry-run mode discovers companies, finds contacts, resolves emails, and prints the actions that would be taken without sending any emails.

Send emails after confirmation:

```bash
python main.py openai.com --send
```

When `--send` is provided, the application still requires an explicit `SEND` confirmation before delivering emails.

## Safety Controls

- **Dry-run mode by default:** Running the command without `--send` never sends emails.
- **SEND confirmation checkpoint:** Even when `--send` is passed, the user must type `SEND` before live delivery begins.
- **Lead deduplication:** Leads are deduplicated before sending to avoid contacting the same person more than once in a run.

## Reliability and Error Handling

- **Request timeouts:** External API requests use timeouts so the CLI does not hang indefinitely.
- **Retry strategy:** Transient request failures are retried by the shared HTTP client.
- **Rate-limit handling:** Rate-limit responses are handled centrally to reduce duplicated logic across service integrations.
- **Graceful degradation:** Missing company, person, or email fields are skipped or handled without crashing the entire pipeline.
- **Partial failure handling:** A failed lookup for one company or contact does not prevent the pipeline from continuing with other available leads.

## Example Output

```text
$ python main.py openai.com

Starting outreach pipeline for: openai.com

============================================================
Company: ExampleAI
Domain : exampleai.com
============================================================
Jane Smith | VP Marketing | jane.smith@exampleai.com
[DRY RUN] Would send email to jane.smith@exampleai.com
Subject: Quick question about ExampleAI
Preview: Hi Jane Smith, I came across ExampleAI while researching companies similar to exampleai.com. Your role as VP Marketing stood out...

============================================================
Company: ModelWorks
Domain : modelworks.com
============================================================
No decision makers found.

Pipeline completed.
```

## Design Decisions

### Service Separation

Each external provider is isolated in its own service module. This keeps API-specific request formats, response parsing, and failure handling out of the CLI orchestration code.

### Shared HTTP Client

The project uses a shared HTTP client so common network behavior is implemented once. Timeouts, retries, and rate-limit handling apply consistently across Ocean.io, Prospeo, and Brevo.

### Email Resolution Abstraction

Email resolution is accessed through an EazyReach-compatible layer instead of being coupled directly to Prospeo. This preserves the original assignment interface and makes it easier to swap in EazyReach or another enrichment provider later.

## Limitations

- Processes only the first page of API results.
- Uses Prospeo as the EazyReach substitute because EazyReach credits were unavailable.
- Uses a simple email template.

## Future Improvements

- Add multi-page pagination for all supported providers.
- Improve email personalization with richer company and contact context.
- Add a web dashboard for reviewing leads before sending.
- Support additional enrichment providers behind the same email-resolution interface.

## Conclusion

Outreach Engine demonstrates a practical, service-oriented approach to building an outreach automation workflow. It integrates multiple external APIs, includes safety controls for live email delivery, and handles unreliable third-party data in a way that is appropriate for a software engineering internship submission.
