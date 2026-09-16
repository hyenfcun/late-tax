from pathlib import Path

import numpy as np
import pandas as pd


INPUT_FILE = Path("data/processed/late_tax_analytics.csv")
OUTPUT_FILE = Path(
    "reports/week5_late_tax_concentration.csv"
)

LATE_THRESHOLD_MIN = 5.0


def main():
    df = pd.read_csv(INPUT_FILE)

    required_columns = {
        "route_id",
        "time_period",
        "schedule_lateness_min",
        "late_trip_flag",
        "excess_late_tax_min",
    }

    missing = required_columns - set(df.columns)

    if missing:
        raise ValueError(
            f"Missing required columns: {sorted(missing)}"
        )

    # ---------------------------------------------------------
    # Metric consistency checks
    # ---------------------------------------------------------

    expected_late_flag = (
        df["schedule_lateness_min"] >= LATE_THRESHOLD_MIN
    ).astype(int)

    actual_late_flag = (
        df["late_trip_flag"]
        .astype(int)
    )

    late_flag_mismatches = int(
        (expected_late_flag != actual_late_flag).sum()
    )

    if late_flag_mismatches != 0:
        raise AssertionError(
            f"late_trip_flag mismatch: "
            f"{late_flag_mismatches} rows"
        )

    if (df["excess_late_tax_min"] < 0).any():
        raise AssertionError(
            "excess_late_tax_min contains negative values."
        )

    # ---------------------------------------------------------
    # Route × time-period concentration table
    # ---------------------------------------------------------

    concentration = (
        df.groupby(
            ["route_id", "time_period"],
            observed=True,
        )
        .agg(
            trips=("trip_id", "size"),
            late_trips=("late_trip_flag", "sum"),
            excess_late_tax_min=(
                "excess_late_tax_min",
                "sum",
            ),
        )
        .reset_index()
    )

    concentration["late_trip_pct"] = (
        concentration["late_trips"]
        / concentration["trips"]
        * 100
    )

    total_late_tax = (
        concentration["excess_late_tax_min"].sum()
    )

    if total_late_tax <= 0:
        raise AssertionError(
            "Total excess Late Tax must be positive."
        )

    concentration["late_tax_share_pct"] = (
        concentration["excess_late_tax_min"]
        / total_late_tax
        * 100
    )

    concentration = (
        concentration.sort_values(
            "excess_late_tax_min",
            ascending=False,
        )
        .reset_index(drop=True)
    )

    concentration["late_tax_rank"] = (
        np.arange(1, len(concentration) + 1)
    )

    concentration[
        "cumulative_late_tax_share_pct"
    ] = (
        concentration["late_tax_share_pct"]
        .cumsum()
    )

    # ---------------------------------------------------------
    # Pareto indicators
    # ---------------------------------------------------------

    concentration["pareto_80_flag"] = (
        concentration[
            "cumulative_late_tax_share_pct"
        ] <= 80
    )

    # Include the first group that crosses 80%.
    crosses_80 = (
        concentration[
            "cumulative_late_tax_share_pct"
        ] >= 80
    )

    if crosses_80.any():
        first_cross_idx = crosses_80.idxmax()

        concentration.loc[
            :first_cross_idx,
            "pareto_80_flag",
        ] = True

    # ---------------------------------------------------------
    # Round presentation metrics
    # ---------------------------------------------------------

    round_columns = [
        "late_trip_pct",
        "excess_late_tax_min",
        "late_tax_share_pct",
        "cumulative_late_tax_share_pct",
    ]

    concentration[round_columns] = (
        concentration[round_columns].round(2)
    )

    # ---------------------------------------------------------
    # Validation
    # ---------------------------------------------------------

    grouped_trips = int(
        concentration["trips"].sum()
    )

    grouped_late_trips = int(
        concentration["late_trips"].sum()
    )

    source_late_trips = int(
        df["late_trip_flag"].sum()
    )

    share_total = float(
        concentration[
            "late_tax_share_pct"
        ].sum()
    )

    if grouped_trips != len(df):
        raise AssertionError(
            "Grouped trips do not match source dataset."
        )

    if grouped_late_trips != source_late_trips:
        raise AssertionError(
            "Grouped late trips do not match source dataset."
        )

    if not np.isclose(
        concentration[
            "excess_late_tax_min"
        ].sum(),
        df["excess_late_tax_min"].sum(),
        atol=0.01,
    ):
        raise AssertionError(
            "Grouped Late Tax does not reconcile "
            "to source dataset."
        )

    # ---------------------------------------------------------
    # Save
    # ---------------------------------------------------------

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    concentration.to_csv(
        OUTPUT_FILE,
        index=False,
    )

    # ---------------------------------------------------------
    # Business summary
    # ---------------------------------------------------------

    top_3_share = (
        concentration
        .head(3)["late_tax_share_pct"]
        .sum()
    )

    top_5_share = (
        concentration
        .head(5)["late_tax_share_pct"]
        .sum()
    )

    pareto_groups = int(
        concentration["pareto_80_flag"].sum()
    )

    # ---------------------------------------------------------
    # Print results
    # ---------------------------------------------------------

    print(
        "===== WEEK 5.2: LATE-TAX CONCENTRATION ====="
    )
    print()

    print(f"Input: {INPUT_FILE}")
    print(f"Trips analyzed: {len(df):,}")
    print(
        f"Late trips: {source_late_trips:,} "
        f"({source_late_trips / len(df) * 100:.2f}%)"
    )
    print(
        f"Total excess Late Tax: "
        f"{total_late_tax:.2f} minutes"
    )

    print()

    print(
        "===== ROUTE × TIME-PERIOD "
        "LATE-TAX CONCENTRATION ====="
    )

    print(
        concentration[
            [
                "late_tax_rank",
                "route_id",
                "time_period",
                "trips",
                "late_trips",
                "late_trip_pct",
                "excess_late_tax_min",
                "late_tax_share_pct",
                "cumulative_late_tax_share_pct",
                "pareto_80_flag",
            ]
        ].to_string(index=False)
    )

    print()
    print("===== PARETO SUMMARY =====")

    print(
        f"Top 3 groups account for "
        f"{top_3_share:.2f}% of total Late Tax"
    )

    print(
        f"Top 5 groups account for "
        f"{top_5_share:.2f}% of total Late Tax"
    )

    print(
        f"{pareto_groups} of "
        f"{len(concentration)} groups are needed "
        f"to reach at least 80% of total Late Tax"
    )

    print()
    print("===== VALIDATION =====")

    print(
        f"Grouped trips: {grouped_trips:,}"
    )

    print(
        f"Grouped late trips: "
        f"{grouped_late_trips:,}"
    )

    print(
        f"Late Tax share total: "
        f"{share_total:.2f}%"
    )

    print(
        f"late_trip_flag mismatches: "
        f"{late_flag_mismatches}"
    )

    print("Validation: PASS")

    print()
    print(f"Saved: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()

