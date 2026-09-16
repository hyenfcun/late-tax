import csv
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from statistics import median

INPUT_FILE = Path("data/processed/daly_powell_all_v2.csv")
OUTPUT_FILE = Path("data/processed/late_tax_analytics.csv")
REPORT_FILE = Path("reports/feature_summary.md")


def get_time_period(hour):
    if 7 <= hour < 10:
        return "Morning Peak"
    elif 10 <= hour < 16:
        return "Midday"
    elif 16 <= hour < 19:
        return "Evening Peak"
    elif 19 <= hour < 24:
        return "Evening"
    else:
        return "Overnight"


with INPUT_FILE.open(newline="") as f:
    rows = list(csv.DictReader(f))


# --------------------------------
# Route baseline lateness
# --------------------------------
route_delay_values = defaultdict(list)

for row in rows:
    route_delay_values[row["route_id"]].append(
        float(row["arrival_delay_min"])
    )

route_baselines = {
    route: median(values)
    for route, values in route_delay_values.items()
}

route_counts = {
    route: len(values)
    for route, values in route_delay_values.items()
}


# --------------------------------
# Feature engineering
# --------------------------------
output_rows = []

for row in rows:
    service_date = datetime.strptime(
        row["service_date"],
        "%Y-%m-%d",
    ).date()

    scheduled_sec = float(
        row["scheduled_departure_sec"]
    )

    service_day_offset = int(
        scheduled_sec // 86400
    )

    calendar_date = (
        service_date
        + timedelta(days=service_day_offset)
    )

    scheduled_clock_hour = int(
        (scheduled_sec % 86400) // 3600
    )

    arrival_delay = float(
        row["arrival_delay_min"]
    )

    route = row["route_id"]

    route_baseline = route_baselines[route]

    schedule_lateness = max(
        arrival_delay,
        0,
    )

    excess_late_tax = max(
        arrival_delay - route_baseline,
        0,
    )

    new_row = dict(row)

    new_row["service_day_of_week"] = (
        service_date.strftime("%A")
    )

    new_row["service_day_offset"] = (
        service_day_offset
    )

    new_row["calendar_date"] = (
        calendar_date.isoformat()
    )

    new_row["calendar_day_of_week"] = (
        calendar_date.strftime("%A")
    )

    new_row["calendar_year_month"] = (
        calendar_date.strftime("%Y-%m")
    )

    new_row["scheduled_clock_hour"] = (
        scheduled_clock_hour
    )

    new_row["time_period"] = get_time_period(
        scheduled_clock_hour
    )

    new_row["is_morning_peak"] = int(
        7 <= scheduled_clock_hour < 10
    )

    new_row["is_evening_peak"] = int(
        16 <= scheduled_clock_hour < 19
    )

    new_row["schedule_lateness_min"] = round(
        schedule_lateness,
        4,
    )

    new_row["route_baseline_delay_min"] = round(
        route_baseline,
        4,
    )

    new_row["route_baseline_sample_size"] = (
        route_counts[route]
    )

    new_row["baseline_reliable_flag"] = int(
        route_counts[route] >= 30
    )

    new_row["excess_late_tax_min"] = round(
        excess_late_tax,
        4,
    )

    new_row["late_trip_flag"] = int(
        arrival_delay >= 5
    )

    new_row["severe_delay_flag"] = int(
        arrival_delay >= 10
    )

    output_rows.append(new_row)


fieldnames = list(output_rows[0].keys())

with OUTPUT_FILE.open(
    "w",
    newline="",
) as f:
    writer = csv.DictWriter(
        f,
        fieldnames=fieldnames,
    )

    writer.writeheader()
    writer.writerows(output_rows)


# --------------------------------
# Summary metrics
# --------------------------------
avg_schedule_lateness = sum(
    float(r["schedule_lateness_min"])
    for r in output_rows
) / len(output_rows)

avg_excess_late_tax = sum(
    float(r["excess_late_tax_min"])
    for r in output_rows
) / len(output_rows)

affected_trips = sum(
    float(r["excess_late_tax_min"]) > 0
    for r in output_rows
)

period_counts = defaultdict(int)

for row in output_rows:
    period_counts[row["time_period"]] += 1


lines = [
    "# Week 2 — Feature Engineering Summary",
    "",
    f"- Analytical rows: {len(output_rows):,}",
    f"- Analytical columns: {len(fieldnames)}",
    f"- Average schedule lateness: "
    f"{avg_schedule_lateness:.2f} min",
    f"- Average Excess Late Tax: "
    f"{avg_excess_late_tax:.2f} min",
    f"- Trips above route baseline: "
    f"{affected_trips:,} "
    f"({affected_trips / len(output_rows):.1%})",
    "",
    "## Route Baselines",
    "",
    "| Route | Median Baseline (min) | Rows | Reliable |",
    "|---|---:|---:|---|",
]

for route in sorted(route_baselines):
    count = route_counts[route]

    lines.append(
        f"| {route} "
        f"| {route_baselines[route]:.2f} "
        f"| {count:,} "
        f"| {'Yes' if count >= 30 else 'No'} |"
    )

lines += [
    "",
    "## Metric Definitions",
    "",
    "### Schedule Lateness",
    "",
    "`schedule_lateness_min = "
    "max(arrival_delay_min, 0)`",
    "",
    "Minutes arriving at Powell later than scheduled.",
    "",
    "### Excess Late Tax",
    "",
    "`excess_late_tax_min = "
    "max(arrival_delay_min - route_baseline_delay_min, 0)`",
    "",
    "Minutes of lateness above the typical median lateness "
    "for the same route.",
    "",
    "Route baselines with fewer than 30 observations are "
    "flagged as unreliable and should not drive route-level conclusions.",
]

REPORT_FILE.write_text(
    "\n".join(lines),
    encoding="utf-8",
)

print("Feature engineering complete.")
print(f"Rows: {len(output_rows):,}")
print(f"Columns: {len(fieldnames)}")
print(
    f"Average schedule lateness: "
    f"{avg_schedule_lateness:.2f} min"
)
print(
    f"Average Excess Late Tax: "
    f"{avg_excess_late_tax:.2f} min"
)
print(f"Analytics file: {OUTPUT_FILE}")
print(f"Report: {REPORT_FILE}")

