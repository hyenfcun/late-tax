from pathlib import Path
import pandas as pd


# ============================================================
# WEEK 6.1 — BUILD BI-READY DATASET
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

FACT_PATH = PROJECT_ROOT / "data" / "processed" / "late_tax_analytics.csv"
HOTSPOT_PATH = PROJECT_ROOT / "reports" / "week5_operational_hotspots.csv"

OUTPUT_DIR = PROJECT_ROOT / "data" / "bi"

FACT_OUTPUT = OUTPUT_DIR / "late_tax_dashboard.csv"
HOTSPOT_OUTPUT = OUTPUT_DIR / "operational_hotspots.csv"


# ============================================================
# VALIDATION HELPERS
# ============================================================

def require_columns(df, required_columns, dataset_name):
    missing = [c for c in required_columns if c not in df.columns]

    if missing:
        raise ValueError(
            f"{dataset_name} is missing required columns:\n"
            + "\n".join(f"  - {c}" for c in missing)
        )


# ============================================================
# LOAD DATA
# ============================================================

print("\n===== WEEK 6.1: BUILD BI DATASET =====\n")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print(f"Loading trip-level analytics:\n{FACT_PATH}")
fact = pd.read_csv(FACT_PATH)

print(f"\nLoading Week 5 hotspot output:\n{HOTSPOT_PATH}")

if not HOTSPOT_PATH.exists():
    raise FileNotFoundError(
        "\nWeek 5 hotspot output was not found:\n"
        f"{HOTSPOT_PATH}\n\n"
        "Do not rebuild Week 5 logic inside Power BI.\n"
        "Confirm the Week 5 report file exists first."
    )

hotspots = pd.read_csv(HOTSPOT_PATH)


# ============================================================
# VALIDATE SOURCE SCHEMA
# ============================================================

required_fact_columns = [
    "trip_id",
    "service_date",
    "route_id",
    "scheduled_departure",
    "arrival_delay_min",
    "departure_delay_min",
    "travel_time_delta_min",
    "source_month",
    "calendar_date",
    "calendar_day_of_week",
    "calendar_year_month",
    "scheduled_clock_hour",
    "time_period",
    "schedule_lateness_min",
    "route_baseline_delay_min",
    "route_baseline_sample_size",
    "baseline_reliable_flag",
    "excess_late_tax_min",
    "late_trip_flag",
    "severe_delay_flag",
]

