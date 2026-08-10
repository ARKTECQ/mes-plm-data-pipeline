#Contains the analytical SQL queries

-- 1. Production Efficiency by Product and Week
SELECT
    product_id,

    EXTRACT(YEAR FROM date) AS year,

    EXTRACT(WEEK FROM date) AS week,

    SUM(actual_qty) AS total_actual,

    SUM(planned_qty) AS total_planned,

    ROUND(
        SUM(actual_qty)::NUMERIC /
        NULLIF(SUM(planned_qty), 0),
        4
    ) AS fulfillment_rate

FROM fact_production_kpis

WHERE date >= CURRENT_DATE - INTERVAL '30 days'

GROUP BY
    product_id,
    EXTRACT(YEAR FROM date),
    EXTRACT(WEEK FROM date)

ORDER BY
    year,
    week,
    fulfillment_rate DESC;


-- 2. Downtime Correlation with Recent Engineering Changes
-- Compare downtime during the 7 days before and after each approved ECN
WITH downtime_comparison AS (

    SELECT
        e.change_id,
        e.product_id,
        e.request_date,

        -- Downtime events before the ECN
        COUNT(d.event_id) FILTER (
            WHERE d.start_time >= e.request_date - INTERVAL '7 days'
              AND d.start_time < e.request_date
        ) AS downtime_events_before,

        -- Total downtime before the ECN
        ROUND(
            COALESCE(
                SUM(d.downtime_minutes) FILTER (
                    WHERE d.start_time >= e.request_date - INTERVAL '7 days'
                      AND d.start_time < e.request_date
                ),
                0
            )::NUMERIC,
            2
        ) AS downtime_minutes_before,

        -- Downtime events after the ECN
        COUNT(d.event_id) FILTER (
            WHERE d.start_time >= e.request_date
              AND d.start_time < e.request_date + INTERVAL '7 days'
        ) AS downtime_events_after,

        -- Total downtime after the ECN
        ROUND(
            COALESCE(
                SUM(d.downtime_minutes) FILTER (
                    WHERE d.start_time >= e.request_date
                      AND d.start_time < e.request_date + INTERVAL '7 days'
                ),
                0
            )::NUMERIC,
            2
        ) AS downtime_minutes_after

    FROM ecn_events e

    LEFT JOIN machine_downtime d
        ON d.start_time >= e.request_date - INTERVAL '7 days'
       AND d.start_time < e.request_date + INTERVAL '7 days'

    WHERE e.approved_flag = TRUE

    GROUP BY
        e.change_id,
        e.product_id,
        e.request_date
)

SELECT
    *,

    -- Indicates whether downtime increased or decreased
    CASE
        WHEN downtime_minutes_after > downtime_minutes_before
            THEN 'Increased'
        WHEN downtime_minutes_after < downtime_minutes_before
            THEN 'Decreased'
        ELSE 'No Change'
    END AS downtime_trend,

    -- Percentage change in downtime
    ROUND(
        CASE
            WHEN downtime_minutes_before = 0 THEN NULL
            ELSE (
                (downtime_minutes_after - downtime_minutes_before)
                / downtime_minutes_before
            ) * 100
        END,
        2
    ) AS downtime_change_percent

FROM downtime_comparison

ORDER BY request_date DESC;



-- 3. Defect Rate Before and After Change Request Approval
-- Uses request_date as the change reference date
SELECT
    f.product_id,
    e.change_id,
    e.request_date,

    AVG(f.defect_rate)
        FILTER (
            WHERE f.date < e.request_date
        ) AS defect_before,

    AVG(f.defect_rate)
        FILTER (
            WHERE f.date >= e.request_date
        ) AS defect_after

FROM fact_production_kpis f

JOIN ecn_events e
    ON f.product_id = e.product_id

WHERE e.approved_flag = TRUE

GROUP BY
    f.product_id,
    e.change_id,
    e.request_date

ORDER BY
    e.request_date;



-- 4. Top 5 Machines by Downtime
SELECT
    machine_id,
    ROUND(
        SUM(downtime_minutes)::NUMERIC,
        2
    ) AS total_downtime_minutes

FROM machine_downtime
GROUP BY machine_id
ORDER BY total_downtime_minutes DESC
LIMIT 5;



