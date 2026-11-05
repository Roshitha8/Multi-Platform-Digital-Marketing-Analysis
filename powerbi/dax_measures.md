# Power BI DAX Measures & Data Model Specification

## 1. Data Model Overview & Architecture
To ensure enterprise-grade reporting performance and adherence to Power BI best practices, this solution utilizes a **Star Schema** architectural design.

### Relationship Architecture:
- **Fact Table**: `campaign_data_cleaned` (Ingested from `data/campaign_data_cleaned.csv`)
- **Dimension Table**: `DimDate` (Generated via DAX Calendar Table)
- **Relationship**: `DimDate[Date] (1) <---> (*) campaign_data_cleaned[date]` (Single Direction, Active)

---

## 2. Date Dimension Table (DAX DDL)
Create a new calculated table in Power BI Desktop via **Modeling > New Table**:

```dax
DimDate = 
VAR StartDate = DATE(2026, 1, 1)
VAR EndDate = DATE(2026, 6, 30)
RETURN
    ADDCOLUMNS(
        CALENDAR(StartDate, EndDate),
        "Year", YEAR([Date]),
        "Month Number", MONTH([Date]),
        "Month Name", FORMAT([Date], "MMMM"),
        "Month Short", FORMAT([Date], "MMM"),
        "Year-Month", FORMAT([Date], "YYYY-MM"),
        "Quarter", "Q" & FORMAT([Date], "Q"),
        "Day of Week", FORMAT([Date], "dddd"),
        "Day of Week Number", WEEKDAY([Date], 2), -- Monday = 1
        "Is Weekend", IF(WEEKDAY([Date], 2) >= 6, "Weekend", "Weekday")
    )
```
*Sort `Month Short` and `Month Name` by the `Month Number` column.*

---

## 3. Dedicated Measures Table
Best Practice: Create an empty disconnected table named `_Measures` to store all analytical DAX metrics:
```dax
_Measures = { BLANK() }
```

---

## 4. Complete DAX Measures Library

### A. Volume & Spend Measures
```dax
// 1. Total Impressions
Total Impressions = 
SUM(campaign_data_cleaned[impressions])
// Format: #,##0

// 2. Total Clicks
Total Clicks = 
SUM(campaign_data_cleaned[clicks])
// Format: #,##0

// 3. Total Advertising Spend
Total Spend = 
SUM(campaign_data_cleaned[ad_spend])
// Format: $#,##0.00

// 4. Total Conversions
Total Conversions = 
SUM(campaign_data_cleaned[conversions])
// Format: #,##0

// 5. Total Revenue Generated
Total Revenue = 
SUM(campaign_data_cleaned[revenue])
// Format: $#,##0.00

// 6. Net Profit (Operating Margin)
Net Profit = 
[Total Revenue] - [Total Spend]
// Format: $#,##0.00

// 7. Net Profit Margin (%)
Profit Margin Pct = 
DIVIDE([Net Profit], [Total Revenue], 0)
// Format: 0.00%
```

---

### B. Marketing Efficiency KPIs
```dax
// 8. Click-Through Rate (CTR)
CTR = 
DIVIDE([Total Clicks], [Total Impressions], 0)
// Format: 0.00%

// 9. Cost Per Click (CPC)
CPC = 
DIVIDE([Total Spend], [Total Clicks], 0)
// Format: $#,##0.00

// 10. Cost Per Acquisition (CPA)
CPA = 
DIVIDE([Total Spend], [Total Conversions], 0)
// Format: $#,##0.00

// 11. Conversion Rate (CVR)
Conversion Rate = 
DIVIDE([Total Conversions], [Total Clicks], 0)
// Format: 0.00%

// 12. Return On Ad Spend (ROAS)
ROAS = 
DIVIDE([Total Revenue], [Total Spend], 0)
// Format: 0.00x

// 13. Average Order Revenue (AOR)
Average Order Revenue = 
DIVIDE([Total Revenue], [Total Conversions], 0)
// Format: $#,##0.00
```

---

### C. Contextual & Benchmark Variance Measures
```dax
// 14. Target Benchmark ROAS Constant
Target ROAS Benchmark = 2.50

// 15. ROAS Variance vs Benchmark
ROAS Variance vs Target = 
[ROAS] - [Target ROAS Benchmark]
// Format: +0.00x;-0.00x;0.00x

// 16. Platform Spend Share (%)
Platform Spend Share = 
DIVIDE(
    [Total Spend], 
    CALCULATE([Total Spend], ALLSELECTED(campaign_data_cleaned[platform])), 
    0
)
// Format: 0.00%

// 17. Platform Revenue Share (%)
Platform Revenue Share = 
DIVIDE(
    [Total Revenue], 
    CALCULATE([Total Revenue], ALLSELECTED(campaign_data_cleaned[platform])), 
    0
)
// Format: 0.00%

// 18. Strategic Recommendation Flag
Strategic Action = 
SWITCH(
    TRUE(),
    [ROAS] >= 3.20, "SCALE UP (+20% Budget)",
    [ROAS] >= 2.20, "MAINTAIN / OPTIMIZE",
    "REDUCE / RESTRUCTURE (-30% Budget)"
)

// 19. Campaign Rank by Total Revenue
Campaign Revenue Rank = 
IF(
    ISINSCOPE(campaign_data_cleaned[campaign_name]),
    RANKX(ALLSELECTED(campaign_data_cleaned[campaign_name]), [Total Revenue], , DESC, Dense)
)

// 20. Campaign Rank by ROAS
Campaign ROAS Rank = 
IF(
    ISINSCOPE(campaign_data_cleaned[campaign_name]),
    RANKX(ALLSELECTED(campaign_data_cleaned[campaign_name]), [ROAS], , DESC, Dense)
)
```
