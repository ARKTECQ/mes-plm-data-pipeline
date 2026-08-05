import pandas as pd

# Read the source files
orders = pd.read_parquet("data/landing/production_orders.parquet")
logs = pd.read_parquet("data/landing/machine_logs.parquet")
kpis = pd.read_parquet("data/curated/production_kpis.parquet")

# Convert to datetime
orders["start_time"] = pd.to_datetime(orders["start_time"])
orders["end_time"] = pd.to_datetime(orders["end_time"])
logs["timestamp"] = pd.to_datetime(logs["timestamp"])

# Get first order
order = orders[orders["order_id"] == "ORD-0010"].iloc[0]

# Filter logs for this order
order_logs = logs[
    (logs["timestamp"] >= order["start_time"]) &
    (logs["timestamp"] <= order["end_time"])
]

print("========== ORDER ==========")
print(order)

print("\n========== MATCHING LOGS ==========")
print(order_logs)

print("\n========== MANUAL KPI ==========")
print("Total Output :", order_logs["output_count"].sum())
print("Defects      :", order_logs["defect_flag"].sum())
print("Avg Cycle    :", order_logs["cycle_time_ms"].mean())

print("\n========== KPI FILE ==========")
print(kpis[kpis["order_id"] == "ORD-0001"])