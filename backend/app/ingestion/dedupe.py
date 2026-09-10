from app.models import Incident


def dedupe_incidents(incidents: list[Incident]) -> list[Incident]:
    seen: set[str] = set()
    result: list[Incident] = []

    for incident in incidents:
        key = incident.source_record_id
        if key in seen:
            continue
        seen.add(key)
        result.append(incident)

    return result
