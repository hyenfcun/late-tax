from pathlib import Path
import zipfile

import pandas as pd


HISTORICAL_DIR = Path("data/raw/historical")
OUTPUT_DIR = Path("data/processed")

DALY_CITY = {"901901", "901902", "901903"}
POWELL = {"901301", "901302"}

COLUMNS = [
    "trip_id",
    "service_date",
    "stop_sequence",
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
        hours, minutes, seconds = map(int, value.split(":"))
        return hours * 3600 + minutes * 60 + seconds
    except (ValueError, AttributeError):
        return None


def process_month(zip_path):
    month = zip_path.stem.replace("gtfs_", "").replace("_so", "")
    output_path = OUTPUT_DIR / f"daly_powell_{month}.csv"

    print(f"\nProcessing {month}...")

    origin_parts = []
    destination_parts = []

    with zipfile.ZipFile(zip_path) as zf:
        if "stop_observations.txt" not in zf.namelist():
            print(f"SKIPPED {month}: stop_observations.txt not found")
            return None

        with zf.open("stop_observations.txt") as file:
            for chunk in pd.read_csv(
                file,
                usecols=COLUMNS,
                dtype=str,
                chunksize=250_000,
            ):
                bart = chunk[chunk["agency_id"] == "BA"]

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
        print(f"SKIPPED {month}: Daly City or Powell observations missing")
        return None


    origins = pd.concat(origin_parts, ignore_index=True)
    destinations = pd.concat(destination_parts, ignore_index=True)

    origins["stop_sequence"] = pd.to_numeric(
        origins["stop_sequence"],
        errors="coerce",
    )

    destinations["stop_sequence"] = pd.to_numeric(
        destinations["stop_sequence"],
        errors="coerce",
    )

    origins = origins.rename(
        columns={
            "stop_sequence": "origin_sequence",
            "from_stop_id": "origin_stop_id",
            "scheduled_departure_time": "scheduled_departure",
            "observed_departure_time": "observed_departure",
        }
    )

    destinations = destinations.rename(
        columns={
            "stop_sequence": "destination_sequence",
            "to_stop_id": "destination_stop_id",
            "scheduled_arrival_time": "scheduled_arrival",
            "observed_arrival_time": "observed_arrival",
        }
    )

    origins = origins[
        [
            "trip_id",
            "service_date",
            "route_id",
            "origin_sequence",
            "origin_stop_id",
            "scheduled_departure",
            "observed_departure",
        ]
    ]

    destinations = destinations[
        [
            "trip_id",
            "service_date",
            "route_id",
            "destination_sequence",
            "destination_stop_id",
            "scheduled_arrival",
            "observed_arrival",
        ]
    ]

    journeys = origins.merge(
        destinations,
        on=["trip_id", "service_date", "route_id"],
        how="inner",
    )

    journeys = journeys[
        journeys["destination_sequence"]
        > journeys["origin_sequence"]
    ].copy()

    journeys["service_date"] = pd.to_datetime(
        journeys["service_date"],
        format="%Y%m%d",
        errors="coerce",
    )

    journeys = journeys[
        journeys["service_date"].notna()
        & (journeys["service_date"].dt.dayofweek < 5)
    ].copy()

    for column in [
        "scheduled_departure",
        "observed_departure",
        "scheduled_arrival",
        "observed_arrival",
    ]:
        journeys[column + "_sec"] = journeys[column].apply(
            time_to_seconds
        )

    journeys = journeys.dropna(
        subset=[
            "scheduled_departure_sec",
            "observed_departure_sec",
            "scheduled_arrival_sec",
            "observed_arrival_sec",
        ]
    )

    # Weekday morning commute: 7:00 AM to before 10:00 AM
    journeys = journeys[
        (journeys["scheduled_departure_sec"] >= 7 * 3600)
        & (journeys["scheduled_departure_sec"] < 10 * 3600)
    ].copy()

    journeys["scheduled_travel_min"] = (
        journeys["scheduled_arrival_sec"]
        - journeys["scheduled_departure_sec"]
    ) / 60

    journeys["observed_travel_min"] = (
        journeys["observed_arrival_sec"]
        - journeys["observed_departure_sec"]
    ) / 60

    journeys["arrival_delay_min"] = (
        journeys["observed_arrival_sec"]
        - journeys["scheduled_arrival_sec"]
    ) / 60

    journeys = journeys[
        (journeys["scheduled_travel_min"] > 0)
        & (journeys["observed_travel_min"] > 0)
    ].copy()

    journeys = journeys.drop_duplicates(
        subset=["trip_id", "service_date"]
    )

    journeys["source_month"] = month

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    journeys.to_csv(
        output_path,
        index=False,
    )

    print(f"{month}: {len(journeys):,} journeys")

    return journeys


def main():
    zip_files = sorted(
        HISTORICAL_DIR.glob("gtfs_*_so.zip")
    )

    if not zip_files:
        raise FileNotFoundError(
            "No historical GTFS ZIP files found."
        )

    print(f"Found {len(zip_files)} historical GTFS files.")

    all_months = []

    for zip_path in zip_files:
        result = process_month(zip_path)

        if result is not None and not result.empty:
            all_months.append(result)

    if not all_months:
        raise RuntimeError(
            "No journeys were extracted from any month."
        )

    combined = pd.concat(
        all_months,
        ignore_index=True,
    )

    combined = combined.sort_values(
        ["service_date", "scheduled_departure"]
    )

    combined_path = OUTPUT_DIR / "daly_powell_all.csv"

    combined.to_csv(
        combined_path,
        index=False,
    )

    print("\n==============================")
    print("PIPELINE COMPLETE")
    print("==============================")
    print(f"Months processed: {len(all_months)}")
    print(f"Total journeys: {len(combined):,}")
    print(
        "Date range:",
        combined["service_date"].min().date(),
        "to",
        combined["service_date"].max().date(),
    )
    print(f"Combined file: {combined_path}")


if __name__ == "__main__":
    main()



