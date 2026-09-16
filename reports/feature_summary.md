# Week 2 — Feature Engineering Summary

- Analytical rows: 1,813
- Analytical columns: 35
- Average schedule lateness: 1.78 min
- Average Excess Late Tax: 0.67 min
- Trips above route baseline: 472 (26.0%)

## Route Baselines

| Route | Median Baseline (min) | Rows | Reliable |
|---|---:|---:|---|
| BA:Blue-N | 0.82 | 479 | Yes |
| BA:Green-N | 1.12 | 680 | Yes |
| BA:Red-N | 4.00 | 7 | No |
| BA:Yellow-N | 1.48 | 647 | Yes |

## Metric Definitions

### Schedule Lateness

`schedule_lateness_min = max(arrival_delay_min, 0)`

Minutes arriving at Powell later than scheduled.

### Excess Late Tax

`excess_late_tax_min = max(arrival_delay_min - route_baseline_delay_min, 0)`

Minutes of lateness above the typical median lateness for the same route.

Route baselines with fewer than 30 observations are flagged as unreliable and should not drive route-level conclusions.