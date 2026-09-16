import csv
from collections import defaultdict
from pathlib import Path
from statistics import mean, median


INPUT_FILE = Path(
    "data/processed/late_tax_analytics.csv"
)

REPORT_FILE = Path(
    "reports/late_tax_patterns.md"
)


# --------------------------------
# Load analytics dataset
# --------------------------------

with INPUT_FILE.open(newline="") as f:
    rows = list(csv.DictReader(f))


# --------------------------------
# Helper functions
# --------------------------------

def percentile(values, p):
    values = sorted(values)

    index = round(
        (len(values) - 1) * p
    )

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

    late_5 = sum(
        float(r["schedule_lateness_min"]) >= 5
        for r in group_rows
    )

    late_10 = sum(
        float(r["schedule_lateness_min"]) >= 10
        for r in group_rows
    )

    return {
        "trips": len(group_rows),
        "mean_tax": mean(excess),
        "median_tax": median(excess),
        "p90_tax": percentile(excess, 0.90),
        "p95_tax": percentile(excess, 0.95),
        "avg_lateness": mean(lateness),
        "late_5_rate": late_5 / len(group_rows),
        "late_10_rate": late_10 / len(group_rows),
    }


def group_by(*columns):
    groups = defaultdict(list)

    for row in rows:
        key = tuple(
            row[column]
            for column in columns
        )

        groups[key].append(row)

    return groups


# --------------------------------
# Overall distribution
# --------------------------------

overall = summarize(rows)


# --------------------------------
# Route x time-period analysis
# --------------------------------

route_period_groups = group_by(
    "route_id",
    "time_period",
)

route_period_results = []

for key, group_rows in route_period_groups.items():
    route, period = key

    result = summarize(group_rows)

    route_period_results.append(
        (
            route,
            period,
            result,
        )
    )


# --------------------------------
# Weekday x time-period analysis
# --------------------------------

weekday_period_groups = group_by(
    "calendar_day_of_week",
    "time_period",
)

weekday_period_results = []

for key, group_rows in weekday_period_groups.items():
    weekday, period = key

    result = summarize(group_rows)

    weekday_period_results.append(
        (
            weekday,
            period,
            result,
        )
    )


# --------------------------------
# Monthly analysis
# --------------------------------

month_groups = group_by(
    "calendar_year_month"
)

month_results = []

for key, group_rows in month_groups.items():
    month = key[0]

    result = summarize(group_rows)

    month_results.append(
        (
            month,
            result,
        )
    )


# --------------------------------
# Extreme-delay observations
# --------------------------------

extreme_rows = sorted(
    rows,
    key=lambda r: float(
        r["schedule_lateness_min"]
    ),
    reverse=True,
)[:15]


# --------------------------------
# Minimum sample-size guardrail
# --------------------------------

MIN_SAMPLE = 30

eligible_route_period = [
    x
    for x in route_period_results
    if x[2]["trips"] >= MIN_SAMPLE
]

eligible_weekday_period = [
    x
    for x in weekday_period_results
    if x[2]["trips"] >= MIN_SAMPLE
]


worst_route_period = max(
    eligible_route_period,
    key=lambda x: x[2]["p95_tax"],
)

worst_weekday_period = max(
    eligible_weekday_period,
    key=lambda x: x[2]["p95_tax"],
)


# --------------------------------
# Build report
# --------------------------------

lines = [
    "# Week 3 — Late Tax Pattern Analysis",
    "",
    "## Objective",
    "",
    (
        "Identify when and where riders experience "
        "the greatest Late Tax, with emphasis on "
        "tail risk rather than averages alone."
    ),
    "",
    "## Overall Distribution",
    "",
    f"- Trips analyzed: {overall['trips']:,}",
    (
        f"- Average Excess Late Tax: "
        f"{overall['mean_tax']:.2f} min"
    ),
    (
        f"- Median Excess Late Tax: "
        f"{overall['median_tax']:.2f} min"
    ),
    (
        f"- P90 Excess Late Tax: "
        f"{overall['p90_tax']:.2f} min"
    ),
    (
        f"- P95 Excess Late Tax: "
        f"{overall['p95_tax']:.2f} min"
    ),
    (
        f"- Probability of ≥5 min schedule lateness: "
        f"{overall['late_5_rate']:.1%}"
    ),
    (
        f"- Probability of ≥10 min schedule lateness: "
        f"{overall['late_10_rate']:.1%}"
    ),
    "",
    "## Route × Time Period",
    "",
    (
        "| Route | Period | Trips | Avg Tax | "
        "Median | P90 | P95 | ≥5 min Late | ≥10 min Late |"
    ),
    (
        "|---|---|---:|---:|---:|---:|---:|"
        "---:|---:|"
    ),
]


