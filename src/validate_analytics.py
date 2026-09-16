import csv
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from statistics import median

MASTER_FILE = Path("data/processed/daly_powell_all_v2.csv")
ANALYTICS_FILE = Path("data/processed/late_tax_analytics.csv")
REPORT_FILE = Path("reports/analytics_quality_report.md")

with MASTER_FILE.open(newline="") as f:
    master = list(csv.DictReader(f))

with ANALYTICS_FILE.open(newline="") as f:
    rows = list(csv.DictReader(f))

checks = []


def check(name, condition, detail=""):
    status = "PASS" if condition else "FAIL"

    checks.append(
        {
            "name": name,
            "status": status,
            "detail": detail,
        }
    )

    print(f"{status}: {name}")


# --------------------------------
# 1. Row preservation
# --------------------------------
check(
    "Row count matches master dataset",
    len(rows) == len(master),
    f"master={len(master)}, analytics={len(rows)}",
)


# --------------------------------
# 2. Composite-key uniqueness
# --------------------------------
keys = [
    (r["trip_id"], r["service_date"])
    for r in rows
]

check(
    "Composite key remains unique",
    len(keys) == len(set(keys)),
    f"duplicate keys={len(keys) - len(set(keys))}",
)


# --------------------------------
# 3. Required engineered columns
# --------------------------------
required = [
    "service_day_of_week",
    "service_day_offset",
    "calendar_date",
    "calendar_day_of_week",
    "calendar_year_month",
    "scheduled_clock_hour",
    "time_period",
    "is_morning_peak",
    "is_evening_peak",
    "schedule_lateness_min",
    "route_baseline_delay_min",
    "route_baseline_sample_size",
    "baseline_reliable_flag",
    "excess_late_tax_min",
    "late_trip_flag",
    "severe_delay_flag",
]

missing_columns = [
    col
    for col in required
    if col not in rows[0]
]

check(
    "All required engineered columns exist",
    len(missing_columns) == 0,
    f"missing={missing_columns}",
)


# --------------------------------
# 4. Missing engineered values
# --------------------------------
missing_values = 0

for row in rows:
    for col in required:
        if row.get(col, "").strip() == "":
            missing_values += 1

check(
    "No missing engineered values",
    missing_values == 0,
    f"missing values={missing_values}",
)


# --------------------------------
# 5. GTFS calendar semantics
# --------------------------------
calendar_errors = 0
offset_values = set()

for row in rows:
    service_date = datetime.strptime(
        row["service_date"],
        "%Y-%m-%d",
    ).date()

    offset = int(
        row["service_day_offset"]
    )

    offset_values.add(offset)

    expected_date = (
        service_date
        + timedelta(days=offset)
    )

    if (
        row["calendar_date"]
        != expected_date.isoformat()
    ):
        calendar_errors += 1

check(
    "Calendar date correctly applies GTFS day offset",
    calendar_errors == 0,
    f"errors={calendar_errors}",
)

check(
    "Service-day offsets are expected",
    offset_values.issubset({0, 1}),
    f"offsets={sorted(offset_values)}",
)


# --------------------------------
# 6. Clock-hour validity
# --------------------------------
hours = [
    int(r["scheduled_clock_hour"])
    for r in rows
]

check(
    "Clock hour is between 0 and 23",
    all(0 <= h <= 23 for h in hours),
)


# --------------------------------
# 7. Time-period validity
# --------------------------------
valid_periods = {
    "Morning Peak",
    "Midday",
    "Evening Peak",
    "Evening",
    "Overnight",
}

periods = {
    r["time_period"]
    for r in rows
}

check(
    "Time-period labels are valid",
    periods.issubset(valid_periods),
    f"periods={sorted(periods)}",
)


# --------------------------------
# 8. Metric non-negativity
# --------------------------------
schedule_lateness = [
    float(r["schedule_lateness_min"])
    for r in rows
]

excess_tax = [
    float(r["excess_late_tax_min"])
    for r in rows
]

check(
    "Schedule lateness is non-negative",
    all(v >= 0 for v in schedule_lateness),
)

check(
    "Excess Late Tax is non-negative",
    all(v >= 0 for v in excess_tax),
)


# --------------------------------
# 9. Excess cannot exceed raw lateness
# --------------------------------
excess_errors = sum(
    float(r["excess_late_tax_min"])
    >
    float(r["schedule_lateness_min"]) + 0.01
    for r in rows
)

check(
    "Excess Late Tax does not exceed schedule lateness",
    excess_errors == 0,
    f"errors={excess_errors}",
)


# --------------------------------
# 10. Route baseline consistency
# --------------------------------
route_values = defaultdict(list)

for row in rows:
    route_values[row["route_id"]].append(
        float(row["arrival_delay_min"])
    )

expected_baselines = {
    route: median(values)
    for route, values in route_values.items()
}

baseline_errors = 0
sample_size_errors = 0
reliable_flag_errors = 0

for row in rows:
    route = row["route_id"]

    expected_baseline = expected_baselines[
        route
    ]

    actual_baseline = float(
        row["route_baseline_delay_min"]
    )

    if abs(
        expected_baseline
        - actual_baseline
    ) > 0.01:
        baseline_errors += 1

    expected_size = len(
        route_values[route]
    )

    if (
        int(row["route_baseline_sample_size"])
        != expected_size
    ):
        sample_size_errors += 1

    expected_flag = int(
        expected_size >= 30
    )

    if (
        int(row["baseline_reliable_flag"])
        != expected_flag
    ):
        reliable_flag_errors += 1


check(
    "Route baselines are consistent",
    baseline_errors == 0,
    f"errors={baseline_errors}",
)

check(
    "Route baseline sample sizes are consistent",
    sample_size_errors == 0,
    f"errors={sample_size_errors}",
)

check(
    "Baseline reliability flags are correct",
    reliable_flag_errors == 0,
    f"errors={reliable_flag_errors}",
)


# --------------------------------
# 11. Delay flags
# --------------------------------
late_flag_errors = 0
severe_flag_errors = 0

for row in rows:
    delay = float(
        row["arrival_delay_min"]
    )

    if int(row["late_trip_flag"]) != int(
        delay >= 5
    ):
        late_flag_errors += 1

    if int(row["severe_delay_flag"]) != int(
        delay >= 10
    ):
        severe_flag_errors += 1


check(
    "5-minute delay flags are correct",
    late_flag_errors == 0,
    f"errors={late_flag_errors}",
)

check(
    "10-minute severe-delay flags are correct",
    severe_flag_errors == 0,
    f"errors={severe_flag_errors}",
)


# --------------------------------
# Final status
# --------------------------------
failed = [
    c
    for c in checks
    if c["status"] == "FAIL"
]

overall_status = (
    "PASS"
    if not failed
    else "FAIL"
)


lines = [
    "# Week 2 — Analytics Dataset QA",
    "",
    f"- Master rows: {len(master):,}",
    f"- Analytics rows: {len(rows):,}",
    f"- Analytics columns: {len(rows[0])}",
    f"- Overall status: **{overall_status}**",
    "",
    "## Validation Results",
    "",
    "| Check | Status | Detail |",
    "|---|---|---|",
]

for c in checks:
    lines.append(
        f"| {c['name']} "
        f"| {c['status']} "
        f"| {c['detail']} |"
    )

REPORT_FILE.write_text(
    "\n".join(lines),
    encoding="utf-8",
)

print()
print(
    f"Overall analytics QA: "
    f"{overall_status}"
)
print(
    f"Report saved to: "
    f"{REPORT_FILE}"
)
