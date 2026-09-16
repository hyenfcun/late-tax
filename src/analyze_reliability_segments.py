from pathlib import Path

import numpy as np
import pandas as pd


INPUT_FILE = Path("data/processed/late_tax_analytics.csv")
OUTPUT_FILE = Path("reports/week5_reliability_segments.csv")

MIN_SAMPLE_SIZE = 30


def classify_segment(
    trips: int,
    late_trip_pct: float,
    avg_late_severity_min: float,
    frequency_cutoff: float,
    severity_cutoff: float,
) -> str:
    if trips < MIN_SAMPLE_SIZE:
        return "Insufficient Sample"

    high_frequency = late_trip_pct >= frequency_cutoff
    high_severity = avg_late_severity_min >= severity_cutoff

    if high_frequency and high_severity:
        return "Critical"

    if high_frequency:
        return "Chronic"

    if high_severity:
        return "Acute"

    return "Reliable"


def main():
    df = pd.read_csv(INPUT_FILE)

    required_columns = {
        "route_id",
        "time_period",
        "schedule_lateness_min",
        "arrival_delay_min",
        "late_trip_flag",
    }

    missing = required_columns - set(df.columns)

    if missing:
        raise ValueError(
            f"Missing required columns: {sorted(missing)}"
        )

    # Use the canonical late-trip feature created
    # in the analytical feature pipeline.
    df["is_late"] = (
        df["late_trip_flag"].astype(int)
    )

    # Severity is the actual arrival delay
    # among trips classified as late.
    df["late_severity_min"] = np.where(
        df["is_late"] == 1,
        df["arrival_delay_min"],
        np.nan,
    )

    segments = (
        df.groupby(
            ["route_id", "time_period"],
            observed=True,
        )
        .agg(
            trips=("schedule_lateness_min", "size"),
            avg_lateness_min=(
                "schedule_lateness_min",
                "mean",
            ),
            median_lateness_min=(
                "schedule_lateness_min",
                "median",
            ),
            p90_lateness_min=(
                "schedule_lateness_min",
                lambda x: x.quantile(0.90),
            ),
            late_trips=("is_late", "sum"),
            avg_late_severity_min=(
                "late_severity_min",
                "mean",
            ),
            max_lateness_min=(
                "schedule_lateness_min",
                "max",
            ),
        )
        .reset_index()
    )

    segments["late_trip_pct"] = (
        segments["late_trips"]
        / segments["trips"]
        * 100
    )

    frequency_cutoff = (
        segments["late_trip_pct"].median()
    )

    severity_cutoff = (
        segments["avg_late_severity_min"]
        .dropna()
        .median()
    )

    segments["reliability_segment"] = segments.apply(
        lambda row: classify_segment(
            row["trips"],
            row["late_trip_pct"],
            (
                row["avg_late_severity_min"]
                if pd.notna(
                    row["avg_late_severity_min"]
                )
                else 0.0
            ),
            frequency_cutoff,
            severity_cutoff,
        ),
        axis=1,
    )

    numeric_columns = [
        "avg_lateness_min",
        "median_lateness_min",
        "p90_lateness_min",
        "late_trip_pct",
        "avg_late_severity_min",
        "max_lateness_min",
    ]

    segments[numeric_columns] = (
        segments[numeric_columns].round(2)
    )

    segment_order = {
        "Critical": 1,
        "Chronic": 2,
        "Acute": 3,
        "Reliable": 4,
        "Insufficient Sample": 5,
    }

    segments["_segment_order"] = (
        segments["reliability_segment"]
        .map(segment_order)
    )

    segments = (
        segments.sort_values(
            [
                "_segment_order",
                "late_trip_pct",
                "avg_late_severity_min",
            ],
            ascending=[
                True,
                False,
                False,
            ],
        )
        .drop(columns="_segment_order")
        .reset_index(drop=True)
    )

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    segments.to_csv(
        OUTPUT_FILE,
        index=False,
    )

    total_late_trips = int(
        segments["late_trips"].sum()
    )

    if segments["trips"].sum() != len(df):
        raise AssertionError(
            "Grouped trip count does not match source dataset."
        )

    if total_late_trips != int(
        df["late_trip_flag"].sum()
    ):
        raise AssertionError(
            "Grouped late-trip count does not match canonical feature."
        )

    print(
        "===== WEEK 5.1: RELIABILITY SEGMENTATION ====="
    )
    print()

    print(f"Input: {INPUT_FILE}")
    print(f"Trips analyzed: {len(df):,}")

    print(
        "Late definition: canonical late_trip_flag "
        "(arrival delay >= 5 minutes)"
    )

    print(
        f"Late trips: {total_late_trips:,} "
        f"({total_late_trips / len(df) * 100:.2f}%)"
    )

    print(
        f"Minimum sample for segmentation: "
        f"{MIN_SAMPLE_SIZE} trips"
    )

    print(
        "Frequency cutoff "
        f"(median late-trip %): "
        f"{frequency_cutoff:.2f}%"
    )

    print(
        "Severity cutoff "
        f"(median late-trip severity): "
        f"{severity_cutoff:.2f} minutes"
    )

    print()
    print("===== SEGMENT COUNTS =====")

    print(
        segments["reliability_segment"]
        .value_counts()
        .to_string()
    )

    print()

    print(
        "===== ROUTE × TIME-PERIOD SEGMENTS ====="
    )

    print(
        segments[
            [
                "route_id",
                "time_period",
                "trips",
                "late_trips",
                "late_trip_pct",
                "avg_late_severity_min",
                "p90_lateness_min",
                "reliability_segment",
            ]
        ].to_string(index=False)
    )

    print()
    print("===== VALIDATION =====")

    print(
        f"Grouped trips: "
        f"{int(segments['trips'].sum()):,}"
    )

    print(
        f"Grouped late trips: "
        f"{total_late_trips:,}"
    )

    print("Canonical late flag: PASS")
    print("Validation: PASS")

    print()
    print(f"Saved: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()

