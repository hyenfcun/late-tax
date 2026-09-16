import csv
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from statistics import median

MASTER_FILE = Path("data/processed/daly_powell_all_v2.csv")
REPORT_FILE = Path("reports/coverage_report.md")

with MASTER_FILE.open(newline="") as f:
    rows = list(csv.DictReader(f))

# -----------------------------
# Parse fields
# -----------------------------
for row in rows:
    row["_date"] = datetime.strptime(
        row["service_date"], "%Y-%m-%d"
    ).date()

    row["_hour"] = int(
        row["scheduled_departure"].split(":")[0]
    )

# -----------------------------
# Overall coverage
# -----------------------------
dates = [row["_date"] for row in rows]

start_date = min(dates)
end_date = max(dates)

source_months = sorted(
    set(row["source_month"] for row in rows)
)

unique_service_days = len(set(dates))

# -----------------------------
# Monthly coverage
# -----------------------------
monthly_rows = Counter()
monthly_days = defaultdict(set)

for row in rows:
    month = row["source_month"]

    monthly_rows[month] += 1
    monthly_days[month].add(row["_date"])

monthly_counts = list(monthly_rows.values())
monthly_median = median(monthly_counts)

# Flag unusually sparse months
sparse_threshold = monthly_median * 0.25

# -----------------------------
# Route coverage
# -----------------------------
route_counts = Counter(
    row["route_id"] for row in rows
)

# -----------------------------
# Weekday coverage
# -----------------------------
weekday_order = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]

weekday_counts = Counter(
    row["_date"].strftime("%A")
    for row in rows
)

# -----------------------------
# Hour coverage
# -----------------------------
hour_counts = Counter(
    row["_hour"] for row in rows
)

# -----------------------------
# Create report
# -----------------------------
lines = []

lines.append("# Week 2 — Coverage Audit")
lines.append("")

lines.append("## Overall Coverage")
lines.append("")
lines.append(f"- Total observations: {len(rows)}")
lines.append(f"- Date range: {start_date} to {end_date}")
lines.append(f"- Source months: {len(source_months)}")
lines.append(f"- Unique service days: {unique_service_days}")
lines.append("")

lines.append("## Monthly Coverage")
lines.append("")
lines.append("| Month | Rows | Service Days | Avg Trips / Service Day |")
lines.append("|---|---:|---:|---:|")

for month in source_months:
    row_count = monthly_rows[month]
    day_count = len(monthly_days[month])

    avg = row_count / day_count if day_count else 0

    lines.append(
        f"| {month} | {row_count} | {day_count} | {avg:.2f} |"
    )

lines.append("")
lines.append(f"- Median monthly observations: {monthly_median:.1f}")
lines.append(
    f"- Sparse-month review threshold: < {sparse_threshold:.1f} rows"
)
lines.append("")

sparse_months = [
    month
    for month in source_months
    if monthly_rows[month] < sparse_threshold
]

if sparse_months:
    lines.append(
        "- Months flagged for review: "
        + ", ".join(sparse_months)
    )
else:
    lines.append("- Months flagged for review: None")

lines.append("")

lines.append("## Route Coverage")
lines.append("")
lines.append("| Route | Rows |")
lines.append("|---|---:|")

for route, count in sorted(route_counts.items()):
    lines.append(f"| {route} | {count} |")

lines.append("")

lines.append("## Weekday Coverage")
lines.append("")
lines.append("| Weekday | Rows |")
lines.append("|---|---:|")

for weekday in weekday_order:
    lines.append(
        f"| {weekday} | {weekday_counts.get(weekday, 0)} |"
    )

lines.append("")

lines.append("## Scheduled Departure Hour Coverage")
lines.append("")
lines.append("| Hour | Rows |")
lines.append("|---|---:|")

for hour in sorted(hour_counts):
    lines.append(f"| {hour:02d}:00 | {hour_counts[hour]} |")

lines.append("")
lines.append("## Interpretation")
lines.append("")
lines.append(
    "This audit is used to determine whether the current dataset "
    "has sufficient temporal and route coverage before calculating "
    "the final Late Tax metrics."
)

REPORT_FILE.write_text(
    "\n".join(lines),
    encoding="utf-8"
)

print(f"Coverage audit complete.")
print(f"Report saved to: {REPORT_FILE}")
print()
print(f"Total observations: {len(rows)}")
print(f"Unique service days: {unique_service_days}")
print(f"Source months: {len(source_months)}")
print(f"Median monthly observations: {monthly_median:.1f}")
print(
    "Months flagged for review:",
    ", ".join(sparse_months) if sparse_months else "None"
)
