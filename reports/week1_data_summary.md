# Week 1 — Data Acquisition Pipeline

## Objective

Build a reproducible historical transit-data pipeline for the Daly City → Powell Street corridor using 511 SF Bay data.

## Data Coverage

- Date range: 2025-06-03 to 2026-08-31
- Source months: 15
- Master dataset rows: 1,813
- Columns: 19
- Routes observed: BA:Blue-N, BA:Green-N, BA:Red-N, BA:Yellow-N

## Week 1 Pipeline

1. Check historical data availability
2. Download historical source data
3. Extract Daly City → Powell trips
4. Validate corridor direction using scheduled GTFS stop sequence
5. Preserve weekday observations across the full service day
6. Generate monthly processed datasets
7. Combine monthly outputs into a master analytical dataset

## Main Scripts

- `src/check_historical_availability.py`
- `src/download_historical.py`
- `src/extract_daly_powell.py`
- `src/extract_daly_powell_v2.py`

## Output

The final local master dataset is:

`data/processed/daly_powell_all_v2.csv`

Raw and generated processed datasets are intentionally excluded from GitHub.

A 20-row recruiter-facing sample is available at:

`data/sample/daly_powell_sample.csv`

## Pipeline Refinement

An initial morning-only extraction produced 308 observations across 111 service dates.

A Week 2 coverage audit showed that the 07:00–10:00 filter materially reduced temporal coverage. The extraction pipeline was therefore redesigned to preserve all weekday observations, producing 1,813 trips across 313 GTFS service dates.

Peak-period segmentation is now handled downstream during feature engineering rather than during extraction.

## Notes

API credentials are stored locally through environment variables and are not committed to version control.
