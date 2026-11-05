"""
Multi-Platform Digital Marketing Campaign Performance Analysis
Test Suite: tests/test_data_quality.py

Validates dataset existence, schema integrity, hygiene constraints,
and business logic rules using pytest.
"""

import os
import pandas as pd
import pytest

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_CSV_PATH = os.path.join(BASE_DIR, "data", "raw_campaign_data.csv")
CLEANED_CSV_PATH = os.path.join(BASE_DIR, "data", "campaign_data_cleaned.csv")

REQUIRED_COLUMNS = [
    "record_id", "date", "platform", "campaign_id", "campaign_name",
    "campaign_type", "target_audience", "device_type", "region",
    "impressions", "clicks", "ad_spend", "conversions", "revenue"
]

VALID_PLATFORMS = {"Meta Ads", "Google Ads", "LinkedIn Ads", "X Ads"}
VALID_DEVICES = {"Mobile", "Desktop", "Tablet"}
VALID_REGIONS = {"North America", "Europe", "Asia-Pacific", "Latin America"}

def test_raw_data_exists_and_meets_volume_target():
    assert os.path.exists(RAW_CSV_PATH), f"Raw CSV missing at {RAW_CSV_PATH}"
    df_raw = pd.read_csv(RAW_CSV_PATH)
    assert len(df_raw) >= 10000, f"Expected >= 10,000 raw rows, found {len(df_raw)}"
    for col in REQUIRED_COLUMNS:
        assert col in df_raw.columns, f"Required column '{col}' missing from raw dataset"

def test_cleaned_data_exists_and_meets_volume_target():
    assert os.path.exists(CLEANED_CSV_PATH), f"Cleaned CSV missing at {CLEANED_CSV_PATH}"
    df_clean = pd.read_csv(CLEANED_CSV_PATH)
    assert len(df_clean) >= 10000, f"Expected >= 10,000 cleaned rows, found {len(df_clean)}"
    for col in REQUIRED_COLUMNS:
        assert col in df_clean.columns, f"Required column '{col}' missing from cleaned dataset"

def test_cleaned_data_has_unique_record_ids():
    df_clean = pd.read_csv(CLEANED_CSV_PATH)
    num_unique = df_clean["record_id"].nunique()
    total_rows = len(df_clean)
    assert num_unique == total_rows, f"Duplicate record IDs found: {total_rows - num_unique} duplicate(s)"

def test_cleaned_data_has_zero_nulls():
    df_clean = pd.read_csv(CLEANED_CSV_PATH)
    null_counts = df_clean.isnull().sum()
    total_nulls = null_counts.sum()
    assert total_nulls == 0, f"Found {total_nulls} null values in cleaned data: {null_counts[null_counts > 0].to_dict()}"

def test_clicks_do_not_exceed_impressions():
    df_clean = pd.read_csv(CLEANED_CSV_PATH)
    invalid_mask = df_clean["clicks"] > df_clean["impressions"]
    invalid_count = invalid_mask.sum()
    assert invalid_count == 0, f"Found {invalid_count} records where clicks > impressions"

def test_conversions_do_not_exceed_clicks():
    df_clean = pd.read_csv(CLEANED_CSV_PATH)
    invalid_mask = df_clean["conversions"] > df_clean["clicks"]
    invalid_count = invalid_mask.sum()
    assert invalid_count == 0, f"Found {invalid_count} records where conversions > clicks"

def test_spend_and_revenue_are_non_negative():
    df_clean = pd.read_csv(CLEANED_CSV_PATH)
    negative_spend = (df_clean["ad_spend"] < 0).sum()
    negative_revenue = (df_clean["revenue"] < 0).sum()
    assert negative_spend == 0, f"Found {negative_spend} records with negative ad_spend"
    assert negative_revenue == 0, f"Found {negative_revenue} records with negative revenue"

def test_categorical_standardization():
    df_clean = pd.read_csv(CLEANED_CSV_PATH)
    assert set(df_clean["platform"].unique()).issubset(VALID_PLATFORMS), "Unstandardized platform values found"
    assert set(df_clean["device_type"].unique()).issubset(VALID_DEVICES), "Unstandardized device_type values found"
    assert set(df_clean["region"].unique()).issubset(VALID_REGIONS), "Unstandardized region values found"

def test_date_iso_format_and_six_month_range():
    df_clean = pd.read_csv(CLEANED_CSV_PATH)
    parsed_dates = pd.to_datetime(df_clean["date"], format="%Y-%m-%d", errors="coerce")
    assert parsed_dates.notnull().all(), "Invalid ISO date syntax detected"
    min_date = parsed_dates.min()
    max_date = parsed_dates.max()
    assert min_date >= pd.Timestamp("2026-01-01"), f"Date before 2026-01-01: {min_date}"
    assert max_date <= pd.Timestamp("2026-06-30"), f"Date after 2026-06-30: {max_date}"

def test_minimum_campaign_count():
    df_clean = pd.read_csv(CLEANED_CSV_PATH)
    campaign_count = df_clean["campaign_id"].nunique()
    assert campaign_count >= 40, f"Expected at least 40 campaigns, found {campaign_count}"
