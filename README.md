# MES PLM POC
This repository contains the Proof of Concept for the MES-PLM Data Pipeline.

# Week1 - Environment Setup and Dataset Preparation

## Folder Structure
- data/raw/mes
- data/raw/plm
- src/etl
- src/transform
- notebooks
- docs
- powerbi
- .gitignore
- README.md

## Completed Tasks
- Created the project folder structure.
- Generated synthetic datasets for MES and PLM.
- Organized datasets into separate MES and PLM     folders.
- Installed required Python libraries.
- Set up Git and GitHub repository.
- Created notebooks for testing and practice.

## MES CSV Datasets
- machine_logs.csv
- production_orders.csv
- downtime_events.csv

## PLM CSV Datasets
- bom.csv
- product_metadata.csv
- ecn_requests.csv

# Week 2 - Data Ingestion

The objective of Week 2 was to build a reliable data ingestion pipeline for MES and PLM datasets.

## Folder Structure
- data/raw/mes
- data/raw/plm
- data/landing
- data/errors
- logs
- src/data_gen
- src/etl
- src/transform
- notebooks
- docs
- powerbi
- .gitignore
- README.md

## Features Implemented
- Read raw CSV files using Pandas.
- Performed schema validation by checking whether all required columns are present.
- Converted valid CSV files into Parquet format.
- Stored converted Parquet files in the `data/landing` folder.
- Implemented logging using Python's `logging` module.
- Recorded successful execution, warnings and errors in `logs/ingest.log`.
- Implemented error handling for invalid datasets.
- Stored files with schema validation errors in the `data/errors` folder.
- Tested the ingestion pipeline using both valid and invalid CSV files.

## Schema Validation
Before converting a CSV file, the pipeline checks whether all required columns are present.

- If the schema matches, the file is processed.
- If any required column is missing, the file is rejected.

## Logging
The pipeline maintains a log file at:

logs/ingest.log


The log records:
- Pipeline start and completion
- Successfully processed files
- Missing files
- Schema validation failures
- Unexpected errors during ingestion

## Error Handling
If a file fails schema validation:
- The file is copied to the `data/errors` folder.
- An error message is written to `logs/ingest.log`.
- The remaining files continue to be processed without stopping the pipeline.

## Input

```
data/raw/
```

Contains both MES and PLM CSV files.

---

## Output

```
data/landing/
```

Contains all successfully converted Parquet files.


## Scripts to convert CSV to Parquet format
### MES

```
python src/etl/ingest_mes.py
```

Processes:

- machine_logs.csv
- production_orders.csv
- downtime_events.csv

### PLM

```
python src/etl/ingest_plm.py
```

Processes:

- bom.csv
- product_metadata.csv
- ecn_requests.csv

# Week 3 - Data Transformation & KPI Computation

## Folder Structure

- data
  - raw
    - mes
      - downtime_events.csv
      - machine_logs.csv
      - production_orders.csv
    - plm
      - bom.csv
      - ecn_requests.csv
      - product_metadata.csv
    - electrolyser_reference.csv
  - landing
    - machine_logs.parquet
    - production_orders.parquet
    - downtime_events.parquet
    - bom.parquet
    - product_metadata.parquet
    - ecn_requests.parquet
    - electrolyser_reference.parquet
  - curated
    - production_kpis.parquet
  - errors
    - machine_logs.csv.schema_error.csv
    - Test_csv_for_error_handling.csv
    - Test_schema_for_error.csv

- logs
  - ingest.log

- src
  - data_gen
    - synthetic_data.ipynb
    - synthetic_data.py
    - generate_electrolyser_reference.py
  - etl
    - ingest_mes.py
    - ingest_plm.py
    - ingest_electrolyser_reference.py
  - transform
    - transform_kpis.py

- notebooks
  - week3_kpi_transformation.ipynb

- docs
  - Dataset_Schema.md
  - transformation_logic.md

- powerbi

- check_kpi.py
- .gitignore
- README.md

---

## Objective

Transform the ingested MES and PLM datasets into a curated production KPI dataset by integrating multiple data sources and computing manufacturing KPIs, including OEE.

---

## Tasks Completed

### 1. Electrolyser Reference Dataset

