from pathlib import Path
import sys

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]

ANALYTICS_FILE = ROOT / "data" / "processed" / "late_tax_analytics.csv"
BI_DASHBOARD_FILE = ROOT / "data" / "bi" / "late_tax_dashboard.csv"
BI_HOTSPOTS_FILE = ROOT / "data" / "bi" / "operational_hotspots.csv"

REPORT_FILE = ROOT / "reports" / "final_validation.txt"

WEEK6_EVIDENCE = [
    ROOT / "reports" / "week6" / "Executive_Overview.png",
    ROOT / "reports" / "week6" / "Operation_Hotspots.png",
    ROOT / "reports" / "week6" / "Reliability_Detail.png",
    ROOT / "reports" / "week6" / "Semantic_Model.png",
]

WK7_ARTIFACTS = [
    ROOT / "reports" / "executive_summary.md",
    ROOT / "reports" / "recommendations.md",
    ROOT / "docs" / "architecture.md",
]

REQUIRED_COLUMNS = {
    "trip_id",
    "service_date",
    "route_id",
    "arrival_delay_min",
    "route_baseline_delay_min",
    "excess_late_tax_min",
    "late_trip_flag",
    "severe_delay_flag",
    "time_period",
}

EXPECTED_ROUTES = {
    "BA:Yellow-N",
    "BA:Green-N",
    "BA:Blue-N",
    "BA:Red-N",
}

results = []


def check(name, condition, detail=""):
    status = "PASS" if condition else "FAIL"
    results.append((status, name, detail))


def file_ok(path):
    return path.exists() and path.is_file() and path.stat().st_size > 0


print("\n===== WEEK 7: FINAL PROJECT VALIDATION =====\n")

# --------------------------------------------------
# 1. Core analytics dataset
# --------------------------------------------------

check(
    "Analytics dataset exists",
    file_ok(ANALYTICS_FILE),
    str(ANALYTICS_FILE.relative_to(ROOT)),
)

if not file_ok(ANALYTICS_FILE):
    df = None
else:
    df = pd.read_csv(ANALYTICS_FILE)

if df is not None:

    # --------------------------------------------------
    # 2. Dataset structure
    # --------------------------------------------------

    check(
        "Expected analytics row count",
        len(df) == 1813,
        f"{len(df):,} rows",
    )

    missing_columns = sorted(REQUIRED_COLUMNS - set(df.columns))

    check(
        "Required analytics schema",
        len(missing_columns) == 0,
        (
            "all required columns present"
            if not missing_columns
            else f"missing: {', '.join(missing_columns)}"
        ),
    )

    duplicate_trip_keys = int(
        df.duplicated(subset=["service_date", "trip_id"]).sum()
    )

    check(
        "Unique service-date trip key",
        duplicate_trip_keys == 0,
        f"{duplicate_trip_keys} duplicate service_date + trip_id keys",
    )

    # --------------------------------------------------
    # 3. Metric definitions
    # --------------------------------------------------

    expected_late_flag = (df["arrival_delay_min"] >= 5).astype(int)

    late_flag_mismatches = int(
        (expected_late_flag != df["late_trip_flag"]).sum()
    )

    check(
        "Late-trip definition",
        late_flag_mismatches == 0,
        f"{late_flag_mismatches} mismatches",
    )

    negative_late_tax = int((df["excess_late_tax_min"] < 0).sum())

    check(
        "Late Tax is non-negative",
        negative_late_tax == 0,
        f"{negative_late_tax} negative values",
    )

    # --------------------------------------------------
    # 4. Headline KPI reconciliation
    # --------------------------------------------------

    total_trips = len(df)
    late_trips = int(df["late_trip_flag"].sum())
    late_trip_pct = late_trips / total_trips * 100
    total_late_tax = float(df["excess_late_tax_min"].sum())

    check(
        "Total late trips",
        late_trips == 121,
        f"{late_trips:,}",
    )

    check(
        "Overall late-trip rate",
        abs(late_trip_pct - 6.67) <= 0.02,
        f"{late_trip_pct:.2f}%",
    )

    check(
        "Total Late Tax reconciliation",
        abs(total_late_tax - 1222.38) <= 0.05,
        f"{total_late_tax:,.2f} minutes",
    )

    # --------------------------------------------------
    # 5. Route coverage
    # --------------------------------------------------

    actual_routes = set(df["route_id"].dropna().unique())

    check(
        "Expected route coverage",
        actual_routes == EXPECTED_ROUTES,
        ", ".join(sorted(actual_routes)),
    )

    # --------------------------------------------------
    # 6. Primary hotspot benchmark
    # --------------------------------------------------

    yellow_overnight = df[
        (df["route_id"] == "BA:Yellow-N")
        & (df["time_period"] == "Overnight")
    ]

    yo_trips = len(yellow_overnight)
    yo_late_trips = int(yellow_overnight["late_trip_flag"].sum())
    yo_late_pct = (
        yo_late_trips / yo_trips * 100
        if yo_trips
        else 0
    )
    yo_late_tax = float(
        yellow_overnight["excess_late_tax_min"].sum()
    )
    yo_late_tax_share = (
        yo_late_tax / total_late_tax * 100
        if total_late_tax
        else 0
    )

    check(
        "Yellow-N Overnight trip count",
        yo_trips == 335,
        f"{yo_trips:,}",
    )

    check(
        "Yellow-N Overnight late trips",
        yo_late_trips == 88,
        f"{yo_late_trips:,}",
    )

    check(
        "Yellow-N Overnight late-trip rate",
        abs(yo_late_pct - 26.27) <= 0.02,
        f"{yo_late_pct:.2f}%",
    )

    check(
        "Yellow-N Overnight Late Tax",
        abs(yo_late_tax - 834.58) <= 0.05,
        f"{yo_late_tax:,.2f} minutes",
    )

    check(
        "Yellow-N Overnight Late Tax share",
        abs(yo_late_tax_share - 68.28) <= 0.02,
        f"{yo_late_tax_share:.2f}%",
    )

