from typing import Any


def detect_fields(rows: list[dict[str, Any]]) -> set[str]:
    fields: set[str] = set()
    for row in rows[:50]:
        fields.update(row.keys())
    return fields


def has_any(fields: set[str], candidates: list[str]) -> bool:
    return any(candidate in fields for candidate in candidates)
