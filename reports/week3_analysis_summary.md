# Week 3 — Late Tax Pattern Investigation

## Objective

Investigate the reliability patterns identified in the analytical dataset, validate unusual findings, and determine whether observed Late Tax concentrations represent meaningful patterns or data/time-semantics artifacts.

## Analysis Performed

Week 3 extended the validated analytical dataset through:

- Late Tax pattern analysis
- Route-level reliability investigation
- Time-period analysis
- Post-midnight service-day investigation
- GTFS-style time semantics validation
- Targeted validation of the midnight reliability finding

## Key Finding

The analysis identified an unusually high Late Tax concentration associated with Yellow-N observations during the overnight period.

Rather than treating the pattern as an immediate operational conclusion, the project investigated whether it could be explained by service-day boundaries, post-midnight timestamps, or other time-semantics issues.

## Validation Approach

The investigation separated the target Yellow-N post-midnight pattern from:

- other Yellow-N midnight observations
- Yellow-N non-midnight observations
- non-target route observations

This allowed the unusual pattern to be tested against relevant comparison groups rather than relying only on aggregate averages.

## Interpretation

The Yellow-N overnight pattern remained analytically important after targeted validation.

However, the result is treated as a reliability pattern requiring further investigation rather than proof of a specific operational cause.

This distinction is important because transit schedule data can contain service-day and post-midnight semantics that make apparently simple clock-time comparisons misleading.

## Week 3 Outcome

Week 3 moved the project from descriptive KPI analysis into hypothesis-driven investigation and validation.

The validated pattern became the basis for the SQL segmentation and route-by-time-period analysis developed in Week 4.

## Related Reports

- `late_tax_patterns.md`
- `midnight_reliability_investigation.md`
- `midnight_finding_validation.md`
- `time_semantics_audit.md`