- Created a new synthetic dataset `electrolyser_reference.csv`.
- Generated benchmark efficiency (`benchmark_efficiency_nm3_per_kwh`) and rated power (`rated_power_kw`) for all 100 products.
- Used `product_id` as the primary key to link the reference dataset with production data.

---

### 2. ETL for Electrolyser Reference

- Created a separate ETL pipeline:
  - `src/etl/ingest_electrolyser_reference.py`
- Validated the dataset schema.
- Converted:
  ```
  data/raw/electrolyser_reference.csv
  ```
  into
  ```
  data/landing/electrolyser_reference.parquet
  ```
- Logged ingestion status and schema validation results.

---

### 3. Data Transformation

Loaded all landing datasets:

- machine_logs.parquet
- production_orders.parquet
- downtime_events.parquet
- bom.parquet
- product_metadata.parquet
- ecn_requests.parquet
- electrolyser_reference.parquet

Performed:

- Datetime conversion
- Missing value analysis
- Duplicate record validation
- Schema verification

---

### 4. Dataset Linkage

Implemented joins between datasets:

- Production Orders ↔ Machine Logs (timestamp overlap)
- Production Orders ↔ Downtime Events (timestamp overlap)
- Production KPIs ↔ Electrolyser Reference (`product_id`)

---

### 5. KPI Computation

Computed the following KPIs:

- Total Output
- Total Defects
- Defect Rate
- Average Cycle Time
- Planned Production Time
- Downtime Duration
- Operating Time
- Availability Factor
- Ideal Cycle Time
- Performance Factor
- Quality Factor
- Overall Equipment Effectiveness (OEE)

---

## OEE Formula

Availability

```
Operating Time / Planned Production Time
```

Performance

```
(Ideal Cycle Time × Total Output)
/ Operating Time
```

Quality

```
(Total Output − Defects)
/ Total Output
```

Overall Equipment Effectiveness

```
OEE = Availability × Performance × Quality
```

---

## Output

Generated curated dataset:

```
data/curated/production_kpis.parquet
```

Each record represents one production order with computed KPI values.

---

## Files Added

### Data Generation
- `src/data_gen/generate_electrolyser_reference.py`

### ETL

- `src/etl/ingest_electrolyser_reference.py`

### Transformation

- `src/transform/transform_kpis.py`

### Documentation

- `docs/transformation_logic.md`
- `notebooks/week3_kpi_transformation.ipynb`

---

## Diagnostic Queries

Implemented diagnostic queries to validate the transformation pipeline by:

- Identifying columns containing null values.
- Counting production orders with zero `total_output`.
- Inspecting sample rows with missing KPI values.
- Verifying join results between production orders and machine logs.
- Analyzing null values generated due to unmatched timestamp-based joins.

These diagnostic checks were used to troubleshoot data linkage issues and validate KPI computations before generating the curated dataset.

---

## Notes

- Electrolyser benchmark values are maintained separately in `electrolyser_reference.csv`.
- The dataset is converted into Parquet before transformation.
- OEE Performance is computed using benchmark-based ideal cycle time.
- Machine logs and production orders are linked using timestamp overlap.
- Some production orders may not have matching machine logs due to independently generated synthetic datasets, resulting in undefined Quality and OEE values for those records.

# Week 4 - Analytical Models & Business Queries

## Folder Structure

- data

  - raw
    - mes
      - downtime_events.csv
      - machine_logs.csv
      - production_orders.csv
    - plm
      - bom.csv
      - ecn_requests.csv
      - product_metadata.csv
    - electrolyser_reference.csv

  - landing
    - machine_logs.parquet
    - production_orders.parquet
    - downtime_events.parquet
    - bom.parquet
    - product_metadata.parquet
    - ecn_requests.parquet
    - electrolyser_reference.parquet

  - curated
    - production_kpis.parquet

  - errors
    - machine_logs.csv.schema_error.csv
    - Test_csv_for_error_handling.csv
    - Test_schema_for_error.csv

- logs
  - ingest.log

- src

  - data_gen
    - synthetic_data.ipynb
    - synthetic_data.py
    - generate_electrolyser_reference.py

  - etl
    - ingest_mes.py
    - ingest_plm.py
    - ingest_electrolyser_reference.py

  - transform
    - transform_kpis.py

  - sql
    - schema.sql
    - queries.sql
    - load_data.py

- notebooks
  - week3_kpi_transformation.ipynb