for route, period, result in sorted(
    route_period_results,
    key=lambda x: x[2]["p95_tax"],
    reverse=True,
):
    lines.append(
        f"| {route} "
        f"| {period} "
        f"| {result['trips']:,} "
        f"| {result['mean_tax']:.2f} "
        f"| {result['median_tax']:.2f} "
        f"| {result['p90_tax']:.2f} "
        f"| {result['p95_tax']:.2f} "
        f"| {result['late_5_rate']:.1%} "
        f"| {result['late_10_rate']:.1%} |"
    )


lines += [
    "",
    "## Weekday × Time Period",
    "",
    (
        "| Weekday | Period | Trips | Avg Tax | "
        "P90 | P95 | ≥5 min Late | ≥10 min Late |"
    ),
    (
        "|---|---|---:|---:|---:|---:|"
        "---:|---:|"
    ),
]


for weekday, period, result in sorted(
    weekday_period_results,
    key=lambda x: x[2]["p95_tax"],
    reverse=True,
):
    lines.append(
        f"| {weekday} "
        f"| {period} "
        f"| {result['trips']:,} "
        f"| {result['mean_tax']:.2f} "
        f"| {result['p90_tax']:.2f} "
        f"| {result['p95_tax']:.2f} "
        f"| {result['late_5_rate']:.1%} "
        f"| {result['late_10_rate']:.1%} |"
    )


lines += [
    "",
    "## Monthly Pattern",
    "",
    (
        "| Month | Trips | Avg Tax | Median | "
        "P90 | P95 | ≥5 min Late |"
    ),
    "|---|---:|---:|---:|---:|---:|---:|",
]


for month, result in sorted(month_results):
    lines.append(
        f"| {month} "
        f"| {result['trips']:,} "
        f"| {result['mean_tax']:.2f} "
        f"| {result['median_tax']:.2f} "
        f"| {result['p90_tax']:.2f} "
        f"| {result['p95_tax']:.2f} "
        f"| {result['late_5_rate']:.1%} |"
    )


lines += [
    "",
    "## Highest-Risk Segments",
    "",
    (
        f"- Highest P95 route × period "
        f"(minimum {MIN_SAMPLE} trips): "
        f"{worst_route_period[0]} / "
        f"{worst_route_period[1]} — "
        f"{worst_route_period[2]['p95_tax']:.2f} min."
    ),
    (
        f"- Highest P95 weekday × period "
        f"(minimum {MIN_SAMPLE} trips): "
        f"{worst_weekday_period[0]} / "
        f"{worst_weekday_period[1]} — "
        f"{worst_weekday_period[2]['p95_tax']:.2f} min."
    ),
    "",
    "## Top 15 Extreme Trips",
    "",
    (
        "| Date | Route | Period | Schedule Lateness | "
        "Excess Late Tax | Departure Delay | Travel Delta |"
    ),
    "|---|---|---|---:|---:|---:|---:|",
]


for row in extreme_rows:
    lines.append(
        f"| {row['calendar_date']} "
        f"| {row['route_id']} "
        f"| {row['time_period']} "
        f"| {float(row['schedule_lateness_min']):.2f} "
        f"| {float(row['excess_late_tax_min']):.2f} "
        f"| {float(row['departure_delay_min']):.2f} "
        f"| {float(row['travel_time_delta_min']):.2f} |"
    )


lines += [
    "",
    "## Interpretation Guardrails",
    "",
    (
        "- Excess Late Tax is relative to each route's "
        "median arrival-delay baseline."
    ),
    (
        "- P90 and P95 describe tail-risk conditions and "
        "should not be interpreted as typical trips."
    ),
    (
        f"- Segment rankings require at least "
        f"{MIN_SAMPLE} observations."
    ),
    (
        "- Descriptive patterns do not establish "
        "causal relationships."
    ),
]


REPORT_FILE.write_text(
    "\n".join(lines) + "\n"
)


print(
    f"Wrote {REPORT_FILE}"
)

print(
    f"Analyzed {len(rows):,} trips"
)

print(
    "Worst eligible route-period:",
    worst_route_period[0],
    "/",
    worst_route_period[1],
    f"P95={worst_route_period[2]['p95_tax']:.2f}",
)

print(
    "Worst eligible weekday-period:",
    worst_weekday_period[0],
    "/",
    worst_weekday_period[1],
    f"P95={worst_weekday_period[2]['p95_tax']:.2f}",
)
