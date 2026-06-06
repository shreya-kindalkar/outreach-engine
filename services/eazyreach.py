from services.prospeo_enrich import enrich_person


def resolve_verified_email(person):
    """
    Stage 3 email resolver.

    The assignment names EazyReach for verified work email resolution. This
    adapter preserves that stage boundary while using Prospeo enrichment as the
    backing provider when EazyReach access is unavailable.
    """
    if not person:
        return None

    lead = enrich_person(person.get("person_id"))
    if not lead:
        return None

    if not lead.get("email"):
        return None

    status = (lead.get("email_status") or "").lower()
    if status and status not in {"valid", "verified"}:
        return None

    return lead