- docs

  - Dataset_Schema.md
  - transformation_logic.md

  - query_results
    - query_01_production_efficiency.csv
    - query_02_downtime_ecn.csv
    - query_03_defect_rate_ecn.csv
    - query_04_top_machines_downtime.csv
    - query_05_average_oee.csv
    - query_06_monthly_production_trend.csv
    - query_07_production_loss_by_product.csv
    - query_08_downtime_pareto_with_reason.csv
    - query_09_product_production_summary.csv
    - query_10_overall_production_kpi.csv

- powerbi

- check_kpi.py

- .gitignore

- README.md

---

## Objective

The objective of Week 4 was to load the curated production KPI data into an analytical store, design an analytical database schema, and create SQL queries that answer important manufacturing and business questions.

PostgreSQL was used as the local analytical store for the proof of concept.

The analytical layer enables production, quality, downtime, OEE, and engineering-change data to be queried using SQL.

---

## Analytical Store

### PostgreSQL

PostgreSQL was selected as the local analytical database for the POC.

The database used for the project is:

Database: mesplm
Schema: public

PostgreSQL was used as a local substitute for Azure Synapse so that the analytical schema and SQL queries could be developed, executed, and validated locally.

The same analytical design can be adapted to a cloud analytical platform such as Azure Synapse.

---

## Analytical Schema

A dimensional analytical schema was created to organize production and reference data.

### Dimension Tables

#### 1. dim_product

Stores product master information.

Important columns include:

- product_id
- product_name
- design_release_date

#### 2. dim_machine

Stores machine-related information.

Important columns include:

- machine_id
- machine_type

#### 3. dim_time

Stores calendar information used for time-based analysis.

Important columns include:

- date
- year
- month
- week

### Fact Table

#### fact_production_kpis

Stores production-level KPI information generated during Week 3.

Important columns include:

- order_id
- product_id
- machine_id
- date
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

Additional analytical tables were loaded for engineering changes and machine downtime:

- ecn_events
- machine_downtime

---

## Schema Definition

The analytical database schema was defined in:

src/sql/schema.sql

The DDL script creates the required analytical tables and defines their columns and keys.

The schema was executed in PostgreSQL and validated against the loaded data.

---

## Data Loading

The Week 3 curated KPI dataset and supporting datasets were loaded into PostgreSQL.

The main curated dataset is:

data/curated/production_kpis.parquet

The landing datasets used for analytical loading include:

data/landing/

- production_orders.parquet
- machine_logs.parquet
- downtime_events.parquet
- bom.parquet
- product_metadata.parquet
- ecn_requests.parquet
- electrolyser_reference.parquet

The PostgreSQL loading process was implemented using Python and database connectivity libraries.

The loaded data was validated using SQL queries in pgAdmin.

---

## Analytical SQL Queries

All analytical queries are maintained in:

src/sql/queries.sql

A total of 10 business-oriented SQL queries were developed.

### Query 1 - Production Efficiency by Product and Week

Calculates weekly production performance for each product over the recent 30-day period.

The query calculates:

- Total actual quantity
- Total planned quantity
- Fulfillment rate

Business question:

> How efficiently are products meeting their planned production quantities?

---

### Query 2 - Downtime Correlation with Recent Engineering Changes

Compares machine downtime during the 7-day period before and after each approved Engineering Change Notice (ECN).

The query calculates:

- Downtime events before the ECN
- Downtime minutes before the ECN
- Downtime events after the ECN
- Downtime minutes after the ECN
- Downtime trend
- Percentage change in downtime

The query classifies the downtime trend as:

- Increased
- Decreased
- No Change

Business question:

> Did machine downtime increase or decrease after an approved engineering change?

### Note

The available ECN dataset contains request_date and approved_flag, but does not contain a separate approval date.

Therefore, the ECN request_date is used as the reference date for the before/after comparison, and only approved ECNs are included.

---

### Query 3 - Defect Rate Before and After Approved Change Request

Compares the average defect rate for a product before and after an approved engineering change request.

The query calculates:

- Defect rate before the change reference date
- Defect rate after the change reference date
- Product
- Engineering change ID
- Change request date

Business question:

> Did product quality change after an approved engineering change?

---

### Query 4 - Top 5 Machines by Downtime

Ranks machines based on their total recorded downtime.

