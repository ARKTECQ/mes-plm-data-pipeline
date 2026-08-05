# Transformation Logic - Week 3

## Objective

Transform MES and PLM datasets into a curated KPI dataset for production analysis.

---

# Input Datasets

The transformation reads the following datasets from the Landing layer:

- machine_logs.parquet
- production_orders.parquet
- downtime_events.parquet
- bom.parquet
- product_metadata.parquet
- ecn_requests.parquet
- electrolyser_reference.parquet

---

# Join Strategy

## Machine Logs → Production Orders

Machine logs are linked to production orders using overlapping timestamps.

Condition:

```
machine_logs.timestamp >= production_orders.start_time

AND

machine_logs.timestamp <= production_orders.end_time
```

---

## Downtime Events → Production Orders

Downtime events are linked using overlapping production order time windows.

Condition:

```
downtime.start_time >= production_orders.start_time

AND

downtime.end_time <= production_orders.end_time
```

---

## Electrolyser Reference → Production KPIs

The electrolyser reference dataset is joined using:

```
product_id
```

This provides:

- benchmark_efficiency_nm3_per_kwh
- rated_power_kw

required for OEE calculation.

---

# KPI Calculations

## Total Output

```
Total Output = SUM(output_count)
```

Calculated from machine logs belonging to a production order.

---

## Defects

```
Defects = SUM(defect_flag)
```

---

## Defect Rate

```
Defect Rate = Defects / Total Output
```

---

## Average Cycle Time

```
Average Cycle Time = AVG(cycle_time_ms)
```

---

## Planned Time

```
Planned Time = end_time - start_time
```

---

## Downtime

```
Downtime = SUM(downtime_end - downtime_start)
```

---

## Operating Time

```
Operating Time = Planned Time - Downtime
```

---

## Availability

```
Availability = Operating Time / Planned Time
```

---

## Ideal Cycle Time

Using the electrolyser benchmark:

```
Ideal Cycle Time (ms) =
(3600 / (Benchmark Efficiency × Rated Power)) × 1000
```

---

## Performance

```
Performance =
(Ideal Cycle Time × Total Output)
/ Operating Time
```

---

## Quality

```
Quality =
(Total Output - Defects)
/ Total Output
```

---

## Overall Equipment Effectiveness (OEE)

```
OEE =
Availability × Performance × Quality
```

---

# Output Dataset

The transformation generates:

```
data/curated/production_kpis.parquet
```

Each row represents one production order.

Output columns include:

- order_id
- product_id
- planned_qty
- actual_qty
- total_output
- defects
- defect_rate
- avg_cycle_time_ms
- planned_time_ms
- downtime_ms
- operating_time_ms
- benchmark_efficiency_nm3_per_kwh
- rated_power_kw
- ideal_cycle_time_ms
- performance_factor
- quality_factor
- availability_factor
- oee

---

# Assumptions

- Machine logs and downtime events are associated with production orders using timestamp overlap.
- Electrolyser benchmark values are obtained from the reference dataset using product_id.
- Some production orders may have no matching machine logs because the synthetic datasets were generated independently. In such cases, Total Output becomes zero, resulting in undefined Quality and OEE values.
