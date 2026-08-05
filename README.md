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

- `src/data_gen/synthetic_data.py`
- `src/data_gen/generate_electrolyser_reference.py`

### ETL

- `src/etl/ingest_mes.py`
- `src/etl/ingest_plm.py`
- `src/etl/ingest_electrolyser_reference.py`

### Transformation

- `src/transform/transform_kpis.py`

### Documentation

- `docs/transformation_logic.md`
- `notebooks/week3_kpi_transformation.ipynb`

---

## Technologies Used

- Python
- Pandas
- Parquet
- Jupyter Notebook
- VS Code

---

## Notes

- Electrolyser benchmark values are maintained separately in `electrolyser_reference.csv`.
- The dataset is converted into Parquet before transformation.
- OEE Performance is computed using benchmark-based ideal cycle time.
- Machine logs and production orders are linked using timestamp overlap.
- Some production orders may not have matching machine logs due to independently generated synthetic datasets, resulting in undefined Quality and OEE values for those records.