The query calculates:

- Machine ID
- Total downtime in minutes

Business question:

> Which machines contribute the most to production downtime?

---

### Query 5 - Average OEE by Product

Calculates the average manufacturing KPI values for each product.

The query reports:

- Average availability
- Average performance
- Average quality
- Average OEE

Products are ordered by OEE to identify products with relatively lower overall equipment effectiveness.

Business question:

> Which products have lower overall equipment effectiveness and may require further analysis?

---

### Query 6 - Monthly Production Performance Trend

Aggregates production data by month to identify production and quality trends.

The query calculates:

- Total production orders
- Number of active products
- Total planned quantity
- Total actual quantity
- Total defects
- Fulfillment rate
- Average defect rate
- Average OEE

Business question:

> How are production volume, fulfillment, quality, and OEE changing over time?

---

### Query 7 - Production Loss by Product

Measures the difference between planned and actual production quantities.

The query calculates:

- Total planned quantity
- Total actual quantity
- Production gap
- Production gap percentage

The production gap is calculated as:

Production Gap = Planned Quantity - Actual Quantity

Business question:

> Which products have the largest gap between planned and actual production?

---

### Query 8 - Downtime Pareto Analysis

Performs a Pareto-style analysis of downtime by reason code.

The query calculates:

- Total downtime by reason
- Percentage contribution to total downtime
- Cumulative downtime percentage

Business question:

> Which downtime reasons contribute most to overall machine downtime?

This helps identify the major downtime causes that should be prioritized for improvement.

---

### Query 9 - Product Production Summary

Provides an overall production summary for each product.

The query calculates:

- Total production orders
- Total planned quantity
- Total actual quantity
- Total defects

Business question:

> What is the overall production volume and quality status of each product?

---

### Query 10 - Overall Production KPI Summary

Provides a high-level summary of the entire production dataset.

The query calculates:

- Total production orders
- Total products
- Total planned quantity
- Total actual quantity
- Total defects
- Overall fulfillment rate
- Average defect rate
- Average OEE

Business question:

> What is the overall production and KPI performance across the complete dataset?

---

## Query Result Validation

- All analytical queries were executed successfully in PostgreSQL using pgAdmin.

- The final query outputs were exported as CSV files for documentation and further analysis.

---

## Query Result Files

Sample query outputs are stored in:

docs/query_results/

The folder contains:

- query_01_production_efficiency.csv
- query_02_downtime_ecn.csv
- query_03_defect_rate_ecn.csv
- query_04_top_machines_downtime.csv
- query_05_average_oee.csv
- query_06_monthly_production_trend.csv
- query_07_production_loss_by_product.csv
- query_08_downtime_pareto_with_reason.csv
- query_09_product_production_summary.csv
- query_10_overall_production_kpi.csv

These files contain sample outputs generated from the executed PostgreSQL analytical queries.

---

## Data Quality and NULL Handling

Data quality was validated before performing analytical queries.

The following checks were performed:

- Duplicate record checks
- NULL value checks
- Product coverage checks
- Production order counts
- KPI record counts
- Query result validation

 KPI-level NULL values are not artificially replaced when the underlying calculation cannot be meaningfully performed.

For example, if a production order has no matching machine-log records, total_output may be zero and metrics such as:

- defect_rate
- quality_factor
- oee

may remain NULL where the calculation is undefined.

This prevents invalid values from being introduced into the analytical dataset.

---

## Week 4 Deliverables

The following Week 4 deliverables were completed:

- PostgreSQL analytical database setup
- Analytical schema design
- DDL implementation in src/sql/schema.sql
- Loading of analytical datasets into PostgreSQL
- Curated KPI integration
- 10 analytical business queries
- Query validation using pgAdmin
- Sample query result exports
- Documentation of analytical logic
- PostgreSQL substitution documented for the unavailable Azure Synapse environment

---

## Week 4 Files

### SQL

src/sql/

- schema.sql
- queries.sql
- load_data.py

### Analytical Results

docs/query_results/

- query_01_production_efficiency.csv
- query_02_downtime_ecn.csv
- query_03_defect_rate_ecn.csv
- query_04_top_machines_downtime.csv
- query_05_average_oee.csv
- query_06_monthly_production_trend.csv
- query_07_production_loss_by_product.csv
- query_08_downtime_pareto_with_reason.csv
- query_09_product_production_summary.csv
- query_10_overall_production_kpi.csv

