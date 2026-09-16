from pathlib import Path

import numpy as np
import pandas as pd


SEGMENT_FILE = Path(
    "reports/week5_reliability_segments.csv"
)

CONCENTRATION_FILE = Path(
    "reports/week5_late_tax_concentration.csv"
)

OUTPUT_FILE = Path(
    "reports/week5_operational_hotspots.csv"
)

MIN_SAMPLE_SIZE = 30


def assign_priority_tier(row):
    if row["trips"] < MIN_SAMPLE_SIZE:
        return "Insufficient Sample"

    if row["pareto_80_flag"]:
        return "P1 - Primary Hotspot"

    if row["late_tax_share_pct"] >= 5:
        return "P2 - High Burden"

    if row["reliability_segment"] in {
        "Critical",
        "Chronic",
        "Acute",
    }:
        return "P3 - Reliability Watch"

    return "Monitor"


def percentile_score(series):
    """
    Convert a metric into a 0-100 percentile score.
    Higher values receive higher scores.
    """
    return (
        series.rank(
            method="average",
            pct=True,
        )
        * 100
    )


def main():
    segments = pd.read_csv(SEGMENT_FILE)
    concentration = pd.read_csv(CONCENTRATION_FILE)

    # ---------------------------------------------------------
    # Validate merge keys
    # ---------------------------------------------------------

    keys = [
        "route_id",
        "time_period",
    ]

    if segments.duplicated(keys).any():
        raise AssertionError(
            "Duplicate route × time-period rows "
            "in segmentation file."
        )

    if concentration.duplicated(keys).any():
        raise AssertionError(
            "Duplicate route × time-period rows "
            "in concentration file."
        )

    # ---------------------------------------------------------
    # Select segmentation metrics
    # ---------------------------------------------------------

    segment_metrics = segments[
        [
            "route_id",
            "time_period",
            "avg_late_severity_min",
            "p90_lateness_min",
            "reliability_segment",
        ]
    ]

    hotspots = concentration.merge(
        segment_metrics,
        on=keys,
        how="left",
        validate="one_to_one",
    )

    if hotspots["reliability_segment"].isna().any():
        raise AssertionError(
            "Some concentration groups did not match "
            "reliability segmentation."
        )

    # ---------------------------------------------------------
    # Eligibility
    # ---------------------------------------------------------

    hotspots["priority_eligible"] = (
        hotspots["trips"] >= MIN_SAMPLE_SIZE
    )

    # ---------------------------------------------------------
    # Percentile components
    #
    # Only eligible groups are scored.
    # ---------------------------------------------------------

    eligible_mask = hotspots["priority_eligible"]

    eligible = hotspots.loc[
        eligible_mask
    ].copy()

    eligible["burden_score"] = percentile_score(
        eligible["late_tax_share_pct"]
    )

    eligible["frequency_score"] = percentile_score(
        eligible["late_trip_pct"]
    )

    # Groups with no late trips have NaN severity.
    # Treat as zero severity for prioritization.
    eligible["severity_metric"] = (
        eligible["avg_late_severity_min"]
        .fillna(0)
    )

    eligible["severity_score"] = percentile_score(
        eligible["severity_metric"]
    )

    eligible["priority_score"] = (
        0.60 * eligible["burden_score"]
        + 0.25 * eligible["frequency_score"]
        + 0.15 * eligible["severity_score"]
    )

    hotspots["burden_score"] = np.nan
    hotspots["frequency_score"] = np.nan
    hotspots["severity_score"] = np.nan
    hotspots["priority_score"] = np.nan

    score_columns = [
        "burden_score",
        "frequency_score",
        "severity_score",
        "priority_score",
    ]

    hotspots.loc[
        eligible.index,
        score_columns,
    ] = eligible[score_columns]

    # ---------------------------------------------------------
    # Priority tiers
    # ---------------------------------------------------------

    hotspots["priority_tier"] = hotspots.apply(
        assign_priority_tier,
        axis=1,
    )

    tier_order = {
        "P1 - Primary Hotspot": 1,
        "P2 - High Burden": 2,
        "P3 - Reliability Watch": 3,
        "Monitor": 4,
        "Insufficient Sample": 5,
    }

    hotspots["_tier_order"] = (
        hotspots["priority_tier"]
        .map(tier_order)
    )

    hotspots = (
        hotspots.sort_values(
            [
                "_tier_order",
                "priority_score",
                "late_tax_share_pct",
            ],
            ascending=[
                True,
                False,
                False,
            ],
        )
        .drop(columns="_tier_order")
        .reset_index(drop=True)
    )

    hotspots["operational_priority_rank"] = np.where(
        hotspots["priority_eligible"],
        hotspots[
            "priority_eligible"
        ].cumsum(),
        np.nan,
    )

    # ---------------------------------------------------------
    # Round presentation metrics
    # ---------------------------------------------------------

    round_columns = [
        "late_trip_pct",
        "excess_late_tax_min",
        "late_tax_share_pct",
        "cumulative_late_tax_share_pct",
        "avg_late_severity_min",
        "p90_lateness_min",
        "burden_score",
        "frequency_score",
        "severity_score",
        "priority_score",
    ]

    hotspots[round_columns] = (
        hotspots[round_columns].round(2)
    )

    # ---------------------------------------------------------
    # Validation
    # ---------------------------------------------------------

    if len(hotspots) != len(concentration):
        raise AssertionError(
            "Row count changed after merge."
        )

    if int(hotspots["trips"].sum()) != 1813:
        raise AssertionError(
            "Trip total no longer reconciles."
        )

    if int(hotspots["late_trips"].sum()) != 121:
        raise AssertionError(
            "Late-trip total no longer reconciles."
        )

    if not np.isclose(
        hotspots["late_tax_share_pct"].sum(),
        100,
        atol=0.1,
    ):
        raise AssertionError(
            "Late Tax shares do not reconcile "
            "to approximately 100%."
        )

    # ---------------------------------------------------------
    # Save
    # ---------------------------------------------------------

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    hotspots.to_csv(
        OUTPUT_FILE,
        index=False,
    )

    # ---------------------------------------------------------
    # Output
    # ---------------------------------------------------------

    print(
        "===== WEEK 5.3: OPERATIONAL HOTSPOTS ====="
    )
    print()

    print(
        "Priority score weights: "
        "60% burden / 25% frequency / "
        "15% severity"
    )

    print(
        f"Minimum sample: {MIN_SAMPLE_SIZE} trips"
    )

    print()

    print("===== PRIORITY TIER COUNTS =====")

    print(
        hotspots["priority_tier"]
        .value_counts()
        .to_string()
    )

    print()

    print("===== HOTSPOT PRIORITY TABLE =====")

    print(
        hotspots[
            [
                "operational_priority_rank",
                "route_id",
                "time_period",
                "trips",
                "late_trip_pct",
                "avg_late_severity_min",
                "late_tax_share_pct",
                "reliability_segment",
                "priority_score",
                "priority_tier",
            ]
        ].to_string(index=False)
    )

    print()
    print("===== TOP OPERATIONAL PRIORITIES =====")

    priorities = hotspots[
        hotspots["priority_tier"].isin(
            [
                "P1 - Primary Hotspot",
                "P2 - High Burden",
            ]
        )
    ]

    print(
        priorities[
            [
                "route_id",
                "time_period",
                "late_tax_share_pct",
                "late_trip_pct",
                "priority_score",
                "priority_tier",
            ]
        ].to_string(index=False)
    )

    print()
    print("===== VALIDATION =====")
    print(f"Groups: {len(hotspots)}")
    print(f"Trips: {int(hotspots['trips'].sum()):,}")
    print(
        f"Late trips: "
        f"{int(hotspots['late_trips'].sum()):,}"
    )
    print(
        f"Late Tax share: "
        f"{hotspots['late_tax_share_pct'].sum():.2f}%"
    )
    print("Validation: PASS")

    print()
    print(f"Saved: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()

