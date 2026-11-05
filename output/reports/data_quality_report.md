# Data Quality & Cleaning Audit Report

## 1. Executive Summary
This report documents the automated end-to-end data audit and cleaning procedure performed on the raw digital marketing campaign dataset (`raw_campaign_data.csv`). All data quality anomalies were methodically addressed following industry-standard ETL hygiene principles.

---

## 2. Dataset Dimension Summary
| Metric | Count / Status |
| :--- | :--- |
| **Initial Raw Records** | 11,814 |
| **Duplicate Rows Identified & Removed** | 67 |
| **Final Cleaned Record Count** | 11,747 |
| **Target Date Range** | 2026-01-01 to 2026-06-30 |
| **Active Platforms** | Meta Ads, Google Ads, LinkedIn Ads, X Ads |
| **Active Distinct Campaigns** | 44 |

---

## 3. Detailed Data Quality Audit & Cleaning Decisions

### A. Duplicate Records
- **Identified**: 67 exact duplicate rows caused by upstream webhook retry duplications.
- **Action Taken**: Filtered out all duplicate instances, retaining canonical first records. Regenerated contiguous unique primary keys (`REC-000001` onwards).

### B. Text & Categorical Normalization
- **Platform Inconsistencies**: 722 records had mixed casing or legacy naming (e.g. `meta ads`, `Twitter`, `GOOGLE ADS`). Standardized into four official platform categories: `Meta Ads`, `Google Ads`, `LinkedIn Ads`, `X Ads`.
- **Device Types**: 60 records had missing or unstandardized casing. Standardized to Title Case (`Mobile`, `Desktop`, `Tablet`) and missing entries imputed with dominant category (`Mobile`).
- **Target Audience**: 75 records had missing audience descriptors. Imputed via historical campaign ID metadata mappings.
- **Campaign Names**: Cleaned leading and trailing whitespace artifacts.

### C. Date Standardization
- **Inconsistent Formats**: 982 records had non-standard date syntax (`MM/DD/YYYY`, `YYYY/MM/DD`, `DD-MM-YYYY`). Standardized all dates to ISO 8601 `YYYY-MM-DD`.

### D. Numerical Metrics Validation & Imputation
- **Negative Ad Spend**: 12 records with negative values (representing accounting reversals/chargebacks) were rectified to positive ad spend via `abs()`.
- **Missing Impressions**: 35 records imputed via campaign-specific median benchmark CTR.
- **Missing Clicks**: 30 records imputed via campaign-specific median benchmarks.
- **Missing Ad Spend**: 25 records imputed using campaign median spend per slice.
- **Missing Revenue**: 30 records imputed using conversion count and campaign Average Order Value (AOV).
- **Logical Inconsistency (Clicks > Impressions)**: 15 instances adjusted by ensuring `impressions = clicks + buffer`.
- **Logical Inconsistency (Conversions > Clicks)**: 10 attribution over-reporting glitches capped at `conversions = clicks`.

---

## 4. Final Quality Assurance Validation Checks
| Validation Check | Expected Rule | Audit Result | Status |
| :--- | :--- | :--- | :--- |
| **Unique Record ID** | Count == Distinct Count | 11,747 / 11,747 | PASSED |
| **Missing Values (Nulls)** | 0 across all columns | 0 nulls | PASSED |
| **Impressions vs Clicks** | Impressions >= Clicks | Min diff: 25 | PASSED |
| **Clicks vs Conversions** | Clicks >= Conversions | Min diff: 0 | PASSED |
| **Spend Non-negativity** | Ad Spend >= $0.00 | Min spend: $34.63 | PASSED |
| **Revenue Non-negativity** | Revenue >= $0.00 | Min revenue: $0.00 | PASSED |
