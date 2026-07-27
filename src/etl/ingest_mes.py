import logging
import pandas as pd
from pathlib import Path

# Project Paths
PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = PROJECT_ROOT / "data" / "raw" / "mes"
LANDING_DIR = PROJECT_ROOT / "data" / "landing"
ERROR_DIR = PROJECT_ROOT / "data" / "errors"
LOG_DIR = PROJECT_ROOT / "logs"

# Create folders if they don't exist
LANDING_DIR.mkdir(parents=True, exist_ok=True)
ERROR_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)

# Logging Configuration
logging.basicConfig(
    filename=LOG_DIR / "ingest.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# Expected Schema for MES Files
EXPECTED_SCHEMAS = {

    "machine_logs.csv": [
        "timestamp",
        "machine_id",
        "status",
        "cycle_time_ms",
        "output_count",
        "defect_flag"
    ],

    "production_orders.csv": [
        "order_id",
        "product_id",
        "start_time",
        "end_time",
        "planned_qty",
        "actual_qty"
    ],

    "downtime_events.csv": [
        "event_id",
        "machine_id",
        "start_time",
        "end_time",
        "reason_code"
    ],

    #for Test csv's
    #"Test_csv_for_error_handling.csv": [
    #"timestamp",
    #"machine_id",
    #"status",
    #"cycle_time_ms",
    #"output_count",
    #"defect_flag"
#]
}


# Validate Schema
def validate_columns(df, expected_columns):

    missing = [col for col in expected_columns if col not in df.columns]
    extra = [col for col in df.columns if col not in expected_columns]

    return missing, extra


# Ingest Single File
def ingest_file(filename):

    source_file = RAW_DIR / filename

    if not source_file.exists():
        logging.warning(f"{filename} not found.")
        print(f"⚠ {filename} not found.")
        return

    try:

        df = pd.read_csv(source_file)

        missing, extra = validate_columns(
            df,
            EXPECTED_SCHEMAS[filename]
        )

        if missing:
            logging.error(f"{filename} missing columns: {missing}")

            error_file = ERROR_DIR / f"{filename}.schema_error.csv"
            df.to_csv(error_file, index=False)

            print(f"❌ Schema validation failed : {filename}")
            return

        if extra:
            logging.warning(f"{filename} has extra columns: {extra}")

        output_file = LANDING_DIR / filename.replace(".csv", ".parquet")

        df.to_parquet(output_file, index=False)

        logging.info(f"{filename} converted successfully.")

        print(f"✅ {filename} → {output_file.name}")

    except Exception as e:

        logging.error(f"Error processing {filename}: {e}")

        print(f"❌ Error processing {filename}")
        print(e)


# Run MES Ingestion
def run_mes_ingestion():

    logging.info("========== MES Ingestion Started ==========")

    for filename in EXPECTED_SCHEMAS:
        ingest_file(filename)

    logging.info("========== MES Ingestion Completed ==========")

# Main
if __name__ == "__main__":
    run_mes_ingestion()