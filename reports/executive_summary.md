# Late Tax — Executive Summary

## Business Problem

Transit reliability is often summarized using average delay or on-time performance, but these metrics can hide where repeated lateness creates the largest operational burden.

The Late Tax project evaluates where excess schedule delay is concentrated across routes and time periods and converts those findings into an operational prioritization framework.

The core business question is:

> Where should reliability improvement efforts be prioritized to address the largest share of measured excess delay burden?

---

## Data Scope

The analytical dataset contains:

- 1,813 observed trips
- 313 service days
- Coverage from June 3, 2025 through August 31, 2026
- Four northbound route groups: Yellow-N, Green-N, Blue-N, and Red-N
- 19 route × time-period analytical groups

Across the full dataset:

- 121 trips were classified as late
- Overall late-trip rate: 6.67%
- Total measured excess Late Tax: 1,222.38 minutes

A trip is classified as late when arrival delay is at least 5 minutes.

Late Tax measures excess observed delay relative to each route's typical median delay:

`max(arrival_delay_min - route_baseline_delay_min, 0)`

Late Tax therefore represents excess delay burden rather than direct monetary cost.

---

## Executive Findings

### 1. Late Tax is highly concentrated rather than system-wide

A small number of route × time-period groups account for most measured excess delay.

The three largest contributors account for approximately 84.57% of total Late Tax, while the top five account for approximately 92.74%.

This means only 3 of the 19 route × time-period groups are required to exceed 80% of measured Late Tax.

The operational problem is therefore concentrated enough to support targeted intervention rather than system-wide action.

### 2. Yellow-N Overnight is the dominant operational hotspot

Yellow-N Overnight contains:

- 335 observed trips
- 88 late trips
- 26.27% late-trip rate
- 834.58 excess Late Tax minutes
- 68.28% of total measured Late Tax
- Priority score: 95.71
- Reliability segment: Chronic
- Priority tier: P1 — Primary Hotspot

Yellow-N Overnight alone accounts for more than two-thirds of all measured Late Tax.

Its operational importance is driven primarily by recurrence and cumulative burden rather than a small number of extreme-delay events.

### 3. Overnight service is not universally unreliable

Overnight observations account for approximately 74.17% of total Late Tax, but the burden is not evenly distributed across overnight routes.

Yellow-N Overnight contributes approximately 92.06% of all Overnight Late Tax.

By comparison:

- Green-N Overnight late-trip rate: 2.76%
- Blue-N Overnight late-trip rate: 0.00%

The appropriate conclusion is therefore not that overnight service is generally unreliable.

The evidence supports a narrower finding: excess-delay burden is disproportionately concentrated in Yellow-N Overnight.

### 4. Severity alone is not sufficient for prioritization

Yellow-N Evening demonstrates why operational decisions should not rely on a single delay metric.

Its average late-trip severity is approximately 24 minutes and it is classified as Critical, but it contributes only approximately 1.84% of total Late Tax.

In contrast, Yellow-N Overnight has lower average late-trip severity but contributes 68.28% of total Late Tax because delays occur much more frequently across a substantially larger observed sample.

Operational prioritization should therefore combine:

- Delay burden
- Delay frequency
- Delay severity
- Sample size

rather than ranking segments using severity alone.

### 5. Green-N Midday represents a different type of reliability risk

Green-N Midday is the second-largest Late Tax contributor:

- 266 observed trips
- 4.51% late-trip rate
- Approximately 10.34-minute average late-trip severity
- 10.51% of total Late Tax
- Priority score: 91.07
- Reliability segment: Critical
- Priority tier: P1 — Primary Hotspot

Unlike Yellow-N Overnight, its priority is driven more strongly by delay severity.

This illustrates why reliability problems should be segmented rather than treated as one uniform operational issue.

---

## Operational Priorities

### Priority 1 — Investigate Yellow-N Overnight

Yellow-N Overnight should receive the highest operational attention because it represents the largest combination of recurrence and aggregate excess-delay burden.

Potential investigation areas include:

- Terminal departure discipline
- Schedule recovery time
- Overnight operator transitions
- Recurrent operational bottlenecks
- Schedule padding or timetable feasibility
- Conditions affecting post-midnight service

The analysis identifies where investigation should be focused but does not establish the underlying cause.

### Priority 2 — Investigate Green-N Midday

Green-N Midday combines meaningful aggregate Late Tax with relatively high delay severity.

The operational objective should be to identify whether severe delays are associated with recurring service conditions, specific departure windows, or other identifiable operational patterns.

### Priority 3 — Maintain targeted monitoring

Green-N Overnight and Blue-N Evening should remain on the reliability watch list because they contribute meaningful Late Tax burden despite being less dominant than the primary hotspots.

Lower-volume groups should continue to be monitored but should not be prioritized using unstable percentages when sample sizes are insufficient.

---

## Decision Metrics

Operational monitoring should track multiple measures together:

- Late Trip %
- Total Late Tax Minutes
- Late Tax Share %
- Average Late Severity
- P95 Lateness
- Trip Volume
- Reliability Segment
- Operational Priority Score

No single metric should independently determine operational priority.

---

## Analytical Guardrails

The analysis is descriptive and does not establish causality.

Observed route and time-period coverage is uneven, so minimum-sample thresholds are used to reduce unstable comparisons.

Groups with fewer than 30 observed trips are classified as `Insufficient Sample` for operational prioritization.

Service-day and post-midnight time semantics were separately audited during earlier project phases to reduce the risk of misinterpreting overnight observations.

The operational priority score is a transparent decision-support heuristic:

- 60% Late Tax burden
- 25% late frequency
- 15% late severity

These weights reflect this project's objective of prioritizing aggregate excess-delay burden. Different operational objectives could justify different weighting schemes.

---

## Business Conclusion

The Late Tax analysis shows that reliability burden is not evenly distributed across the system.

Approximately 84.57% of measured Late Tax is concentrated in only three route × time-period groups, with Yellow-N Overnight alone contributing 68.28%.

This concentration creates a practical decision opportunity: rather than treating all routes and service periods equally, operations teams can focus investigation and reliability-improvement resources on a small number of high-burden segments.

The project converts raw schedule-performance data into a reproducible analytical pipeline, SQL reliability layer, operational prioritization framework, and Power BI semantic model designed to support that decision.
