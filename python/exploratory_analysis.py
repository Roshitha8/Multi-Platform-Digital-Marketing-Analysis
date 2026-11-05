"""
Multi-Platform Digital Marketing Campaign Performance Analysis
Module: python/exploratory_analysis.py

Conducts comprehensive Exploratory Data Analysis (EDA) on the cleaned dataset.
Generates 10 high-resolution visualizations saved to output/charts/:
1. 01_platform_spend_vs_revenue.png
2. 02_platform_roas_comparison.png
3. 03_platform_efficiency_metrics.png
4. 04_monthly_spend_revenue_trajectory.png
5. 05_monthly_roas_trend.png
6. 06_top_bottom_campaigns_roas.png
7. 07_regional_performance_breakdown.png
8. 08_device_performance_matrix.png
9. 09_campaign_type_performance.png
10. 10_correlation_heatmap.png
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set publication style
plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Arial", "Helvetica"]
plt.rcParams["axes.edgecolor"] = "#CCCCCC"
plt.rcParams["axes.linewidth"] = 0.8

PRIMARY_COLOR = "#1F4E78"
SECONDARY_COLOR = "#2E75B6"
ACCENT_GREEN = "#2E7D32"
ACCENT_RED = "#C62828"
ACCENT_ORANGE = "#E65100"

def run_eda(cleaned_csv_path: str, charts_dir: str):
    os.makedirs(charts_dir, exist_ok=True)
    print(f"Loading cleaned data from: {cleaned_csv_path}")
    df = pd.read_csv(cleaned_csv_path)

    # -------------------------------------------------------------
    # 1. Platform Spend vs. Revenue
    # -------------------------------------------------------------
    plat_agg = df.groupby("platform", as_index=False).agg({
        "ad_spend": "sum",
        "revenue": "sum",
        "conversions": "sum"
    }).sort_values("revenue", ascending=False)

    fig, ax = plt.subplots(figsize=(9, 5))
    x = np.arange(len(plat_agg))
    width = 0.35

    rects1 = ax.bar(x - width/2, plat_agg["ad_spend"] / 1e6, width, label="Ad Spend ($M)", color="#7F7F7F", edgecolor="none")
    rects2 = ax.bar(x + width/2, plat_agg["revenue"] / 1e6, width, label="Revenue ($M)", color=PRIMARY_COLOR, edgecolor="none")

    ax.set_ylabel("USD (Millions $)", fontsize=11, fontweight="bold")
    ax.set_title("Platform Advertising Spend vs. Revenue Generated", fontsize=13, fontweight="bold", pad=15)
    ax.set_xticks(x)
    ax.set_xticklabels(plat_agg["platform"], fontsize=10, fontweight="bold")
    ax.legend(frameon=True)

    # Value labels
    for rect in rects1:
        h = rect.get_height()
        ax.annotate(f"${h:.2f}M", xy=(rect.get_x() + rect.get_width()/2, h),
                    xytext=(0, 3), textcoords="offset points", ha="center", va="bottom", fontsize=9)
    for rect in rects2:
        h = rect.get_height()
        ax.annotate(f"${h:.2f}M", xy=(rect.get_x() + rect.get_width()/2, h),
                    xytext=(0, 3), textcoords="offset points", ha="center", va="bottom", fontsize=9, fontweight="bold")

    plt.tight_layout()
    chart1_path = os.path.join(charts_dir, "01_platform_spend_vs_revenue.png")
    plt.savefig(chart1_path, dpi=300)
    plt.close()
    print(" Saved Chart 1: Platform Spend vs Revenue")

    # -------------------------------------------------------------
    # 2. Platform ROAS Comparison
    # -------------------------------------------------------------
    plat_agg["roas"] = plat_agg["revenue"] / plat_agg["ad_spend"]
    plat_agg_sorted = plat_agg.sort_values("roas", ascending=True)

    fig, ax = plt.subplots(figsize=(8, 4.5))
    colors = [ACCENT_GREEN if r >= 3.0 else SECONDARY_COLOR if r >= 2.0 else ACCENT_ORANGE for r in plat_agg_sorted["roas"]]
    bars = ax.barh(plat_agg_sorted["platform"], plat_agg_sorted["roas"], color=colors, height=0.55)

    ax.axvline(2.5, color=ACCENT_RED, linestyle="--", linewidth=1.5, label="Target Benchmark ROAS (2.5x)")
    ax.set_xlabel("Return on Ad Spend (ROAS)", fontsize=11, fontweight="bold")
    ax.set_title("Platform Efficiency: Return on Ad Spend (ROAS)", fontsize=13, fontweight="bold", pad=15)
    ax.legend(loc="lower right")

    for bar in bars:
        w = bar.get_width()
        ax.annotate(f"{w:.2f}x", xy=(w, bar.get_y() + bar.get_height()/2),
                    xytext=(5, 0), textcoords="offset points", ha="left", va="center", fontsize=10, fontweight="bold")

    plt.tight_layout()
    chart2_path = os.path.join(charts_dir, "02_platform_roas_comparison.png")
    plt.savefig(chart2_path, dpi=300)
    plt.close()
    print(" Saved Chart 2: Platform ROAS Comparison")

    # -------------------------------------------------------------
    # 3. Platform Efficiency Metrics (CTR, CPC, CPA, CVR)
    # -------------------------------------------------------------
    plat_full = df.groupby("platform", as_index=False).agg({
        "impressions": "sum",
        "clicks": "sum",
        "ad_spend": "sum",
        "conversions": "sum"
    })
    plat_full["ctr_pct"] = (plat_full["clicks"] / plat_full["impressions"]) * 100.0
    plat_full["cpc"] = plat_full["ad_spend"] / plat_full["clicks"]
    plat_full["cpa"] = plat_full["ad_spend"] / plat_full["conversions"]
    plat_full["cvr_pct"] = (plat_full["conversions"] / plat_full["clicks"]) * 100.0

    fig, axes = plt.subplots(2, 2, figsize=(12, 8))

    # CTR
    sns.barplot(data=plat_full, x="platform", y="ctr_pct", hue="platform", ax=axes[0, 0], palette="Blues_r", legend=False)
    axes[0, 0].set_title("Click-Through Rate (CTR %)", fontweight="bold")
    axes[0, 0].set_ylabel("CTR (%)")
    axes[0, 0].set_xlabel("")
    for p in axes[0, 0].patches:
        axes[0, 0].annotate(f"{p.get_height():.2f}%", (p.get_x() + p.get_width()/2., p.get_height()),
                            ha='center', va='bottom', xytext=(0, 3), textcoords='offset points', fontsize=9)

    # CPC
    sns.barplot(data=plat_full, x="platform", y="cpc", hue="platform", ax=axes[0, 1], palette="Blues_r", legend=False)
    axes[0, 1].set_title("Cost Per Click (CPC $)", fontweight="bold")
    axes[0, 1].set_ylabel("CPC ($ USD)")
    axes[0, 1].set_xlabel("")
    for p in axes[0, 1].patches:
        axes[0, 1].annotate(f"${p.get_height():.2f}", (p.get_x() + p.get_width()/2., p.get_height()),
                            ha='center', va='bottom', xytext=(0, 3), textcoords='offset points', fontsize=9)

    # Conversion Rate
    sns.barplot(data=plat_full, x="platform", y="cvr_pct", hue="platform", ax=axes[1, 0], palette="Greens_r", legend=False)
    axes[1, 0].set_title("Conversion Rate (CVR %)", fontweight="bold")
    axes[1, 0].set_ylabel("CVR (%)")
    axes[1, 0].set_xlabel("")
    for p in axes[1, 0].patches:
        axes[1, 0].annotate(f"{p.get_height():.2f}%", (p.get_x() + p.get_width()/2., p.get_height()),
                            ha='center', va='bottom', xytext=(0, 3), textcoords='offset points', fontsize=9)

    # CPA
    sns.barplot(data=plat_full, x="platform", y="cpa", hue="platform", ax=axes[1, 1], palette="Oranges_r", legend=False)
    axes[1, 1].set_title("Cost Per Acquisition (CPA $)", fontweight="bold")
    axes[1, 1].set_ylabel("CPA ($ USD)")
    axes[1, 1].set_xlabel("")
    for p in axes[1, 1].patches:
        axes[1, 1].annotate(f"${p.get_height():.2f}", (p.get_x() + p.get_width()/2., p.get_height()),
                            ha='center', va='bottom', xytext=(0, 3), textcoords='offset points', fontsize=9)

    plt.suptitle("Cross-Platform Marketing Efficiency Dashboard", fontsize=15, fontweight="bold", y=0.98)
    plt.tight_layout()
    chart3_path = os.path.join(charts_dir, "03_platform_efficiency_metrics.png")
    plt.savefig(chart3_path, dpi=300)
    plt.close()
    print(" Saved Chart 3: Platform Efficiency Metrics")

    # -------------------------------------------------------------
    # 4. Monthly Spend and Revenue Trajectory
    # -------------------------------------------------------------
    df["year_month"] = df["date"].str.slice(0, 7)
    month_agg = df.groupby("year_month", as_index=False).agg({
        "ad_spend": "sum",
        "revenue": "sum"
    }).sort_values("year_month")
    month_agg["profit"] = month_agg["revenue"] - month_agg["ad_spend"]

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(month_agg["year_month"], month_agg["revenue"] / 1e3, marker="o", linewidth=2.5, color=PRIMARY_COLOR, label="Revenue ($K)")
    ax.plot(month_agg["year_month"], month_agg["profit"] / 1e3, marker="s", linewidth=2.2, color=ACCENT_GREEN, label="Net Profit ($K)")
    ax.plot(month_agg["year_month"], month_agg["ad_spend"] / 1e3, marker="^", linewidth=2.0, color="#7F7F7F", linestyle="--", label="Ad Spend ($K)")

    ax.set_ylabel("USD (Thousands $)", fontsize=11, fontweight="bold")
    ax.set_title("Monthly Trajectory: Ad Spend, Revenue, and Net Profit (H1 2026)", fontsize=13, fontweight="bold", pad=15)
    ax.legend(frameon=True)

    for i, row in month_agg.iterrows():
        ax.annotate(f"${row['revenue']/1e3:.0f}K", (row["year_month"], row["revenue"]/1e3),
                    xytext=(0, 7), textcoords="offset points", ha="center", fontsize=8.5, fontweight="bold", color=PRIMARY_COLOR)
        ax.annotate(f"${row['ad_spend']/1e3:.0f}K", (row["year_month"], row["ad_spend"]/1e3),
                    xytext=(0, -14), textcoords="offset points", ha="center", fontsize=8.5, color="#555555")

    plt.tight_layout()
    chart4_path = os.path.join(charts_dir, "04_monthly_spend_revenue_trajectory.png")
    plt.savefig(chart4_path, dpi=300)
    plt.close()
    print(" Saved Chart 4: Monthly Spend and Revenue Trajectory")

    # -------------------------------------------------------------
    # 5. Monthly ROAS Trend
    # -------------------------------------------------------------
    month_agg["roas"] = month_agg["revenue"] / month_agg["ad_spend"]
    fig, ax = plt.subplots(figsize=(9, 4.5))
    ax.plot(month_agg["year_month"], month_agg["roas"], marker="o", linewidth=2.5, color=ACCENT_GREEN, label="Monthly ROAS")
    ax.axhline(month_agg["roas"].mean(), color=ACCENT_RED, linestyle=":", linewidth=1.5,
               label=f"H1 Average ROAS ({month_agg['roas'].mean():.2f}x)")

    ax.set_ylabel("Return on Ad Spend (ROAS)", fontsize=11, fontweight="bold")
    ax.set_title("Month-over-Month Return on Ad Spend (ROAS) Trend", fontsize=13, fontweight="bold", pad=15)
    ax.set_ylim(2.0, 4.0)
    ax.legend(loc="upper left")

    for i, row in month_agg.iterrows():
        ax.annotate(f"{row['roas']:.2f}x", (row["year_month"], row["roas"]),
                    xytext=(0, 8), textcoords="offset points", ha="center", fontsize=9.5, fontweight="bold")

    plt.tight_layout()
    chart5_path = os.path.join(charts_dir, "05_monthly_roas_trend.png")
    plt.savefig(chart5_path, dpi=300)
    plt.close()
    print(" Saved Chart 5: Monthly ROAS Trend")

    # -------------------------------------------------------------
    # 6. Top 5 vs Bottom 5 Campaigns by ROAS
    # -------------------------------------------------------------
    camp_agg = df.groupby(["campaign_name", "platform"], as_index=False).agg({
        "ad_spend": "sum",
        "revenue": "sum",
        "conversions": "sum"
    })
    camp_agg["roas"] = camp_agg["revenue"] / camp_agg["ad_spend"]

    top5 = camp_agg.nlargest(5, "roas").copy()
    top5["group"] = "Top 5 (Scale Up)"
    bot5 = camp_agg.nsmallest(5, "roas").copy()
    bot5["group"] = "Bottom 5 (Restructure)"
    top_bot = pd.concat([top5, bot5]).sort_values("roas", ascending=True)

    fig, ax = plt.subplots(figsize=(10, 6))
    bar_colors = [ACCENT_RED if g == "Bottom 5 (Restructure)" else ACCENT_GREEN for g in top_bot["group"]]
    bars = ax.barh(top_bot["campaign_name"], top_bot["roas"], color=bar_colors, height=0.6)

    ax.axvline(2.5, color="#555555", linestyle="--", linewidth=1.2, label="Benchmark ROAS (2.5x)")
    ax.set_xlabel("ROAS (Return on Ad Spend)", fontsize=11, fontweight="bold")
    ax.set_title("Top 5 vs. Bottom 5 Campaigns by Return on Ad Spend (ROAS)", fontsize=13, fontweight="bold", pad=15)
    ax.legend(loc="lower right")

    for bar in bars:
        w = bar.get_width()
        ax.annotate(f"{w:.2f}x", xy=(w, bar.get_y() + bar.get_height()/2),
                    xytext=(5, 0), textcoords="offset points", ha="left", va="center", fontsize=9, fontweight="bold")

    plt.tight_layout()
    chart6_path = os.path.join(charts_dir, "06_top_bottom_campaigns_roas.png")
    plt.savefig(chart6_path, dpi=300)
    plt.close()
    print(" Saved Chart 6: Top/Bottom Campaigns by ROAS")

    # -------------------------------------------------------------
    # 7. Regional Performance Breakdown
    # -------------------------------------------------------------
    reg_agg = df.groupby("region", as_index=False).agg({
        "ad_spend": "sum",
        "revenue": "sum",
        "conversions": "sum"
    }).sort_values("revenue", ascending=False)
    reg_agg["roas"] = reg_agg["revenue"] / reg_agg["ad_spend"]
    reg_agg["cpa"] = reg_agg["ad_spend"] / reg_agg["conversions"]

    fig, ax1 = plt.subplots(figsize=(9, 5))
    x = np.arange(len(reg_agg))
    w = 0.35

    ax1.bar(x - w/2, reg_agg["revenue"] / 1e6, width=w, label="Revenue ($M)", color=PRIMARY_COLOR)
    ax1.bar(x + w/2, reg_agg["ad_spend"] / 1e6, width=w, label="Ad Spend ($M)", color="#A6A6A6")
    ax1.set_ylabel("USD (Millions $)", fontsize=11, fontweight="bold")
    ax1.set_xticks(x)
    ax1.set_xticklabels(reg_agg["region"], fontsize=10, fontweight="bold")
    ax1.set_title("Geographic Performance Breakdown: Revenue vs. Spend", fontsize=13, fontweight="bold", pad=15)
    ax1.legend(loc="upper right")

    for i, r in reg_agg.reset_index(drop=True).iterrows():
        ax1.annotate(f"ROAS: {r['roas']:.2f}x\nCPA: ${r['cpa']:.2f}",
                     (x[i], max(r["revenue"]/1e6, r["ad_spend"]/1e6) + 0.2),
                     ha="center", fontsize=8.5, fontweight="bold", color="#333333")

    ax1.set_ylim(0, max(reg_agg["revenue"]/1e6) * 1.25)
    plt.tight_layout()
    chart7_path = os.path.join(charts_dir, "07_regional_performance_breakdown.png")
    plt.savefig(chart7_path, dpi=300)
    plt.close()
    print(" Saved Chart 7: Regional Performance Breakdown")

    # -------------------------------------------------------------
    # 8. Device Performance Matrix
    # -------------------------------------------------------------
    dev_agg = df.groupby("device_type", as_index=False).agg({
        "impressions": "sum",
        "clicks": "sum",
        "conversions": "sum",
        "revenue": "sum",
        "ad_spend": "sum"
    })
    dev_agg["roas"] = dev_agg["revenue"] / dev_agg["ad_spend"]
    dev_agg["cvr_pct"] = (dev_agg["conversions"] / dev_agg["clicks"]) * 100.0

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.5))

    # Conversion share
    ax1.pie(dev_agg["conversions"], labels=dev_agg["device_type"], autopct="%1.1f%%",
            startangle=140, colors=[PRIMARY_COLOR, SECONDARY_COLOR, "#BDD7EE"], explode=(0.04, 0.04, 0.04))
    ax1.set_title("Share of Total Conversions by Device", fontweight="bold")

    # CVR and ROAS comparison
    x_dev = np.arange(len(dev_agg))
    w_dev = 0.35
    ax2.bar(x_dev - w_dev/2, dev_agg["cvr_pct"], width=w_dev, label="Conversion Rate (%)", color=ACCENT_GREEN)
    ax2.bar(x_dev + w_dev/2, dev_agg["roas"], width=w_dev, label="ROAS (x)", color=PRIMARY_COLOR)
    ax2.set_xticks(x_dev)
    ax2.set_xticklabels(dev_agg["device_type"], fontweight="bold")
    ax2.set_title("Conversion Rate vs. ROAS by Device", fontweight="bold")
    ax2.legend()

    for i in range(len(dev_agg)):
        ax2.annotate(f"{dev_agg['cvr_pct'].iloc[i]:.2f}%", (x_dev[i] - w_dev/2, dev_agg['cvr_pct'].iloc[i]),
                     ha='center', va='bottom', xytext=(0, 3), textcoords='offset points', fontsize=9)
        ax2.annotate(f"{dev_agg['roas'].iloc[i]:.2f}x", (x_dev[i] + w_dev/2, dev_agg['roas'].iloc[i]),
                     ha='center', va='bottom', xytext=(0, 3), textcoords='offset points', fontsize=9, fontweight="bold")

    plt.tight_layout()
    chart8_path = os.path.join(charts_dir, "08_device_performance_matrix.png")
    plt.savefig(chart8_path, dpi=300)
    plt.close()
    print(" Saved Chart 8: Device Performance Matrix")

    # -------------------------------------------------------------
    # 9. Campaign Type Performance
    # -------------------------------------------------------------
    type_agg = df.groupby("campaign_type", as_index=False).agg({
        "ad_spend": "sum",
        "revenue": "sum",
        "conversions": "sum"
    })
    type_agg["roas"] = type_agg["revenue"] / type_agg["ad_spend"]
    type_agg = type_agg.sort_values("roas", ascending=True)

    fig, ax = plt.subplots(figsize=(9, 5))
    bars = ax.barh(type_agg["campaign_type"], type_agg["roas"], color=PRIMARY_COLOR, height=0.6)
    ax.axvline(2.5, color=ACCENT_RED, linestyle="--", linewidth=1.2, label="Benchmark ROAS (2.5x)")
    ax.set_xlabel("Return on Ad Spend (ROAS)", fontsize=11, fontweight="bold")
    ax.set_title("Campaign Strategy Breakdown: ROAS by Tactical Ad Type", fontsize=13, fontweight="bold", pad=15)
    ax.legend(loc="lower right")

    for bar in bars:
        w = bar.get_width()
        ax.annotate(f"{w:.2f}x", xy=(w, bar.get_y() + bar.get_height()/2),
                    xytext=(5, 0), textcoords="offset points", ha="left", va="center", fontsize=9, fontweight="bold")

    plt.tight_layout()
    chart9_path = os.path.join(charts_dir, "09_campaign_type_performance.png")
    plt.savefig(chart9_path, dpi=300)
    plt.close()
    print(" Saved Chart 9: Campaign Type Performance")

    # -------------------------------------------------------------
    # 10. Correlation Heatmap
    # -------------------------------------------------------------
    corr_cols = ["ad_spend", "impressions", "clicks", "conversions", "revenue"]
    corr_matrix = df[corr_cols].corr()

    fig, ax = plt.subplots(figsize=(7, 6))
    sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="Blues", cbar=True, ax=ax,
                linewidths=0.5, square=True, annot_kws={"size": 10, "weight": "bold"})
    ax.set_title("Marketing Metrics Telemetry Correlation Matrix", fontsize=13, fontweight="bold", pad=15)
    ax.set_xticklabels(["Ad Spend", "Impressions", "Clicks", "Conversions", "Revenue"], rotation=45, ha="right", fontsize=9.5)
    ax.set_yticklabels(["Ad Spend", "Impressions", "Clicks", "Conversions", "Revenue"], rotation=0, fontsize=9.5)

    plt.tight_layout()
    chart10_path = os.path.join(charts_dir, "10_correlation_heatmap.png")
    plt.savefig(chart10_path, dpi=300)
    plt.close()
    print(" Saved Chart 10: Correlation Heatmap")

    print(f"\nAll 10 EDA charts generated and saved successfully to: {charts_dir}")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    cleaned_csv = os.path.join(base_dir, "data", "campaign_data_cleaned.csv")
    charts_folder = os.path.join(base_dir, "output", "charts")

    run_eda(cleaned_csv, charts_folder)
