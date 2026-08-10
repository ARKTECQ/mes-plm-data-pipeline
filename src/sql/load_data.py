import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

PROJECT_ROOT = Path(__file__).resolve().parents[2]
LANDING_DIR = PROJECT_ROOT / "data" / "landing"
CURATED_DIR = PROJECT_ROOT / "data" / "curated"
SCHEMA_FILE = PROJECT_ROOT / "src" / "sql" / "schema.sql"


# Load Database Configuration
load_dotenv(PROJECT_ROOT / ".env")

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "mesplm")


if not DB_USER or not DB_PASSWORD:
    raise ValueError(
        "Database credentials not found. "
        "Check your .env file."
    )


DATABASE_URL = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)



# Create PostgreSQL Engine
engine = create_engine(DATABASE_URL)



# Load Source Data
print("Loading Parquet datasets...")

kpis = pd.read_parquet(
    CURATED_DIR / "production_kpis.parquet"
)

orders = pd.read_parquet(
    LANDING_DIR / "production_orders.parquet"
)

products = pd.read_parquet(
    LANDING_DIR / "product_metadata.parquet"
)

logs = pd.read_parquet(
    LANDING_DIR / "machine_logs.parquet"
)

ecn = pd.read_parquet(
    LANDING_DIR / "ecn_requests.parquet"
)

downtime = pd.read_parquet(
    LANDING_DIR / "downtime_events.parquet"
)



# Prepare Product Dimension

dim_product = products[
    [
        "product_id",
        "product_name",
        "design_release_date"
    ]
].copy()

dim_product["design_release_date"] = pd.to_datetime(
    dim_product["design_release_date"],
    errors="coerce"
).dt.date

dim_product = dim_product.drop_duplicates(
    subset=["product_id"]
)



# Prepare Machine Dimension
dim_machine = logs[
    ["machine_id"]
].drop_duplicates().copy()



# Prepare Time Dimension
orders["start_time"] = pd.to_datetime(
    orders["start_time"],
    errors="coerce"
)

dim_time = pd.DataFrame({
    "date": orders["start_time"].dt.date
})

dim_time = dim_time.dropna().drop_duplicates()

dim_time["year"] = pd.to_datetime(
    dim_time["date"]
).dt.year

dim_time["month"] = pd.to_datetime(
    dim_time["date"]
).dt.month

dim_time["week"] = pd.to_datetime(
    dim_time["date"]
).dt.isocalendar().week.astype(int)



# Prepare Fact Table
fact = kpis.copy()

# Connect KPI records to production order dates
order_dates = orders[
    ["order_id", "start_time"]
].copy()

order_dates["date"] = order_dates["start_time"].dt.date

order_dates = order_dates[
    ["order_id", "date"]
].drop_duplicates(
    subset=["order_id"]
)


fact = fact.merge(
    order_dates,
    on="order_id",
    how="left"
)

# Prepare ECN Events
ecn_events = ecn[
    [
        "change_id",
        "product_id",
        "change_type",
        "request_date",
        "approved_flag"
    ]
].copy()

ecn_events["request_date"] = pd.to_datetime(
    ecn_events["request_date"],
    errors="coerce"
).dt.date

ecn_events = ecn_events.drop_duplicates(
    subset=["change_id"]
)

# Prepare Machine Downtime
machine_downtime = downtime[
    [
        "event_id",
        "machine_id",
        "start_time",
        "end_time",
        "reason_code"
    ]
].copy()

machine_downtime["start_time"] = pd.to_datetime(
    machine_downtime["start_time"],
    errors="coerce"
)

machine_downtime["end_time"] = pd.to_datetime(
    machine_downtime["end_time"],
    errors="coerce"
)

machine_downtime["downtime_minutes"] = (
    machine_downtime["end_time"] - machine_downtime["start_time"]
).dt.total_seconds() / 60

machine_downtime = machine_downtime.drop_duplicates(
    subset=["event_id"]
)



# Keep only columns defined in the PostgreSQL fact table
fact = fact[
    [
        "order_id",
        "product_id",
        "date",
        "planned_qty",
        "actual_qty",
        "total_output",
        "defects",
        "defect_rate",
        "avg_cycle_time_ms",
        "planned_time_ms",
        "downtime_ms",
        "operating_time_ms",
        "benchmark_efficiency_nm3_per_kwh",
        "rated_power_kw",
        "ideal_cycle_time_ms",
        "performance_factor",
        "quality_factor",
        "availability_factor",
        "oee"
    ]
]



# Create Tables Using schema.sql
print("Creating PostgreSQL tables...")

with engine.begin() as connection:

    with open(SCHEMA_FILE, "r", encoding="utf-8") as file:
        schema_sql = file.read()

    connection.execute(text(schema_sql))

# Clear existing analytical data before reloading

print("Clearing existing analytical data...")

with engine.begin() as connection:
    connection.execute(text("""
        TRUNCATE TABLE
            machine_downtime,
            ecn_events,
            fact_production_kpis,
            dim_time,
            dim_machine,
            dim_product
        CASCADE;
    """))

# Load Data into PostgreSQL
print("Loading dim_product...")

dim_product.to_sql(
    "dim_product",
    engine,
    if_exists="append",
    index=False
)


print("Loading dim_machine...")

dim_machine.to_sql(
    "dim_machine",
    engine,
    if_exists="append",
    index=False
)


print("Loading dim_time...")

dim_time.to_sql(
    "dim_time",
    engine,
    if_exists="append",
    index=False
)


print("Loading fact_production_kpis...")

fact.to_sql(
    "fact_production_kpis",
    engine,
    if_exists="append",
    index=False
)

print("Loading ecn_events...")

ecn_events.to_sql(
    "ecn_events",
    engine,
    if_exists="append",
    index=False
)


print("Loading machine_downtime...")

machine_downtime.to_sql(
    "machine_downtime",
    engine,
    if_exists="append",
    index=False
)

print("Week 4 data loading completed!")