---

## Week 4 Outcome

By the end of Week 4, the project contains a working analytical layer on top of the MES-PLM data pipeline.

The analytical pipeline follows:

Raw MES + PLM Data
        ↓
CSV Ingestion
        ↓
Parquet Landing Layer
        ↓
KPI Transformation
        ↓
Curated Production KPIs
        ↓
PostgreSQL Analytical Store
        ↓
Analytical SQL Queries
        ↓
Business Insights / Query Results

The analytical layer provides a foundation for further visualization and dashboard development using Power BI.

# Week 5 – Power BI Dashboard & Analytics

## Folder Structure 
 
- data 
 
  - raw 
    - mes 
      - downtime_events.csv 
      - machine_logs.csv 
      - production_orders.csv 
    - plm 
      - bom.csv 
      - ecn_requests.csv 
      - product_metadata.csv 
    - electrolyser_reference.csv 
 
  - landing 
    - machine_logs.parquet 
    - production_orders.parquet 
    - downtime_events.parquet 
    - bom.parquet 
    - product_metadata.parquet 
    - ecn_requests.parquet 
    - electrolyser_reference.parquet 
 
  - curated 
    - production_kpis.parquet 
 
  - errors 
    - machine_logs.csv.schema_error.csv 
    - Test_csv_for_error_handling.csv 
    - Test_schema_for_error.csv 
 
- logs 
  - ingest.log 
 
- src 
 
  - data_gen 
    - synthetic_data.ipynb 
    - synthetic_data.py 
    - generate_electrolyser_reference.py 
 
  - etl 
    - ingest_mes.py 
    - ingest_plm.py 
    - ingest_electrolyser_reference.py 
 
  - transform 
    - transform_kpis.py 
 
  - sql 
    - schema.sql 
    - queries.sql 
    - load_data.py 
 
- notebooks 
  - week3_kpi_transformation.ipynb 
 
- docs 
 
  - Dataset_Schema.md 
  - transformation_logic.md 
  - powerbi_user_guide.md
 
  - screenshots
    - production_overview.png
    - machine_performance.png
    - quality_metrics.png
    - downtime_analysis.png
    - engineering_change_impact_overview.png
    - engineering_change_impact_selected.png
 
  - query_results 
    - query_01_production_efficiency.csv 
    - query_02_downtime_ecn.csv 
    - query_03_defect_rate_ecn.csv 
    - query_04_top_machines_downtime.csv 
    - query_05_average_oee.csv 
    - query_06_monthly_production_trend.csv 
    - query_07_production_loss_by_product.csv 
    - query_08_downtime_pareto_with_reason.csv 
    - query_09_product_production_summary.csv 
    - query_10_overall_production_kpi.csv 
 
- powerbi 
  - mes_plm_report.pbix
 
- check_kpi.py 
 
- .gitignore 
 
- README.md

---

## Overview

Week 5 focused on building an interactive Power BI dashboard using the
curated manufacturing and PLM data prepared during the previous weeks.

The objective was to transform the processed production, machine, quality,
downtime, and engineering change data into an interactive dashboard that
provides meaningful operational insights.

---

## Objectives

The main objectives completed during Week 5 were:

- Build an interactive Power BI dashboard.
- Create production performance KPIs.
- Analyze machine-level performance.
- Analyze product quality and defects.
- Analyze machine downtime.
- Evaluate the impact of Engineering Change Notifications (ECNs).
- Create calculated Power BI measures.
- Add a 3-month rolling average for OEE.
- Implement interactive filters and slicers.
- Prepare dashboard documentation and screenshots.

---

# Dashboard Structure

The final Power BI report contains five analytical pages:

1. Production Overview
2. Machine Performance
3. Quality Metrics
4. Downtime Analysis
5. Engineering Change Impact

---

# 1. Production Overview

### Purpose

Provides a high-level view of production performance and overall equipment
effectiveness.

### KPIs

- Total Production Orders
- Total Planned Quantity
- Total Actual Quantity
- Average OEE

### Visualizations

- Planned vs Actual Production by Month
- Monthly OEE Trend
- 3-Month Rolling Average OEE

### Filters

- Product
- Production Date

### Key Analysis

