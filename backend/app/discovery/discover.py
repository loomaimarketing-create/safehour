from app.discovery.registry import SOURCE_REGISTRY


def list_known_sources() -> list[dict]:
    return [
        {
            "city": source.city,
            "country": source.country,
            "provider": source.provider,
            "dataset_id": source.dataset_id,
            "source_url": source.source_url,
            "api_type": source.api_type,
        }
        for source in SOURCE_REGISTRY
    ]
