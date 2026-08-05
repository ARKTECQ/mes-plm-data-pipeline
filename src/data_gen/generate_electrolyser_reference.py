import pandas as pd
import random
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_DIR = PROJECT_ROOT / "data" / "raw"

RAW_DIR.mkdir(parents=True, exist_ok=True)

product_metadata = pd.read_csv(
    RAW_DIR / "plm" / "product_metadata.csv"
)
#col1
reference_df = product_metadata[["product_id"]].copy()
#col2 - generate values between 1.6 and 2.0 for every product.
reference_df["benchmark_efficiency_nm3_per_kwh"] = [
    round(random.uniform(1.6, 2.0), 2)
    for _ in range(len(reference_df))
]
#col 3
reference_df["rated_power_kw"] = [
    random.choice([10, 15, 20, 25, 30])
    for _ in range(len(reference_df))
]

print(reference_df.head())

reference_df.to_csv(
    RAW_DIR / "electrolyser_reference.csv",
    index=False
)

print("Electrolyser reference dataset created successfully.")
