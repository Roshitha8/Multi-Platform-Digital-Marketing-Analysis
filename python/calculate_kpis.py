"""
Multi-Platform Digital Marketing Campaign Performance Analysis
Module: python/calculate_kpis.py

Provides robust, production-grade calculation of digital marketing KPIs
both at the row-level and across aggregated dimensional slices.

Key Formulas:
- CTR (%) = (Clicks / Impressions) * 100
- CPC ($) = Ad Spend / Clicks
- CPA ($) = Ad Spend / Conversions
- Conversion Rate (%) = (Conversions / Clicks) * 100
- ROAS (ratio) = Revenue / Ad Spend
- Average Order Revenue ($) = Revenue / Conversions

Critical Guardrail:
In aggregations, ratios/rates are computed strictly from summed numerators
and denominators (e.g. SUM(Revenue) / SUM(Ad Spend)), never by averaging
row-level ratios. Safe division handles zero-denominator edge cases.
"""

from typing import Union, Dict, Any
import pandas as pd
import numpy as np

def safe_divide(numerator: Union[float, int, pd.Series], denominator: Union[float, int, pd.Series], default=None):
    """
    Safely divides numerator by denominator, returning default (or np.nan) when denominator is 0 or null.
    """
    if isinstance(numerator, pd.Series) or isinstance(denominator, pd.Series):
        denom = denominator.replace(0, np.nan)
        res = numerator / denom
        if default is not None:
            res = res.fillna(default)
        return res
    else:
        if denominator is None or denominator == 0 or np.isnan(denominator):
            return default
        return numerator / denominator

def calculate_row_level_kpis(df: pd.DataFrame) -> pd.DataFrame:
    """
    Appends row-level KPI metrics to a copy of the input DataFrame.
    """
    res = df.copy()
    res["ctr_pct"] = safe_divide(res["clicks"] * 100.0, res["impressions"], default=0.0).round(2)
    res["cpc"] = safe_divide(res["ad_spend"], res["clicks"], default=0.0).round(2)
    res["cpa"] = safe_divide(res["ad_spend"], res["conversions"], default=0.0).round(2)
    res["conversion_rate_pct"] = safe_divide(res["conversions"] * 100.0, res["clicks"], default=0.0).round(2)
    res["roas"] = safe_divide(res["revenue"], res["ad_spend"], default=0.0).round(2)
    res["aor"] = safe_divide(res["revenue"], res["conversions"], default=0.0).round(2)
    return res

def calculate_aggregate_kpis(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Computes overall summary KPIs across an entire dataset using true aggregated numerators and denominators.
    """
    total_impressions = int(df["impressions"].sum())
    total_clicks = int(df["clicks"].sum())
    total_spend = float(df["ad_spend"].sum())
    total_conversions = int(df["conversions"].sum())
    total_revenue = float(df["revenue"].sum())

    ctr_pct = safe_divide(total_clicks * 100.0, total_impressions, default=0.0)
    cpc = safe_divide(total_spend, total_clicks, default=0.0)
    cpa = safe_divide(total_spend, total_conversions, default=0.0)
    cvr_pct = safe_divide(total_conversions * 100.0, total_clicks, default=0.0)
    roas = safe_divide(total_revenue, total_spend, default=0.0)
    aor = safe_divide(total_revenue, total_conversions, default=0.0)

    return {
        "total_records": len(df),
        "total_impressions": total_impressions,
        "total_clicks": total_clicks,
        "total_spend": round(total_spend, 2),
        "total_conversions": total_conversions,
        "total_revenue": round(total_revenue, 2),
        "net_profit": round(total_revenue - total_spend, 2),
        "ctr_pct": round(ctr_pct, 2),
        "cpc": round(cpc, 2),
        "cpa": round(cpa, 2),
        "conversion_rate_pct": round(cvr_pct, 2),
        "roas": round(roas, 2),
        "average_order_revenue": round(aor, 2)
    }

def aggregate_by_dimension(df: pd.DataFrame, dimension: Union[str, list]) -> pd.DataFrame:
    """
    Groups by one or more dimensions and computes correct aggregate KPIs.
    """
    grouped = df.groupby(dimension, as_index=False).agg({
        "impressions": "sum",
        "clicks": "sum",
        "ad_spend": "sum",
        "conversions": "sum",
        "revenue": "sum"
    })

    grouped["ctr_pct"] = (grouped["clicks"] / grouped["impressions"] * 100.0).round(2)
    grouped["cpc"] = (grouped["ad_spend"] / grouped["clicks"]).round(2)
    grouped["cpa"] = (grouped["ad_spend"] / grouped["conversions"]).round(2)
    grouped["conversion_rate_pct"] = (grouped["conversions"] / grouped["clicks"] * 100.0).round(2)
    grouped["roas"] = (grouped["revenue"] / grouped["ad_spend"]).round(2)
    grouped["average_order_revenue"] = (grouped["revenue"] / grouped["conversions"]).round(2)

    grouped["ad_spend"] = grouped["ad_spend"].round(2)
    grouped["revenue"] = grouped["revenue"].round(2)

    return grouped

if __name__ == "__main__":
    import os
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    cleaned_csv = os.path.join(base_dir, "data", "campaign_data_cleaned.csv")
    if os.path.exists(cleaned_csv):
        df = pd.read_csv(cleaned_csv)
        summary = calculate_aggregate_kpis(df)
        print("=== OVERALL MARKETING KPI SUMMARY ===")
        for k, v in summary.items():
            print(f"  {k}: {v}")
    else:
        print(f"File not found: {cleaned_csv}")
