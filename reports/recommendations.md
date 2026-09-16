# Late Tax — Operational Recommendations

## Objective

Translate the Late Tax findings into a focused operational action plan.

The recommendations prioritize route × time-period groups where reliability interventions could address the largest measured excess-delay burden while accounting for frequency, severity, and sample size.

---

## Recommendation 1 — Prioritize Yellow-N Overnight Investigation

### Observation

Yellow-N Overnight is the dominant operational hotspot in the dataset.

### Evidence

- 335 observed trips
- 88 late trips
- 26.27% late-trip rate
- 834.58 excess Late Tax minutes
- 68.28% of total Late Tax
- Priority score: 95.71
- Reliability segment: Chronic
- Priority tier: P1 — Primary Hotspot

### Business Implication

The largest opportunity for reducing measured excess-delay burden is concentrated in one specific route × time-period combination.

The issue appears to be driven more by recurring lateness than by isolated extreme-delay events.

### Recommended Action

Conduct a targeted operational review of Yellow-N Overnight service.

Investigation should examine:

- Scheduled versus actual terminal departure timing
- Overnight schedule recovery time
- Operator transition or shift-change effects
- Recurring post-midnight bottlenecks
- Schedule feasibility
- Potential timetable padding needs
- Repeated delay patterns within specific departure windows

### Metrics to Monitor

- Late Trip %
- Total Late Tax Minutes
- Late Tax Share %
- Average Late Severity
- P95 Lateness
- Trip Volume

### Success Signal

A sustained decline in Yellow-N Overnight Late Tax share and late-trip frequency without deterioration in other service periods.

---

## Recommendation 2 — Investigate High-Severity Green-N Midday Delays

### Observation

Green-N Midday is the second-highest operational priority and represents a different reliability pattern from Yellow-N Overnight.

### Evidence

- 266 observed trips
- 12 late trips
- 4.51% late-trip rate
- Approximately 10.34-minute average late-trip severity
- 128.42 excess Late Tax minutes
- 10.51% of total Late Tax
- Priority score: 91.07
- Reliability segment: Critical
- Priority tier: P1 — Primary Hotspot

### Business Implication

Green-N Midday does not experience lateness as frequently as Yellow-N Overnight, but when delays occur they tend to be more severe.

This suggests that frequency reduction alone may not be the appropriate operational objective.

### Recommended Action

Investigate whether severe Green-N Midday delays cluster around:

- Specific scheduled departures
- Particular weekdays
- Recurring service windows
- Operational disruptions
- Vehicle or operator availability
- Schedule recovery constraints

### Metrics to Monitor

- Average Late Severity
- P95 Lateness
- Late Trip %
- Late Tax Minutes
- Severe-delay trip count

### Success Signal

Reduction in high-severity delay events and P95 lateness while maintaining or improving the overall late-trip rate.

---

## Recommendation 3 — Maintain Watch Status for Secondary Hotspots

### Observation

Green-N Overnight and Blue-N Evening contribute meaningful Late Tax burden but are substantially less dominant than the two primary hotspots.

### Evidence

Green-N Overnight:

- 181 observed trips
- 2.76% late-trip rate
- 5.79% of total Late Tax
- Priority score: 76.07
- Priority tier: P1 — Primary Hotspot

Blue-N Evening:

- 5.12% of total Late Tax
- 2.91% late-trip rate
- Priority score: 73.21
- Priority tier: P2 — High Burden

### Business Implication

These segments warrant monitoring, but operational resources should not be diverted away from higher-burden segments unless their performance deteriorates.

### Recommended Action

Maintain these segments on the operational watch list and trigger deeper investigation if:

- Late Tax share increases materially
- Late-trip rate rises across multiple periods
- P95 lateness deteriorates
- Trip volume grows while reliability declines

### Metrics to Monitor

- Late Tax Share %
- Late Trip %
- P95 Lateness
- Priority Score
- Rolling monthly trend

---

## Recommendation 4 — Do Not Prioritize Using Severity Alone

### Observation

Some segments show extreme individual delays but contribute little to total system burden.

Yellow-N Evening is an example.

### Evidence

Yellow-N Evening has:

- Approximately 24-minute average late-trip severity
- Critical reliability classification
- Only approximately 1.84% of total Late Tax

### Business Implication

Ranking operational problems using average delay severity alone can over-prioritize low-frequency events and under-prioritize recurring moderate delays.

### Recommended Action

Use a multi-metric prioritization framework that combines:

- 60% Late Tax burden
- 25% late frequency
- 15% late severity

Retain minimum-sample safeguards when comparing route-period groups.

### Metrics to Monitor

- Late Tax Share %
- Late Trip %
- Average Late Severity
- Trip Volume
- Priority Score

---

## Recommendation 5 — Preserve Sample-Size Guardrails

### Observation

Route and time-period coverage is uneven.

Some groups contain too few trips to support stable operational conclusions.

### Evidence

The Week 5 framework classifies groups with fewer than 30 observed trips as:

`Insufficient Sample`

### Business Implication

Small samples can create misleading percentages and exaggerated rankings.

For example, a group with only a few observed trips can appear highly unreliable after one delayed trip.

### Recommended Action

Continue applying minimum-sample thresholds before assigning operational priority.

Use low-volume groups for monitoring and data-collection improvement rather than immediate intervention decisions.

### Metrics to Monitor

- Trip Volume
- Coverage by route
- Coverage by month
- Coverage by time period

---

## Recommended Operating Framework

Operational review should follow this sequence:

1. Identify high Late Tax burden
2. Evaluate delay frequency
3. Evaluate delay severity
4. Confirm sufficient sample size
5. Assign operational priority
6. Investigate root causes
7. Monitor post-intervention performance

This framework separates analytical prioritization from causal diagnosis.

The current analysis identifies where operational attention should be focused, but additional operational data would be required to determine why those reliability problems occur.

---

## Decision Summary

The recommended priority order is:

1. Yellow-N Overnight — highest immediate investigation priority
2. Green-N Midday — high-severity primary hotspot
3. Green-N Overnight — continued targeted monitoring
4. Blue-N Evening — high-burden watch segment
5. Remaining segments — monitor according to sample size and trend changes

The most important decision principle is that operational attention should be allocated based on cumulative burden, recurrence, severity, and data reliability together rather than any single delay metric.
