# Power BI User Guide

## 1. Purpose

The Power BI report provides an interactive view of manufacturing production,
machine performance, product quality, downtime, and the impact of engineering
change requests.

The report contains five dashboard pages:

1. Production Overview
2. Machine Performance
3. Quality Metrics
4. Downtime Analysis
5. Engineering Change Impact

The dashboard is designed to help users monitor production KPIs, identify
performance and quality issues, analyze machine downtime, and evaluate the
impact of engineering changes.

---

# 2. Opening the Report

1. Open Power BI Desktop.
2. Select **File → Open**.
3. Open the report located at:

   `powerbi/mes_plm_report.pbix`

4. Wait for the report and data model to load.

---

# 3. Data Sources

The report uses the curated manufacturing data prepared during the ETL
pipeline.

The main analytical data sources include:

- Production KPI data
- Production orders
- Product information
- Machine information
- Machine downtime events
- Engineering Change Notification (ECN) events
- Time dimension

The data is available through PostgreSQL and/or the curated datasets used
by the project.

---

# 4. Refreshing Data

To refresh the dashboard:

1. Open the Power BI report.
2. Select **Home → Refresh**.
3. Power BI reloads the available data.
4. Wait until all visuals finish updating.

If Power BI cannot connect to PostgreSQL:

1. Go to **Transform data → Data source settings**.
2. Select the PostgreSQL data source.
3. Select **Edit Permissions** if credentials need to be updated.
4. Verify the server, database, username, and password.
5. Refresh the report again.

If PostgreSQL is unavailable because of network issues, the curated
Parquet/CSV data can be used as an alternative data source.

---

# 5. Dashboard Pages

## 5.1 Production Overview

### Purpose

The Production Overview page provides a high-level view of production
performance and OEE trends.

### Main KPIs

- **Total Production Orders** – Total number of production orders.
- **Total Planned Qty** – Total quantity planned for production.
- **Total Actual Qty** – Total quantity actually produced.
- **Average OEE** – Average Overall Equipment Effectiveness.

### Visuals

#### Planned vs Actual Production

Compares the planned production quantity with the actual production quantity
for each month.

This helps identify months where production was below or above the planned
target.

#### Monthly OEE Trend

Displays the monthly OEE trend over time.

The chart contains:

- Monthly OEE
- 3-Month Rolling Average OEE

The rolling average smooths short-term fluctuations and helps identify the
overall direction of production efficiency.

### Filters

- **Product Filter** – Filters production information by product.
- **Date Filter** – Filters the dashboard based on the selected production
  date range.

### How to interpret

Use this page as the starting point for understanding overall production
performance.

Compare planned and actual quantities first, then use the OEE trend to
identify periods of improving or declining operational efficiency.

---

# 5.2 Machine Performance

### Purpose

The Machine Performance page focuses on machine-level performance, cycle
time, and downtime.

### Main KPI

- **Total Downtime (min)** – Total recorded machine downtime in minutes.
- **Average Cycle Time (ms)** – Average machine cycle time.

### Visuals

#### Machine Downtime Ranking

Ranks machines according to their total downtime.

Machines with higher downtime require further investigation because they may
be contributing to production losses.

#### Top Downtime Reasons

Shows the major reasons responsible for machine downtime.

Examples include:

- Power Outage
- Sensor Fault
- Tool Replacement
- Machine Failure
- Quality Inspection
- Operator Break
- Scheduled Maintenance

#### Average Cycle Time by Machine

Shows the average cycle time for each machine.

This allows users to compare machine performance and identify machines with
relatively higher cycle times.

#### Cycle Time Distribution

Shows how the average cycle times of machines are distributed across
different cycle-time ranges.

The chart uses cycle-time bins to group machines with similar average cycle
times.

### Filter

- **Machine Filter** – Select a specific machine to analyze its performance.

### How to interpret

Use the Machine Performance page to identify machines with high downtime or
unusually high cycle times.

The downtime ranking can be compared with the downtime reasons to understand
both **which machines are affected** and **why downtime is occurring**.

---

# 5.3 Quality Metrics

### Purpose

The Quality Metrics page monitors product quality and defect performance.

### Main KPIs

