import csv
from collections import Counter, defaultdict
from pathlib import Path
from statistics import median

INPUT_FILE = Path("data/processed/late_tax_analytics.csv")
REPORT_FILE = Path("reports/delay_baseline_audit.md")

with INPUT_FILE.open(newline="") as f:
    rows = list(csv.DictReader(f))


def percentile(values, p):
    values = sorted(values)
    index = round((len(values) - 1) * p)
    return values[index]


arrival = [float(r["arrival_delay_min"]) for r in rows]
departure = [float(r["departure_delay_min"]) for r in rows]
travel_delta = [float(r["travel_time_delta_min"]) for r in rows]


# -----------------------------
# Distribution statistics
# -----------------------------
def describe(values):
    return {
        "min": min(values),
        "p25": percentile(values, 0.25),
        "median": median(values),
        "p75": percentile(values, 0.75),
        "p95": percentile(values, 0.95),
        "max": max(values),
    }


arrival_stats = describe(arrival)
departure_stats = describe(departure)
travel_stats = describe(travel_delta)


# -----------------------------
# Delay buckets
# -----------------------------
arrival_buckets = {
    "<1 min": sum(v < 1 for v in arrival),
    "1–2 min": sum(1 <= v < 2 for v in arrival),
    "2–5 min": sum(2 <= v < 5 for v in arrival),
    "5–10 min": sum(5 <= v < 10 for v in arrival),
    "10+ min": sum(v >= 10 for v in arrival),
}


# -----------------------------
# Most common delay values
# -----------------------------
rounded_arrival = Counter(
    round(v, 2) for v in arrival
)

common_values = rounded_arrival.most_common(10)


# -----------------------------
# Median delay by route
# -----------------------------
route_values = defaultdict(list)

for r in rows:
    route_values[r["route_id"]].append(
        float(r["arrival_delay_min"])
    )


# -----------------------------
# Median delay by time period
# -----------------------------
period_values = defaultdict(list)

for r in rows:
    period_values[r["time_period"]].append(
        float(r["arrival_delay_min"])
    )


# -----------------------------
# Relationship between departure
# and arrival delay
# -----------------------------
same_within_10sec = sum(
    abs(
        float(r["arrival_delay_min"])
        - float(r["departure_delay_min"])
    ) <= (10 / 60)
    for r in rows
)

same_within_30sec = sum(
    abs(
        float(r["arrival_delay_min"])
        - float(r["departure_delay_min"])
    ) <= 0.5
    for r in rows
)


lines = [
    "# Week 2 — Delay Baseline Audit",
    "",
    f"- Total observations: {len(rows):,}",
    "",
    "## Delay Distribution",
    "",
    "| Metric | Min | P25 | Median | P75 | P95 | Max |",
    "|---|---:|---:|---:|---:|---:|---:|",
    (
        f"| Arrival delay | "
        f"{arrival_stats['min']:.2f} | "
        f"{arrival_stats['p25']:.2f} | "
        f"{arrival_stats['median']:.2f} | "
        f"{arrival_stats['p75']:.2f} | "
        f"{arrival_stats['p95']:.2f} | "
        f"{arrival_stats['max']:.2f} |"
    ),
    (
        f"| Departure delay | "
        f"{departure_stats['min']:.2f} | "
        f"{departure_stats['p25']:.2f} | "
        f"{departure_stats['median']:.2f} | "
        f"{departure_stats['p75']:.2f} | "
        f"{departure_stats['p95']:.2f} | "
        f"{departure_stats['max']:.2f} |"
    ),
    (
        f"| Travel-time delta | "
        f"{travel_stats['min']:.2f} | "
        f"{travel_stats['p25']:.2f} | "
        f"{travel_stats['median']:.2f} | "
        f"{travel_stats['p75']:.2f} | "
        f"{travel_stats['p95']:.2f} | "
        f"{travel_stats['max']:.2f} |"
    ),
    "",
    "## Arrival Delay Buckets",
    "",
    "| Bucket | Trips | Share |",
    "|---|---:|---:|",
]

for bucket, count in arrival_buckets.items():
    lines.append(
        f"| {bucket} | {count:,} | {count / len(rows):.1%} |"
    )

lines += [
    "",
    "## Most Common Arrival Delay Values",
    "",
    "| Delay (min) | Trips |",
    "|---:|---:|",
]

for value, count in common_values:
    lines.append(f"| {value:.2f} | {count:,} |")

lines += [
    "",
    "## Median Arrival Delay by Route",
    "",
    "| Route | Median Delay (min) | Rows |",
    "|---|---:|---:|",
]

for route in sorted(route_values):
    values = route_values[route]
    lines.append(
        f"| {route} | {median(values):.2f} | {len(values):,} |"
    )

lines += [
    "",
    "## Median Arrival Delay by Time Period",
    "",
    "| Time Period | Median Delay (min) | Rows |",
    "|---|---:|---:|",
]

for period in sorted(period_values):
    values = period_values[period]
    lines.append(
        f"| {period} | {median(values):.2f} | {len(values):,} |"
    )

lines += [
    "",
    "## Departure vs Arrival",
    "",
    f"- Arrival and departure delay within 10 seconds: "
    f"{same_within_10sec:,} ({same_within_10sec / len(rows):.1%})",
    f"- Arrival and departure delay within 30 seconds: "
    f"{same_within_30sec:,} ({same_within_30sec / len(rows):.1%})",
    "",
    "## Decision Use",
    "",
    "This audit determines whether raw arrival lateness should be "
    "used directly as Late Tax or adjusted against a systematic "
    "baseline before final KPI construction.",
]

REPORT_FILE.write_text(
    "\n".join(lines),
    encoding="utf-8",
)

print(f"Report saved to: {REPORT_FILE}")