The page allows users to compare planned production against actual output
and monitor OEE trends over time.

The 3-month rolling average smooths monthly OEE fluctuations and provides a
clearer view of the underlying production performance trend.

---

# 2. Machine Performance

### Purpose

Analyzes machine-level cycle time and downtime performance.

### KPIs

- Total Downtime
- Average Cycle Time

### Visualizations

- Machine Downtime Ranking
- Top Downtime Reasons
- Average Cycle Time by Machine
- Cycle Time Distribution

### Filter

- Machine

### Key Analysis

The page identifies machines with high downtime and compares the average
cycle time of different machines.

The cycle-time distribution groups machine average cycle times into ranges
to provide an overview of cycle-time variation across machines.

---

# 3. Quality Metrics

### Purpose

Monitors product quality and defect performance.

### KPIs

- Total Defects
- Average Defect Rate

### Visualizations

- Defect Rate by Product
- Defect Trend by Month

### Filters

- Product
- Date

### Key Analysis

The page helps identify products with relatively high defect rates and
observe how defects change over time.

---

# 4. Downtime Analysis

### Purpose

Provides detailed analysis of production downtime.

### KPI

- Total Downtime in Minutes

### Visualizations

- Downtime by Reason
- Downtime by Machine
- Downtime Trend Over Time

### Filter

- Date Range

### Key Analysis

The page identifies the major causes of downtime, machines contributing to
downtime, and changes in downtime over time.

This allows potential production bottlenecks and recurring downtime causes
to be investigated.

---

# 5. Engineering Change Impact

### Purpose

Evaluates the impact of Engineering Change Notifications (ECNs) on
production performance and quality.

### Filters

- Change ID
- Change Type

### KPIs

- Before Change OEE
- After Change OEE
- Before Change Defect Rate
- After Change Defect Rate
- Selected Change Date

### Visualizations

- OEE Before vs After Change
- Defect Rate Before vs After Change

### Key Analysis

The page compares production and quality KPIs before and after an
engineering change.

Users can select a specific Change ID to investigate the impact of an
individual engineering change.

Two analysis states are supported:

- Engineering Change Overview
- Selected Engineering Change

---

# Power BI Calculated Measures

The following analytical measures were implemented in Power BI:

### OEE Components

- Average Availability
- Average Performance
- Average Quality
- Average OEE

### Rolling Average

A 3-month rolling average OEE measure was created to identify the underlying
OEE trend while reducing short-term monthly fluctuations.

Example:

```DAX
3 Month Rolling Average OEE =
CALCULATE(
    AVERAGE('public fact_production_kpis'[oee]),
    DATESINPERIOD(
        'public dim_time'[date],
        MAX('public dim_time'[date]),
        -3,
        MONTH
    )
)
```

---

# Understanding the Dashboard

The recommended analysis flow is:

1. Start with **Production Overview** to understand overall production and OEE performance.

2. Move to **Machine Performance** to identify machines with high downtime or cycle times.

3. Use **Quality Metrics** to identify products with high defect rates.

4. Use **Downtime Analysis** to determine the major causes and timing of downtime.

5. Use **Engineering Change Impact** to evaluate whether engineering changes improved production efficiency and product quality.

---

# Troubleshooting

### Dashboard visuals show errors

Check that the required curated data files exist and that the PostgreSQL connection is available.

### Power BI cannot connect to PostgreSQL

Verify:

- PostgreSQL server is running.
- Server and database names are correct.
- User credentials are correct.
- Network connectivity is available.

### Data appears outdated

Select **Home → Refresh** in Power BI Desktop.

### Production order count is incorrect

Verify that the production KPI data contains the expected number of unique orders and refresh the Power BI dataset.

### Engineering Change Impact shows no values

Check that a valid **Change ID** is selected and that the corresponding ECN data is available.

---

# Report Deliverables

The final Power BI report should be saved as:

`powerbi/mes_plm_report.pbix`

Dashboard screenshots should be saved under:

`docs/screenshots/`

Recommended screenshots:

- `production_overview.png`
- `machine_performance.png`
- `quality_metrics.png`
- `downtime_analysis.png`
- `engineering_change_impact_overview.png`
- `engineering_change_impact_selected.png`

This user guide provides instructions for opening, refreshing, filtering, and interpreting the Power BI report.