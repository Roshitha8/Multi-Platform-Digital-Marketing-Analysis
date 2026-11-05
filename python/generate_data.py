"""
Multi-Platform Digital Marketing Campaign Performance Analysis
Module: python/generate_data.py

Generates a realistic synthetic advertising dataset covering 6 months (Jan 1, 2026 - Jun 30, 2026)
across Meta Ads, Google Ads, LinkedIn Ads, and X Ads.

Features:
- ~12,500 records across 44 distinct campaigns (11 per platform).
- Realistic platform benchmarks for CTR, CPC, CPA, CVR, and ROAS.
- Multi-dimensional dimensions: Platform, Campaign, Campaign Type, Target Audience, Device, Region.
- Introduces controlled, realistic data quality flaws in the raw dataset:
  * Exact duplicate records (~120 rows)
  * Inconsistent casing and naming in Platform, Device, and Region
  * Trailing and leading whitespaces in Campaign Names
  * Inconsistent date formatting (YYYY-MM-DD, MM/DD/YYYY, YYYY/MM/DD)
  * Missing values (NaN) in Audience, Device, Spend, Revenue, Impressions, Clicks
  * A small number of invalid edge-case records (negative spend, clicks > impressions, conversions > clicks)
- Fixed random seed (seed=42) for 100% reproducibility.
"""

import os
import random
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

