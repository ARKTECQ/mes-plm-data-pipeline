--Product Dimension
CREATE TABLE IF NOT EXISTS dim_product (
    product_id TEXT PRIMARY KEY,
    product_name TEXT,
    design_release_date DATE
);


--Machine Dimension
CREATE TABLE IF NOT EXISTS dim_machine (
    machine_id TEXT PRIMARY KEY
);


--Time Dimension
CREATE TABLE IF NOT EXISTS dim_time (
    date DATE PRIMARY KEY,
    year INT,
    month INT,
    week INT
);


--Production KPI Fact Table
CREATE TABLE IF NOT EXISTS fact_production_kpis (
    order_id TEXT PRIMARY KEY,

    product_id TEXT,
    date DATE,

    planned_qty INT,
    actual_qty INT,
    total_output INT,
    defects INT,

    defect_rate DOUBLE PRECISION,
    avg_cycle_time_ms DOUBLE PRECISION,

    planned_time_ms DOUBLE PRECISION,
    downtime_ms DOUBLE PRECISION,
    operating_time_ms DOUBLE PRECISION,

    benchmark_efficiency_nm3_per_kwh DOUBLE PRECISION,
    rated_power_kw DOUBLE PRECISION,
    ideal_cycle_time_ms DOUBLE PRECISION,

    performance_factor DOUBLE PRECISION,
    quality_factor DOUBLE PRECISION,
    availability_factor DOUBLE PRECISION,
    oee DOUBLE PRECISION,

    FOREIGN KEY (product_id)
        REFERENCES dim_product(product_id),

    FOREIGN KEY (date)
        REFERENCES dim_time(date)
);

-- ECN Events
CREATE TABLE IF NOT EXISTS ecn_events (
    change_id TEXT PRIMARY KEY,
    product_id TEXT,
    change_type TEXT,
    request_date DATE,
    approved_flag BOOLEAN,

    FOREIGN KEY (product_id)
        REFERENCES dim_product(product_id)
);

-- Machine Downtime
CREATE TABLE IF NOT EXISTS machine_downtime (
    event_id TEXT PRIMARY KEY,
    machine_id TEXT,
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    reason_code TEXT,
    downtime_minutes DOUBLE PRECISION,

    FOREIGN KEY (machine_id)
        REFERENCES dim_machine(machine_id)
);