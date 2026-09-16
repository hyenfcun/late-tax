import csv
from pathlib import Path
from statistics import mean, median


INPUT_FILE = Path(
    "data/processed/late_tax_analytics.csv"
)

REPORT_FILE = Path(
    "reports/midnight_finding_validation.md"
)


with INPUT_FILE.open(newline="") as f:
    rows = list(csv.DictReader(f))


def summarize(group):
    arrival = [
        float(r["arrival_delay_min"])
        for r in group
    ]

    departure = [
        float(r["departure_delay_min"])
        for r in group
    ]

    travel = [
        float(r["travel_time_delta_min"])
        for r in group
    ]

    late5 = sum(
        float(r["schedule_lateness_min"]) >= 5
        for r in group
    )

    return {
        "trips": len(group),
        "avg_arrival": mean(arrival),
        "median_arrival": median(arrival),
        "avg_departure": mean(departure),
        "avg_travel": mean(travel),
        "late5_rate": late5 / len(group),
    }


yellow_2408 = [
    r for r in rows
    if r["route_id"] == "BA:Yellow-N"
    and r["scheduled_departure"] == "24:08:00"
]

yellow_other_midnight = [
    r for r in rows
    if r["route_id"] == "BA:Yellow-N"
    and int(r["scheduled_clock_hour"]) == 0
    and r["scheduled_departure"] != "24:08:00"
]

yellow_non_midnight = [
    r for r in rows
    if r["route_id"] == "BA:Yellow-N"
    and int(r["scheduled_clock_hour"]) != 0
]

all_except_2408 = [
    r for r in rows
    if not (
        r["route_id"] == "BA:Yellow-N"
        and r["scheduled_departure"] == "24:08:00"
    )
]


segments = [
    (
        "Yellow-N 24:08",
        yellow_2408,
    ),
    (
        "Yellow-N other midnight",
        yellow_other_midnight,
    ),
    (
        "Yellow-N non-midnight",
        yellow_non_midnight,
    ),
    (
        "All trips except Yellow-N 24:08",
        all_except_2408,
    ),
]


results = [
    (
        label,
        summarize(group),
    )
    for label, group in segments
]


lines = [
    "# Week 3 — Midnight Finding Robustness Check",
    "",
    "## Question",
    "",
    (
        "Is the elevated Yellow-N midnight reliability "
        "risk driven only by the frequently observed "
        "24:08 scheduled departure?"
    ),
    "",
    "## Segment Comparison",
    "",
    (
        "| Segment | Trips | Avg Arrival Delay | "
        "Median Arrival Delay | Avg Departure Delay | "
        "Avg Travel Delta | >=5 min Late |"
    ),
    "|---|---:|---:|---:|---:|---:|---:|",
]


for label, result in results:
    lines.append(
        f"| {label} "
        f"| {result['trips']:,} "
        f"| {result['avg_arrival']:.2f} "
        f"| {result['median_arrival']:.2f} "
        f"| {result['avg_departure']:.2f} "
        f"| {result['avg_travel']:.2f} "
        f"| {result['late5_rate']:.1%} |"
    )


other_midnight = summarize(
    yellow_other_midnight
)

non_midnight = summarize(
    yellow_non_midnight
)


lines += [
    "",
    "## Result",
    "",
    (
        "- The 24:08 departure is the largest component "
        "of the target segment and shows elevated "
        "reliability risk."
    ),
    (
        f"- However, the other Yellow-N midnight "
        f"departures also show a "
        f"{other_midnight['late5_rate']:.1%} rate of "
        "lateness of at least five minutes."
    ),
    (
        f"- Yellow-N non-midnight trips show only a "
        f"{non_midnight['late5_rate']:.1%} rate of "
        "lateness of at least five minutes."
    ),
    (
        "- Therefore, the observed pattern is not solely "
        "an artifact of the 24:08 scheduled departure."
    ),
    "",
    "## Interpretation",
    "",
    (
        "The evidence supports describing the finding as "
        "an elevated reliability pattern among observed "
        "Yellow-N trips scheduled shortly after midnight, "
        "rather than attributing the pattern to Yellow-N "
        "service generally or to the 24:08 departure alone."
    ),
    "",
    "## Guardrails",
    "",
    (
        "- This is a descriptive robustness check, not "
        "a causal test."
    ),
    (
        "- The other-midnight comparison contains fewer "
        "observations than the 24:08 group, so its "
        "estimates should be interpreted with greater "
        "uncertainty."
    ),
]


REPORT_FILE.write_text(
    "\n".join(lines) + "\n"
)


print(f"Wrote {REPORT_FILE}")

for label, result in results:
    print(
        f"{label}: "
        f"n={result['trips']}, "
        f"avg arrival={result['avg_arrival']:.2f}, "
        f">=5min={result['late5_rate']:.1%}"
    )

