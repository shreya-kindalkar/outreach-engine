import time

import requests


def post(url, headers, payload, service_name, retries=3, timeout=15):
    """POST with basic timeout, retry, and rate-limit handling."""
    for attempt in range(retries):
        try:
            response = requests.post(
                url,
                headers=headers,
                json=payload,
                timeout=timeout,
            )

            if response.status_code == 429:
                retry_after = response.headers.get("Retry-After")
                wait_seconds = (
                    int(retry_after)
                    if retry_after and retry_after.isdigit()
                    else 2 ** attempt
                )
                print(f"{service_name} rate limited. Retrying in {wait_seconds}s.")
                time.sleep(wait_seconds)
                continue

            if response.status_code >= 500:
                wait_seconds = 2 ** attempt
                print(
                    f"{service_name} server error {response.status_code}. "
                    f"Retrying in {wait_seconds}s."
                )
                time.sleep(wait_seconds)
                continue

            if 400 <= response.status_code < 500:
                print(
                    f"{service_name} request failed "
                    f"({response.status_code}): {response.text}"
                )
                return None

            response.raise_for_status()
            return response

        except requests.RequestException as exc:
            if attempt == retries - 1:
                print(f"{service_name} request failed: {exc}")
                return None
            time.sleep(2 ** attempt)

    print(f"{service_name} failed after {retries} attempts.")
    return None


def post_json(url, headers, payload, service_name, retries=3, timeout=15):
    response = post(url, headers, payload, service_name, retries, timeout)
    if not response:
        return None

    try:
        return response.json()
    except ValueError as exc:
        print(f"{service_name} returned invalid JSON: {exc}")
        return None
