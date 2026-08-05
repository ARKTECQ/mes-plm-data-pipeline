import logging
import pandas as pd
from pathlib import Path

# Project Paths
PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DIR = PROJECT_ROOT / "data" / "raw"
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

# Expected Schema
EXPECTED_COLUMNS = [
    "product_id",
    "benchmark_efficiency_nm3_per_kwh",
    "rated_power_kw"
]


# Validate Schema
def validate_columns(df, expected_columns):

    missing = [col for col in expected_columns if col not in df.columns]
    extra = [col for col in df.columns if col not in expected_columns]

    return missing, extra


# Ingest File
def ingest_file():

    source_file = RAW_DIR / "electrolyser_reference.csv"

    if not source_file.exists():
        logging.warning("electrolyser_reference.csv not found.")
        print("⚠ electrolyser_reference.csv not found.")
        return

    try:

        df = pd.read_csv(source_file)

        missing, extra = validate_columns(
            df,
            EXPECTED_COLUMNS
        )

        if missing:
            logging.error(
                f"electrolyser_reference.csv missing columns: {missing}"
            )

            error_file = ERROR_DIR / "electrolyser_reference.schema_error.csv"

            df.to_csv(error_file, index=False)

            print("❌ Schema validation failed.")
            return

        if extra:
            logging.warning(
                f"electrolyser_reference.csv has extra columns: {extra}"
            )

        output_file = LANDING_DIR / "electrolyser_reference.parquet"

        df.to_parquet(output_file, index=False)

        logging.info("electrolyser_reference.csv converted successfully.")

        print(f"✅ electrolyser_reference.csv → {output_file.name}")

    except Exception as e:

        logging.error(
            f"Error processing electrolyser_reference.csv: {e}"
        )

        print("❌ Error processing electrolyser_reference.csv")
        print(e)


# Run Ingestion
def run_reference_ingestion():

    logging.info(
        "========== Electrolyser Reference Ingestion Started =========="
    )

    ingest_file()

    logging.info(
        "========== Electrolyser Reference Ingestion Completed =========="
    )


# Main
if __name__ == "__main__":
    run_reference_ingestion()