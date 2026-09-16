from pathlib import Path
import zipfile
import pandas as pd

HISTORICAL_DIR = Path("data/raw/historical")
REPORT_FILE = Path("reports/postmerge_filter_audit.md")

DALY_CITY = {"901901", "901902", "901903"}
POWELL = {"901301", "901302"}

OBS_COLUMNS = [
    "trip_id",
    "service_date",
    "observed_arrival_time",
    "observed_departure_time",
    "route_id",
    "agency_id",
    "from_stop_id",
    "to_stop_id",
    "scheduled_arrival_time",
    "scheduled_departure_time",
]


def time_to_seconds(value):
    if pd.isna(value):
        return None

    try:
        h, m, s = map(int, str(value).split(":"))
        return h * 3600 + m * 60 + s
    except (ValueError, AttributeError):
        return None


def get_valid_trip_ids(zf):
    with zf.open("stop_times.txt") as f:
        stop_times = pd.read_csv(
            f,
            usecols=[
                "trip_id",
                "stop_id",
                "stop_sequence",
            ],
            dtype={
                "trip_id": str,
                "stop_id": str,
            },
        )

    stop_times["stop_sequence"] = pd.to_numeric(
        stop_times["stop_sequence"],
        errors="coerce",
    )

    daly = stop_times[
        stop_times["stop_id"].isin(DALY_CITY)
    ][["trip_id", "stop_sequence"]].rename(
        columns={"stop_sequence": "daly_sequence"}
    )

    powell = stop_times[
        stop_times["stop_id"].isin(POWELL)
    ][["trip_id", "stop_sequence"]].rename(
        columns={"stop_sequence": "powell_sequence"}
    )

    direction = daly.merge(
        powell,
        on="trip_id",
        how="inner",
    )

    direction = direction[
        direction["powell_sequence"]
        > direction["daly_sequence"]
    ]

    return set(direction["trip_id"].unique())


def stats(df):
    if df.empty:
        return 0, 0

    return len(df), df["service_date"].nunique()


results = []

