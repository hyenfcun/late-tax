# Week 1 — Data Acquisition Pipeline

## Objective

Build a reproducible historical transit-data pipeline for the Daly City → Powell Street corridor using 511 SF Bay data.

## Data Coverage

- Date range: 2025-06-03 to 2026-08-17
- Source months: 15
- Master dataset rows: 308
- Columns: 19
- Routes observed: BA:Blue-N, BA:Green-N, BA:Red-N, BA:Yellow-N

## Week 1 Pipeline

1. Check historical data availability
2. Download historical source data
3. Extract Daly City → Powell trips
4. Refine extraction logic
5. Generate monthly processed datasets
6. Combine monthly outputs into a master analytical dataset

## Main Scripts

- `src/check_historical_availability.py`
- `src/download_historical.py`
- `src/extract_daly_powell.py`
- `src/extract_daly_powell_v2.py`

## Output

The final local master dataset is:

`data/processed/daly_powell_all_v2.csv`

Generated/raw datasets are intentionally excluded from GitHub.

A 20-row recruiter-facing sample is available at:

`data/sample/daly_powell_sample.csv`

## Notes

API credentials are stored locally through environment variables and are not committed to version control.
