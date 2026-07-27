# Dataset Schema

This document describes the synthetic MES and PLM datasets used in the project.


## MES

1. Machine_logs.csv

| Column        | Data Type | Description                                      |
|---------------|-----------|--------------------------------------------------|
| timestamp     | datetime  | Date and time of machine activity                |
| machine_id    | string    | Unique machine identifier (e.g., M01)            |
| status        | string    | Machine status (Running, Idle, Maintenance)      |
| cycle_time_ms | integer   | Time taken for one production cycle              |
| output_count  | integer   | Number of units produced                         |
| defect_flag   | string    | Indicates whether defects were detected (Yes/No) |

Sample Row

| timestamp           | machine_id | status  | cycle_time_ms | output_count | defect_flag |
|---------------------|------------|---------|---------------|--------------|-------------|
| 2026-03-15 10:30:12 | M01        | Running | 1450          | 8            | No          |



2. production_orders.csv

| Column      | Data Type | Description                    |
|-------------|-----------|--------------------------------|
| order_id    | string    | Unique production order ID     |
| product_id  | string    | Product being manufactured     |
| start_time  | datetime  | Production start time          |
| end_time    | datetime  | Production end time            |
| planned_qty | integer   | Planned production quantity    |
| actual_qty  | integer   | Actual production quantity     |

Sample Row

| order_id | product_id | start_time          | end_time            | planned_qty | actual_qty |
|----------|------------|---------------------|---------------------|-------------|------------|
| ORD-0001 | PROD-001   | 2026-03-15 08:00:00 | 2026-03-15 14:00:00 | 300         | 295        |



3. downtime_events.csv

| Column      | Data Type | Description               |
|-------------|-----------|---------------------------|
| event_id    | string    | Unique downtime event ID  |
| machine_id  | string    | Machine identifier        |
| start_time  | datetime  | Downtime start time       |
| end_time    | datetime  | Downtime end time         |
| reason_code | string    | Reason for downtime       |

Sample Row

| event_id | machine_id | start_time          | end_time            | reason_code      |
|----------|------------|---------------------|---------------------|------------------|
| DT-001   | M03        | 2026-02-20 09:15:00 | 2026-02-20 10:00:00 | Machine Failure  |



4. product_metadata.csv

| Column              | Data Type | Description               |
|---------------------|-----------|---------------------------|
| product_id          | string    | Unique product identifier |
| product_name        | string    | Product name              |
| design_release_date | date      | Design release date       |
| CAD_file_ref        | string    | CAD file reference        |

Sample Row

| product_id | product_name | design_release_date | CAD_file_ref        |
|------------|--------------|---------------------|---------------------|
| PROD-001   | Widget Alpha | 2025-08-10          | widget_alpha_v1.step |



5. bom.csv

| Column            | Data Type | Description                     |
|-------------------|-----------|---------------------------------|
| product_id        | string    | Product identifier              |
| component_id      | string    | Component identifier            |
| quantity          | integer   | Required component quantity     |
| component_version | string    | Component version               |

Sample Row

| product_id | component_id | quantity | component_version |
|------------|--------------|----------|-------------------|
| PROD-001   | COMP-005     | 4        | v2.0              |

---

6. ecn_requests.csv

| Column        | Data Type | Description                        |
|---------------|-----------|------------------------------------|
| change_id     | string    | Engineering change request ID      |
| product_id    | string    | Product identifier                 |
| change_type   | string    | Type of engineering change         |
| request_date  | date      | Date of change request             |
| approved_flag | string    | Approval status (Yes/No)           |

Sample Row

| change_id | product_id | change_type  | request_date | approved_flag |
|-----------|------------|--------------|--------------|---------------|
| ECN-001   | PROD-010   | Design Update | 2026-01-18   | Yes          |