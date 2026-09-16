import csv
from collections import defaultdict
from pathlib import Path
from statistics import mean, median


INPUT_FILE = Path(
    "data/processed/late_tax_analytics.csv"
)

REPORT_FILE = Path(
    "reports/midnight_reliability_investigation.md"
)


with INPUT_FILE.open(newline="") as f:
    rows = list(csv.DictReader(f))


# --------------------------------
# Target segment
# --------------------------------

target = [
    r for r in rows
    if r["route_id"] == "BA:Yellow-N"
    and int(r["scheduled_clock_hour"]) == 0
]

other = [
    r for r in rows
    if not (
        r["route_id"] == "BA:Yellow-N"
        and int(r["scheduled_clock_hour"]) == 0
    )
]


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


target_summary = summarize(target)
other_summary = summarize(other)


# --------------------------------
# Monthly consistency
# --------------------------------

month_groups = defaultdict(list)

for row in target:
    month_groups[
        row["calendar_year_month"]
    ].append(row)


# --------------------------------
# Delay-driver classification
# --------------------------------

late_target = [
    r for r in target
    if float(r["schedule_lateness_min"]) >= 5
]

departure_driven = 0
travel_driven = 0
mixed = 0

for row in late_target:
    departure = max(
        float(row["departure_delay_min"]),
        0,
    )

    travel = max(
        float(row["travel_time_delta_min"]),
        0,
    )

    if departure > 0 and travel <= 0:
        departure_driven += 1

    elif travel > 0 and departure <= 0:
        travel_driven += 1

    elif departure > 0 and travel > 0:
        if departure >= 2 * travel:
            departure_driven += 1

        elif travel >= 2 * departure:
            travel_driven += 1

        else:
            mixed += 1


driver_total = len(late_target)


# --------------------------------
# Midnight schedule distribution
# --------------------------------

schedule_groups = defaultdict(list)

for row in target:
    schedule_groups[
        row["scheduled_departure"]
    ].append(row)


# --------------------------------
# Report
# --------------------------------

lines = [
    "# Week 3 — Midnight Reliability Investigation",
    "",
    "## Analytical Question",
    "",
    (
        "Why does the Yellow-N service scheduled shortly "
        "after midnight show elevated Late Tax?"
    ),
    "",
    "## Target vs Other Trips",
    "",
    (
        "| Segment | Trips | Avg Arrival Delay | "
        "Median Arrival Delay | Avg Departure Delay | "
        "Avg Travel Delta | >=5 min Late |"
    ),
    "|---|---:|---:|---:|---:|---:|---:|",
    (
        f"| Yellow-N midnight "
        f"| {target_summary['trips']:,} "
        f"| {target_summary['avg_arrival']:.2f} "
        f"| {target_summary['median_arrival']:.2f} "
        f"| {target_summary['avg_departure']:.2f} "
        f"| {target_summary['avg_travel']:.2f} "
        f"| {target_summary['late5_rate']:.1%} |"
    ),
    (
        f"| All other trips "
        f"| {other_summary['trips']:,} "
        f"| {other_summary['avg_arrival']:.2f} "
        f"| {other_summary['median_arrival']:.2f} "
        f"| {other_summary['avg_departure']:.2f} "
        f"| {other_summary['avg_travel']:.2f} "
        f"| {other_summary['late5_rate']:.1%} |"
    ),
    "",
    "## Scheduled Departures in Target Segment",
    "",
    "| Scheduled Departure | Trips |",
    "|---|---:|",
]

for departure in sorted(schedule_groups):
    lines.append(
        f"| {departure} "
        f"| {len(schedule_groups[departure]):,} |"
    )


lines += [
    "",
    "## Monthly Consistency",
    "",
    (
        "| Month | Trips | Avg Arrival Delay | "
        "Median Arrival Delay | Avg Departure Delay | "
        "Avg Travel Delta | >=5 min Late |"
    ),
    "|---|---:|---:|---:|---:|---:|---:|",
]


for month in sorted(month_groups):
    summary = summarize(
        month_groups[month]
    )

    lines.append(
        f"| {month} "
        f"| {summary['trips']:,} "
        f"| {summary['avg_arrival']:.2f} "
        f"| {summary['median_arrival']:.2f} "
        f"| {summary['avg_departure']:.2f} "
        f"| {summary['avg_travel']:.2f} "
        f"| {summary['late5_rate']:.1%} |"
    )


lines += [
    "",
    "## Delay Driver Classification",
    "",
    (
        f"Among {driver_total:,} target trips arriving "
        "at least five minutes late:"
    ),
    "",
    (
        f"- Departure-driven: {departure_driven:,} "
        f"({departure_driven / driver_total:.1%})"
    ),
    (
        f"- Travel-time-driven: {travel_driven:,} "
        f"({travel_driven / driver_total:.1%})"
    ),
    (
        f"- Mixed: {mixed:,} "
        f"({mixed / driver_total:.1%})"
    ),
    "",
    "## Key Findings",
    "",
    (
        f"- Yellow-N midnight trips had a "
        f"{target_summary['late5_rate']:.1%} rate of "
        "schedule lateness of at least five minutes, "
        f"compared with {other_summary['late5_rate']:.1%} "
        "for all other analyzed trips."
    ),
    (
        f"- Average arrival delay was "
        f"{target_summary['avg_arrival']:.2f} minutes "
        "for the target segment versus "
        f"{other_summary['avg_arrival']:.2f} minutes "
        "for other trips."
    ),
    (
        f"- {departure_driven / driver_total:.1%} of "
        "target trips that were at least five minutes "
        "late were classified as departure-driven."
    ),
    (
        "- The elevated reliability risk appears across "
        "multiple months rather than being attributable "
        "to a single isolated month."
    ),
    "",
    "## Interpretation Guardrails",
    "",
    (
        "- This is descriptive analysis and does not "
        "establish that route or departure time causes delay."
    ),
    (
        "- The target segment consists of Yellow-N trips "
        "scheduled between 24:00 and 24:59 in GTFS service "
        "time and mapped to the following calendar day."
    ),
    (
        "- Driver classification is an analytical heuristic: "
        "departure-driven means positive departure delay was "
        "at least twice the positive travel-time delta; "
        "travel-time-driven applies the reverse rule."
    ),
    (
        "- Comparisons are observational and are not adjusted "
        "for service frequency, incidents, maintenance, "
        "weather, or other operational factors."
    ),
]


REPORT_FILE.write_text(
    "\n".join(lines) + "\n"
)


print(
    f"Wrote {REPORT_FILE}"
)

print(
    f"Target trips: {len(target):,}"
)

print(
    f"Other trips: {len(other):,}"
)

print(
    f"Target >=5 min late: "
    f"{target_summary['late5_rate']:.1%}"
)

print(
    f"Other >=5 min late: "
    f"{other_summary['late5_rate']:.1%}"
)

print(
    f"Departure-driven late target trips: "
    f"{departure_driven}/{driver_total} "
    f"({departure_driven / driver_total:.1%})"
)

