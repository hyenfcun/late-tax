# Week 3 — Midnight Reliability Investigation

## Analytical Question

Why does the Yellow-N service scheduled shortly after midnight show elevated Late Tax?

## Target vs Other Trips

| Segment | Trips | Avg Arrival Delay | Median Arrival Delay | Avg Departure Delay | Avg Travel Delta | >=5 min Late |
|---|---:|---:|---:|---:|---:|---:|
| Yellow-N midnight | 298 | 4.22 | 3.66 | 3.11 | 1.12 | 29.2% |
| All other trips | 1,515 | 1.30 | 1.12 | 1.17 | 0.14 | 2.2% |

## Scheduled Departures in Target Segment

| Scheduled Departure | Trips |
|---|---:|
| 24:01:00 | 31 |
| 24:07:00 | 15 |
| 24:08:00 | 250 |
| 24:17:00 | 2 |

## Monthly Consistency

| Month | Trips | Avg Arrival Delay | Median Arrival Delay | Avg Departure Delay | Avg Travel Delta | >=5 min Late |
|---|---:|---:|---:|---:|---:|---:|
| 2025-06 | 11 | 3.59 | 2.37 | 2.80 | 0.79 | 18.2% |
| 2025-07 | 15 | 4.80 | 3.70 | 4.57 | 0.23 | 33.3% |
| 2025-08 | 20 | 4.73 | 4.39 | 3.55 | 1.18 | 40.0% |
| 2025-09 | 21 | 4.18 | 4.53 | 2.47 | 1.71 | 28.6% |
| 2025-10 | 22 | 3.21 | 2.51 | 2.20 | 1.01 | 13.6% |
| 2025-11 | 20 | 3.64 | 2.96 | 2.46 | 1.18 | 20.0% |
| 2025-12 | 21 | 3.49 | 2.75 | 2.20 | 1.29 | 19.0% |
| 2026-01 | 22 | 5.80 | 6.41 | 4.55 | 1.24 | 59.1% |
| 2026-02 | 19 | 4.45 | 3.37 | 2.64 | 1.81 | 21.1% |
| 2026-03 | 21 | 4.34 | 4.23 | 3.28 | 1.06 | 33.3% |
| 2026-04 | 21 | 4.90 | 4.40 | 3.91 | 0.99 | 42.9% |
| 2026-05 | 20 | 3.52 | 3.56 | 2.57 | 0.95 | 10.0% |
| 2026-06 | 21 | 4.29 | 3.55 | 3.27 | 1.02 | 33.3% |
| 2026-07 | 23 | 5.14 | 4.20 | 3.54 | 1.60 | 47.8% |
| 2026-08 | 21 | 3.00 | 2.47 | 2.71 | 0.29 | 9.5% |

## Delay Driver Classification

Among 87 target trips arriving at least five minutes late:

- Departure-driven: 70 (80.5%)
- Travel-time-driven: 4 (4.6%)
- Mixed: 13 (14.9%)

## Key Findings

- Yellow-N midnight trips had a 29.2% rate of schedule lateness of at least five minutes, compared with 2.2% for all other analyzed trips.
- Average arrival delay was 4.22 minutes for the target segment versus 1.30 minutes for other trips.
- 80.5% of target trips that were at least five minutes late were classified as departure-driven.
- The elevated reliability risk appears across multiple months rather than being attributable to a single isolated month.

## Interpretation Guardrails

- This is descriptive analysis and does not establish that route or departure time causes delay.
- The target segment consists of Yellow-N trips scheduled between 24:00 and 24:59 in GTFS service time and mapped to the following calendar day.
- Driver classification is an analytical heuristic: departure-driven means positive departure delay was at least twice the positive travel-time delta; travel-time-driven applies the reverse rule.
- Comparisons are observational and are not adjusted for service frequency, incidents, maintenance, weather, or other operational factors.
