# Week 4 — SQL Reliability Analysis

## Objective

Build a reproducible SQL analytics layer on top of the Late Tax analytical dataset and identify where schedule-related delay burden is concentrated across routes and time periods.

## Dataset Coverage

- 1,813 observed trips
- 313 service days
- Coverage: June 3, 2025 through August 31, 2026
- Routes represented: Yellow-N, Green-N, Blue-N, and Red-N

Coverage is uneven across routes and months, so small route-month samples are not treated as equally reliable comparisons.

## Core Reliability KPIs

Across the analytical dataset:

- Average schedule lateness: 1.78 minutes
- Median schedule lateness: 1.12 minutes
- 90th percentile schedule lateness: 3.90 minutes
- Late-trip rate: 6.67%
- Severe-delay trips: 16
- Total excess Late Tax: 1,222.38 minutes

The mean exceeds the median, indicating that higher-delay observations increase the overall average and motivating analysis beyond a single mean metric.

## Route-Level Findings

Yellow-N is the largest contributor to measured excess Late Tax:

- 647 observed trips
- 2.64-minute average schedule lateness
- 5.70-minute P90 schedule lateness
- 13.76% late-trip rate
- 862.43 excess Late Tax minutes

Green-N contributed 269.05 excess minutes and Blue-N contributed 82.20.

Red-N contained only seven observations across the full dataset and is therefore not treated as directly comparable to the higher-volume routes.

## Time-Period Findings

Overnight service accounted for:

- 580 observed trips
- 16.03% late-trip rate
- 906.60 excess Late Tax minutes
- 74.17% of total measured excess Late Tax

By comparison:

- Morning Peak late-trip rate: 1.95%
- Evening Peak late-trip rate: 1.68%

However, the overnight result should not be interpreted as evidence that overnight service is broadly unreliable. Route-by-time-period analysis shows that the measured burden is highly concentrated.

## Route × Time-Period Concentration

Yellow-N Overnight is the dominant route-time combination:

- 335 observed trips
- 3.93-minute average schedule lateness
- 26.27% late-trip rate
- 834.58 excess Late Tax minutes
- 92.06% of all Overnight excess Late Tax

This combination alone represents approximately 68.3% of total excess Late Tax in the analytical dataset.

The concentration is not replicated across the other overnight routes:

- Green-N Overnight: 2.76% late-trip rate
- Blue-N Overnight: 0.00% late-trip rate

The evidence therefore supports a more specific finding: measured Late Tax is concentrated in the Yellow-N Overnight segment rather than across overnight observations generally.

## Monthly Ranking Method

Monthly route reliability was evaluated using CTEs and SQL window functions.

Because route-month sample sizes vary substantially, rankings are assigned only when a route-month contains at least 20 observed trips. Smaller groups remain visible in the analytical output but are not assigned reliability ranks.

This prevents very small samples from producing misleading rankings.

## SQL Techniques Used

The analytical layer demonstrates:

- CTEs
- conditional aggregation
- GROUP BY analysis
- median and percentile calculations
- window functions
- partitioned ranking
- cumulative contribution analysis
- route/time segmentation
- sample-size eligibility logic

## Interpretation and Limitations

The analysis identifies concentration patterns, not causal explanations.

Observed coverage varies across routes and months, and some route-month combinations contain limited samples. In addition, service-day and post-midnight time semantics require careful handling, as documented in the project's earlier validation work.

For these reasons, the Yellow-N Overnight result should be treated as a validated analytical pattern and a candidate for further operational investigation rather than proof of a specific underlying cause.

## Week 4 Outcome

Week 4 added a reproducible SQL analytics layer to the existing Python-based pipeline and translated the analytical dataset into reliability KPIs, route comparisons, temporal analysis, and route-time concentration findings.

The primary finding for downstream BI work is the disproportionate concentration of measured excess Late Tax in the Yellow-N Overnight segment.
