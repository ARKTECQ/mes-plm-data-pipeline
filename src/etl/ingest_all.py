from pathlib import Path
import pandas as pd

# Project paths
BASE_PATH = Path(__file__).resolve().parents[2]

RAW_PATH = BASE_PATH / "data" / "raw"
LANDING_PATH = BASE_PATH / "data" / "landing"

# Create landing folder 
LANDING_PATH.mkdir(parents=True, exist_ok=True)

# List of CSV files
csv_files = [
    "plm/product_metadata.csv",
    "plm/bom.csv",
    "plm/ecn_requests.csv",
    "mes/machine_logs.csv",
    "mes/production_orders.csv",
    "mes/downtime_events.csv"
]

# Convert each CSV to Parquet
for file in csv_files:

    csv_path = RAW_PATH / file

    parquet_name = csv_path.stem + ".parquet"
    parquet_path = LANDING_PATH / parquet_name

    df = pd.read_csv(csv_path)

    df.to_parquet(parquet_path, index=False)

    print(f"Converted: {csv_path.name} -> {parquet_name}")

print("\nAll CSV files converted successfully!")