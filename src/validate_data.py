import csv
from collections import Counter
from pathlib import Path

# -----------------------------
# File paths
# -----------------------------
MASTER_FILE = Path("data/processed/daly_powell_all_v2.csv")
MONTHLY_FILES = sorted(Path("data/processed").glob("daly_powell_v2_*.csv"))
REPORT_FILE = Path("reports/data_quality_report.txt")

report = []


def log(text=""):
    print(text)
    report.append(str(text))


# -----------------------------
# Load master dataset
# -----------------------------
with MASTER_FILE.open(newline="") as f:
    rows = list(csv.DictReader(f))
    master_columns = list(rows[0].keys())

log("LATE TAX - DATA QUALITY REPORT")
log("=" * 40)

log(f"Master file: {MASTER_FILE}")
log(f"Total rows: {len(rows)}")
log(f"Total columns: {len(master_columns)}")
log(f"Monthly files: {len(MONTHLY_FILES)}")


# -----------------------------
# 1. Schema validation
# -----------------------------
schema_errors = 0

for file in MONTHLY_FILES:
    with file.open(newline="") as f:
        reader = csv.reader(f)
        header = next(reader)

    if header != master_columns:
        schema_errors += 1

log()
log("1. SCHEMA VALIDATION")
log(f"Schema mismatches: {schema_errors}")
log("Status: PASS" if schema_errors == 0 else "Status: REVIEW")


# -----------------------------
# 2. Exact duplicate rows
# -----------------------------
exact_rows = [tuple(row.values()) for row in rows]
exact_duplicates = len(exact_rows) - len(set(exact_rows))

log()
log("2. EXACT DUPLICATES")
log(f"Exact duplicate rows: {exact_duplicates}")
log("Status: PASS" if exact_duplicates == 0 else "Status: REVIEW")


# -----------------------------
# 3. trip_id reuse
# -----------------------------
trip_ids = [row["trip_id"] for row in rows]
trip_counts = Counter(trip_ids)

repeated_trip_ids = sum(1 for count in trip_counts.values() if count > 1)
extra_trip_id_occurrences = len(trip_ids) - len(set(trip_ids))

log()
log("3. TRIP ID CHECK")
log(f"Repeated trip_id values: {repeated_trip_ids}")
log(f"Extra trip_id occurrences: {extra_trip_id_occurrences}")
log("Note: trip_id may repeat across different service dates.")


# -----------------------------
# 4. Composite key validation
# -----------------------------
composite_keys = [
    (row["trip_id"], row["service_date"])
    for row in rows
]

duplicate_composite_keys = (
    len(composite_keys) - len(set(composite_keys))
)

log()
log("4. COMPOSITE KEY")
log("Key: trip_id + service_date")
log(f"Duplicate composite keys: {duplicate_composite_keys}")
log(
    "Status: PASS"
    if duplicate_composite_keys == 0
    else "Status: REVIEW"
)


# -----------------------------
# 5. Missing values
# -----------------------------
log()
log("5. MISSING VALUES")

total_missing = 0

for col in master_columns:
    missing = sum(
        1
        for row in rows
        if row[col] is None or row[col].strip() == ""
    )

    total_missing += missing
    log(f"{col}: {missing}")

log(f"Total missing values: {total_missing}")
log("Status: PASS" if total_missing == 0 else "Status: REVIEW")


# -----------------------------
# 6. Numeric sanity checks
# -----------------------------
numeric_cols = [
    "scheduled_travel_min",
    "observed_travel_min",
    "arrival_delay_min",
    "departure_delay_min",
    "travel_time_delta_min",
]

log()
log("6. NUMERIC SANITY CHECKS")

for col in numeric_cols:
    values = [float(row[col]) for row in rows]

    log()
    log(col)
    log(f"min: {min(values)}")
    log(f"max: {max(values)}")
    log(f"negative count: {sum(v < 0 for v in values)}")
    log(f"zero count: {sum(v == 0 for v in values)}")


# -----------------------------
# 7. Formula validation
# -----------------------------
travel_formula_errors = 0
delay_formula_errors = 0

for row in rows:
    scheduled = float(row["scheduled_travel_min"])
    observed = float(row["observed_travel_min"])
    travel_delta = float(row["travel_time_delta_min"])

    arrival_delay = float(row["arrival_delay_min"])
    departure_delay = float(row["departure_delay_min"])

    if abs((observed - scheduled) - travel_delta) > 0.01:
        travel_formula_errors += 1

    if abs((arrival_delay - departure_delay) - travel_delta) > 0.01:
        delay_formula_errors += 1

log()
log("7. FORMULA VALIDATION")
log(f"Travel-time formula errors: {travel_formula_errors}")
log(f"Delay formula errors: {delay_formula_errors}")

if travel_formula_errors == 0 and delay_formula_errors == 0:
    log("Status: PASS")
else:
    log("Status: REVIEW")


# -----------------------------
# Save report
# -----------------------------
REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)

REPORT_FILE.write_text(
    "\n".join(report),
    encoding="utf-8"
)

log()
log(f"Report saved to: {REPORT_FILE}")


