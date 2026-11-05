-- ============================================================================
-- MULTI-PLATFORM DIGITAL MARKETING CAMPAIGN PERFORMANCE ANALYSIS
-- Database: SQLite (digital_marketing.db)
-- Author: Senior Data Analyst & SQL Developer
--
-- Note: Synthetic dataset for multi-platform marketing performance evaluation.
-- All ratio/rate metrics (CTR, CPC, CPA, CVR, ROAS) are calculated using
-- aggregated numerators and denominators to prevent ratio averaging distortion.
-- Division-by-zero safeguards are implemented using NULLIF() and CASE statements.
-- ============================================================================

-- ----------------------------------------------------------------------------
-- TABLE CREATION SCRIPT (DDL)
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS campaign_performance (
    record_id TEXT PRIMARY KEY,
    date TEXT NOT NULL,
    platform TEXT NOT NULL,
    campaign_id TEXT NOT NULL,
    campaign_name TEXT NOT NULL,
    campaign_type TEXT NOT NULL,
    target_audience TEXT NOT NULL,
    device_type TEXT NOT NULL,
    region TEXT NOT NULL,
    impressions INTEGER NOT NULL,
    clicks INTEGER NOT NULL,
    ad_spend REAL NOT NULL,
    conversions INTEGER NOT NULL,
    revenue REAL NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_date ON campaign_performance(date);
CREATE INDEX IF NOT EXISTS idx_platform ON campaign_performance(platform);
CREATE INDEX IF NOT EXISTS idx_campaign ON campaign_performance(campaign_id);
CREATE INDEX IF NOT EXISTS idx_region ON campaign_performance(region);
CREATE INDEX IF NOT EXISTS idx_device ON campaign_performance(device_type);

-- ============================================================================
-- 1. TOTAL ADVERTISING SPEND
-- Beginner Explanation: Sums up the total ad spend across all platforms and campaigns.
-- ============================================================================
SELECT 
    ROUND(SUM(ad_spend), 2) AS total_ad_spend_usd
FROM campaign_performance;


-- ============================================================================
-- 2. TOTAL IMPRESSIONS AND CLICKS
-- Beginner Explanation: Calculates total ad views (impressions) and total user clicks,
-- alongside the overall Click-Through Rate (CTR).
-- ============================================================================
SELECT 
    SUM(impressions) AS total_impressions,
    SUM(clicks) AS total_clicks,
    ROUND((CAST(SUM(clicks) AS REAL) / NULLIF(SUM(impressions), 0)) * 100.0, 2) AS overall_ctr_pct
FROM campaign_performance;


-- ============================================================================
-- 3. TOTAL CONVERSIONS AND REVENUE
-- Beginner Explanation: Measures bottom-line business volume: total customer conversions,
-- total generated revenue, and overall Return On Ad Spend (ROAS).
-- ============================================================================
SELECT 
    SUM(conversions) AS total_conversions,
    ROUND(SUM(revenue), 2) AS total_revenue_usd,
    ROUND(SUM(revenue) - SUM(ad_spend), 2) AS net_profit_usd,
    ROUND(SUM(revenue) / NULLIF(SUM(ad_spend), 0), 2) AS overall_roas
FROM campaign_performance;


-- ============================================================================
-- 4. PLATFORM-WISE ADVERTISING EXPENDITURE
-- Beginner Explanation: Breaks down total budget allocation across the four advertising
-- channels (Meta, Google, LinkedIn, X) with share of total spend.
-- ============================================================================
SELECT 
    platform,
    ROUND(SUM(ad_spend), 2) AS platform_spend_usd,
    ROUND((SUM(ad_spend) * 100.0) / (SELECT SUM(ad_spend) FROM campaign_performance), 2) AS spend_share_pct
FROM campaign_performance
GROUP BY platform
ORDER BY platform_spend_usd DESC;


-- ============================================================================
-- 5. PLATFORM-WISE CLICK-THROUGH RATE (CTR)
-- Beginner Explanation: CTR = (Total Clicks / Total Impressions) * 100.
-- Indicates how effectively ad creatives capture user interest on each platform.
-- ============================================================================
SELECT 
    platform,
    SUM(impressions) AS total_impressions,
    SUM(clicks) AS total_clicks,
    ROUND((CAST(SUM(clicks) AS REAL) / NULLIF(SUM(impressions), 0)) * 100.0, 2) AS platform_ctr_pct
FROM campaign_performance
GROUP BY platform
ORDER BY platform_ctr_pct DESC;


-- ============================================================================
-- 6. PLATFORM-WISE COST PER CLICK (CPC)
-- Beginner Explanation: CPC = Total Ad Spend / Total Clicks.
-- Shows how much the company pays on average for every visitor brought to the site.
-- ============================================================================
SELECT 
    platform,
    ROUND(SUM(ad_spend), 2) AS total_ad_spend,
    SUM(clicks) AS total_clicks,
    ROUND(SUM(ad_spend) / NULLIF(SUM(clicks), 0), 2) AS platform_cpc_usd
FROM campaign_performance
GROUP BY platform
ORDER BY platform_cpc_usd ASC;


-- ============================================================================
-- 7. PLATFORM-WISE COST PER ACQUISITION (CPA)
-- Beginner Explanation: CPA = Total Ad Spend / Total Conversions.
-- Tells marketing managers how much it costs to acquire one paying customer or lead.
-- ============================================================================
SELECT 
    platform,
    ROUND(SUM(ad_spend), 2) AS total_ad_spend,
    SUM(conversions) AS total_conversions,
    ROUND(SUM(ad_spend) / NULLIF(SUM(conversions), 0), 2) AS platform_cpa_usd
FROM campaign_performance
GROUP BY platform
ORDER BY platform_cpa_usd ASC;


-- ============================================================================
-- 8. PLATFORM-WISE CONVERSION RATE (CVR)
-- Beginner Explanation: Conversion Rate = (Total Conversions / Total Clicks) * 100.
-- Highlights the traffic quality and landing page purchase intent per network.
-- ============================================================================
SELECT 
    platform,
    SUM(clicks) AS total_clicks,
    SUM(conversions) AS total_conversions,
    ROUND((CAST(SUM(conversions) AS REAL) / NULLIF(SUM(clicks), 0)) * 100.0, 2) AS conversion_rate_pct
FROM campaign_performance
GROUP BY platform
ORDER BY conversion_rate_pct DESC;


-- ============================================================================
-- 9. PLATFORM-WISE RETURN ON AD SPEND (ROAS)
-- Beginner Explanation: ROAS = Total Revenue / Total Ad Spend.
-- A ROAS of 3.0 means $3.00 revenue was earned for every $1.00 spent on advertising.
-- ============================================================================
SELECT 
    platform,
    ROUND(SUM(ad_spend), 2) AS total_ad_spend,
    ROUND(SUM(revenue), 2) AS total_revenue,
    ROUND(SUM(revenue) / NULLIF(SUM(ad_spend), 0), 2) AS roas,
    ROUND(SUM(revenue) - SUM(ad_spend), 2) AS net_profit_usd
FROM campaign_performance
GROUP BY platform
ORDER BY roas DESC;


-- ============================================================================
-- 10. HIGHEST REVENUE-GENERATING PLATFORM
-- Beginner Explanation: Identifies the top-earning network and its relative contribution.
-- ============================================================================
SELECT 
    platform,
    ROUND(SUM(revenue), 2) AS total_revenue_usd,
    ROUND((SUM(revenue) * 100.0) / (SELECT SUM(revenue) FROM campaign_performance), 2) AS revenue_share_pct
FROM campaign_performance
GROUP BY platform
ORDER BY total_revenue_usd DESC
LIMIT 1;


-- ============================================================================
-- 11. TOP 10 BEST-PERFORMING CAMPAIGNS (BY REVENUE AND ROAS)
-- Beginner Explanation: Ranks the top revenue-driving campaigns with healthy returns.
-- ============================================================================
SELECT 
    campaign_id,
    campaign_name,
    platform,
    campaign_type,
    ROUND(SUM(ad_spend), 2) AS total_spend,
    ROUND(SUM(revenue), 2) AS total_revenue,
    ROUND(SUM(revenue) / NULLIF(SUM(ad_spend), 0), 2) AS roas,
    SUM(conversions) AS total_conversions
FROM campaign_performance
GROUP BY campaign_id, campaign_name, platform, campaign_type
ORDER BY total_revenue DESC
LIMIT 10;


-- ============================================================================
-- 12. LOWEST-PERFORMING CAMPAIGNS (BY ROAS WITH MINIMUM SPEND FILTER)
-- Beginner Explanation: Filters for campaigns that consumed at least $10,000 in spend
-- but delivered weak returns, highlighting immediate cost-cutting candidates.
-- ============================================================================
SELECT 
    campaign_id,
    campaign_name,
    platform,
    campaign_type,
    ROUND(SUM(ad_spend), 2) AS total_spend,
    ROUND(SUM(revenue), 2) AS total_revenue,
    ROUND(SUM(revenue) / NULLIF(SUM(ad_spend), 0), 2) AS roas,
    ROUND(SUM(ad_spend) / NULLIF(SUM(conversions), 0), 2) AS cpa
FROM campaign_performance
GROUP BY campaign_id, campaign_name, platform, campaign_type
HAVING SUM(ad_spend) >= 10000.0
ORDER BY roas ASC
LIMIT 10;


-- ============================================================================
-- 13. MONTHLY ADVERTISING EXPENDITURE TREND
-- Beginner Explanation: Aggregates spend by calendar month to show seasonal scaling.
-- ============================================================================
SELECT 
    SUBSTR(date, 1, 7) AS year_month,
    ROUND(SUM(ad_spend), 2) AS monthly_spend_usd,
    COUNT(DISTINCT record_id) AS total_daily_records
FROM campaign_performance
GROUP BY SUBSTR(date, 1, 7)
ORDER BY year_month ASC;


-- ============================================================================
-- 14. MONTHLY REVENUE AND PROFIT TRENDS
-- Beginner Explanation: Tracks revenue and net operating return per calendar month.
-- ============================================================================
SELECT 
    SUBSTR(date, 1, 7) AS year_month,
    ROUND(SUM(ad_spend), 2) AS monthly_spend,
    ROUND(SUM(revenue), 2) AS monthly_revenue,
    ROUND(SUM(revenue) - SUM(ad_spend), 2) AS monthly_net_profit,
    SUM(conversions) AS monthly_conversions
FROM campaign_performance
GROUP BY SUBSTR(date, 1, 7)
ORDER BY year_month ASC;


-- ============================================================================
-- 15. MONTHLY ROAS AND EFFICIENCY TRENDS
-- Beginner Explanation: Compares month-over-month ROAS, CTR, and CPA efficiency.
-- ============================================================================
SELECT 
    SUBSTR(date, 1, 7) AS year_month,
    ROUND(SUM(revenue) / NULLIF(SUM(ad_spend), 0), 2) AS monthly_roas,
    ROUND((CAST(SUM(clicks) AS REAL) / NULLIF(SUM(impressions), 0)) * 100.0, 2) AS monthly_ctr_pct,
    ROUND(SUM(ad_spend) / NULLIF(SUM(conversions), 0), 2) AS monthly_cpa_usd
FROM campaign_performance
GROUP BY SUBSTR(date, 1, 7)
ORDER BY year_month ASC;


-- ============================================================================
-- 16. REGION-WISE CAMPAIGN PERFORMANCE
-- Beginner Explanation: Evaluates geographic expansion across North America, Europe,
-- Asia-Pacific, and Latin America.
-- ============================================================================
SELECT 
    region,
    ROUND(SUM(ad_spend), 2) AS total_spend,
    ROUND(SUM(revenue), 2) AS total_revenue,
    SUM(conversions) AS total_conversions,
    ROUND(SUM(revenue) / NULLIF(SUM(ad_spend), 0), 2) AS region_roas,
    ROUND(SUM(ad_spend) / NULLIF(SUM(conversions), 0), 2) AS region_cpa
FROM campaign_performance
GROUP BY region
ORDER BY total_revenue DESC;


-- ============================================================================
-- 17. DEVICE-WISE CONVERSION AND REVENUE ANALYSIS
-- Beginner Explanation: Compares Mobile, Desktop, and Tablet conversions and AOV.
-- ============================================================================
SELECT 
    device_type,
    SUM(clicks) AS total_clicks,
    SUM(conversions) AS total_conversions,
    ROUND((CAST(SUM(conversions) AS REAL) / NULLIF(SUM(clicks), 0)) * 100.0, 2) AS cvr_pct,
    ROUND(SUM(ad_spend), 2) AS total_spend,
    ROUND(SUM(revenue), 2) AS total_revenue,
    ROUND(SUM(revenue) / NULLIF(SUM(conversions), 0), 2) AS avg_order_revenue,
    ROUND(SUM(revenue) / NULLIF(SUM(ad_spend), 0), 2) AS device_roas
FROM campaign_performance
GROUP BY device_type
ORDER BY total_revenue DESC;


-- ============================================================================
-- 18. CAMPAIGN-TYPE COMPARISON
-- Beginner Explanation: Evaluates tactical campaign formats (Search, Social Feed,
-- Retargeting, Performance Max, Video, Lead Gen, etc.).
-- ============================================================================
SELECT 
    campaign_type,
    COUNT(DISTINCT campaign_id) AS campaign_count,
    ROUND(SUM(ad_spend), 2) AS total_spend,
    ROUND(SUM(revenue), 2) AS total_revenue,
    ROUND((CAST(SUM(clicks) AS REAL) / NULLIF(SUM(impressions), 0)) * 100.0, 2) AS ctr_pct,
    ROUND((CAST(SUM(conversions) AS REAL) / NULLIF(SUM(clicks), 0)) * 100.0, 2) AS cvr_pct,
    ROUND(SUM(revenue) / NULLIF(SUM(ad_spend), 0), 2) AS roas
FROM campaign_performance
GROUP BY campaign_type
ORDER BY total_revenue DESC;


-- ============================================================================
-- 19. HIGH-SPEND AND LOW-CONVERSION CAMPAIGNS (BUDGET DRAIN AUDIT)
-- Beginner Explanation: Pinpoints campaigns spending above average but yielding
-- below-median conversion counts or ROAS < 2.0.
-- ============================================================================
WITH campaign_aggregates AS (
    SELECT 
        campaign_id,
        campaign_name,
        platform,
        campaign_type,
        SUM(ad_spend) AS spend,
        SUM(conversions) AS total_conversions,
        SUM(revenue) AS revenue,
        SUM(revenue) / NULLIF(SUM(ad_spend), 0) AS campaign_roas,
        SUM(ad_spend) / NULLIF(SUM(conversions), 0) AS campaign_cpa
    FROM campaign_performance
    GROUP BY campaign_id, campaign_name, platform, campaign_type
),
benchmark AS (
    SELECT AVG(spend) AS avg_campaign_spend FROM campaign_aggregates
)
SELECT 
    ca.campaign_id,
    ca.campaign_name,
    ca.platform,
    ca.campaign_type,
    ROUND(ca.spend, 2) AS spend_usd,
    ca.total_conversions,
    ROUND(ca.revenue, 2) AS revenue_usd,
    ROUND(ca.campaign_roas, 2) AS roas,
    ROUND(ca.campaign_cpa, 2) AS cpa_usd
FROM campaign_aggregates ca
CROSS JOIN benchmark b
WHERE ca.spend >= b.avg_campaign_spend AND ca.campaign_roas < 2.0
ORDER BY ca.spend DESC;


-- ============================================================================
-- 20. BUDGET OPTIMIZATION RECOMMENDATIONS
-- Beginner Explanation: Automatically segments campaigns into strategic action tiers:
-- 'SCALE UP' (High ROAS >= 3.2), 'MAINTAIN / OPTIMIZE' (ROAS 2.2 - 3.2),
-- 'REDUCE / RESTRUCTURE' (ROAS < 2.2).
-- ============================================================================
SELECT 
    campaign_name,
    platform,
    ROUND(SUM(ad_spend), 2) AS total_spend,
    ROUND(SUM(revenue), 2) AS total_revenue,
    ROUND(SUM(revenue) / NULLIF(SUM(ad_spend), 0), 2) AS roas,
    CASE 
        WHEN (SUM(revenue) / NULLIF(SUM(ad_spend), 0)) >= 3.20 THEN 'SCALE UP (+20% Budget)'
        WHEN (SUM(revenue) / NULLIF(SUM(ad_spend), 0)) >= 2.20 THEN 'MAINTAIN / OPTIMIZE'
        ELSE 'REDUCE / RESTRUCTURE (-30% Budget)'
    END AS strategic_action_recommendation
FROM campaign_performance
GROUP BY campaign_id, campaign_name, platform
ORDER BY roas DESC;
