# Week 2 — Late Tax KPI Analysis

## Overall KPIs

- Trips analyzed: 1,813
- Average schedule lateness: 1.78 min
- Average Excess Late Tax: 0.67 min
- Median Excess Late Tax: 0.00 min
- 95th percentile Excess Late Tax: 4.32 min
- Trips above route baseline: 26.0%
- Trips ≥5 min late: 121 (6.7%)
- Trips ≥10 min late: 16 (0.9%)

## Delay Composition

- Average departure delay: 1.49 min
- Average in-transit travel-time delta: 0.30 min

Arrival lateness can be interpreted as the combination of departure delay and changes in travel time between Daly City and Powell.

## By Time Period

| Period | Trips | Avg Excess Tax | P95 Excess Tax | Avg Schedule Lateness | Above Baseline |
|---|---:|---:|---:|---:|---:|
| Morning Peak | 308 | 0.14 | 0.10 | 1.20 | 5.2% |
| Midday | 518 | 0.27 | 0.35 | 1.30 | 6.8% |
| Evening Peak | 238 | 0.17 | 0.23 | 1.18 | 6.3% |
| Evening | 169 | 0.57 | 1.48 | 1.61 | 43.2% |
| Overnight | 580 | 1.56 | 6.03 | 2.83 | 57.4% |

## By Calendar Weekday

| Weekday | Trips | Avg Excess Tax | P95 Excess Tax | Avg Schedule Lateness |
|---|---:|---:|---:|---:|
| Monday | 273 | 0.31 | 0.92 | 1.31 |
| Tuesday | 353 | 0.75 | 5.05 | 1.90 |
| Wednesday | 443 | 0.67 | 5.40 | 1.73 |
| Thursday | 347 | 0.61 | 3.58 | 1.74 |
| Friday | 339 | 0.80 | 4.65 | 1.93 |
| Saturday | 58 | 1.60 | 4.47 | 3.07 |

## By Month

| Month | Trips | Avg Excess Tax | P95 Excess Tax | Avg Schedule Lateness |
|---|---:|---:|---:|---:|
| 2025-06 | 65 | 0.41 | 1.03 | 1.43 |
| 2025-07 | 61 | 0.83 | 4.40 | 1.85 |
| 2025-08 | 310 | 0.56 | 4.38 | 1.64 |
| 2025-09 | 393 | 0.46 | 3.25 | 1.56 |
| 2025-10 | 202 | 0.49 | 3.00 | 1.62 |
| 2025-11 | 75 | 0.63 | 3.27 | 1.74 |
| 2025-12 | 70 | 0.64 | 3.58 | 1.74 |
| 2026-01 | 69 | 1.74 | 7.95 | 2.96 |
| 2026-02 | 67 | 1.03 | 5.47 | 2.23 |
| 2026-03 | 58 | 1.05 | 3.75 | 2.28 |
| 2026-04 | 66 | 1.10 | 5.42 | 2.32 |
| 2026-05 | 96 | 0.58 | 2.92 | 1.72 |
| 2026-06 | 88 | 0.95 | 5.37 | 2.04 |
| 2026-07 | 100 | 0.94 | 5.97 | 1.98 |
| 2026-08 | 93 | 0.44 | 1.80 | 1.56 |

## By Route

| Route | Trips | Avg Excess Tax | P95 Excess Tax | Avg Schedule Lateness | Baseline Reliable |
|---|---:|---:|---:|---:|---|
| BA:Blue-N | 479 | 0.17 | 0.60 | 0.99 | Yes |
| BA:Green-N | 680 | 0.40 | 2.27 | 1.51 | Yes |
| BA:Red-N | 7 | 1.24 | 7.90 | 4.37 | No |
| BA:Yellow-N | 647 | 1.33 | 5.97 | 2.64 | Yes |

## Interpretation Guardrails

- Excess Late Tax is measured relative to each route's median arrival-delay baseline.
- BA:Red-N has insufficient observations for reliable route-level conclusions.
- Monthly totals should not be compared directly because the number of observations differs by month; normalized per-trip KPIs are used instead.
- Schedule lateness and Excess Late Tax are both retained for transparency.