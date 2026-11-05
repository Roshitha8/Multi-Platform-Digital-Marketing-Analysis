# Power BI Dashboard Implementation & Build Guide

## Multi-Platform Digital Marketing Campaign Performance Analysis

This guide provides end-to-end, click-by-click instructions to build a production-grade 4-page interactive Power BI report using **Power BI Desktop**.

---

## 1. Quick Ingestion Setup

### Step 1: Ingest Cleaned Data
1. Open **Power BI Desktop**.
2. Click **Get Data > Text/CSV**.
3. Select `Multi-Platform-Digital-Marketing-Analysis/data/campaign_data_cleaned.csv`.
4. Verify column types:
   - `date`: Date
   - `impressions`, `clicks`, `conversions`: Whole Number
   - `ad_spend`, `revenue`: Decimal Number (Currency)
   - All other columns: Text
5. Click **Load**.

### Step 2: Create Date Dimension and Measures
1. Go to **Modeling > New Table** and paste the `DimDate` DAX code from `powerbi/dax_measures.md`.
2. Switch to **Model View** and drag `DimDate[Date]` to `campaign_data_cleaned[date]` to form a 1-to-many single-direction relationship.
3. Create the `_Measures` table and add all 20 DAX measures from `powerbi/dax_measures.md`.

---

## 2. Color Palette & Visual Theme
- **Primary Navy**: `#1F4E78` (Main bars, primary lines, headers)
- **Secondary Blue**: `#2E75B6` (Clicks, comparisons)
- **Success Green**: `#2E7D32` (Conversions, positive ROAS >= 3.0x)
- **Warning Orange**: `#E65100` (Moderate ROAS 2.0x - 3.0x)
- **Alert Red**: `#C62828` (Underperforming ROAS < 2.0x)
- **Card Background**: `#F2F4F8` with `#1F4E78` border
- **Canvas Background**: `#FFFFFF` or light off-white `#F9FAFC`

---

## 3. Page-by-Page Visual Architecture

### PAGE 1: EXECUTIVE OVERVIEW
**Page Objective**: Provide executive leadership with immediate visibility into global advertising investments, revenue return, and top-level efficiency.

#### Header & Global Slicers (Top Banner, Y: 0-100)
- **Title**: `Multi-Platform Digital Marketing Analytics — Executive Overview`
- **Slicers (Horizontal dropdowns/pills)**:
  1. `DimDate[Year-Month]` (Date range filter)
  2. `campaign_data_cleaned[platform]` (Channel filter)
  3. `campaign_data_cleaned[region]` (Geography filter)

#### KPI Scorecard Cards (Y: 110-210)
Use the **New Card Visual** (or 8 single KPI cards):
1. **Total Spend**: `[Total Spend]` (Format: `$4.49M`)
2. **Total Revenue**: `[Total Revenue]` (Format: `$13.43M`)
3. **Net Profit**: `[Net Profit]` (Format: `$8.93M`)
4. **Overall ROAS**: `[ROAS]` (Format: `2.99x`, colored green)
5. **Total Conversions**: `[Total Conversions]` (Format: `121.9K`)
6. **Overall CTR**: `[CTR]` (Format: `2.22%`)
7. **Average CPC**: `[CPC]` (Format: `$1.05`)
8. **Average CPA**: `[CPA]` (Format: `$36.88`)

#### Main Visuals (Y: 230-700)
- **Visual 1 (Top Left, Line & Clustered Column Chart)**:
  - **Title**: `Monthly Spend vs. Revenue Trajectory`
  - **X-axis**: `DimDate[Year-Month]`
  - **Column values**: `[Total Spend]` (Grey `#7F7F7F`)
  - **Line values**: `[Total Revenue]` (Navy `#1F4E78`), `[Net Profit]` (Green `#2E7D32`)
- **Visual 2 (Top Right, Donut Chart)**:
  - **Title**: `Platform Share of Total Revenue`
  - **Legend**: `campaign_data_cleaned[platform]`
  - **Values**: `[Total Revenue]`
  - **Data labels**: Category + Percentage of Total
- **Visual 3 (Bottom Left, Clustered Bar Chart)**:
  - **Title**: `Platform Advertising Expenditure ($M)`
  - **Y-axis**: `campaign_data_cleaned[platform]`
  - **X-axis**: `[Total Spend]`
- **Visual 4 (Bottom Right, Clustered Bar Chart with Conditional Color)**:
  - **Title**: `Platform Return on Ad Spend (ROAS)`
  - **Y-axis**: `campaign_data_cleaned[platform]`
  - **X-axis**: `[ROAS]`
  - **Reference Line**: Constant at `2.50` (Target ROAS)

---

### PAGE 2: PLATFORM PERFORMANCE
**Page Objective**: In-depth competitive benchmarking across Meta Ads, Google Ads, LinkedIn Ads, and X Ads.