def generate_synthetic_data(
    start_date: str = "2026-01-01",
    end_date: str = "2026-06-30",
    seed: int = 42
) -> pd.DataFrame:
    np.random.seed(seed)
    random.seed(seed)

    start_dt = datetime.strptime(start_date, "%Y-%m-%d")
    end_dt = datetime.strptime(end_date, "%Y-%m-%d")
    num_days = (end_dt - start_dt).days + 1
    dates = [start_dt + timedelta(days=d) for d in range(num_days)]

    # Platform campaign configurations (44 distinct campaigns across 4 platforms)
    campaigns = [
        # Meta Ads (11 campaigns)
        {"id": "CMP-META-001", "name": "Meta_Retargeting_Catalog_Sales", "platform": "Meta Ads", "type": "Retargeting", "base_audience": "Past Visitors & Cart Abandoners", "spend_range": (150, 400), "ctr_base": 0.035, "cpc_base": 0.90, "cvr_base": 0.052, "aov_base": 85.0},
        {"id": "CMP-META-002", "name": "Meta_Spring_Fashion_Lookbook", "platform": "Meta Ads", "type": "Social Feed", "base_audience": "Fashion & Apparel Shoppers", "spend_range": (200, 550), "ctr_base": 0.028, "cpc_base": 0.85, "cvr_base": 0.038, "aov_base": 72.0},
        {"id": "CMP-META-003", "name": "Meta_Brand_Awareness_Reels", "platform": "Meta Ads", "type": "Video", "base_audience": "Gen Z & Millennials", "spend_range": (300, 700), "ctr_base": 0.019, "cpc_base": 0.55, "cvr_base": 0.018, "aov_base": 65.0},
        {"id": "CMP-META-004", "name": "Meta_Summer_Promo_LeadGen", "platform": "Meta Ads", "type": "Lead Generation", "base_audience": "Young Urban Consumers", "spend_range": (180, 450), "ctr_base": 0.024, "cpc_base": 1.10, "cvr_base": 0.042, "aov_base": 90.0},
        {"id": "CMP-META-005", "name": "Meta_Lookalike_HighValue_Buyers", "platform": "Meta Ads", "type": "Social Feed", "base_audience": "High-Income Shoppers", "spend_range": (250, 600), "ctr_base": 0.026, "cpc_base": 1.15, "cvr_base": 0.045, "aov_base": 120.0},
        {"id": "CMP-META-006", "name": "Meta_Instagram_Stories_FlashSale", "platform": "Meta Ads", "type": "Social Feed", "base_audience": "Engaged Followers 18-34", "spend_range": (220, 500), "ctr_base": 0.031, "cpc_base": 0.75, "cvr_base": 0.040, "aov_base": 68.0},
        {"id": "CMP-META-007", "name": "Meta_Fitness_Wellness_Push", "platform": "Meta Ads", "type": "Social Feed", "base_audience": "Health & Fitness Enthusiasts", "spend_range": (140, 350), "ctr_base": 0.025, "cpc_base": 0.80, "cvr_base": 0.034, "aov_base": 78.0},
        {"id": "CMP-META-008", "name": "Meta_HomeDecor_Inspiration_Ad", "platform": "Meta Ads", "type": "Social Feed", "base_audience": "Homeowners & Families", "spend_range": (160, 420), "ctr_base": 0.022, "cpc_base": 0.95, "cvr_base": 0.031, "aov_base": 110.0},
        {"id": "CMP-META-009", "name": "Meta_Electronics_NewLaunch", "platform": "Meta Ads", "type": "Display", "base_audience": "Tech Gadget Lovers", "spend_range": (280, 650), "ctr_base": 0.021, "cpc_base": 1.05, "cvr_base": 0.029, "aov_base": 145.0},
        {"id": "CMP-META-010", "name": "Meta_VIP_Loyalty_Rewards", "platform": "Meta Ads", "type": "Retargeting", "base_audience": "Loyalty Members", "spend_range": (120, 300), "ctr_base": 0.042, "cpc_base": 0.88, "cvr_base": 0.065, "aov_base": 95.0},
        {"id": "CMP-META-011", "name": "Meta_MemorialDay_WeekendSpecial", "platform": "Meta Ads", "type": "Social Feed", "base_audience": "Holiday Bargain Hunters", "spend_range": (200, 520), "ctr_base": 0.029, "cpc_base": 0.92, "cvr_base": 0.039, "aov_base": 82.0},

        # Google Ads (11 campaigns)
        {"id": "CMP-GOOG-001", "name": "Google_Search_HighIntent_Brand", "platform": "Google Ads", "type": "Search", "base_audience": "High-Intent Brand Seekers", "spend_range": (350, 850), "ctr_base": 0.058, "cpc_base": 2.20, "cvr_base": 0.078, "aov_base": 135.0},
        {"id": "CMP-GOOG-002", "name": "Google_Search_Generic_Keywords", "platform": "Google Ads", "type": "Search", "base_audience": "In-Market Category Shoppers", "spend_range": (400, 950), "ctr_base": 0.039, "cpc_base": 2.80, "cvr_base": 0.048, "aov_base": 115.0},
        {"id": "CMP-GOOG-003", "name": "Google_PMax_Omnichannel_Growth", "platform": "Google Ads", "type": "Performance Max", "base_audience": "Multi-Channel Shoppers", "spend_range": (450, 1100), "ctr_base": 0.032, "cpc_base": 1.75, "cvr_base": 0.055, "aov_base": 140.0},
        {"id": "CMP-GOOG-004", "name": "Google_Display_Remarketing_Audience", "platform": "Google Ads", "type": "Display", "base_audience": "Website Drop-offs", "spend_range": (150, 400), "ctr_base": 0.012, "cpc_base": 0.70, "cvr_base": 0.022, "aov_base": 90.0},
        {"id": "CMP-GOOG-005", "name": "Google_Shopping_Bestsellers", "platform": "Google Ads", "type": "Shopping", "base_audience": "E-commerce Product Searchers", "spend_range": (300, 750), "ctr_base": 0.041, "cpc_base": 1.45, "cvr_base": 0.062, "aov_base": 105.0},
        {"id": "CMP-GOOG-006", "name": "Google_YouTube_Action_Video", "platform": "Google Ads", "type": "Video", "base_audience": "YouTube Video Viewers 18-49", "spend_range": (250, 600), "ctr_base": 0.015, "cpc_base": 0.95, "cvr_base": 0.021, "aov_base": 85.0},
        {"id": "CMP-GOOG-007", "name": "Google_Search_Competitor_Conquest", "platform": "Google Ads", "type": "Search", "base_audience": "Competitor Audience", "spend_range": (320, 800), "ctr_base": 0.033, "cpc_base": 3.60, "cvr_base": 0.035, "aov_base": 125.0},
        {"id": "CMP-GOOG-008", "name": "Google_Search_Local_StoreVisits", "platform": "Google Ads", "type": "Search", "base_audience": "Local Geotargeted Shoppers", "spend_range": (180, 450), "ctr_base": 0.046, "cpc_base": 1.85, "cvr_base": 0.058, "aov_base": 98.0},
        {"id": "CMP-GOOG-009", "name": "Google_PMax_Retail_SpringPromo", "platform": "Google Ads", "type": "Performance Max", "base_audience": "Seasonal In-Market Shoppers", "spend_range": (380, 900), "ctr_base": 0.034, "cpc_base": 1.80, "cvr_base": 0.053, "aov_base": 130.0},
        {"id": "CMP-GOOG-010", "name": "Google_Search_Enterprise_Solutions", "platform": "Google Ads", "type": "Search", "base_audience": "Commercial & SME Buyers", "spend_range": (300, 700), "ctr_base": 0.038, "cpc_base": 4.10, "cvr_base": 0.042, "aov_base": 240.0},
        {"id": "CMP-GOOG-011", "name": "Google_Shopping_Clearance_Deals", "platform": "Google Ads", "type": "Shopping", "base_audience": "Discount Product Searchers", "spend_range": (200, 500), "ctr_base": 0.044, "cpc_base": 1.25, "cvr_base": 0.059, "aov_base": 75.0},

        # LinkedIn Ads (11 campaigns)
        {"id": "CMP-LINK-001", "name": "LinkedIn_B2B_SaaS_Demo_Leads", "platform": "LinkedIn Ads", "type": "Lead Generation", "base_audience": "IT Directors & CTOs", "spend_range": (400, 900), "ctr_base": 0.009, "cpc_base": 7.50, "cvr_base": 0.026, "aov_base": 650.0},
        {"id": "CMP-LINK-002", "name": "LinkedIn_Enterprise_Whitepaper_Download", "platform": "LinkedIn Ads", "type": "Content Download", "base_audience": "Finance & Operations Executives", "spend_range": (350, 800), "ctr_base": 0.012, "cpc_base": 6.80, "cvr_base": 0.032, "aov_base": 480.0},
        {"id": "CMP-LINK-003", "name": "LinkedIn_Executive_Brand_ThoughtLeadership", "platform": "LinkedIn Ads", "type": "Social Feed", "base_audience": "C-Suite & Business Founders", "spend_range": (300, 750), "ctr_base": 0.007, "cpc_base": 8.20, "cvr_base": 0.018, "aov_base": 720.0},
        {"id": "CMP-LINK-004", "name": "LinkedIn_HR_Tech_Summit_Registration", "platform": "LinkedIn Ads", "type": "Event Promotion", "base_audience": "HR & Talent Acquisition VPs", "spend_range": (280, 650), "ctr_base": 0.010, "cpc_base": 6.40, "cvr_base": 0.028, "aov_base": 420.0},
        {"id": "CMP-LINK-005", "name": "LinkedIn_Sponsored_InMail_Consulting", "platform": "LinkedIn Ads", "type": "Sponsored Message", "base_audience": "Mid-Market VP of Sales", "spend_range": (320, 700), "ctr_base": 0.014, "cpc_base": 7.10, "cvr_base": 0.029, "aov_base": 550.0},
        {"id": "CMP-LINK-006", "name": "LinkedIn_Cloud_Migration_Webinar", "platform": "LinkedIn Ads", "type": "Event Promotion", "base_audience": "DevOps & Cloud Architects", "spend_range": (360, 820), "ctr_base": 0.011, "cpc_base": 7.80, "cvr_base": 0.025, "aov_base": 610.0},
        {"id": "CMP-LINK-007", "name": "LinkedIn_FinTech_Industry_Report", "platform": "LinkedIn Ads", "type": "Content Download", "base_audience": "Banking & FinTech Leaders", "spend_range": (310, 720), "ctr_base": 0.013, "cpc_base": 6.90, "cvr_base": 0.031, "aov_base": 510.0},
        {"id": "CMP-LINK-008", "name": "LinkedIn_Account_Based_Marketing_Tier1", "platform": "LinkedIn Ads", "type": "Social Feed", "base_audience": "Fortune 500 Decision Makers", "spend_range": (450, 1050), "ctr_base": 0.008, "cpc_base": 9.40, "cvr_base": 0.024, "aov_base": 880.0},
        {"id": "CMP-LINK-009", "name": "LinkedIn_Cybersecurity_CaseStudy", "platform": "LinkedIn Ads", "type": "Content Download", "base_audience": "CISOs & Security Analysts", "spend_range": (340, 780), "ctr_base": 0.010, "cpc_base": 7.60, "cvr_base": 0.027, "aov_base": 590.0},
        {"id": "CMP-LINK-010", "name": "LinkedIn_SaaS_FreeTrial_Signups", "platform": "LinkedIn Ads", "type": "Lead Generation", "base_audience": "Product Managers & Tech Leads", "spend_range": (380, 850), "ctr_base": 0.011, "cpc_base": 7.20, "cvr_base": 0.030, "aov_base": 540.0},
        {"id": "CMP-LINK-011", "name": "LinkedIn_SMB_Growth_Kit", "platform": "LinkedIn Ads", "type": "Lead Generation", "base_audience": "Small Business Owners", "spend_range": (260, 600), "ctr_base": 0.013, "cpc_base": 5.90, "cvr_base": 0.033, "aov_base": 390.0},

        # X Ads / Twitter (11 campaigns)
        {"id": "CMP-XAD-001", "name": "X_TechSummit_TrendTakeover", "platform": "X Ads", "type": "Trend Takeover", "base_audience": "Tech Enthusiasts & Developers", "spend_range": (350, 800), "ctr_base": 0.018, "cpc_base": 0.65, "cvr_base": 0.015, "aov_base": 60.0},
        {"id": "CMP-XAD-002", "name": "X_ProductLaunch_Engagement_Blitz", "platform": "X Ads", "type": "Promoted Post", "base_audience": "Early Adopters & Gamers", "spend_range": (250, 600), "ctr_base": 0.022, "cpc_base": 0.55, "cvr_base": 0.019, "aov_base": 55.0},
        {"id": "CMP-XAD-003", "name": "X_FlashSale_Hashtag_Push", "platform": "X Ads", "type": "Promoted Post", "base_audience": "Online Deal Seekers", "spend_range": (200, 500), "ctr_base": 0.025, "cpc_base": 0.48, "cvr_base": 0.022, "aov_base": 50.0},
        {"id": "CMP-XAD-004", "name": "X_Crypto_FinTech_Roundup", "platform": "X Ads", "type": "Promoted Post", "base_audience": "Crypto & FinTech Traders", "spend_range": (280, 650), "ctr_base": 0.017, "cpc_base": 0.72, "cvr_base": 0.016, "aov_base": 75.0},
        {"id": "CMP-XAD-005", "name": "X_LiveEvent_Video_Sponsorship", "platform": "X Ads", "type": "Video", "base_audience": "Live Stream & Sports Fans", "spend_range": (320, 750), "ctr_base": 0.015, "cpc_base": 0.60, "cvr_base": 0.014, "aov_base": 58.0},
        {"id": "CMP-XAD-006", "name": "X_Gaming_Console_Contest", "platform": "X Ads", "type": "Promoted Post", "base_audience": "Competitive Gamers 18-30", "spend_range": (220, 520), "ctr_base": 0.027, "cpc_base": 0.45, "cvr_base": 0.020, "aov_base": 52.0},
        {"id": "CMP-XAD-007", "name": "X_Developer_DevOps_Challenge", "platform": "X Ads", "type": "Promoted Post", "base_audience": "Software Engineers & Data Geeks", "spend_range": (260, 580), "ctr_base": 0.019, "cpc_base": 0.68, "cvr_base": 0.018, "aov_base": 65.0},
        {"id": "CMP-XAD-008", "name": "X_Entertainment_MovieTeaser", "platform": "X Ads", "type": "Video", "base_audience": "Film & Pop Culture Fans", "spend_range": (300, 700), "ctr_base": 0.021, "cpc_base": 0.52, "cvr_base": 0.012, "aov_base": 48.0},
        {"id": "CMP-XAD-009", "name": "X_AppInstall_Utility_Sprint", "platform": "X Ads", "type": "App Install", "base_audience": "Mobile App Power Users", "spend_range": (240, 560), "ctr_base": 0.026, "cpc_base": 0.50, "cvr_base": 0.025, "aov_base": 42.0},
        {"id": "CMP-XAD-010", "name": "X_Ecosystem_Partnership_News", "platform": "X Ads", "type": "Promoted Post", "base_audience": "Business Followers & Industry Analysts", "spend_range": (210, 480), "ctr_base": 0.016, "cpc_base": 0.62, "cvr_base": 0.014, "aov_base": 62.0},
        {"id": "CMP-XAD-011", "name": "X_Summer_Festival_TicketPromo", "platform": "X Ads", "type": "Promoted Post", "base_audience": "Music & Festival Goers", "spend_range": (250, 590), "ctr_base": 0.024, "cpc_base": 0.54, "cvr_base": 0.017, "aov_base": 56.0},
    ]

    regions = ["North America", "Europe", "Asia-Pacific", "Latin America"]
    region_weights = [0.45, 0.30, 0.18, 0.07]

    devices = ["Mobile", "Desktop", "Tablet"]
    device_weights = {"Meta Ads": [0.72, 0.22, 0.06], "Google Ads": [0.55, 0.38, 0.07], "LinkedIn Ads": [0.40, 0.54, 0.06], "X Ads": [0.80, 0.16, 0.04]}

    rows = []
    record_counter = 10001

    # Generate daily records for each campaign
    # To reach ~12,500 records: 44 campaigns across 181 days. If on any day a campaign records 1-2 regional/device segments:
    # Let's average ~1.55 segment records per campaign per day = 44 * 181 * 1.55 ≈ 12,344 records.
    for current_date in dates:
        day_of_week = current_date.weekday() # 0=Mon, 6=Sun
        is_weekend = day_of_week in [5, 6]
        month = current_date.month # 1 to 6

        # Seasonal multiplier (Q1 starts steady, March spring bump, May-June summer ramp)
        seasonal_mult = 1.0 + (month - 1) * 0.04 + (0.08 if month in [3, 5, 6] else 0.0)

        for cmp in campaigns:
            # Active probability: LinkedIn active less on weekends, Meta/X more on weekends
            if cmp["platform"] == "LinkedIn Ads" and is_weekend:
                if random.random() < 0.35:
                    continue
            elif cmp["platform"] in ["Meta Ads", "X Ads"] and not is_weekend:
                pass # always active

            # Choose 1 or 2 regional slices for this campaign on this day
            num_slices = random.choices([1, 2, 3], weights=[0.55, 0.38, 0.07])[0]
            selected_regions = random.choices(regions, weights=region_weights, k=num_slices)

            for region in selected_regions:
                # Device selection
                platform_device_weights = device_weights[cmp["platform"]]
                device = random.choices(devices, weights=platform_device_weights)[0]

                # Regional modifiers
                region_spend_mod = {"North America": 1.25, "Europe": 1.05, "Asia-Pacific": 0.85, "Latin America": 0.65}[region]
                region_cvr_mod = {"North America": 1.15, "Europe": 1.05, "Asia-Pacific": 0.90, "Latin America": 0.80}[region]

                # Device modifiers
                device_cpc_mod = {"Mobile": 0.88, "Desktop": 1.18, "Tablet": 0.95}[device]
                device_cvr_mod = {"Mobile": 0.85, "Desktop": 1.25, "Tablet": 0.95}[device]
                device_aov_mod = {"Mobile": 0.92, "Desktop": 1.15, "Tablet": 0.98}[device]

                # Base daily spend for slice
                spend_low, spend_high = cmp["spend_range"]
                slice_fraction = 1.0 / num_slices
                base_spend = random.uniform(spend_low, spend_high) * slice_fraction * seasonal_mult * region_spend_mod
                ad_spend = round(max(15.0, base_spend * random.uniform(0.85, 1.18)), 2)

                # CPC calculation with noise
                effective_cpc = max(0.20, cmp["cpc_base"] * device_cpc_mod * random.uniform(0.88, 1.15))
                expected_clicks = ad_spend / effective_cpc
                clicks = int(round(expected_clicks * random.uniform(0.90, 1.10)))
                clicks = max(1, clicks)

                # CTR calculation
                effective_ctr = max(0.005, min(0.09, cmp["ctr_base"] * random.uniform(0.88, 1.15)))
                expected_impressions = clicks / effective_ctr
                impressions = int(round(expected_impressions * random.uniform(0.92, 1.12)))
                impressions = max(clicks + random.randint(10, 50), impressions)

                # CVR and conversions
                effective_cvr = max(0.005, min(0.15, cmp["cvr_base"] * device_cvr_mod * region_cvr_mod * random.uniform(0.85, 1.20)))
                conversions = int(round(clicks * effective_cvr))
                # Ensure realistic constraint
                conversions = min(clicks, conversions)

                # Revenue calculation based on AOV (Average Order Value)
                if conversions > 0:
                    aov = cmp["aov_base"] * device_aov_mod * random.uniform(0.85, 1.22)
                    revenue = round(conversions * aov, 2)
                else:
                    revenue = 0.0

                rows.append({
                    "record_id": f"REC-{record_counter:06d}",
                    "date": current_date.strftime("%Y-%m-%d"),
                    "platform": cmp["platform"],
                    "campaign_id": cmp["id"],
                    "campaign_name": cmp["name"],
                    "campaign_type": cmp["type"],
                    "target_audience": cmp["base_audience"],
                    "device_type": device,
                    "region": region,
                    "impressions": int(impressions),
                    "clicks": int(clicks),
                    "ad_spend": float(ad_spend),
                    "conversions": int(conversions),
                    "revenue": float(revenue)
                })
                record_counter += 1

    df_clean_baseline = pd.DataFrame(rows)
    print(f"Generated {len(df_clean_baseline)} baseline realistic records.")

    # Now create raw dataset with intentional, documented data quality anomalies:
    df_raw = df_clean_baseline.copy()

    # 1. Duplicate records (~120 duplicate rows)
    num_duplicates = 120
    dup_indices = np.random.choice(len(df_raw), size=num_duplicates, replace=False)
    dup_rows = df_raw.iloc[dup_indices].copy()
    df_raw = pd.concat([df_raw, dup_rows], ignore_index=True)
    # Shuffle slightly
    df_raw = df_raw.sample(frac=1.0, random_state=seed).reset_index(drop=True)
    print(f"Added {num_duplicates} exact duplicate records.")

    # 2. Inconsistent formatting in text columns
    # Platform variations
    platform_variations = {
        "Meta Ads": ["Meta Ads", "meta ads", "Meta", "META ADS"],
        "Google Ads": ["Google Ads", "google ads", "Google", "GOOGLE ADS"],
        "LinkedIn Ads": ["LinkedIn Ads", "linkedin ads", "LinkedIn", "LINKEDIN ADS"],
        "X Ads": ["X Ads", "x ads", "Twitter", "X (Twitter) Ads", "X ADS"]
    }
    for i in range(len(df_raw)):
        if random.random() < 0.08:
            cur_p = df_raw.at[i, "platform"]
            if cur_p in platform_variations:
                df_raw.at[i, "platform"] = random.choice(platform_variations[cur_p])

    # Device type variations (case inconsistency)
    device_variations = {
        "Mobile": ["Mobile", "mobile", "MOBILE"],
        "Desktop": ["Desktop", "desktop", "DESKTOP"],
        "Tablet": ["Tablet", "tablet", "TABLET"]
    }
    for i in range(len(df_raw)):
        if random.random() < 0.07:
            cur_d = df_raw.at[i, "device_type"]
            if cur_d in device_variations:
                df_raw.at[i, "device_type"] = random.choice(device_variations[cur_d])

    # Region casing
    for i in range(len(df_raw)):
        if random.random() < 0.05:
            df_raw.at[i, "region"] = df_raw.at[i, "region"].lower()

    # Campaign name leading/trailing whitespaces
    for i in range(len(df_raw)):
        if random.random() < 0.06:
            df_raw.at[i, "campaign_name"] = f"  {df_raw.at[i, 'campaign_name']} "

    # 3. Inconsistent date formats
    for i in range(len(df_raw)):
        if random.random() < 0.08:
            orig_d = df_raw.at[i, "date"]
            dt_obj = datetime.strptime(orig_d, "%Y-%m-%d")
            format_choice = random.choice(["%m/%d/%Y", "%Y/%m/%d"])
            df_raw.at[i, "date"] = dt_obj.strftime(format_choice)

    # 4. Missing values (NaNs)
    # Target audience missing (~75 rows)
    missing_aud_idx = np.random.choice(len(df_raw), size=75, replace=False)
    df_raw.loc[missing_aud_idx, "target_audience"] = np.nan

    # Device type missing (~60 rows)
    missing_dev_idx = np.random.choice(len(df_raw), size=60, replace=False)
    df_raw.loc[missing_dev_idx, "device_type"] = np.nan

    # Impressions missing (~35 rows)
    missing_imp_idx = np.random.choice(len(df_raw), size=35, replace=False)
    df_raw.loc[missing_imp_idx, "impressions"] = np.nan

    # Clicks missing (~30 rows)
    missing_clk_idx = np.random.choice(len(df_raw), size=30, replace=False)
    df_raw.loc[missing_clk_idx, "clicks"] = np.nan

    # Ad spend missing (~25 rows)
    missing_spd_idx = np.random.choice(len(df_raw), size=25, replace=False)
    df_raw.loc[missing_spd_idx, "ad_spend"] = np.nan

    # Revenue missing (~30 rows)
    missing_rev_idx = np.random.choice(len(df_raw), size=30, replace=False)
    df_raw.loc[missing_rev_idx, "revenue"] = np.nan

    # 5. Invalid records to test data cleaning edge cases
    # Negative ad spend (~12 rows, e.g. billing error / refund anomaly)
    neg_spend_idx = np.random.choice(len(df_raw), size=12, replace=False)
    df_raw.loc[neg_spend_idx, "ad_spend"] = -np.abs(df_raw.loc[neg_spend_idx, "ad_spend"])

    # Clicks > impressions (~15 rows, tracking glitch)
    inv_clicks_idx = np.random.choice(len(df_raw), size=15, replace=False)
    for idx in inv_clicks_idx:
        imp = df_raw.at[idx, "impressions"]
        if pd.notnull(imp):
            df_raw.at[idx, "clicks"] = imp + random.randint(10, 50)

    # Conversions > clicks (~10 rows, attribution pixel duplicate firing)
    inv_cvr_idx = np.random.choice(len(df_raw), size=10, replace=False)
    for idx in inv_cvr_idx:
        clk = df_raw.at[idx, "clicks"]
        if pd.notnull(clk) and clk > 0:
            df_raw.at[idx, "conversions"] = clk + random.randint(5, 20)

    print(f"Generated raw dataset with {len(df_raw)} records containing realistic anomalies.")
    return df_raw

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, "data")
    os.makedirs(data_dir, exist_ok=True)
    raw_path = os.path.join(data_dir, "raw_campaign_data.csv")

    raw_df = generate_synthetic_data(seed=42)
    raw_df.to_csv(raw_path, index=False)
    print(f"Successfully saved raw dataset to: {raw_path}")
    print(f"Shape: {raw_df.shape}")
