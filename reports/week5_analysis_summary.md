# Week 5 — Reliability Segmentation and Operational Prioritization

## Objective

Extend the Week 4 reliability analysis into an operational prioritization framework that distinguishes between frequent lateness, severe lateness, and aggregate Late Tax burden.

The goal is not simply to identify the route-period with the largest delay metric, but to determine where reliability interventions could address the greatest measured burden while accounting for sample size and recurrence.

## Dataset

- 1,813 observed trips
- 121 late trips
- Late-trip rate: 6.67%
- Total excess Late Tax: 1,222.38 minutes
- 19 route × time-period groups

The canonical late-trip definition is:

`late_trip_flag = 1 when arrival_delay_min >= 5 minutes`

Excess Late Tax is defined as:

`max(arrival_delay_min - route_baseline_delay_min, 0)`

These metrics measure different concepts. A trip can contribute positive excess Late Tax without being classified as a late trip if it exceeds the route baseline but remains below the 5-minute late threshold.

## Reliability Segmentation

Route × time-period groups were segmented using two dimensions:

- Frequency: late-trip percentage
- Severity: average arrival delay among late trips

The median frequency and severity values across groups were used as dataset-specific high/low cutoffs.

Groups with fewer than 30 observed trips were classified as `Insufficient Sample` and excluded from operational prioritization conclusions.

This prevents small-denominator groups, such as Red-N Morning Peak with only 3 observed trips, from appearing disproportionately important because of unstable percentages.

### Segmentation Results

Eligible groups were classified as:

- Critical: high frequency and high severity
- Chronic: high frequency and lower severity
- Acute: lower frequency and high severity
- Reliable: lower frequency and lower severity
- Insufficient Sample: fewer than 30 trips

Examples:

- Green-N Midday: Critical
- Yellow-N Overnight: Chronic
- Yellow-N Evening: Critical
- Blue-N Midday: Acute

The segmentation demonstrates that high severity alone does not necessarily imply high operational priority.

## Late Tax Concentration

Late Tax burden is highly concentrated across a small number of route × time-period groups.

### Largest Contributors

1. Yellow-N Overnight
   - 335 trips
   - 88 late trips
   - 26.27% late-trip rate
   - 834.58 excess Late Tax minutes
   - 68.28% of total Late Tax

2. Green-N Midday
   - 266 trips
   - 12 late trips
   - 4.51% late-trip rate
   - 128.42 excess Late Tax minutes
   - 10.51% of total Late Tax

3. Green-N Overnight
   - 181 trips
   - 5 late trips
   - 2.76% late-trip rate
   - 70.72 excess Late Tax minutes
   - 5.79% of total Late Tax

Using unrounded Late Tax values, the top three groups account for approximately 84.57% of total measured Late Tax.

The top five groups account for approximately 92.74%.

Only 3 of 19 route × time-period groups are required to exceed 80% of total Late Tax, indicating substantial concentration rather than system-wide uniformity.

## Operational Priority Framework

Operational prioritization combines:

- 60% Late Tax burden
- 25% late frequency
- 15% late severity

The score is a transparent prioritization heuristic, not a statistical or causal model.

Priority tiers were assigned separately from the numeric score:

- P1 — Primary Hotspot
- P2 — High Burden
- P3 — Reliability Watch
- Monitor
- Insufficient Sample

## Primary Operational Priorities

### P1 — Yellow-N Overnight

- 68.28% of total Late Tax
- 26.27% late-trip rate
- Priority score: 95.71
- Reliability segment: Chronic

This is the dominant operational hotspot. Its importance is driven by recurrence and aggregate burden rather than extreme severity on isolated trips.

### P1 — Green-N Midday

- 10.51% of total Late Tax
- 4.51% late-trip rate
- Average late-trip severity: 10.34 minutes
- Priority score: 91.07
- Reliability segment: Critical

This group combines meaningful aggregate burden with relatively high severity.

### P1 — Green-N Overnight

- 5.79% of total Late Tax
- 2.76% late-trip rate
- Priority score: 76.07
- Reliability segment: Chronic

### P2 — Blue-N Evening

- 5.12% of total Late Tax
- 2.91% late-trip rate
- Priority score: 73.21
- Reliability segment: Chronic

## Key Business Finding

Severity alone does not determine operational priority.

For example, Yellow-N Evening has an average late-trip severity of approximately 24 minutes and is classified as Critical, but it contributes only 1.84% of total Late Tax.

In contrast, Yellow-N Overnight has lower average late-trip severity but contributes 68.28% of total Late Tax because lateness occurs much more frequently across a substantially larger number of observed trips.

This demonstrates why operational prioritization should consider recurrence, burden, and sample size together rather than ranking locations using a single delay metric.

## Validation

Week 5 results were independently validated using Python and DuckDB SQL.

Validation confirmed:

- 1,813 total trips
- 121 late trips
- 6.67% late-trip rate
- 1,222.38 total excess Late Tax minutes
- 100% reconciliation of route-period Late Tax shares
- 0 late-trip flag definition mismatches
- Yellow-N Overnight: 335 trips, 88 late trips, 26.27% late-trip rate, 68.28% Late Tax share
- Top-three Late Tax share: approximately 84.57%

All validation checks passed.

## Limitations

The analysis is descriptive and does not establish causality.

Route and time-period coverage is uneven, so minimum-sample guardrails are used to reduce unstable comparisons.

The priority score is a decision-support heuristic whose weights reflect the project objective of reducing aggregate Late Tax burden. Different operational objectives could justify different weights.

Late Tax is measured relative to each route's typical median delay, so it should be interpreted as excess observed lateness rather than direct monetary cost.

## Week 5 Conclusion

Week 5 converts reliability metrics into a structured operational prioritization framework.

The strongest finding is that Late Tax burden is highly concentrated: approximately 84.57% is associated with only three route × time-period groups, led overwhelmingly by Yellow-N Overnight.

This suggests that targeted reliability improvements at a small number of operational hotspots could address a large share of the measured excess-delay burden.
