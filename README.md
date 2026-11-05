# Multi-Platform Digital Marketing Campaign Performance Analysis

![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![SQLite](https://img.shields.io/badge/Database-SQLite-003B57?logo=sqlite)
![Pandas](https://img.shields.io/badge/Data%20Analysis-Pandas%20%7C%20NumPy-150458?logo=pandas)
![Visualization](https://img.shields.io/badge/Visualization-Matplotlib%20%7C%20Seaborn-orange)
![Excel](https://img.shields.io/badge/Reporting-Microsoft%20Excel-217346?logo=microsoftexcel)
![Power BI](https://img.shields.io/badge/BI%20Dashboard-Microsoft%20Power%20BI-F2C811?logo=powerbi)
![Pytest](https://img.shields.io/badge/Testing-Pytest%2016%2F16%20Passed-green?logo=pytest)

---

## 1. Project Overview & Business Problem

In modern digital marketing, advertising teams deploy budgets across fragmented ad networks—primarily **Meta Ads (Facebook & Instagram)**, **Google Ads**, **LinkedIn Ads**, and **X Ads (Twitter)**. Without unified cross-channel performance attribution, organizations face critical operational challenges:
- Blind budget allocation leading to capital loss in underperforming channels.
- Siloed ad platform analytics obscuring true unit economics (CTR, CPC, CPA, ROAS).
- Misleading KPI averaging (averaging ratios rather than aggregating numerators and denominators).
- Inability to dynamically reallocate capital based on empirical conversion yield.

This end-to-end data analytics project provides an enterprise-ready analytical solution that cleans, models, analyzes, and visualizes cross-platform marketing investments across **11,747 validated daily campaign records** spanning six months (**January 1, 2026 to June 30, 2026**).

> [!NOTE]
> **Synthetic Data Disclaimer**: This project is built upon a realistic synthetic dataset generated for analytical modeling, portfolio demonstration, and performance evaluation. All findings represent simulated business telemetry and do not disclose actual company advertising results.

---

## 2. Technology Stack

- **Data Processing & Pipeline**: Python 3.10+, Pandas, NumPy
- **Relational Database Management**: SQLite (`digital_marketing.db`), SQL (DDL, Aggregations, CTEs, Windowing)
- **Exploratory Data Analysis**: Matplotlib, Seaborn
- **Spreadsheet Analytics & Dashboarding**: Microsoft Excel (`openpyxl`, Dynamic Formulas, Chart Engines, Conditional Formatting)
- **Business Intelligence**: Microsoft Power BI Desktop (Star Schema Modeling, DAX Measures, Multi-page Dashboard)
- **Automated Testing & QA**: Pytest (16 automated validation test cases)

---

## 3. Project Directory Structure

```
Multi-Platform-Digital-Marketing-Analysis/
│
├── data/
│   ├── raw_campaign_data.csv             # Ingested raw dataset with controlled real-world anomalies (11,814 rows)
│   └── campaign_data_cleaned.csv         # Cleaned, validated, normalized dataset (11,747 rows)
│
├── database/
│   ├── digital_marketing.db              # SQLite database with indexed 'campaign_performance' table
│   ├── marketing_analysis.sql            # 20 production SQL analytical queries with beginner-friendly explanations
│   └── build_database.py                 # Automated DB build and SQL query validation runner
│
├── python/
│   ├── generate_data.py                  # Synthetic dataset generator with industry benchmark parameters
│   ├── data_cleaning.py                  # End-to-end automated ETL and data quality audit engine
│   ├── calculate_kpis.py                 # Core marketing math library with safe-division guardrails
│   └── exploratory_analysis.py           # Publication-ready EDA script generating 10 high-resolution charts
│
├── excel/
│   ├── Digital_Marketing_Analysis.xlsx   # 7-sheet dynamic workbook with formulas, charts, and executive cards
│   └── generate_excel_workbook.py        # Automated programmatic Excel workbook builder
│
├── powerbi/
│   ├── dax_measures.md                   # Complete 20-measure DAX library and DimDate calendar table
│   └── dashboard_guide.md                # 4-page step-by-step visual implementation guide
│
├── output/
│   ├── charts/                           # 10 High-resolution (300 DPI) visualization figures
│   │   ├── 01_platform_spend_vs_revenue.png
│   │   ├── 02_platform_roas_comparison.png
│   │   ├── 03_platform_efficiency_metrics.png
│   │   ├── 04_monthly_spend_revenue_trajectory.png
│   │   ├── 05_monthly_roas_trend.png
│   │   ├── 06_top_bottom_campaigns_roas.png
│   │   ├── 07_regional_performance_breakdown.png
│   │   ├── 08_device_performance_matrix.png
│   │   ├── 09_campaign_type_performance.png
│   │   └── 10_correlation_heatmap.png
│   └── reports/
│       ├── data_quality_report.md        # Comprehensive data cleaning audit log
│       └── business_insights.md          # 10 strategic questions answered with budget recommendations
│
├── tests/
│   ├── test_data_quality.py              # Pytest suite validating schema, nulls, unique IDs, and business logic
│   └── test_kpis.py                      # Pytest suite validating math formulas, DB queries, and Excel structures
│
├── README.md                             # Comprehensive project documentation
├── requirements.txt                      # Project Python dependencies
└── .gitignore                            # Version control exclusion rules
```

---

## 4. Dataset Description & Cleaning Methodology

### Telemetry Dimensions & Schema (14 Columns)
- `record_id`: Unique tracking ID (`REC-000001` to `REC-011747`).
- `date`: Daily timestamp formatted as ISO 8601 (`YYYY-MM-DD`).
- `platform`: Ad network (`Meta Ads`, `Google Ads`, `LinkedIn Ads`, `X Ads`).
- `campaign_id`: Campaign identifier across 44 active campaigns (`CMP-META-001`, `CMP-GOOG-001`, etc.).
- `campaign_name`: Semantic campaign naming reflecting strategy.
- `campaign_type`: Tactical format (`Search`, `Social Feed`, `Retargeting`, `Performance Max`, `Video`, `Lead Generation`, etc.).
- `target_audience`: Demographic & behavioral target audience.
- `device_type`: Traffic channel (`Mobile`, `Desktop`, `Tablet`).
- `region`: Geographic slice (`North America`, `Europe`, `Asia-Pacific`, `Latin America`).
- `impressions`: Raw ad views (Integer).
- `clicks`: Direct link interactions (Integer).
- `ad_spend`: Advertising expenditure in USD ($).
- `conversions`: Verified goal completions / purchases (Integer).
- `revenue`: Top-line gross commercial return in USD ($).

### Data Cleaning & ETL Hygiene Steps:
1. **Deduplication**: 67 exact duplicate records resulting from simulated webhook retry storms were identified and removed.
2. **Text Normalization**: Standardized 700+ inconsistent platform and device casing variants (`meta ads` -> `Meta Ads`, `Twitter` -> `X Ads`, `mobile` -> `Mobile`).
3. **Date Harmonization**: Parsed mixed datetime syntaxes (`MM/DD/YYYY`, `YYYY/MM/DD`) into uniform ISO 8601 `YYYY-MM-DD`.
4. **Missing Value Imputation**: Imputed missing audiences, devices, and numerical metrics using historical campaign-specific median benchmarks.
5. **Telemetry Consistency Guards**: Rectified accounting negative spend refunds (`abs()`), guaranteed `impressions >= clicks`, and capped attribution double-counting glitches (`conversions <= clicks`).

---

## 5. Marketing KPI Mathematical Definitions

To prevent **Simpson's Paradox** and ratio distortion, all aggregate metrics are computed strictly from aggregated numerators and denominators:

| KPI | Formula | Description |
| :--- | :--- | :--- |
| **CTR (Click-Through Rate)** | $\text{CTR} = \left(\frac{\sum \text{Clicks}}{\sum \text{Impressions}}\right) \times 100$ | Creative resonance and interest |
| **CPC (Cost Per Click)** | $\text{CPC} = \frac{\sum \text{Ad Spend}}{\sum \text{Clicks}}$ | Unit cost of acquired site traffic |
| **CPA (Cost Per Acquisition)** | $\text{CPA} = \frac{\sum \text{Ad Spend}}{\sum \text{Conversions}}$ | Capital required to generate one paying customer |
| **CVR (Conversion Rate)** | $\text{CVR} = \left(\frac{\sum \text{Conversions}}{\sum \text{Clicks}}\right) \times 100$ | Landing page purchase intent |
| **ROAS (Return on Ad Spend)** | $\text{ROAS} = \frac{\sum \text{Revenue}}{\sum \text{Ad Spend}}$ | Gross revenue multiple earned per dollar of ad spend |
| **AOR (Average Order Revenue)** | $\text{AOR} = \frac{\sum \text{Revenue}}{\sum \text{Conversions}}$ | Monetization value per conversion |
| **Net Profit** | $\text{Net Profit} = \sum \text{Revenue} - \sum \text{Ad Spend}$ | Gross operating contribution margin |

---

## 6. SQL Database & Analytical Queries

The project imports all cleaned data into an indexed SQLite database (`database/digital_marketing.db`) and executes 20 production queries in `database/marketing_analysis.sql`:

1. `Total Advertising Spend`: Calculates aggregate media investment ($4,496,807.67).
2. `Total Impressions & Clicks`: Calculates 191.97M impressions, 4.26M clicks, and 2.22% overall CTR.
3. `Total Conversions & Revenue`: Evaluates 121,951 conversions, $13.43M revenue, and 2.99x ROAS.
4. `Platform-wise Expenditure`: Breakdown of media budget allocation per network.
5. `Platform-wise CTR`: Benchmarking ad interaction rates (Google 3.44% vs LinkedIn 1.08%).
6. `Platform-wise CPC`: Cost of traffic (X Ads $0.57 vs LinkedIn $7.28).
7. `Platform-wise CPA`: Cost per lead/buyer (Meta $20.21 vs LinkedIn $203.11).
8. `Platform-wise Conversion Rate`: Google (3.82%) and Meta (4.32%) lead conversion efficiency.
9. `Platform-wise ROAS`: Meta (4.09x) and Google (3.68x) dominate capital return.
10. `Highest Revenue Platform`: Google Ads leads with $4.78M (35.57% revenue share).
11. `Top 10 Campaigns`: Ranks highest revenue generators led by Google PMax ($937K) and High Intent Search ($753K).
12. `Lowest 10 Campaigns by ROAS`: Identifies underperforming campaigns (Movie Teasers 1.17x, Competitor Search 1.41x).
13. `Monthly Spend Trajectory`: Tracks seasonal expansion from $667.9K (Jan) to $838.2K (Jun).
14. `Monthly Revenue & Net Profit`: Confirms stable profit scaling from $1.33M (Jan) to $1.66M (Jun).
15. `Monthly ROAS Stability`: Demonstrates steady month-over-month ROAS around 2.99x.
16. `Regional Breakdown`: North America delivers $7.54M (56.1%) at 3.21x ROAS.
17. `Device Conversion Analysis`: Mobile captures 65.6% volume; Desktop delivers 4.60% CVR and $158.03 AOR.
18. `Campaign Type Strategy`: Search, Shopping, and Retargeting deliver > 5.0x ROAS.
19. `High-Spend Low-Conversion Audit`: Flags 6 campaigns spending >$80K with ROAS < 2.0x.
20. `Budget Optimization Tiers`: Automatically categorizes 44 campaigns into 'SCALE UP', 'MAINTAIN', or 'REDUCE'.

---

## 7. Professional Excel Analysis Workbook

The file `excel/Digital_Marketing_Analysis.xlsx` contains 7 structured sheets:
- **Sheet 1: `Dashboard`**: Executive presentation view featuring 6 large KPI scorecards, a dynamic platform summary table, embedded spend vs. revenue column charts, and monthly trajectory line charts.
- **Sheet 2: `Raw_Data`**: Full 11,814-row audit baseline.
- **Sheet 3: `Cleaned_Data`**: 11,747 rows formatted as an Excel Table with strict number and currency formatting.
- **Sheet 4: `KPI_Calculations`**: High-level dynamic formula scorecard (`SUM`, `SUMIF`, safe division).
- **Sheet 5: `Platform_Analysis`**: Platform-level `SUMIF` summary table and native bar charts.
- **Sheet 6: `Campaign_Analysis`**: 44-campaign granular analysis with `SUMIFS` formulas and conditional formatting (green for ROAS >= 3.0x, red for ROAS < 2.0x).
- **Sheet 7: `Monthly_Trends`**: Month-over-month performance with `SUMIFS` date range formulas and dual-series trendlines.

---

## 8. Power BI Dashboard Architecture

Designed following enterprise Star Schema architecture and documented in `powerbi/dax_measures.md` and `powerbi/dashboard_guide.md`:
- **Page 1: Executive Overview**: High-level KPI cards, Monthly Spend vs Revenue, Platform Revenue Donut, Platform ROAS with Target 2.50x line.
- **Page 2: Platform Performance**: Side-by-side benchmarking of Meta, Google, LinkedIn, and X Ads across CTR, CPC, CPA, CVR, and ROAS.
- **Page 3: Campaign Performance**: Top 10 Campaigns by Revenue, Top 10 by ROAS, Scatter efficiency plot (Spend vs Revenue vs Conversions), and underperformer audit table.
- **Page 4: Trend and Audience Analysis**: Temporal conversion curves, Regional Treemap, Device breakdown (Mobile volume vs Desktop purchasing power), and Campaign Type ROAS.

---

## 9. Key Business Insights & Strategic Recommendations

### Empirical Telemetry Summary (H1 2026)
- **Total Media Spend**: **$4,496,807.67**
- **Total Revenue**: **$13,433,039.78**
- **Net Operating Profit**: **$8,936,232.11** (66.5% Net Margin)
- **Overall ROAS**: **2.99x**
- **Customer Conversions**: **121,951**

```
Platform Scorecard:
├── Google Ads:   $1,296,803 Spend | $4,777,473 Revenue | 3.68x ROAS | $25.75 CPA
├── Meta Ads:     $  860,545 Spend | $3,515,670 Revenue | 4.09x ROAS | $20.21 CPA
├── LinkedIn Ads: $1,253,996 Spend | $3,197,549 Revenue | 2.55x ROAS | $203.11 CPA
└── X Ads:        $1,085,463 Spend | $1,942,348 Revenue | 1.79x ROAS | $37.89 CPA
```

### Capital Reallocation: The 70-20-10 Model
1. **Scale Meta Ads (+57% Budget)**: Increase Meta spend from $860K to $1.35M. Meta generates the lowest CPA ($20.21) and highest ROAS (4.09x), driven by VIP Loyalty Rewards (7.72x ROAS) and Catalog Retargeting (5.38x ROAS).
2. **Double Down on Google Intent (+21% Budget)**: Increase Google spend from $1.30M to $1.57M focusing strictly on PMax (5.11x) and High-Intent Brand Search (5.50x).
3. **Restructure X Ads (-58% Budget Cut)**: Slash X Ads spend from $1.08M to $450K. Eliminate costly trend takeovers and entertainment teasers (1.17x ROAS); preserve high-converting App Install Sprints (2.18x ROAS).
4. **Pause Competitor Conquesting**: Google Search Competitor Conquest delivered a weak 1.41x ROAS at an inflated $93.52 CPA. Reallocate funds to shopping bestsellers.
5. **Projected Impact**: Capital reallocation increases overall marketing ROAS from **2.99x to 3.52x**, generating an estimated **+$2.38M in incremental revenue** on fixed budget.

---

## 10. Automated Testing & Validation

Automated test execution using `pytest` verifies 16 distinct assertions:
```bash
$ pytest tests -v
============================= test session starts =============================
tests/test_data_quality.py::test_raw_data_exists_and_meets_volume_target PASSED
tests/test_data_quality.py::test_cleaned_data_exists_and_meets_volume_target PASSED
tests/test_data_quality.py::test_cleaned_data_has_unique_record_ids PASSED
tests/test_data_quality.py::test_cleaned_data_has_zero_nulls PASSED
tests/test_data_quality.py::test_clicks_do_not_exceed_impressions PASSED
tests/test_data_quality.py::test_conversions_do_not_exceed_clicks PASSED
tests/test_data_quality.py::test_spend_and_revenue_are_non_negative PASSED
tests/test_data_quality.py::test_categorical_standardization PASSED
tests/test_data_quality.py::test_date_iso_format_and_six_month_range PASSED
tests/test_data_quality.py::test_minimum_campaign_count PASSED
tests/test_kpis.py::test_safe_divide PASSED
tests/test_kpis.py::test_aggregate_kpi_calculations PASSED
tests/test_kpis.py::test_sqlite_database_and_all_twenty_queries PASSED
tests/test_kpis.py::test_excel_workbook_sheets_and_tables PASSED
tests/test_kpis.py::test_charts_generated PASSED
tests/test_kpis.py::test_markdown_reports_exist PASSED

============================= 16 passed in 8.86s ==============================
```

---

## 11. Quickstart & Execution Guide

### Prerequisites
- Python 3.10+ installed
- Windows, macOS, or Linux

### Installation
```bash
# Clone or navigate to the project directory
cd Multi-Platform-Digital-Marketing-Analysis

# Install dependencies
pip install -r requirements.txt
```

### Reproduce the Entire Project from Scratch
Run each stage sequentially or execute the automated pipeline:
```bash
# 1. Generate synthetic dataset with realistic anomalies
python python/generate_data.py

# 2. Perform automated data cleaning and quality audit
python python/data_cleaning.py

# 3. Build SQLite database and run 20 analytical queries
python database/build_database.py

# 4. Generate professional multi-tab Excel workbook
python excel/generate_excel_workbook.py

# 5. Conduct EDA and generate 10 publication charts
python python/exploratory_analysis.py

# 6. Execute all automated validation test cases
pytest tests -v
```

---

## 12. Project Completion Checklist

- [x] **Synthetic dataset**: 11,814 raw records across 44 campaigns covering 6 months.
- [x] **Data cleaning using Pandas**: 11,747 validated records resolving missing values, duplicates, and format errors.
- [x] **Data quality report**: Saved at `output/reports/data_quality_report.md`.
- [x] **SQLite database**: Fully modeled at `database/digital_marketing.db`.
- [x] **20+ SQL analytical queries**: Production queries in `database/marketing_analysis.sql` with safe division.
- [x] **Excel analysis workbook**: 7-sheet dynamic workbook at `excel/Digital_Marketing_Analysis.xlsx`.
- [x] **Python EDA & 10 charts**: High-resolution charts saved in `output/charts/`.
- [x] **Power BI dashboard & DAX measures**: Documented in `powerbi/dax_measures.md` and `powerbi/dashboard_guide.md`.
- [x] **Business insights report**: 10 strategic questions answered in `output/reports/business_insights.md`.
- [x] **Automated test cases passed**: 16 out of 16 pytest assertions passed cleanly.
- [x] **GitHub-ready README**: Complete portfolio-grade documentation.
