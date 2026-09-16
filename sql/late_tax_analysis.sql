-- ============================================================
-- Late Tax: BART Reliability Analysis
-- Analytical SQL layer
-- Source: data/processed/late_tax_analytics.csv
-- ============================================================


-- 1. DATASET COVERAGE
SELECT
    COUNT(*) AS total_trips,
    COUNT(DISTINCT service_date) AS service_days,
    MIN(service_date) AS first_service_date,
    MAX(service_date) AS last_service_date
FROM late_tax;


-- 2. CORE RELIABILITY KPIs
SELECT
    COUNT(*) AS total_trips,

    ROUND(AVG(schedule_lateness_min), 2)
        AS avg_lateness_min,

    ROUND(MEDIAN(schedule_lateness_min), 2)
        AS median_lateness_min,

    ROUND(
        QUANTILE_CONT(schedule_lateness_min, 0.90),
        2
    ) AS p90_lateness_min,

    SUM(late_trip_flag)
        AS late_trips,

    ROUND(
        100.0 * SUM(late_trip_flag) / COUNT(*),
        2
    ) AS late_trip_pct,

    SUM(severe_delay_flag)
        AS severe_delay_trips,

    ROUND(
        SUM(excess_late_tax_min),
        2
    ) AS total_excess_late_tax_min

FROM late_tax;


-- 3. ROUTE RELIABILITY
SELECT
    route_id,

    COUNT(*) AS trips,

    ROUND(
        AVG(schedule_lateness_min),
        2
    ) AS avg_lateness_min,

    ROUND(
        MEDIAN(schedule_lateness_min),
        2
    ) AS median_lateness_min,

    ROUND(
        QUANTILE_CONT(schedule_lateness_min, 0.90),
        2
    ) AS p90_lateness_min,

    SUM(late_trip_flag)
        AS late_trips,

    ROUND(
        100.0 * SUM(late_trip_flag) / COUNT(*),
        2
    ) AS late_trip_pct,

    ROUND(
        SUM(excess_late_tax_min),
        2
    ) AS excess_late_tax_min

FROM late_tax

GROUP BY route_id

ORDER BY excess_late_tax_min DESC;

-- 4. MONTHLY ROUTE RELIABILITY RANKING
-- Rankings are only assigned to route-month groups with
-- at least 20 observed trips to avoid unstable comparisons.

WITH monthly_route AS (

    SELECT
        calendar_year_month,
        route_id,

        COUNT(*) AS trips,

        ROUND(
            AVG(schedule_lateness_min),
            2
        ) AS avg_lateness_min,

        ROUND(
            100.0 * SUM(late_trip_flag) / COUNT(*),
            2
        ) AS late_trip_pct,

        ROUND(
            SUM(excess_late_tax_min),
            2
        ) AS excess_late_tax_min

    FROM late_tax

    GROUP BY
        calendar_year_month,
        route_id
),

eligible AS (

    SELECT
        *,

        CASE
            WHEN trips >= 20 THEN TRUE
            ELSE FALSE
        END AS ranking_eligible

    FROM monthly_route
),

ranked AS (

    SELECT
        *,

        CASE
            WHEN ranking_eligible THEN
                RANK() OVER (
                    PARTITION BY
                        calendar_year_month,
                        ranking_eligible
                    ORDER BY late_trip_pct DESC
                )
        END AS monthly_late_rate_rank,

        CASE
            WHEN ranking_eligible THEN
                RANK() OVER (
                    PARTITION BY
                        calendar_year_month,
                        ranking_eligible
                    ORDER BY excess_late_tax_min DESC
                )
        END AS monthly_late_tax_rank

    FROM eligible
)

SELECT *
FROM ranked

ORDER BY
    calendar_year_month,
    ranking_eligible DESC,
    monthly_late_tax_rank,
    route_id;
        








-- 5. TIME-PERIOD RELIABILITY
-- Compares frequency, severity, and cumulative Late Tax
-- across different periods of the day.

WITH period_metrics AS (

    SELECT
        time_period,

        COUNT(*) AS trips,

        ROUND(
            AVG(schedule_lateness_min),
            2
        ) AS avg_lateness_min,

        ROUND(
            MEDIAN(schedule_lateness_min),
            2
        ) AS median_lateness_min,

        ROUND(
            QUANTILE_CONT(schedule_lateness_min, 0.90),
            2
        ) AS p90_lateness_min,

        SUM(late_trip_flag) AS late_trips,

        ROUND(
            100.0 * SUM(late_trip_flag) / COUNT(*),
            2
        ) AS late_trip_pct,

        SUM(severe_delay_flag) AS severe_delay_trips,

        ROUND(
            SUM(excess_late_tax_min),
            2
        ) AS excess_late_tax_min

    FROM late_tax

    GROUP BY time_period
),

with_share AS (

    SELECT
        *,

        ROUND(
            100.0 * excess_late_tax_min
            / SUM(excess_late_tax_min) OVER (),
            2
        ) AS late_tax_share_pct

    FROM period_metrics

)

SELECT *
FROM with_share

ORDER BY excess_late_tax_min DESC;

-- 6. ROUTE × TIME-PERIOD LATE TAX CONCENTRATION
-- Identifies whether time-period reliability problems are broad
-- or concentrated within particular routes.

WITH route_period AS (

    SELECT
        route_id,
        time_period,

        COUNT(*) AS trips,

        ROUND(
            AVG(schedule_lateness_min),
            2
        ) AS avg_lateness_min,

        SUM(late_trip_flag) AS late_trips,

        ROUND(
            100.0 * SUM(late_trip_flag) / COUNT(*),
            2
        ) AS late_trip_pct,

        ROUND(
            SUM(excess_late_tax_min),
            2
        ) AS excess_late_tax_min

    FROM late_tax

    GROUP BY
        route_id,
        time_period
),

ranked AS (

    SELECT
        *,

        ROUND(
            100.0 * excess_late_tax_min
            / SUM(excess_late_tax_min) OVER (
                PARTITION BY time_period
            ),
            2
        ) AS period_late_tax_share_pct,

        RANK() OVER (
            PARTITION BY time_period
            ORDER BY excess_late_tax_min DESC
        ) AS period_late_tax_rank

    FROM route_period
)

SELECT *
FROM ranked

ORDER BY
    time_period,
    period_late_tax_rank,
    route_id;