required_hotspot_columns = [
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

require_columns(
    fact,
    required_fact_columns,
    "late_tax_analytics.csv",
)

require_columns(
    hotspots,
    required_hotspot_columns,
    "week5_operational_hotspots.csv",
)


# ============================================================
# BASIC SOURCE CHECKS
# ============================================================

source_rows = len(fact)

print("\n===== SOURCE CHECK =====")
print(f"Trip rows: {source_rows:,}")
print(f"Unique trips: {fact['trip_id'].nunique():,}")
print(f"Routes: {fact['route_id'].nunique()}")
print(f"Route × time-period groups: {fact.groupby(['route_id', 'time_period']).ngroups}")


# ============================================================
# PREPARE DATE / REPORTING FIELDS
# ============================================================

fact["calendar_date"] = pd.to_datetime(
    fact["calendar_date"],
    errors="coerce",
)

if fact["calendar_date"].isna().any():
    raise ValueError(
        "calendar_date contains values that could not be parsed."
    )

fact["calendar_year"] = fact["calendar_date"].dt.year
fact["calendar_month_number"] = fact["calendar_date"].dt.month
fact["calendar_month_name"] = fact["calendar_date"].dt.month_name()
fact["calendar_quarter"] = (
    "Q" + fact["calendar_date"].dt.quarter.astype(str)
)

fact["route_time_key"] = (
    fact["route_id"].astype(str)
    + " | "
    + fact["time_period"].astype(str)
)

hotspots["route_time_key"] = (
    hotspots["route_id"].astype(str)
    + " | "
    + hotspots["time_period"].astype(str)
)


# ============================================================
# PREPARE WEEK 5 HOTSPOT FIELDS
# ============================================================

hotspot_keep_columns = [
    "route_time_key",
    "trips",
    "late_trip_pct",
    "avg_late_severity_min",
    "late_tax_share_pct",
    "reliability_segment",
    "priority_score",
    "priority_tier",
]

if "operational_priority_rank" in hotspots.columns:
    hotspot_keep_columns.append("operational_priority_rank")

hotspot_lookup = hotspots[hotspot_keep_columns].copy()

hotspot_lookup = hotspot_lookup.rename(
    columns={
        "trips": "segment_trips",
        "late_trip_pct": "segment_late_trip_pct",
        "avg_late_severity_min": "segment_avg_late_severity_min",
        "late_tax_share_pct": "segment_late_tax_share_pct",
        "priority_score": "segment_priority_score",
        "priority_tier": "segment_priority_tier",
        "reliability_segment": "segment_reliability_segment",
        "operational_priority_rank": "segment_priority_rank",
    }
)


# ============================================================
# MERGE TRIP DATA WITH WEEK 5 OPERATIONAL PRIORITIES
# ============================================================

bi = fact.merge(
    hotspot_lookup,
    on="route_time_key",
    how="left",
    validate="many_to_one",
)


# ============================================================
# VALIDATE MERGE
# ============================================================

if len(bi) != source_rows:
    raise ValueError(
        f"Row count changed after merge: "
        f"{source_rows:,} -> {len(bi):,}"
    )

unmatched = bi["segment_priority_tier"].isna().sum()

if unmatched > 0:
    unmatched_groups = (
        bi.loc[
            bi["segment_priority_tier"].isna(),
            ["route_id", "time_period"]
        ]
        .drop_duplicates()
        .sort_values(["route_id", "time_period"])
    )

    print("\nWARNING: unmatched route × time-period groups:")
    print(unmatched_groups.to_string(index=False))


# ============================================================
# BI DISPLAY FIELDS
# ============================================================

bi["late_trip_label"] = bi["late_trip_flag"].map(
    {
        1: "Late",
        0: "Not Late",
    }
)

bi["severe_delay_label"] = bi["severe_delay_flag"].map(
    {
        1: "Severe Delay",
        0: "Not Severe",
    }
)

bi["sample_status"] = bi["segment_trips"].apply(
    lambda x: (
        "Eligible"
        if pd.notna(x) and x >= 30
        else "Insufficient Sample"
    )
)


# ============================================================
# SORT FOR REPRODUCIBLE OUTPUT
# ============================================================

bi = bi.sort_values(
    [
        "calendar_date",
        "route_id",
        "scheduled_departure",
        "trip_id",
    ]
).reset_index(drop=True)

hotspots_export = hotspots.sort_values(
    [
        "operational_priority_rank"
        if "operational_priority_rank" in hotspots.columns
        else "priority_score"
    ],
    na_position="last",
).reset_index(drop=True)


# ============================================================
# EXPORT
# ============================================================

bi.to_csv(
    FACT_OUTPUT,
    index=False,
)

hotspots_export.to_csv(
    HOTSPOT_OUTPUT,
    index=False,
)


# ============================================================
# FINAL VALIDATION
# ============================================================

print("\n===== BI DATASET OUTPUT =====")

print(
    f"\nCreated:\n"
    f"{FACT_OUTPUT}\n"
    f"Rows: {len(bi):,}\n"
    f"Columns: {len(bi.columns)}"
)

print(
    f"\nCreated:\n"
    f"{HOTSPOT_OUTPUT}\n"
    f"Rows: {len(hotspots_export):,}"
)

print("\n===== PRIORITY TIER COUNTS =====")

tier_counts = (
    hotspots_export["priority_tier"]
    .value_counts(dropna=False)
)

print(tier_counts.to_string())


# ============================================================
# CHECK PRIMARY HOTSPOT
# ============================================================

primary_check = hotspots_export[
    (hotspots_export["route_id"] == "BA:Yellow-N")
    & (hotspots_export["time_period"] == "Overnight")
]

print("\n===== PRIMARY HOTSPOT CHECK =====")

if len(primary_check) == 1:
    check_columns = [
        "route_id",
        "time_period",
        "trips",
        "late_trip_pct",
        "avg_late_severity_min",
        "late_tax_share_pct",
        "priority_score",
        "priority_tier",
    ]

    print(
        primary_check[check_columns]
        .to_string(index=False)
    )
else:
    print(
        "WARNING: Expected exactly one "
        "BA:Yellow-N × Overnight row."
    )


# ============================================================
# FINAL STATUS
# ============================================================

print("\n===== VALIDATION =====")

print(
    "PASS - trip-level row count preserved"
    if len(bi) == source_rows
    else "FAIL - trip-level row count changed"
)

print(
    "PASS - all route × time-period groups matched Week 5"
    if unmatched == 0
    else f"WARNING - {unmatched:,} trip rows unmatched"
)

print("\nRESULT: BI-ready datasets created successfully.")

