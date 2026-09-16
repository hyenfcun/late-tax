# Week 2 — Analytics Dataset QA

- Master rows: 1,813
- Analytics rows: 1,813
- Analytics columns: 35
- Overall status: **PASS**

## Validation Results

| Check | Status | Detail |
|---|---|---|
| Row count matches master dataset | PASS | master=1813, analytics=1813 |
| Composite key remains unique | PASS | duplicate keys=0 |
| All required engineered columns exist | PASS | missing=[] |
| No missing engineered values | PASS | missing values=0 |
| Calendar date correctly applies GTFS day offset | PASS | errors=0 |
| Service-day offsets are expected | PASS | offsets=[0, 1] |
| Clock hour is between 0 and 23 | PASS |  |
| Time-period labels are valid | PASS | periods=['Evening', 'Evening Peak', 'Midday', 'Morning Peak', 'Overnight'] |
| Schedule lateness is non-negative | PASS |  |
| Excess Late Tax is non-negative | PASS |  |
| Excess Late Tax does not exceed schedule lateness | PASS | errors=0 |
| Route baselines are consistent | PASS | errors=0 |
| Route baseline sample sizes are consistent | PASS | errors=0 |
| Baseline reliability flags are correct | PASS | errors=0 |
| 5-minute delay flags are correct | PASS | errors=0 |
| 10-minute severe-delay flags are correct | PASS | errors=0 |