"""
Multi-Platform Digital Marketing Campaign Performance Analysis
Test Suite: tests/test_kpis.py

Validates marketing KPI math, database query execution, Excel structure,
and chart artifact generation using pytest.
"""

import os
import sqlite3
import pandas as pd
import openpyxl
import pytest

from python.calculate_kpis import (
    safe_divide,
    calculate_row_level_kpis,
    calculate_aggregate_kpis,
    aggregate_by_dimension
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLEANED_CSV_PATH = os.path.join(BASE_DIR, "data", "campaign_data_cleaned.csv")
DB_PATH = os.path.join(BASE_DIR, "database", "digital_marketing.db")
SQL_FILE_PATH = os.path.join(BASE_DIR, "database", "marketing_analysis.sql")
EXCEL_PATH = os.path.join(BASE_DIR, "excel", "Digital_Marketing_Analysis.xlsx")
CHARTS_DIR = os.path.join(BASE_DIR, "output", "charts")
REPORTS_DIR = os.path.join(BASE_DIR, "output", "reports")

def test_safe_divide():
    assert safe_divide(100, 2) == 50.0
    assert safe_divide(100, 0, default=0.0) == 0.0
    assert safe_divide(100, None, default=None) is None

def test_aggregate_kpi_calculations():
    df = pd.read_csv(CLEANED_CSV_PATH)
    metrics = calculate_aggregate_kpis(df)

    expected_ctr = round((metrics["total_clicks"] / metrics["total_impressions"]) * 100.0, 2)
    expected_cpc = round(metrics["total_spend"] / metrics["total_clicks"], 2)
    expected_cpa = round(metrics["total_spend"] / metrics["total_conversions"], 2)
    expected_cvr = round((metrics["total_conversions"] / metrics["total_clicks"]) * 100.0, 2)
    expected_roas = round(metrics["total_revenue"] / metrics["total_spend"], 2)

    assert metrics["ctr_pct"] == expected_ctr
    assert metrics["cpc"] == expected_cpc
    assert metrics["cpa"] == expected_cpa
    assert metrics["conversion_rate_pct"] == expected_cvr
    assert metrics["roas"] == expected_roas

def test_sqlite_database_and_all_twenty_queries():
    assert os.path.exists(DB_PATH), f"SQLite DB missing at {DB_PATH}"
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM campaign_performance;")
    row_count = cursor.fetchone()[0]
    assert row_count >= 10000, f"Expected >= 10,000 DB records, found {row_count}"

    with open(SQL_FILE_PATH, "r", encoding="utf-8") as f:
        sql_content = f.read()

    statements = [stmt.strip() for stmt in sql_content.split(";") if stmt.strip()]
    select_queries = []
    for stmt in statements:
        lines = [line.strip() for line in stmt.split("\n") if line.strip() and not line.strip().startswith("--")]
        if lines:
            cleaned_stmt = " ".join(lines)
            if cleaned_stmt.upper().startswith("SELECT") or cleaned_stmt.upper().startswith("WITH"):
                select_queries.append(stmt)

    assert len(select_queries) >= 20, f"Expected >= 20 SELECT queries, found {len(select_queries)}"

    for idx, query in enumerate(select_queries, 1):
        res_df = pd.read_sql_query(query, conn)
        assert res_df is not None, f"Query {idx} returned None"
        assert len(res_df) > 0, f"Query {idx} returned 0 rows"

    conn.close()

def test_excel_workbook_sheets_and_tables():
    assert os.path.exists(EXCEL_PATH), f"Excel workbook missing at {EXCEL_PATH}"
    wb = openpyxl.load_workbook(EXCEL_PATH, data_only=False)

    required_sheets = {
        "Dashboard", "Raw_Data", "Cleaned_Data",
        "KPI_Calculations", "Platform_Analysis",
        "Campaign_Analysis", "Monthly_Trends"
    }
    assert required_sheets.issubset(set(wb.sheetnames)), f"Missing sheets: {required_sheets - set(wb.sheetnames)}"

    # Validate that KPI formulas exist in KPI_Calculations
    ws_kpi = wb["KPI_Calculations"]
    assert str(ws_kpi["C5"].value).startswith("="), "Formula missing in KPI_Calculations C5"
    assert str(ws_kpi["D5"].value).startswith("="), "Formula missing in KPI_Calculations D5"

def test_charts_generated():
    expected_charts = [
        "01_platform_spend_vs_revenue.png",
        "02_platform_roas_comparison.png",
        "03_platform_efficiency_metrics.png",
        "04_monthly_spend_revenue_trajectory.png",
        "05_monthly_roas_trend.png",
        "06_top_bottom_campaigns_roas.png",
        "07_regional_performance_breakdown.png",
        "08_device_performance_matrix.png",
        "09_campaign_type_performance.png",
        "10_correlation_heatmap.png"
    ]
    for ch in expected_charts:
        p = os.path.join(CHARTS_DIR, ch)
        assert os.path.exists(p), f"Chart {ch} missing from {CHARTS_DIR}"
        assert os.path.getsize(p) > 10000, f"Chart {ch} appears corrupted or empty"

def test_markdown_reports_exist():
    quality_rep = os.path.join(REPORTS_DIR, "data_quality_report.md")
    insights_rep = os.path.join(REPORTS_DIR, "business_insights.md")
    assert os.path.exists(quality_rep), "data_quality_report.md missing"
    assert os.path.exists(insights_rep), "business_insights.md missing"
    assert os.path.getsize(quality_rep) > 500, "data_quality_report.md too small"
    assert os.path.getsize(insights_rep) > 1000, "business_insights.md too small"
