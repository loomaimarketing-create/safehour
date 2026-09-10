# SafeHour Architecture

```text
Official/open data sources
        ↓
Source discovery / registry
        ↓
Adapter
        ↓
Schema validation
        ↓
Normalization
        ↓
Deduplication
        ↓
Incident Store (Supabase/Postgres)
        ↓
Aggregation
        ↓
Risk Engine
        ↓
FastAPI
        ↓
Frontend / Map / Routing
```

## Adapter contract

Every source adapter should implement a common interface:

- identify the source
- fetch records
- normalize records
- expose source metadata
- report quality/errors

## Data flow

1. Discover or configure an official source.
2. Fetch incrementally where possible.
3. Validate schema.
4. Normalize into the common incident model.
5. Deduplicate by source + source record ID.
6. Store raw metadata only when useful and permitted.
7. Aggregate by city/neighborhood/time.
8. Calculate scores with confidence.
9. Serve the result through the API.

## Production priorities

1. Chicago ingestion
2. Supabase persistence
3. Incremental updates and dedupe
4. Hourly/neighborhood aggregation
5. Risk score + confidence
6. Frontend map
7. NYC and LA
8. Global source discovery
9. Routing
10. Alerts/anomaly detection
