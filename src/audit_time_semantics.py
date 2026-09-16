import csv
from collections import Counter
from datetime import datetime, timedelta
from pathlib import Path
from statistics import median

INPUT_FILE = Path("data/processed/late_tax_analytics.csv")
REPORT_FILE = Path("reports/time_semantics_audit.md")

with INPUT_FILE.open(newline="") as f:
    rows = list(csv.DictReader(f))

after_midnight_rows = []
day_offset_counts = Counter()
actual_weekday_counts = Counter()

delays = []

for row in rows:
    scheduled_sec = float(row["scheduled_departure_sec"])

    day_offset = int(scheduled_sec // 86400)

    service_date = datetime.strptime(
        row["service_date"],
        "%Y-%m-%d",
    ).date()

    actual_date = service_date + timedelta(days=day_offset)

    day_offset_counts[day_offset] += 1
    actual_weekday_counts[actual_date.strftime("%A")] += 1

    if day_offset > 0:
        after_midnight_rows.append(row)

    delays.append(float(row["arrival_delay_min"]))

delays_sorted = sorted(delays)

def percentile(values, p):
    index = int((len(values) - 1) * p)
    return values[index]

lines = [
    "# Week 2 — Time Semantics Audit",
    "",
    f"- Total rows: {len(rows):,}",
    f"- Rows with GTFS time >= 24:00: {len(after_midnight_rows):,}",
    f"- Share >= 24:00: {len(after_midnight_rows) / len(rows):.1%}",
    "",
    "## Service-Day Offset",
    "",
    "| Day Offset | Rows |",
    "|---:|---:|",
]

for offset, count in sorted(day_offset_counts.items()):
    lines.append(f"| {offset} | {count} |")

lines += [
    "",
    "## Arrival Delay Distribution",
    "",
    f"- Minimum: {min(delays):.2f} min",
    f"- Median: {median(delays):.2f} min",
    f"- 95th percentile: {percentile(delays_sorted, 0.95):.2f} min",
    f"- Maximum: {max(delays):.2f} min",
    "",
    "## Interpretation",
    "",
    "GTFS times at or above 24:00 belong to the following "
    "calendar day even though they remain associated with the "
    "previous GTFS service_date.",
    "",
    "Feature engineering should therefore preserve service_date "
    "while also creating an adjusted calendar_date and "
    "calendar_day_of_week for time-of-day analysis.",
]

REPORT_FILE.write_text(
    "\n".join(lines),
    encoding="utf-8",
)

print(f"Report saved to: {REPORT_FILE}")
