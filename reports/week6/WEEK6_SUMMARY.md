# Week 6 — BI Semantic Model & Power BI Dashboard

## Objective

Transform the Late Tax analytical dataset into a BI-ready semantic model and interactive Power BI dashboard for reliability monitoring and operational prioritization.

## Semantic Model

Implemented a star-schema-style analytical model using:

- FactTrips
- DimDate
- DimOperationalSegment

The model supports filtering and analysis across date, route, time period, reliability segment, and operational priority dimensions.

## Core Measures

Key Power BI measures include:

- Total Trips
- Late Trips
- Late Trip %
- Total Late Tax Minutes
- Late Tax Share %
- Avg Late Severity
- P95 Lateness
- Primary Hotspots

## Dashboard Pages

### 1. Executive Overview

Provides system-level reliability monitoring with:

- Total Trips
- Late Trips
- Late Trip %
- Total Late Tax Minutes
- Primary Hotspots
- Late Tax by Route & Time Period
- Monthly Late Trip Rate trend
- Route, time-period, and month slicers

### 2. Operational Hotspots

Supports operational prioritization using:

- Route × time-period hotspot table
- Priority Score
- Priority Tier
- Reliability Segment
- Late Tax Share
- Average Late Severity
- P95 Lateness
- Route and priority-tier slicers

### 3. Reliability Detail

Provides deeper diagnostic analysis using:

- Late Trip Rate over time
- Average Late Severity by route
- Late Trip Rate by day of week
- Route, time-period, and month slicers

## Headline Metrics

At the full-dataset level:

- 1,813 trips analyzed
- 121 late trips
- 6.67% late-trip rate
- Approximately 1.2K excess late-tax minutes
- 3 primary operational hotspots

## BI Skills Demonstrated

- Power BI
- DAX measures
- Semantic modeling
- Star-schema design
- Fact and dimension tables
- Relationships
- Interactive slicers
- Cross-filtering
- KPI design
- Time-series analysis
- Operational segmentation
- Priority scoring

## Week 6 Evidence

- Executive_Overview.png
- Operation_Hotspots.png
- Reliability_Detail.png
- Semantic_Model.png

## Status

Week 6 BI dataset, semantic model, and dashboard build completed.

