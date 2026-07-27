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