for zip_path in sorted(
    HISTORICAL_DIR.glob("gtfs_*_so.zip")
):
    month = (
        zip_path.stem
        .replace("gtfs_", "")
        .replace("_so", "")
    )

    print(f"Auditing {month}...")

    with zipfile.ZipFile(zip_path) as zf:
        valid_trip_ids = get_valid_trip_ids(zf)

        origin_parts = []
        destination_parts = []

        with zf.open("stop_observations.txt") as f:
            for chunk in pd.read_csv(
                f,
                usecols=OBS_COLUMNS,
                dtype=str,
                chunksize=250_000,
            ):
                bart = chunk[
                    chunk["agency_id"] == "BA"
                ].copy()

                bart = bart[
                    bart["trip_id"].isin(valid_trip_ids)
                ].copy()

                origins = bart[
                    bart["from_stop_id"].isin(DALY_CITY)
                ].copy()

                destinations = bart[
                    bart["to_stop_id"].isin(POWELL)
                ].copy()

                if not origins.empty:
                    origin_parts.append(origins)

                if not destinations.empty:
                    destination_parts.append(destinations)

        if not origin_parts or not destination_parts:
            continue

        origins = pd.concat(
            origin_parts,
            ignore_index=True,
        )

        destinations = pd.concat(
            destination_parts,
            ignore_index=True,
        )

        origins = origins[
            [
                "trip_id",
                "service_date",
                "route_id",
                "scheduled_departure_time",
                "observed_departure_time",
            ]
        ].rename(
            columns={
                "scheduled_departure_time":
                    "scheduled_departure",
                "observed_departure_time":
                    "observed_departure",
            }
        )

        destinations = destinations[
            [
                "trip_id",
                "service_date",
                "route_id",
                "scheduled_arrival_time",
                "observed_arrival_time",
            ]
        ].rename(
            columns={
                "scheduled_arrival_time":
                    "scheduled_arrival",
                "observed_arrival_time":
                    "observed_arrival",
            }
        )

        journeys = origins.merge(
            destinations,
            on=[
                "trip_id",
                "service_date",
                "route_id",
            ],
            how="inner",
        )

        matched_rows, matched_dates = stats(journeys)

        journeys["service_date"] = pd.to_datetime(
            journeys["service_date"],
            format="%Y%m%d",
            errors="coerce",
        )

        parsed = journeys[
            journeys["service_date"].notna()
        ].copy()

        parsed_rows, parsed_dates = stats(parsed)

        weekday = parsed[
            parsed["service_date"].dt.dayofweek < 5
        ].copy()

        weekday_rows, weekday_dates = stats(weekday)

        for column in [
            "scheduled_departure",
            "observed_departure",
            "scheduled_arrival",
            "observed_arrival",
        ]:
            weekday[column + "_sec"] = (
                weekday[column].apply(time_to_seconds)
            )

        time_valid = weekday.dropna(
            subset=[
                "scheduled_departure_sec",
                "observed_departure_sec",
                "scheduled_arrival_sec",
                "observed_arrival_sec",
            ]
        ).copy()

        time_rows, time_dates = stats(time_valid)

        morning = time_valid[
            (
                time_valid["scheduled_departure_sec"]
                >= 7 * 3600
            )
            &
            (
                time_valid["scheduled_departure_sec"]
                < 10 * 3600
            )
        ].copy()

        morning_rows, morning_dates = stats(morning)

        morning["scheduled_travel_min"] = (
            morning["scheduled_arrival_sec"]
            - morning["scheduled_departure_sec"]
        ) / 60

        morning["observed_travel_min"] = (
            morning["observed_arrival_sec"]
            - morning["observed_departure_sec"]
        ) / 60

        positive = morning[
            (morning["scheduled_travel_min"] > 0)
            &
            (morning["observed_travel_min"] > 0)
        ].copy()

        positive_rows, positive_dates = stats(positive)

        deduped = positive.sort_values(
            [
                "service_date",
                "trip_id",
                "scheduled_departure_sec",
            ]
        ).drop_duplicates(
            subset=[
                "trip_id",
                "service_date",
            ],
            keep="first",
        )

        dedup_rows, dedup_dates = stats(deduped)

        results.append({
            "month": month,
            "matched_rows": matched_rows,
            "matched_dates": matched_dates,
            "parsed_rows": parsed_rows,
            "parsed_dates": parsed_dates,
            "weekday_rows": weekday_rows,
            "weekday_dates": weekday_dates,
            "time_rows": time_rows,
            "time_dates": time_dates,
            "morning_rows": morning_rows,
            "morning_dates": morning_dates,
            "positive_rows": positive_rows,
            "positive_dates": positive_dates,
            "dedup_rows": dedup_rows,
            "dedup_dates": dedup_dates,
        })


lines = [
    "# Week 2 — Post-Merge Filter Audit",
    "",
    "| Month | Matched R/D | Parsed R/D | Weekday R/D | Time-valid R/D | Morning R/D | Positive R/D | Final R/D |",
    "|---|---:|---:|---:|---:|---:|---:|---:|",
]

for r in results:
    lines.append(
        f"| {r['month']} "
        f"| {r['matched_rows']}/{r['matched_dates']} "
        f"| {r['parsed_rows']}/{r['parsed_dates']} "
        f"| {r['weekday_rows']}/{r['weekday_dates']} "
        f"| {r['time_rows']}/{r['time_dates']} "
        f"| {r['morning_rows']}/{r['morning_dates']} "
        f"| {r['positive_rows']}/{r['positive_dates']} "
        f"| {r['dedup_rows']}/{r['dedup_dates']} |"
    )

lines += [
    "",
    "R/D = rows / unique service dates.",
    "",
    "The step with the largest loss in unique service dates identifies the main coverage bottleneck."
]

REPORT_FILE.write_text(
    "\n".join(lines),
    encoding="utf-8",
)

print()
print(f"Report saved to: {REPORT_FILE}")
