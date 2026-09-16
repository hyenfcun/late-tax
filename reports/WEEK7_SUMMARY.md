# Week 7 — Executive Insights, Architecture, and Final Validation

## Objective

Convert the completed Late Tax analysis and Power BI implementation into a recruiter-ready decision-support package with executive findings, operational recommendations, architecture documentation, and reproducible final validation.

## Executive Findings

The analysis covers:

- 1,813 observed trips
- 121 late trips
- 6.67% overall late-trip rate
- 1,222.38 minutes of measured excess Late Tax
- 19 route × time-period groups

The primary finding is strong concentration of excess-delay burden.

Yellow-N Overnight is the dominant operational hotspot:

- 335 observed trips
- 88 late trips
- 26.27% late-trip rate
- 834.58 Late Tax minutes
- 68.28% of total Late Tax

The top three route × time-period groups account for approximately 84.57% of total measured Late Tax.

This supports targeted operational investigation rather than treating reliability as a uniform system-wide problem.

## Business Recommendations

Week 7 translated the analytical findings into an operational decision framework.

Primary recommendations include:

1. Prioritize Yellow-N Overnight for operational investigation.
2. Investigate high-severity Green-N Midday delays separately from recurring-delay hotspots.
3. Maintain targeted monitoring for secondary hotspots.
4. Avoid prioritizing segments using severity alone.
5. Preserve sample-size guardrails when comparing operational segments.

The recommendations distinguish analytical prioritization from causal diagnosis.

## Analytics Architecture

The project architecture documents the end-to-end workflow:

511 SF Bay transit data  
→ Python data collection  
→ data quality and time-semantics validation  
→ feature engineering  
→ canonical trip-level analytics dataset  
→ DuckDB SQL analytics  
→ reliability segmentation  
→ operational prioritization  
→ BI dataset preparation  
→ Power BI semantic model  
→ dashboard  
→ business recommendations

The analytical grain is one observed scheduled trip on one service date.

The validated composite trip key is:

`service_date + trip_id`

## Final Validation

A project-level validation script was added:

`src/validate_project.py`

The script validates:

- analytics dataset availability
- expected row count
- required schema
- composite trip-key uniqueness
- late-trip definition
- non-negative Late Tax
- headline KPI reconciliation
- route coverage
- Yellow-N Overnight benchmark metrics
- BI dataset availability
- Power BI evidence
- Week 7 portfolio artifacts

Final result:

- 21 checks passed
- 0 checks failed
- ALL VALIDATION CHECKS PASSED

The validation output is saved to:

`reports/final_validation.txt`

## Week 7 Deliverables

- `docs/architecture.md`
- `reports/executive_summary.md`
- `reports/recommendations.md`
- `reports/final_validation.txt`
- `reports/WEEK7_SUMMARY.md`
- `src/validate_project.py`

## Skills Demonstrated

- Python
- Pandas
- DuckDB / SQL
- Data validation
- Data quality auditing
- Feature engineering
- Analytical data modeling
- Composite-key / grain validation
- Operational KPI design
- Reliability segmentation
- Decision-support scoring
- Power BI
- DAX
- Star-schema semantic modeling
- Business recommendation development
- Reproducible analytics workflows

## Status

Week 7 completed.

The analytical pipeline, operational prioritization framework, Power BI implementation, executive findings, and final validation are ready for final portfolio packaging.
