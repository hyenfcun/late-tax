from pathlib import Path
import zipfile
import pandas as pd

HISTORICAL_DIR = Path("data/raw/historical")
REPORT_FILE = Path("reports/extraction_funnel_report.md")

DALY_CITY = {"901901", "901902", "901903"}
POWELL = {"901301", "901302"}

OBS_COLUMNS = [
    "trip_id",
    "service_date",
    "route_id",
    "agency_id",
    "from_stop_id",
    "to_stop_id",
]

def get_valid_trip_ids(zf):
    with zf.open("stop_times.txt") as f:
        stop_times = pd.read_csv(
            f,
            usecols=["trip_id", "stop_id", "stop_sequence"],
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

        total_obs_rows = 0
        bart_rows = 0
        valid_trip_rows = 0
        origin_rows = 0
        destination_rows = 0

        all_dates = set()
        bart_dates = set()
        valid_trip_dates = set()
        origin_dates = set()
        destination_dates = set()

        origins = []
        destinations = []

        with zf.open("stop_observations.txt") as f:
            for chunk in pd.read_csv(
                f,
                usecols=OBS_COLUMNS,
                dtype=str,
                chunksize=250_000,
            ):
                total_obs_rows += len(chunk)

                all_dates.update(
                    chunk["service_date"]
                    .dropna()
                    .unique()
                )

                bart = chunk[
                    chunk["agency_id"] == "BA"
                ].copy()

                bart_rows += len(bart)

                bart_dates.update(
                    bart["service_date"]
                    .dropna()
                    .unique()
                )

                valid = bart[
                    bart["trip_id"].isin(valid_trip_ids)
                ].copy()

                valid_trip_rows += len(valid)

                valid_trip_dates.update(
                    valid["service_date"]
                    .dropna()
                    .unique()
                )

                origin = valid[
                    valid["from_stop_id"].isin(
                        DALY_CITY
                    )
                ].copy()

                destination = valid[
                    valid["to_stop_id"].isin(
                        POWELL
                    )
                ].copy()

                origin_rows += len(origin)
                destination_rows += len(destination)

                origin_dates.update(
                    origin["service_date"]
                    .dropna()
                    .unique()
                )

                destination_dates.update(
                    destination["service_date"]
                    .dropna()
                    .unique()
                )

                if not origin.empty:
                    origins.append(
                        origin[
                            [
                                "trip_id",
                                "service_date",
                                "route_id",
                            ]
                        ]
                    )

                if not destination.empty:
                    destinations.append(
                        destination[
                            [
                                "trip_id",
                                "service_date",
                                "route_id",
                            ]
                        ]
                    )

        if origins and destinations:
            origins_df = pd.concat(
                origins,
                ignore_index=True,
            )

            destinations_df = pd.concat(
                destinations,
                ignore_index=True,
            )

            matched = origins_df.merge(
                destinations_df,
                on=[
                    "trip_id",
                    "service_date",
                    "route_id",
                ],
                how="inner",
            )

            matched_rows = len(matched)
            matched_dates = (
                matched["service_date"].nunique()
            )
        else:
            matched_rows = 0
            matched_dates = 0

        results.append({
            "month": month,
            "scheduled_trip_ids": len(valid_trip_ids),
            "total_obs_rows": total_obs_rows,
            "all_dates": len(all_dates),
            "bart_rows": bart_rows,
            "bart_dates": len(bart_dates),
            "valid_trip_rows": valid_trip_rows,
            "valid_trip_dates": len(valid_trip_dates),
            "origin_rows": origin_rows,
            "origin_dates": len(origin_dates),
            "destination_rows": destination_rows,
            "destination_dates": len(destination_dates),
            "matched_rows": matched_rows,
            "matched_dates": matched_dates,
        })


lines = []

lines.append("# Week 2 — Extraction Funnel Audit")
lines.append("")
lines.append(
    "This report identifies where historical observations "
    "are lost between the raw 511 source and the final "
    "Daly City → Powell analytical dataset."
)
lines.append("")

lines.append("| Month | Scheduled Trip IDs | BART Obs Rows | BART Dates | Valid Trip Rows | Valid Dates | Origin Rows | Destination Rows | Matched Rows | Matched Dates |")
lines.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|")

for r in results:
    lines.append(
        f"| {r['month']} "
        f"| {r['scheduled_trip_ids']} "
        f"| {r['bart_rows']} "
        f"| {r['bart_dates']} "
        f"| {r['valid_trip_rows']} "
        f"| {r['valid_trip_dates']} "
        f"| {r['origin_rows']} "
        f"| {r['destination_rows']} "
        f"| {r['matched_rows']} "
        f"| {r['matched_dates']} |"
    )

lines.append("")
lines.append("## Diagnostic Logic")
lines.append("")
lines.append(
    "- If BART Dates are already low, the historical observation "
    "source itself is sparse."
)
lines.append(
    "- If BART Dates are high but Valid Dates drop sharply, "
    "the scheduled-trip matching logic is the bottleneck."
)
lines.append(
    "- If Valid Dates remain high but Matched Dates drop sharply, "
    "the Daly City/Powell origin-destination merge requires review."
)

REPORT_FILE.write_text(
    "\n".join(lines),
    encoding="utf-8",
)

print()
print(f"Report saved to: {REPORT_FILE}")