#### Top Visual: Cross-Platform Scorecard Matrix
- **Matrix Visual**:
  - **Rows**: `campaign_data_cleaned[platform]`
  - **Values**: `[Total Spend]`, `[Total Impressions]`, `[Total Clicks]`, `[CTR]`, `[CPC]`, `[Total Conversions]`, `[Conversion Rate]`, `[CPA]`, `[Total Revenue]`, `[ROAS]`
  - **Conditional Formatting**:
    - `[ROAS]`: Data bars or background color gradient (Red `#FFCDD2` to Green `#C8E6C9`).
    - `[CTR]`: Font color bold.

#### Analytical Comparison Visuals (4-Grid Layout)
1. **Top-Left (Clustered Column Chart)**: `CTR Comparison (%)`
   - **X-axis**: `platform`, **Y-axis**: `[CTR]`
2. **Top-Right (Clustered Column Chart)**: `Cost Per Click (CPC $) by Platform`
   - **X-axis**: `platform`, **Y-axis**: `[CPC]`
3. **Bottom-Left (Clustered Column Chart)**: `Conversion Rate (CVR %) by Platform`
   - **X-axis**: `platform`, **Y-axis**: `[Conversion Rate]`
4. **Bottom-Right (Clustered Column Chart)**: `Cost Per Acquisition (CPA $) by Platform`
   - **X-axis**: `platform`, **Y-axis**: `[CPA]`

---

### PAGE 3: CAMPAIGN PERFORMANCE
**Page Objective**: Granular campaign inspection to identify star performers and flag budget drains.

#### Visual 1 (Top Left, Horizontal Bar Chart)**:
- **Title**: `Top 10 Campaigns by Revenue ($)`
- **Y-axis**: `campaign_data_cleaned[campaign_name]` (Filtered: Top 10 by `[Total Revenue]`)
- **X-axis**: `[Total Revenue]`
- **Color**: Navy `#1F4E78`

#### Visual 2 (Top Right, Horizontal Bar Chart)**:
- **Title**: `Top 10 Campaigns by ROAS`
- **Y-axis**: `campaign_data_cleaned[campaign_name]` (Filtered: Top 10 by `[ROAS]`, Spend >= $20K)
- **X-axis**: `[ROAS]`
- **Color**: Green `#2E7D32`

#### Visual 3 (Scatter / Bubble Plot)**:
- **Title**: `Campaign Efficiency Matrix: Spend vs. Revenue vs. ROAS`
- **X-axis**: `[Total Spend]`
- **Y-axis**: `[Total Revenue]`
- **Size**: `[Total Conversions]`
- **Legend**: `campaign_data_cleaned[platform]`
- **Tooltips**: `campaign_name`, `[ROAS]`, `[CPA]`, `[CTR]`

#### Visual 4 (Bottom Table)**:
- **Title**: `Underperforming Campaigns Audit (ROAS < 2.0x & Spend >= $50K)`
- **Columns**: `campaign_id`, `campaign_name`, `platform`, `campaign_type`, `[Total Spend]`, `[Total Revenue]`, `[ROAS]`, `[CPA]`, `[Strategic Action]`

---

### PAGE 4: TREND AND AUDIENCE ANALYSIS
**Page Objective**: Deconstruct performance by temporal patterns, device channels, regional geography, and ad formats.

#### Visual 1 (Left Area Chart / Line Chart)**:
- **Title**: `Monthly Conversion Volume & CPA Trend`
- **X-axis**: `DimDate[Year-Month]`
- **Line 1 (Left Y-axis)**: `[Total Conversions]`
- **Line 2 (Right Y-axis)**: `[CPA]`

#### Visual 2 (Middle Treemap / Bar Chart)**:
- **Title**: `Regional Revenue & ROAS Contribution`
- **Category**: `campaign_data_cleaned[region]`
- **Values**: `[Total Revenue]`
- **Tooltips**: `[ROAS]`, `[Total Spend]`, `[CPA]`

#### Visual 3 (Donut & Column Chart)**:
- **Title**: `Device Conversions and AOV Analysis`
- **Category**: `campaign_data_cleaned[device_type]` (Mobile vs Desktop vs Tablet)
- **Metrics**: `[Total Conversions]`, `[Average Order Revenue]`, `[ROAS]`

#### Visual 4 (Horizontal Bar Chart)**:
- **Title**: `Performance by Campaign Type / Format`
- **Y-axis**: `campaign_data_cleaned[campaign_type]`
- **X-axis**: `[ROAS]`
- **Data Labels**: Show `[ROAS]` and `[Total Revenue]`

---

## 4. Verification Checklist inside Power BI
- [x] All 20 DAX measures verified against database SQL query results.
- [x] Date table single-direction relationship configured.
- [x] Division-by-zero safeguarded with `DIVIDE()` default `0`.
- [x] Currency metrics formatted to `$#,##0.00` and rates to `0.00%`.