# --------------------------------------------------
# 7. BI outputs
# --------------------------------------------------

check(
    "BI dashboard dataset exists",
    file_ok(BI_DASHBOARD_FILE),
    str(BI_DASHBOARD_FILE.relative_to(ROOT)),
)

check(
    "Operational hotspots BI output exists",
    file_ok(BI_HOTSPOTS_FILE),
    str(BI_HOTSPOTS_FILE.relative_to(ROOT)),
)

if file_ok(BI_DASHBOARD_FILE):
    bi_dashboard = pd.read_csv(BI_DASHBOARD_FILE)

    check(
        "BI dashboard dataset is non-empty",
        len(bi_dashboard) > 0,
        f"{len(bi_dashboard):,} rows",
    )

if file_ok(BI_HOTSPOTS_FILE):
    bi_hotspots = pd.read_csv(BI_HOTSPOTS_FILE)

    check(
        "Operational hotspots output is non-empty",
        len(bi_hotspots) > 0,
        f"{len(bi_hotspots):,} rows",
    )

# --------------------------------------------------
# 8. Power BI evidence
# --------------------------------------------------

missing_week6 = [
    p.name for p in WEEK6_EVIDENCE if not file_ok(p)
]

check(
    "Week 6 Power BI evidence",
    len(missing_week6) == 0,
    (
        "4/4 evidence files present"
        if not missing_week6
        else f"missing: {', '.join(missing_week6)}"
    ),
)

# --------------------------------------------------
# 9. Week 7 portfolio artifacts
# --------------------------------------------------

missing_wk7 = [
    str(p.relative_to(ROOT))
    for p in WK7_ARTIFACTS
    if not file_ok(p)
]

check(
    "Week 7 portfolio artifacts",
    len(missing_wk7) == 0,
    (
        "executive summary, recommendations, architecture present"
        if not missing_wk7
        else f"missing: {', '.join(missing_wk7)}"
    ),
)

# --------------------------------------------------
# Output
# --------------------------------------------------

lines = [
    "===== FINAL PROJECT VALIDATION =====",
    "",
]

for status, name, detail in results:
    line = f"[{status}] {name}"
    if detail:
        line += f" — {detail}"
    lines.append(line)

passed = sum(status == "PASS" for status, _, _ in results)
failed = sum(status == "FAIL" for status, _, _ in results)

lines.extend(
    [
        "",
        "===== SUMMARY =====",
        f"Checks passed: {passed}/{len(results)}",
        f"Checks failed: {failed}",
        "",
        (
            "RESULT: ALL VALIDATION CHECKS PASSED"
            if failed == 0
            else "RESULT: VALIDATION FAILED"
        ),
    ]
)

output = "\n".join(lines)

print(output)

REPORT_FILE.parent.mkdir(parents=True, exist_ok=True)
REPORT_FILE.write_text(output + "\n", encoding="utf-8")

print(
    f"\nValidation report saved to: "
    f"{REPORT_FILE.relative_to(ROOT)}"
)

sys.exit(0 if failed == 0 else 1)
