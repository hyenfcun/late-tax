# Week 3 — Late Tax Pattern Analysis

## Objective

Identify when and where riders experience the greatest Late Tax, with emphasis on tail risk rather than averages alone.

## Overall Distribution

- Trips analyzed: 1,813
- Average Excess Late Tax: 0.67 min
- Median Excess Late Tax: 0.00 min
- P90 Excess Late Tax: 2.45 min
- P95 Excess Late Tax: 4.32 min
- Probability of ≥5 min schedule lateness: 6.7%
- Probability of ≥10 min schedule lateness: 0.9%

## Route × Time Period

| Route | Period | Trips | Avg Tax | Median | P90 | P95 | ≥5 min Late | ≥10 min Late |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| BA:Red-N | Morning Peak | 3 | 2.67 | 0.10 | 7.90 | 7.90 | 33.3% | 33.3% |
| BA:Yellow-N | Overnight | 335 | 2.49 | 1.88 | 5.83 | 6.60 | 26.3% | 1.8% |
| BA:Green-N | Evening Peak | 76 | 0.49 | 0.00 | 0.35 | 3.63 | 5.3% | 1.3% |
| BA:Green-N | Midday | 266 | 0.48 | 0.00 | 0.00 | 2.70 | 4.5% | 2.3% |
| BA:Green-N | Overnight | 181 | 0.39 | 0.00 | 1.53 | 2.27 | 2.8% | 0.0% |
| BA:Blue-N | Evening | 103 | 0.61 | 0.60 | 1.35 | 1.73 | 2.9% | 0.0% |
| BA:Red-N | Evening Peak | 1 | 0.70 | 0.70 | 0.70 | 0.70 | 0.0% | 0.0% |
| BA:Green-N | Evening | 15 | 0.70 | 0.00 | 0.35 | 0.35 | 6.7% | 6.7% |
| BA:Blue-N | Morning Peak | 88 | 0.08 | 0.00 | 0.00 | 0.23 | 1.1% | 0.0% |
| BA:Blue-N | Midday | 135 | 0.07 | 0.00 | 0.00 | 0.23 | 0.7% | 0.0% |
| BA:Blue-N | Evening Peak | 89 | 0.02 | 0.00 | 0.00 | 0.23 | 0.0% | 0.0% |
| BA:Blue-N | Overnight | 64 | 0.02 | 0.00 | 0.00 | 0.23 | 0.0% | 0.0% |
| BA:Yellow-N | Morning Peak | 75 | 0.07 | 0.00 | 0.00 | 0.00 | 0.0% | 0.0% |
| BA:Yellow-N | Evening Peak | 72 | 0.00 | 0.00 | 0.00 | 0.00 | 0.0% | 0.0% |
| BA:Yellow-N | Midday | 115 | 0.00 | 0.00 | 0.00 | 0.00 | 0.0% | 0.0% |
| BA:Yellow-N | Evening | 50 | 0.45 | 0.00 | 0.00 | 0.00 | 2.0% | 2.0% |
| BA:Green-N | Morning Peak | 142 | 0.16 | 0.00 | 0.00 | 0.00 | 2.8% | 0.0% |
| BA:Red-N | Midday | 2 | 0.00 | 0.00 | 0.00 | 0.00 | 0.0% | 0.0% |
| BA:Red-N | Evening | 1 | 0.00 | 0.00 | 0.00 | 0.00 | 0.0% | 0.0% |

## Weekday × Time Period

| Weekday | Period | Trips | Avg Tax | P90 | P95 | ≥5 min Late | ≥10 min Late |
|---|---|---:|---:|---:|---:|---:|---:|
| Friday | Overnight | 117 | 1.80 | 4.88 | 6.90 | 19.7% | 1.7% |
| Tuesday | Overnight | 112 | 1.94 | 5.30 | 6.47 | 21.4% | 0.9% |
| Wednesday | Overnight | 124 | 1.62 | 5.47 | 5.97 | 18.5% | 1.6% |
| Thursday | Overnight | 122 | 1.46 | 4.53 | 5.68 | 13.9% | 0.8% |
| Monday | Evening | 41 | 1.41 | 2.68 | 5.37 | 7.3% | 4.9% |
| Saturday | Overnight | 58 | 1.60 | 3.15 | 4.47 | 10.3% | 0.0% |
| Tuesday | Evening | 35 | 0.55 | 0.60 | 1.38 | 5.7% | 0.0% |
| Monday | Overnight | 47 | 0.13 | 0.00 | 0.88 | 0.0% | 0.0% |
| Wednesday | Midday | 147 | 0.48 | 0.00 | 0.82 | 4.1% | 2.7% |
| Wednesday | Evening | 34 | 0.19 | 0.60 | 0.60 | 0.0% | 0.0% |
| Thursday | Evening | 37 | 0.21 | 0.60 | 0.60 | 0.0% | 0.0% |
| Friday | Evening | 22 | 0.20 | 0.60 | 0.60 | 0.0% | 0.0% |
| Thursday | Morning Peak | 70 | 0.19 | 0.00 | 0.48 | 1.4% | 1.4% |
| Tuesday | Midday | 100 | 0.22 | 0.00 | 0.35 | 3.0% | 0.0% |
| Wednesday | Morning Peak | 68 | 0.20 | 0.00 | 0.23 | 2.9% | 0.0% |
| Monday | Midday | 88 | 0.19 | 0.00 | 0.23 | 2.3% | 0.0% |
| Friday | Midday | 103 | 0.25 | 0.00 | 0.23 | 1.9% | 1.9% |
| Thursday | Evening Peak | 38 | 0.21 | 0.00 | 0.23 | 2.6% | 0.0% |
| Monday | Evening Peak | 47 | 0.09 | 0.00 | 0.23 | 0.0% | 0.0% |
| Tuesday | Morning Peak | 54 | 0.02 | 0.00 | 0.00 | 0.0% | 0.0% |
| Tuesday | Evening Peak | 52 | 0.12 | 0.00 | 0.00 | 1.9% | 0.0% |
| Wednesday | Evening Peak | 70 | 0.07 | 0.00 | 0.00 | 1.4% | 0.0% |
| Monday | Morning Peak | 50 | 0.01 | 0.00 | 0.00 | 0.0% | 0.0% |
| Friday | Morning Peak | 66 | 0.21 | 0.00 | 0.00 | 4.5% | 0.0% |
| Thursday | Midday | 80 | 0.03 | 0.00 | 0.00 | 0.0% | 0.0% |
| Friday | Evening Peak | 31 | 0.52 | 0.00 | 0.00 | 3.2% | 3.2% |

