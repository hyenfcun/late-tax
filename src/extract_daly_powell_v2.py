from pathlib import Path
import zipfile

import pandas as pd


HISTORICAL_DIR = Path("data/raw/historical")
OUTPUT_DIR = Path("data/processed")

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
    """
    Use scheduled GTFS stop_times.txt to identify trips where
    Daly City occurs before Powell Street.
    """

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
    ][
        ["trip_id", "stop_sequence"]
    ].rename(
        columns={
            "stop_sequence": "daly_sequence"
        }
    )

    powell = stop_times[
        stop_times["stop_id"].isin(POWELL)
    ][
        ["trip_id", "stop_sequence"]
    ].rename(
        columns={
            "stop_sequence": "powell_sequence"
        }
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


def process_month(zip_path):
    month = (
        zip_path.stem
        .replace("gtfs_", "")
        .replace("_so", "")
    )

    print(f"\nProcessing {month}...")

    with zipfile.ZipFile(zip_path) as zf:

        required = {
            "stop_times.txt",
            "stop_observations.txt",
        }

        missing = required - set(zf.namelist())

        if missing:
            print(
                f"SKIPPED {month}: "
                f"missing {sorted(missing)}"
            )
            return None

        valid_trip_ids = get_valid_trip_ids(zf)

        print(
            f"Scheduled Daly -> Powell trip IDs: "
            f"{len(valid_trip_ids):,}"
        )

        if not valid_trip_ids:
            print(
                f"SKIPPED {month}: "
                "no scheduled Daly -> Powell trips"
            )
            return None

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

                if bart.empty:
                    continue

                origins = bart[
                    bart["from_stop_id"].isin(DALY_CITY)
                ].copy()

                destinations = bart[
                    bart["to_stop_id"].isin(POWELL)
                ].copy()

                if not origins.empty:
                    origin_parts.append(origins)

                if not destinations.empty:
                    destination_parts.append(
                        destinations
                    )

    if not origin_parts or not destination_parts:
        print(
            f"SKIPPED {month}: "
            "observations missing"
        )
        return None

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
            "from_stop_id",
            "scheduled_departure_time",
            "observed_departure_time",
        ]
    ].rename(
        columns={
            "from_stop_id":
                "origin_stop_id",
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
            "to_stop_id",
            "scheduled_arrival_time",
            "observed_arrival_time",
        ]
    ].rename(
        columns={
            "to_stop_id":
                "destination_stop_id",
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

    print(
        f"Observation matches before filters: "
        f"{len(journeys):,}"
    )

    journeys["service_date"] = pd.to_datetime(
        journeys["service_date"],
        format="%Y%m%d",
        errors="coerce",
    )

    journeys = journeys[
        journeys["service_date"].notna()
    ].copy()

    # Monday-Friday only
    journeys = journeys[
        journeys["service_date"].dt.dayofweek < 5
    ].copy()

    for column in [
        "scheduled_departure",
        "observed_departure",
        "scheduled_arrival",
        "observed_arrival",
    ]:
        journeys[
            column + "_sec"
        ] = journeys[column].apply(
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

    # Morning commute:
    # scheduled departure from Daly City
    # from 07:00 inclusive to 10:00 exclusive.
    journeys = journeys[
        (
            journeys[
                "scheduled_departure_sec"
            ] >= 7 * 3600
        )
        &
        (
            journeys[
                "scheduled_departure_sec"
            ] < 10 * 3600
        )
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

    journeys["departure_delay_min"] = (
        journeys["observed_departure_sec"]
        - journeys["scheduled_departure_sec"]
    ) / 60

    journeys["travel_time_delta_min"] = (
        journeys["observed_travel_min"]
        - journeys["scheduled_travel_min"]
    )

    # Basic validity filters
    journeys = journeys[
        (
            journeys[
                "scheduled_travel_min"
            ] > 0
        )
        &
        (
            journeys[
                "observed_travel_min"
            ] > 0
        )
    ].copy()

    # One record per trip/service date.
    journeys = journeys.sort_values(
        [
            "service_date",
            "trip_id",
            "scheduled_departure_sec",
        ]
    )

    journeys = journeys.drop_duplicates(
        subset=[
            "trip_id",
            "service_date",
        ],
        keep="first",
    )

    journeys["source_month"] = month

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    monthly_path = (
        OUTPUT_DIR
        / f"daly_powell_v2_{month}.csv"
    )

    journeys.to_csv(
        monthly_path,
        index=False,
    )

    print(
        f"{month}: "
        f"{len(journeys):,} final journeys, "
        f"{journeys['service_date'].nunique():,} dates"
    )

    return journeys


def main():

    zip_files = sorted(
        HISTORICAL_DIR.glob(
            "gtfs_*_so.zip"
        )
    )

    if not zip_files:
        raise FileNotFoundError(
            "No historical GTFS ZIP files found."
        )

    print(
        f"Found {len(zip_files)} "
        "historical GTFS files."
    )

    results = []

    for zip_path in zip_files:

        try:
            result = process_month(
                zip_path
            )

            if (
                result is not None
                and not result.empty
            ):
                results.append(result)

        except Exception as exc:
            print(
                f"ERROR processing "
                f"{zip_path.name}: {exc}"
            )
            raise

    if not results:
        raise RuntimeError(
            "No journeys extracted."
        )

    combined = pd.concat(
        results,
        ignore_index=True,
    )

    combined = combined.sort_values(
        [
            "service_date",
            "scheduled_departure_sec",
        ]
    )

    combined_path = (
        OUTPUT_DIR
        / "daly_powell_all_v2.csv"
    )

    combined.to_csv(
        combined_path,
        index=False,
    )

    print()
    print("==============================")
    print("V2 PIPELINE COMPLETE")
    print("==============================")

    print(
        f"Months processed: "
        f"{combined['source_month'].nunique()}"
    )

    print(
        f"Total journeys: "
        f"{len(combined):,}"
    )

    print(
        f"Unique service dates: "
        f"{combined['service_date'].nunique():,}"
    )

    print(
        "Date range:",
        combined["service_date"]
        .min()
        .date(),
        "to",
        combined["service_date"]
        .max()
        .date(),
    )

    print()
    print("Journeys by month:")

    print(
        combined.groupby(
            "source_month"
        ).size().to_string()
    )

    print()
    print(
        f"Combined file: "
        f"{combined_path}"
    )


if __name__ == "__main__":
    main()

