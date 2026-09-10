from dataclasses import dataclass


@dataclass(frozen=True)
class SourceDefinition:
    city: str
    country: str
    provider: str
    dataset_id: str
    source_url: str
    api_type: str


SOURCE_REGISTRY = [
    SourceDefinition(
        city="Chicago",
        country="USA",
        provider="City of Chicago / Socrata",
        dataset_id="ijzp-q8t2",
        source_url="https://data.cityofchicago.org/resource/ijzp-q8t2.json",
        api_type="socrata",
    ),
    SourceDefinition(
        city="New York City",
        country="USA",
        provider="NYPD / NYC Open Data",
        dataset_id="qgea-i56i",
        source_url="https://data.cityofnewyork.us/resource/qgea-i56i.json",
        api_type="socrata",
    ),
    SourceDefinition(
        city="Los Angeles",
        country="USA",
        provider="LAPD / Los Angeles Open Data",
        dataset_id="2nrs-mtv8",
        source_url="https://data.lacity.org/",
        api_type="socrata",
    ),
]
