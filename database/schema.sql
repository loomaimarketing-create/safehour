-- SafeHour MVP Supabase/Postgres schema
-- Run in Supabase SQL editor after reviewing for your project.

create extension if not exists pgcrypto;

create table if not exists cities (
    id uuid primary key default gen_random_uuid(),
    name text not null,
    country text not null,
    region text,
    latitude double precision,
    longitude double precision,
    timezone text,
    created_at timestamptz not null default now()
);

create table if not exists data_sources (
    id uuid primary key default gen_random_uuid(),
    city_id uuid references cities(id) on delete cascade,
    provider text not null,
    source_url text not null,
    api_type text,
    dataset_id text,
    status text not null default 'active',
    quality_score numeric,
    last_successful_sync timestamptz,
    last_schema_check timestamptz,
    created_at timestamptz not null default now()
);

create table if not exists incidents (
    id uuid primary key default gen_random_uuid(),
    source_id uuid not null references data_sources(id) on delete cascade,
    source_record_id text not null,
    occurred_at timestamptz,
    latitude double precision,
    longitude double precision,
    category text not null,
    severity integer,
    metadata jsonb not null default '{}'::jsonb,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now(),
    unique(source_id, source_record_id)
);

create index if not exists incidents_occurred_at_idx on incidents(occurred_at);
create index if not exists incidents_category_idx on incidents(category);
create index if not exists incidents_location_idx on incidents(latitude, longitude);

create table if not exists neighborhoods (
    id uuid primary key default gen_random_uuid(),
    city_id uuid not null references cities(id) on delete cascade,
    name text not null,
    geometry jsonb,
    created_at timestamptz not null default now()
);

create table if not exists hourly_risk (
    id uuid primary key default gen_random_uuid(),
    city_id uuid not null references cities(id) on delete cascade,
    neighborhood_id uuid references neighborhoods(id) on delete cascade,
    weekday integer not null check (weekday between 0 and 6),
    hour integer not null check (hour between 0 and 23),
    category text,
    incident_count integer not null default 0,
    normalized_score numeric,
    confidence numeric,
    sample_size integer,
    period_start timestamptz,
    period_end timestamptz,
    created_at timestamptz not null default now()
);

create table if not exists user_profiles (
    id uuid primary key default gen_random_uuid(),
    baseline jsonb not null default '{}'::jsonb,
    preferences jsonb not null default '{}'::jsonb,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now()
);

create table if not exists user_feedback (
    id uuid primary key default gen_random_uuid(),
    user_id uuid references user_profiles(id) on delete set null,
    city_id uuid references cities(id) on delete set null,
    neighborhood_id uuid references neighborhoods(id) on delete set null,
    feedback_type text not null,
    created_at timestamptz not null default now()
);
