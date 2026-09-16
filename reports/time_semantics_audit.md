# Week 2 — Time Semantics Audit

- Total rows: 1,813
- Rows with GTFS time >= 24:00: 299
- Share >= 24:00: 16.5%

## Service-Day Offset

| Day Offset | Rows |
|---:|---:|
| 0 | 1514 |
| 1 | 299 |

## Arrival Delay Distribution

- Minimum: 0.68 min
- Median: 1.12 min
- 95th percentile: 5.72 min
- Maximum: 25.13 min

## Interpretation

GTFS times at or above 24:00 belong to the following calendar day even though they remain associated with the previous GTFS service_date.

Feature engineering should therefore preserve service_date while also creating an adjusted calendar_date and calendar_day_of_week for time-of-day analysis.