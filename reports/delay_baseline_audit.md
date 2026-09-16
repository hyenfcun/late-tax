# Week 2 — Delay Baseline Audit

- Total observations: 1,813

## Delay Distribution

| Metric | Min | P25 | Median | P75 | P95 | Max |
|---|---:|---:|---:|---:|---:|---:|
| Arrival delay | 0.68 | 0.82 | 1.12 | 1.48 | 5.72 | 25.13 |
| Departure delay | 0.12 | 0.82 | 1.12 | 1.12 | 4.62 | 22.88 |
| Travel-time delta | -1.67 | 0.00 | 0.00 | 0.72 | 1.17 | 18.97 |

## Arrival Delay Buckets

| Bucket | Trips | Share |
|---|---:|---:|
| <1 min | 534 | 29.5% |
| 1–2 min | 956 | 52.7% |
| 2–5 min | 202 | 11.1% |
| 5–10 min | 105 | 5.8% |
| 10+ min | 16 | 0.9% |

## Most Common Arrival Delay Values

| Delay (min) | Trips |
|---:|---:|
| 1.12 | 578 |
| 0.82 | 298 |
| 1.48 | 171 |
| 0.78 | 103 |
| 0.80 | 87 |
| 1.05 | 55 |
| 0.68 | 46 |
| 1.42 | 45 |
| 1.18 | 24 |
| 1.77 | 9 |

## Median Arrival Delay by Route

| Route | Median Delay (min) | Rows |
|---|---:|---:|
| BA:Blue-N | 0.82 | 479 |
| BA:Green-N | 1.12 | 680 |
| BA:Red-N | 4.00 | 7 |
| BA:Yellow-N | 1.48 | 647 |

## Median Arrival Delay by Time Period

| Time Period | Median Delay (min) | Rows |
|---|---:|---:|
| Evening | 1.42 | 169 |
| Evening Peak | 1.05 | 238 |
| Midday | 1.12 | 518 |
| Morning Peak | 1.12 | 308 |
| Overnight | 1.82 | 580 |

## Departure vs Arrival

- Arrival and departure delay within 10 seconds: 1,134 (62.5%)
- Arrival and departure delay within 30 seconds: 1,285 (70.9%)

## Decision Use

This audit determines whether raw arrival lateness should be used directly as Late Tax or adjusted against a systematic baseline before final KPI construction.