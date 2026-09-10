# Data Sources

## Chicago

Official City of Chicago Socrata dataset:

- Dataset: Crimes - 2001 to Present
- Resource ID: `ijzp-q8t2`
- Endpoint: `https://data.cityofchicago.org/resource/ijzp-q8t2.json`

The dataset contains historical crime records and approximate/block-level locations. Recent records may be delayed and data is preliminary.

## New York City

Official NYPD Complaint Data Historic:

- Resource ID: `qgea-i56i`
- Endpoint: `https://data.cityofnewyork.us/resource/qgea-i56i.json`

The adapter maps selected serious categories and complaint date/time.

## Los Angeles

LAPD / City of Los Angeles open data foundation:

- Crime Data 2020-2024
- Resource ID: `2nrs-mtv8`

The LA adapter is defensive and must be schema-validated before production use.

## Source policy

Prefer official government or police sources.

Do not silently mix community reports with official incidents. Every record should retain source identity and quality metadata.