-- 5. Average OEE by Product
SELECT
    product_id,

    ROUND(
        AVG(availability_factor)::NUMERIC,
        4
    ) AS avg_availability,

    ROUND(
        AVG(performance_factor)::NUMERIC,
        4
    ) AS avg_performance,

    ROUND(
        AVG(quality_factor)::NUMERIC,
        4
    ) AS avg_quality,

    ROUND(
        AVG(oee)::NUMERIC,
        4
    ) AS avg_oee

FROM fact_production_kpis

GROUP BY product_id

ORDER BY avg_oee ASC;



-- 6. Monthly Production Performance Trend
SELECT
    DATE_TRUNC('month', date) AS production_date,

    COUNT(*) AS total_orders,

    COUNT(DISTINCT product_id) AS active_products,

    SUM(planned_qty) AS total_planned_qty,

    SUM(actual_qty) AS total_actual_qty,

    SUM(defects) AS total_defects,

    ROUND(
        SUM(actual_qty)::NUMERIC /
        NULLIF(SUM(planned_qty), 0),
        4
    ) AS fulfillment_rate,

    ROUND(
        AVG(defect_rate)::NUMERIC,
        4
    ) AS avg_defect_rate,

    ROUND(
        AVG(oee)::NUMERIC,
        4
    ) AS avg_oee

FROM fact_production_kpis

GROUP BY DATE_TRUNC('month', date)

ORDER BY production_date;



-- 7. Production Loss by Product
SELECT
    product_id,

    SUM(planned_qty) AS total_planned_qty,

    SUM(actual_qty) AS total_actual_qty,

    SUM(planned_qty - actual_qty) AS production_gap,

    ROUND(
        (
            SUM(planned_qty - actual_qty)::NUMERIC /
            NULLIF(SUM(planned_qty), 0)
        ) * 100,
        2
    ) AS production_gap_percentage

FROM fact_production_kpis

GROUP BY product_id

ORDER BY production_gap DESC;



-- 8. Downtime Pareto Analysis
WITH downtime_summary AS (
    SELECT
        reason_code,
        SUM(downtime_minutes) AS total_downtime_minutes
    FROM machine_downtime
    GROUP BY reason_code
),

downtime_total AS (
    SELECT
        SUM(total_downtime_minutes) AS overall_downtime
    FROM downtime_summary
)

SELECT
    d.reason_code,

    ROUND(
        d.total_downtime_minutes::NUMERIC,
        2
    ) AS total_downtime_minutes,

    ROUND(
        (
            (
                d.total_downtime_minutes /
                NULLIF(t.overall_downtime, 0)
            ) * 100
        )::NUMERIC,
        2
    ) AS downtime_percentage,

    ROUND(
        (
            (
                SUM(d.total_downtime_minutes) OVER (
                    ORDER BY d.total_downtime_minutes DESC
                ) /
                NULLIF(t.overall_downtime, 0)
            ) * 100
        )::NUMERIC,
        2
    ) AS cumulative_percentage

FROM downtime_summary d
CROSS JOIN downtime_total t

ORDER BY d.total_downtime_minutes DESC;



-- 09. Product Production Summary
SELECT
    product_id,
    COUNT(*) AS total_orders,
    SUM(planned_qty) AS total_planned_qty,
    SUM(actual_qty) AS total_actual_qty,
    SUM(defects) AS total_defects
FROM fact_production_kpis
GROUP BY product_id
ORDER BY product_id ASC;



-- 10. Overall Production KPI Summary
SELECT
    COUNT(*) AS total_orders,

    COUNT(DISTINCT product_id) AS total_products,

    SUM(planned_qty) AS total_planned_qty,

    SUM(actual_qty) AS total_actual_qty,

    SUM(defects) AS total_defects,

    ROUND(
        SUM(actual_qty)::NUMERIC /
        NULLIF(SUM(planned_qty), 0),
        4
    ) AS overall_fulfillment_rate,

    ROUND(
        AVG(defect_rate)::NUMERIC,
        4
    ) AS average_defect_rate,

    ROUND(
        AVG(oee)::NUMERIC,
        4
    ) AS average_oee

FROM fact_production_kpis;