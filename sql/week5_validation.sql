-- Week 5 Validation
-- Independently validates reliability segmentation
-- and Late Tax concentration findings.

CREATE OR REPLACE VIEW late_tax AS
SELECT *
FROM read_csv_auto(
    'data/processed/late_tax_analytics.csv',
    HEADER = TRUE
);


-- ============================================================
-- 1. SOURCE TOTALS
-- Expected:
-- total_trips = 1813
-- late_trips = 121
-- total_excess_late_tax_min = 1222.38
-- ============================================================

SELECT
    COUNT(*) AS total_trips,
    SUM(late_trip_flag) AS late_trips,
    ROUND(
        100.0 * SUM(late_trip_flag) / COUNT(*),
        2
    ) AS late_trip_pct,
    ROUND(
        SUM(excess_late_tax_min),
        2
    ) AS total_excess_late_tax_min
FROM late_tax;


-- ============================================================
-- 2. ROUTE × TIME-PERIOD CONCENTRATION
-- ============================================================

WITH route_period AS (

    SELECT
        route_id,
        time_period,
        COUNT(*) AS trips,
        SUM(late_trip_flag) AS late_trips,
        SUM(excess_late_tax_min)
            AS excess_late_tax_min

    FROM late_tax

    GROUP BY
        route_id,
        time_period
),

ranked AS (

    SELECT
        *,
        100.0 * excess_late_tax_min
            / SUM(excess_late_tax_min) OVER ()
            AS late_tax_share_pct,

        ROW_NUMBER() OVER (
            ORDER BY excess_late_tax_min DESC
        ) AS late_tax_rank

    FROM route_period
)

SELECT
    late_tax_rank,
    route_id,
    time_period,
    trips,
    late_trips,
    ROUND(excess_late_tax_min, 2)
        AS excess_late_tax_min,
    ROUND(late_tax_share_pct, 2)
        AS late_tax_share_pct

FROM ranked

ORDER BY late_tax_rank;


-- ============================================================
-- 3. TOP-3 LATE TAX SHARE
-- Expected: approximately 84.58%
-- ============================================================

WITH route_period AS (

    SELECT
        route_id,
        time_period,
        SUM(excess_late_tax_min)
            AS excess_late_tax_min

    FROM late_tax

    GROUP BY
        route_id,
        time_period
),

ranked AS (

    SELECT
        *,
        ROW_NUMBER() OVER (
            ORDER BY excess_late_tax_min DESC
        ) AS late_tax_rank

    FROM route_period
),

totals AS (

    SELECT
        SUM(excess_late_tax_min)
            AS total_late_tax
    FROM route_period
)

SELECT
    ROUND(
        100.0
        * SUM(r.excess_late_tax_min)
        / MAX(t.total_late_tax),
        2
    ) AS top_3_late_tax_share_pct

FROM ranked r
CROSS JOIN totals t

WHERE r.late_tax_rank <= 3;


-- ============================================================
-- 4. YELLOW-N OVERNIGHT CONTRIBUTION
-- Expected:
-- trips = 335
-- late_trips = 88
-- late_trip_pct = 26.27%
-- late_tax_share_pct = 68.28%
-- ============================================================

SELECT
    route_id,
    time_period,
    COUNT(*) AS trips,

    SUM(late_trip_flag)
        AS late_trips,

    ROUND(
        100.0
        * SUM(late_trip_flag)
        / COUNT(*),
        2
    ) AS late_trip_pct,

    ROUND(
        SUM(excess_late_tax_min),
        2
    ) AS excess_late_tax_min,

    ROUND(
        100.0
        * SUM(excess_late_tax_min)
        / (
            SELECT SUM(excess_late_tax_min)
            FROM late_tax
        ),
        2
    ) AS late_tax_share_pct

FROM late_tax

WHERE
    route_id = 'BA:Yellow-N'
    AND time_period = 'Overnight'

GROUP BY
    route_id,
    time_period;


-- ============================================================
-- 5. SAMPLE-SIZE GUARDRAIL AUDIT
-- Groups below 30 trips should not drive
-- operational segmentation conclusions.
-- ============================================================

SELECT
    route_id,
    time_period,
    COUNT(*) AS trips,
    SUM(late_trip_flag) AS late_trips

FROM late_tax

GROUP BY
    route_id,
    time_period

HAVING COUNT(*) < 30

ORDER BY trips DESC;