- **Total Defects** – Total number of recorded defects.
- **Average Defect Rate** – Average defect rate across the selected data.

### Visuals

#### Defect Rate by Product

Displays the average defect rate for each product.

Products with higher defect rates may require additional quality
investigation.

#### Defect Trend by Month

Shows how the number of defects changes over time.

This helps identify periods with increasing or decreasing quality issues.

### Filters

- **Product Filter** – Select a specific product.
- **Date Filter** – Select the required date range.

### How to interpret

Use this page to identify products with relatively high defect rates and
observe whether defect levels are improving or worsening over time.

The product filter can be used to investigate a specific product in more
detail.

---

# 5.4 Downtime Analysis

### Purpose

The Downtime Analysis page provides a detailed analysis of machine downtime
by reason, machine, and time period.

### Main KPI

- **Total Downtime (min)** – Total downtime recorded during the selected
  period.

### Visuals

#### Downtime by Reason

Shows the total downtime associated with each downtime reason.

This helps identify the most significant causes of production downtime.

#### Downtime by Machine

Shows total downtime for each machine.

This can be used to identify machines that contribute most to downtime.

#### Downtime Trend Over Time

Displays the change in downtime across the selected time period.

This helps identify periods where downtime increased or decreased.

### Filter

- **Date Range Filter** – Select the start and end dates for the analysis.

### How to interpret

First identify the major downtime reasons, then compare them with the
machines experiencing the highest downtime.

The time trend can then be used to determine whether downtime is a recurring
or period-specific problem.

---

# 5.5 Engineering Change Impact

### Purpose

The Engineering Change Impact page evaluates how engineering change requests
affect production KPIs.

The page compares selected KPIs **before and after an engineering change**.

### Filters

- **Change ID** – Select a specific Engineering Change Request/ECN.
- **Change Type** – Filter changes based on their type.

### Main KPIs

- **Before Change OEE**
- **After Change OEE**
- **Before Change Defect Rate**
- **After Change Defect Rate**

### Selected Change Date

Displays the request date associated with the selected engineering change.

### Visuals

#### OEE Before vs After Change

Compares OEE before and after the selected engineering change.

This helps determine whether the change improved or reduced production
efficiency.

#### Defect Rate Before vs After Change

Compares defect rates before and after the selected engineering change.

This helps determine whether the engineering change had an effect on product
quality.

### Two analysis states

#### Engineering Change Overview

When no specific Change ID is selected, the visuals provide an overview of
the available engineering changes.

#### Selected Engineering Change

When a Change ID is selected, the dashboard focuses on that particular change
and displays its corresponding before/after KPI comparison.

### How to interpret

Select an ECN/change ID to investigate a specific engineering change.

Compare:

**Before Change OEE → After Change OEE**

and

**Before Change Defect Rate → After Change Defect Rate**

An increase in OEE may indicate improved production efficiency, while a
decrease in defect rate may indicate improved product quality.

Both KPIs should be considered together when evaluating the overall impact
of an engineering change.

---

# 6. Interactive Filtering

The dashboard contains interactive slicers and filters.

Depending on the page, users can filter by:

- Date
- Product
- Machine
- Engineering Change ID
- Engineering Change Type

Selecting a filter automatically updates the relevant KPIs and visuals on
the page.

To clear a selection, use the slicer's **Clear/Reset** option or select
**All**, where available.

---

# 7. OEE Measures

The report uses the following OEE-related measures/components:

- Availability
- Performance
- Quality
- OEE

The report also includes a **3-Month Rolling Average OEE** measure.

The rolling average is calculated over a moving three-month period and is
used to identify the underlying OEE trend while reducing the effect of
short-term monthly fluctuations.

---

# 8. Understanding the Dashboard

The recommended analysis flow is:

1. Start with **Production Overview** to understand overall production and
   OEE performance.
2. Move to **Machine Performance** to identify machines with high downtime
   or cycle times.
3. Use **Quality Metrics** to identify products with high defect rates.
4. Use **Downtime Analysis** to determine the major causes and timing of
   downtime.
5. Use **Engineering Change Impact** to evaluate whether engineering changes
   improved production efficiency and product quality.

