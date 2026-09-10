from app.models import Incident


def quality_report(incidents: list[Incident]) -> dict:
    total = len(incidents)
    with_coordinates = sum(
        1
        for item in incidents
        if item.latitude is not None and item.longitude is not None
    )
    with_time = sum(1 for item in incidents if item.occurred_at is not None)

    return {
        "records": total,
        "coordinate_coverage": round(with_coordinates / total, 4) if total else 0,
        "time_coverage": round(with_time / total, 4) if total else 0,
    }
