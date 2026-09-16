import csv
from collections import defaultdict
from pathlib import Path
from statistics import mean, median

INPUT_FILE = Path("data/processed/late_tax_analytics.csv")
REPORT_FILE = Path("reports/kpi_analysis.md")

with INPUT_FILE.open(newline="") as f:
    rows = list(csv.DictReader(f))


def percentile(values, p):
    values = sorted(values)
    index = round((len(values) - 1) * p)
    return values[index]


def summarize(group_rows):
    excess = [
        float(r["excess_late_tax_min"])
        for r in group_rows
    ]

    lateness = [
        float(r["schedule_lateness_min"])
        for r in group_rows
    ]

    departure = [
        float(r["departure_delay_min"])
        for r in group_rows
    ]

    travel_delta = [
        float(r["travel_time_delta_min"])
        for r in group_rows
    ]

    above_baseline = sum(
        v > 0 for v in excess
    )

    return {
        "rows": len(group_rows),
        "avg_excess": mean(excess),
        "median_excess": median(excess),
        "p95_excess": percentile(excess, 0.95),
        "avg_lateness": mean(lateness),
        "avg_departure": mean(departure),
        "avg_travel_delta": mean(travel_delta),
        "above_baseline_share":
            above_baseline / len(group_rows),
    }


def group_by(column):
    groups = defaultdict(list)

    for row in rows:
        groups[row[column]].append(row)

    return groups


# -----------------------------
# Overall KPIs
# -----------------------------
overall = summarize(rows)

late_5 = sum(
    float(r["schedule_lateness_min"]) >= 5
    for r in rows
)

late_10 = sum(
    float(r["schedule_lateness_min"]) >= 10
    for r in rows
)


# -----------------------------
# Time period
# -----------------------------
period_groups = group_by("time_period")


# -----------------------------
# Calendar weekday
# -----------------------------
weekday_groups = group_by(
    "calendar_day_of_week"
)

weekday_order = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
]


# -----------------------------
# Month
# -----------------------------
month_groups = group_by(
    "calendar_year_month"
)


# -----------------------------
# Route
# -----------------------------
route_groups = group_by("route_id")


lines = [
    "# Week 2 — Late Tax KPI Analysis",
    "",
    "## Overall KPIs",
    "",
    f"- Trips analyzed: {len(rows):,}",
    f"- Average schedule lateness: "
    f"{overall['avg_lateness']:.2f} min",
    f"- Average Excess Late Tax: "
    f"{overall['avg_excess']:.2f} min",
    f"- Median Excess Late Tax: "
    f"{overall['median_excess']:.2f} min",
    f"- 95th percentile Excess Late Tax: "
    f"{overall['p95_excess']:.2f} min",
    f"- Trips above route baseline: "
    f"{overall['above_baseline_share']:.1%}",
    f"- Trips ≥5 min late: "
    f"{late_5:,} ({late_5 / len(rows):.1%})",
    f"- Trips ≥10 min late: "
    f"{late_10:,} ({late_10 / len(rows):.1%})",
    "",
    "## Delay Composition",
    "",
    f"- Average departure delay: "
    f"{overall['avg_departure']:.2f} min",
    f"- Average in-transit travel-time delta: "
    f"{overall['avg_travel_delta']:.2f} min",
    "",
    "Arrival lateness can be interpreted as the combination "
    "of departure delay and changes in travel time between "
    "Daly City and Powell.",
    "",
    "## By Time Period",
    "",
    "| Period | Trips | Avg Excess Tax | P95 Excess Tax | Avg Schedule Lateness | Above Baseline |",
    "|---|---:|---:|---:|---:|---:|",
]

period_order = [
    "Morning Peak",
    "Midday",
    "Evening Peak",
    "Evening",
    "Overnight",
]

for period in period_order:
    if period not in period_groups:
        continue

    s = summarize(period_groups[period])

    lines.append(
        f"| {period} "
        f"| {s['rows']:,} "
        f"| {s['avg_excess']:.2f} "
        f"| {s['p95_excess']:.2f} "
        f"| {s['avg_lateness']:.2f} "
        f"| {s['above_baseline_share']:.1%} |"
    )


lines += [
    "",
    "## By Calendar Weekday",
    "",
    "| Weekday | Trips | Avg Excess Tax | P95 Excess Tax | Avg Schedule Lateness |",
    "|---|---:|---:|---:|---:|",
]

for weekday in weekday_order:
    if weekday not in weekday_groups:
        continue

    s = summarize(
        weekday_groups[weekday]
    )

    lines.append(
        f"| {weekday} "
        f"| {s['rows']:,} "
        f"| {s['avg_excess']:.2f} "
        f"| {s['p95_excess']:.2f} "
        f"| {s['avg_lateness']:.2f} |"
    )


lines += [
    "",
    "## By Month",
    "",
    "| Month | Trips | Avg Excess Tax | P95 Excess Tax | Avg Schedule Lateness |",
    "|---|---:|---:|---:|---:|",
]

for month in sorted(month_groups):
    s = summarize(
        month_groups[month]
    )

    lines.append(
        f"| {month} "
        f"| {s['rows']:,} "
        f"| {s['avg_excess']:.2f} "
        f"| {s['p95_excess']:.2f} "
        f"| {s['avg_lateness']:.2f} |"
    )


lines += [
    "",
    "## By Route",
    "",
    "| Route | Trips | Avg Excess Tax | P95 Excess Tax | Avg Schedule Lateness | Baseline Reliable |",
    "|---|---:|---:|---:|---:|---|",
]

for route in sorted(route_groups):
    group = route_groups[route]
    s = summarize(group)

    reliable = all(
        int(r["baseline_reliable_flag"]) == 1
        for r in group
    )

    lines.append(
        f"| {route} "
        f"| {s['rows']:,} "
        f"| {s['avg_excess']:.2f} "
        f"| {s['p95_excess']:.2f} "
        f"| {s['avg_lateness']:.2f} "
        f"| {'Yes' if reliable else 'No'} |"
    )


lines += [
    "",
    "## Interpretation Guardrails",
    "",
    "- Excess Late Tax is measured relative to each route's "
    "median arrival-delay baseline.",
    "- BA:Red-N has insufficient observations for reliable "
    "route-level conclusions.",
    "- Monthly totals should not be compared directly because "
    "the number of observations differs by month; normalized "
    "per-trip KPIs are used instead.",
    "- Schedule lateness and Excess Late Tax are both retained "
    "for transparency.",
]

REPORT_FILE.write_text(
    "\n".join(lines),
    encoding="utf-8",
)

print("KPI analysis complete.")
print(f"Report saved to: {REPORT_FILE}")