## Monthly Pattern

| Month | Trips | Avg Tax | Median | P90 | P95 | ≥5 min Late |
|---|---:|---:|---:|---:|---:|---:|
| 2025-06 | 65 | 0.41 | 0.00 | 0.88 | 1.03 | 3.1% |
| 2025-07 | 61 | 0.83 | 0.00 | 2.32 | 4.40 | 8.2% |
| 2025-08 | 310 | 0.56 | 0.00 | 0.87 | 4.38 | 5.8% |
| 2025-09 | 393 | 0.46 | 0.00 | 1.27 | 3.25 | 4.6% |
| 2025-10 | 202 | 0.49 | 0.00 | 1.33 | 3.00 | 4.5% |
| 2025-11 | 75 | 0.63 | 0.00 | 2.55 | 3.27 | 5.3% |
| 2025-12 | 70 | 0.64 | 0.00 | 2.33 | 3.58 | 5.7% |
| 2026-01 | 69 | 1.74 | 0.00 | 5.47 | 7.95 | 20.3% |
| 2026-02 | 67 | 1.03 | 0.00 | 2.53 | 5.47 | 9.0% |
| 2026-03 | 58 | 1.05 | 0.00 | 3.52 | 3.75 | 12.1% |
| 2026-04 | 66 | 1.10 | 0.00 | 3.68 | 5.42 | 13.6% |
| 2026-05 | 96 | 0.58 | 0.00 | 2.42 | 2.92 | 3.1% |
| 2026-06 | 88 | 0.95 | 0.00 | 3.33 | 5.37 | 10.2% |
| 2026-07 | 100 | 0.94 | 0.00 | 4.10 | 5.97 | 11.0% |
| 2026-08 | 93 | 0.44 | 0.23 | 1.10 | 1.80 | 2.2% |

## Highest-Risk Segments

- Highest P95 route × period (minimum 30 trips): BA:Yellow-N / Overnight — 6.60 min.
- Highest P95 weekday × period (minimum 30 trips): Friday / Overnight — 6.90 min.

## Top 15 Extreme Trips

| Date | Route | Period | Schedule Lateness | Excess Late Tax | Departure Delay | Travel Delta |
|---|---|---|---:|---:|---:|---:|
| 2026-02-17 | BA:Yellow-N | Overnight | 25.13 | 23.65 | 6.17 | 18.97 |
| 2026-01-19 | BA:Yellow-N | Evening | 24.00 | 22.52 | 22.88 | 1.12 |
| 2025-09-05 | BA:Yellow-N | Overnight | 19.78 | 18.30 | 21.45 | -1.67 |
| 2025-08-20 | BA:Green-N | Midday | 18.07 | 16.95 | 18.42 | -0.35 |
| 2025-08-20 | BA:Green-N | Midday | 16.57 | 15.45 | 17.33 | -0.77 |
| 2025-08-29 | BA:Green-N | Evening Peak | 16.42 | 15.30 | 16.70 | -0.28 |
| 2025-06-27 | BA:Yellow-N | Overnight | 13.12 | 11.63 | 8.42 | 4.70 |
| 2026-01-14 | BA:Yellow-N | Overnight | 13.12 | 11.63 | 11.68 | 1.43 |
| 2025-07-23 | BA:Yellow-N | Overnight | 12.58 | 11.10 | 13.08 | -0.50 |
| 2025-09-10 | BA:Green-N | Midday | 12.47 | 11.35 | 12.92 | -0.45 |
| 2026-05-28 | BA:Red-N | Morning Peak | 11.90 | 7.90 | 11.30 | 0.60 |
| 2025-08-25 | BA:Green-N | Evening | 11.22 | 10.10 | 11.57 | -0.35 |
| 2025-10-17 | BA:Green-N | Midday | 10.83 | 9.72 | 11.30 | -0.47 |
| 2025-10-15 | BA:Green-N | Midday | 10.77 | 9.65 | 11.05 | -0.28 |
| 2025-08-29 | BA:Green-N | Midday | 10.72 | 9.60 | 11.12 | -0.40 |

## Interpretation Guardrails

- Excess Late Tax is relative to each route's median arrival-delay baseline.
- P90 and P95 describe tail-risk conditions and should not be interpreted as typical trips.
- Segment rankings require at least 30 observations.
- Descriptive patterns do not establish causal relationships.
