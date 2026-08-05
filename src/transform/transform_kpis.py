import pandas as pd
from pathlib import Path #helps us work with file and folder paths in a clean and platform-independent way

LANDING_DIR = Path("data/landing")
CURATED_DIR = Path("data/curated")
#CURATED_DIR.mkdir(parents=True, exist_ok=True)

logs = pd.read_parquet(LANDING_DIR/"machine_logs.parquet")
orders = pd.read_parquet(LANDING_DIR/"production_orders.parquet")
downtime = pd.read_parquet(LANDING_DIR/"downtime_events.parquet")
bom = pd.read_parquet(LANDING_DIR/"bom.parquet")
products = pd.read_parquet(LANDING_DIR/"product_metadata.parquet")
ecn = pd.read_parquet(LANDING_DIR/"ecn_requests.parquet")
reference = pd.read_parquet(LANDING_DIR / "electrolyser_reference.parquet")

print("Machine logs")
print(logs.head())

print("\nProduction Orders")
print(orders.head())

print("\nDowntime Events")
print(downtime.head())

print("\nBOM")
print(bom.head())

print("\nProduct Metadata")
print(products.head())

print("\nECN Requests")
print(ecn.head())

print("\n========== DATASET INFORMATION ==========\n")

print("Machine Logs:")
print(logs.info())

print("\nProduction Orders:")
print(orders.info())

print("\nDowntime Events:")
print(downtime.info())

print("\nBOM:")
print(bom.info())

print("\nProduct Metadata:")
print(products.info())

print("\nECN Requests:")
print(ecn.info())

print("\nReference:")
print(reference.info())

# Convert string columns to datetime
logs["timestamp"]= pd.to_datetime(logs["timestamp"])
orders["start_time"]= pd.to_datetime(orders["start_time"])
orders["end_time"]=pd.to_datetime(orders["end_time"])
downtime["start_time"] = pd.to_datetime(downtime["start_time"])
downtime["end_time"] = pd.to_datetime(downtime["end_time"])
products["design_release_date"] = pd.to_datetime(products["design_release_date"])
ecn["request_date"] = pd.to_datetime(ecn["request_date"])

print("\n==== AFTER DATETIME CONVERSION ====\n")

print(logs.info())
print(orders.info())
print(downtime.info())
print(products.info())
print(ecn.info())

print("\n ==== CHECK DUPLICATE ROWS ====\n")

print("Machine_logs:", logs.duplicated().sum())
print("Production_orders:", orders.duplicated().sum())
print("Downtime Events:", downtime.duplicated().sum())
print("BOM:", bom.duplicated().sum())
print("Product Metadata:", products.duplicated().sum())
print("ECN Requests:", ecn.duplicated().sum())
print("Reference:",reference.duplicated().sum())

print("\n===check missing values====\n")

print("Machine_logs")
print(logs.isnull().sum())

print("\nProduction_orders")
print(orders.isnull().sum())

print("\nDowntime Events")
print(downtime.isnull().sum())

print("\nBOM")
print(bom.isnull().sum())

print("\nProduct Metadata")
print(products.isnull().sum())

print("\nECN Requests")
print(ecn.isnull().sum())

print("\nReference:")
print(reference.isnull().sum())

def attach_logs_to_order(order_row):
    mask=(
        (logs["timestamp"]>=order_row.start_time) &
        (logs["timestamp"]<= order_row.end_time)
    )
    return logs[mask]

def attach_downtime_to_order(order_row):
    mask = (
        (downtime["start_time"] >= order_row.start_time) &
        (downtime["end_time"] <= order_row.end_time)
    )
    return downtime[mask]

kpi_rows = []
for _, order in orders.iterrows():
    order_logs = attach_logs_to_order(order)
    order_downtime = attach_downtime_to_order(order)

    total_output = order_logs["output_count"].sum()
    total_defects = order_logs["defect_flag"].sum()
    avg_cycle = order_logs["cycle_time_ms"].mean() if not order_logs.empty else None
    planned_time_ms = (order.end_time - order.start_time).total_seconds() * 1000
    downtime_ms = (order_downtime["end_time"] -order_downtime["start_time"]).dt.total_seconds().sum() * 1000
    operating_time_ms = planned_time_ms - downtime_ms
    kpi_rows.append({#create dic of its KPI
        "order_id": order.order_id,
        "product_id": order.product_id,
        "planned_qty": order.planned_qty,
        "actual_qty": order.actual_qty,
        "total_output": int(total_output),
        "defects": int(total_defects),
    "defect_rate": (total_defects / total_output) if total_output else None,
    "avg_cycle_time_ms": avg_cycle,
    "planned_time_ms": planned_time_ms,
    "downtime_ms": downtime_ms,
    "operating_time_ms": operating_time_ms
})

kpi_df = pd.DataFrame(kpi_rows)
kpi_df = kpi_df.merge(
    reference,
    on="product_id",
    how="left"
)

kpi_df["ideal_cycle_time_ms"] = (
    3600.0 /
    (
        kpi_df["benchmark_efficiency_nm3_per_kwh"] *
        kpi_df["rated_power_kw"]
    )
) * 1000

#performance
kpi_df["performance_factor"] = (
    kpi_df["ideal_cycle_time_ms"] *
    kpi_df["total_output"]
) / kpi_df["operating_time_ms"]

#quality
kpi_df["quality_factor"] = (
    kpi_df["total_output"] - kpi_df["defects"]
) / kpi_df["total_output"]
kpi_df["quality_factor"] = kpi_df["quality_factor"].fillna(0)

#Availability
kpi_df["availability_factor"] = (
    kpi_df["operating_time_ms"] /
    kpi_df["planned_time_ms"]
)

#OEE
# OEE
kpi_df["oee"] = (
    kpi_df["availability_factor"] *
    kpi_df["performance_factor"] *
    kpi_df["quality_factor"]
)


print(kpi_df.head())
kpi_df.info()

kpi_df.to_parquet(CURATED_DIR/"production_kpis.parquet",
                  index=False
)

print("Wrote curated KPIs")

