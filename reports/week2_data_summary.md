# Week 2 — Analytics Pipeline & Late Tax Metric

## Objective

Transform the historical Daly City → Powell dataset into a validated analytics-ready table and define a defensible Late Tax metric for downstream SQL analysis and dashboarding.

## Coverage Improvement

An initial morning-only extraction produced 308 observations across 111 service dates.

Coverage audits showed that the raw historical source and trip matching were substantially more complete, while the 07:00–10:00 extraction filter was the primary bottleneck.

The extraction pipeline was redesigned to preserve all weekday observations.

Final master dataset:

- 1,813 trips
- 313 GTFS service dates
- 15 source months
- June 2025 through August 2026
- 19 validated source columns

## Data Quality

Automated validation confirmed:

- 0 schema mismatches
- 0 exact duplicate rows
- 0 duplicate `trip_id + service_date` composite keys
- 0 missing values
- 0 travel-time formula errors
- 0 delay formula errors

The final analytics dataset also passed all engineered-feature QA checks.

## Feature Engineering

The analytics layer contains 35 columns, including:

- actual calendar date
- calendar weekday
- GTFS service-day offset
- normalized clock hour
- time-period classification
- morning/evening peak indicators
- route-specific delay baseline
- schedule lateness
- Excess Late Tax
- 5-minute late-trip flag
- 10-minute severe-delay flag

GTFS times at or above 24:00 are explicitly adjusted to the correct calendar date while preserving the original GTFS `service_date`.

## Metric Definitions

### Schedule Lateness

`schedule_lateness_min = max(arrival_delay_min, 0)`

Minutes a trip reaches Powell later than its scheduled arrival.

### Excess Late Tax

`excess_late_tax_min = max(arrival_delay_min - route_baseline_delay_min, 0)`

Minutes of lateness above the median arrival-delay baseline for the same route.

Route baselines with fewer than 30 observations are flagged as unreliable.

## Key Findings

Across 1,813 trips:

- Average schedule lateness: 1.78 minutes
- Average Excess Late Tax: 0.67 minutes
- 26.0% of trips exceeded their route baseline
- 6.7% of trips arrived at least 5 minutes late
- 0.9% arrived at least 10 minutes late
- 95th percentile Excess Late Tax: 4.32 minutes

Average departure delay was 1.49 minutes versus a 0.30-minute average in-transit travel-time increase, indicating that most average destination lateness was already present at departure.

Among routes with adequate sample size, Yellow-N had the highest average Excess Late Tax at 1.33 minutes.

January 2026 had the highest monthly average Excess Late Tax at 1.74 minutes.

## Analytical Guardrails

- Red-N contains only 7 observations and should not drive route-level conclusions.
- Monthly comparisons use normalized per-trip metrics rather than raw totals because observation counts differ by month.
- GTFS after-midnight service remains associated with the original service date but is also assigned to the correct actual calendar date.
- Schedule lateness and Excess Late Tax are retained together for transparency.

## Week 2 Outputs

Core scripts:

- `src/validate_data.py`
- `src/audit_coverage.py`
- `src/audit_extraction_funnel.py`
- `src/audit_postmerge_filters.py`
- `src/audit_time_semantics.py`
- `src/audit_delay_baseline.py`
- `src/build_features.py`
- `src/analyze_kpis.py`
- `src/validate_analytics.py`

Supporting reports are stored in `reports/`.

The final local analytics dataset is:

`data/processed/late_tax_analytics.csv`

Generated processed datasets remain excluded from GitHub.
