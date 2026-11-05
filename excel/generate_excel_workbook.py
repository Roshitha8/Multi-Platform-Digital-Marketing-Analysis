"""
Multi-Platform Digital Marketing Campaign Performance Analysis
Module: excel/generate_excel_workbook.py

Creates the professional, formula-driven Excel workbook:
excel/Digital_Marketing_Analysis.xlsx

Includes 7 Worksheets:
1. Raw_Data: Initial ingested dataset.
2. Cleaned_Data: Normalized, validated dataset formatted as an Excel Table.
3. KPI_Calculations: Formulas for executive marketing scorecard.
4. Platform_Analysis: Platform summary with SUMIF formulas and native Excel Bar Charts.
5. Campaign_Analysis: 44 campaign breakdown with SUMIFS formulas and conditional formatting.
6. Monthly_Trends: Month-by-month trajectory with SUMIFS and native Line Charts.
7. Dashboard: High-impact executive dashboard with KPI cards, tables, and comparison charts.
"""

import os
import pandas as pd
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.chart import BarChart, LineChart, Reference, Series
from openpyxl.formatting.rule import CellIsRule, ColorScaleRule

def create_excel_workbook(raw_csv_path: str, cleaned_csv_path: str, output_xlsx_path: str):
    print("Generating comprehensive Excel workbook...")
    df_raw = pd.read_csv(raw_csv_path)
    df_cleaned = pd.read_csv(cleaned_csv_path)

    wb = openpyxl.Workbook()
    # Remove default sheet
    default_sheet = wb.active

    # Styling Palettes
    navy_header_fill = PatternFill(start_color="1F4E78", end_color="1F4E78", fill_type="solid")
    steel_header_fill = PatternFill(start_color="2F5597", end_color="2F5597", fill_type="solid")
    accent_kpi_fill = PatternFill(start_color="D9E1F2", end_color="D9E1F2", fill_type="solid")
    card_header_fill = PatternFill(start_color="002060", end_color="002060", fill_type="solid")
    card_body_fill = PatternFill(start_color="F2F2F2", end_color="F2F2F2", fill_type="solid")
    zebra_fill = PatternFill(start_color="F9FAFB", end_color="F9FAFB", fill_type="solid")

    font_header = Font(name="Segoe UI", size=11, bold=True, color="FFFFFF")
    font_bold = Font(name="Segoe UI", size=11, bold=True, color="000000")
    font_card_title = Font(name="Segoe UI", size=9, bold=True, color="FFFFFF")
    font_card_value = Font(name="Segoe UI", size=16, bold=True, color="1F4E78")
    font_body = Font(name="Segoe UI", size=10, color="000000")
    font_title_large = Font(name="Segoe UI", size=16, bold=True, color="1F4E78")
    font_subtitle = Font(name="Segoe UI", size=10, italic=True, color="595959")

    thin_border_side = Side(border_style="thin", color="D9D9D9")
    thick_bottom_side = Side(border_style="medium", color="1F4E78")
    cell_border = Border(left=thin_border_side, right=thin_border_side, top=thin_border_side, bottom=thin_border_side)
    header_border = Border(left=thin_border_side, right=thin_border_side, top=thin_border_side, bottom=thick_bottom_side)

    # -------------------------------------------------------------
    # SHEET 1: Raw_Data
    # -------------------------------------------------------------
    ws_raw = wb.create_sheet(title="Raw_Data")
    ws_raw.views.sheetView[0].showGridLines = True
    raw_headers = list(df_raw.columns)
    ws_raw.append(raw_headers)
    for col_idx, h in enumerate(raw_headers, 1):
        cell = ws_raw.cell(row=1, column=col_idx)
        cell.font = font_header
        cell.fill = steel_header_fill
        cell.alignment = Alignment(horizontal="center", vertical="center")

    # Write raw rows
    for r_idx, row in enumerate(df_raw.itertuples(index=False), 2):
        ws_raw.append(list(row))
        if r_idx % 2 == 0:
            for c_idx in range(1, len(raw_headers) + 1):
                ws_raw.cell(row=r_idx, column=c_idx).fill = zebra_fill
    print(f"Sheet 'Raw_Data' written with {len(df_raw)} records.")

    # -------------------------------------------------------------
    # SHEET 2: Cleaned_Data
    # -------------------------------------------------------------
    ws_clean = wb.create_sheet(title="Cleaned_Data")
    ws_clean.views.sheetView[0].showGridLines = True
    clean_headers = list(df_cleaned.columns)
    ws_clean.append(clean_headers)
    for col_idx, h in enumerate(clean_headers, 1):
        cell = ws_clean.cell(row=1, column=col_idx)
        cell.font = font_header
        cell.fill = navy_header_fill
        cell.alignment = Alignment(horizontal="center", vertical="center")

    num_clean_rows = len(df_cleaned)
    for r_idx, row in enumerate(df_cleaned.itertuples(index=False), 2):
        ws_clean.append(list(row))
        # Formats: impressions(col 10), clicks(col 11), ad_spend(col 12), conversions(col 13), revenue(col 14)
        ws_clean.cell(row=r_idx, column=10).number_format = "#,##0"
        ws_clean.cell(row=r_idx, column=11).number_format = "#,##0"
        ws_clean.cell(row=r_idx, column=12).number_format = "$#,##0.00"
        ws_clean.cell(row=r_idx, column=13).number_format = "#,##0"
        ws_clean.cell(row=r_idx, column=14).number_format = "$#,##0.00"

    print(f"Sheet 'Cleaned_Data' written with {num_clean_rows} records.")

    # -------------------------------------------------------------
    # SHEET 3: KPI_Calculations
    # -------------------------------------------------------------
    ws_kpi = wb.create_sheet(title="KPI_Calculations")
    ws_kpi.views.sheetView[0].showGridLines = True
    ws_kpi["A1"] = "Multi-Platform Marketing Performance Scorecard"
    ws_kpi["A1"].font = font_title_large
    ws_kpi["A2"] = "Master formulas computed dynamically from Cleaned_Data telemetry"
    ws_kpi["A2"].font = font_subtitle

    kpi_table_headers = ["Metric Category", "Marketing KPI", "Excel Dynamic Formula", "Computed Value", "Benchmark Status"]
    for col_idx, th in enumerate(kpi_table_headers, 1):
        cell = ws_kpi.cell(row=4, column=col_idx, value=th)
        cell.font = font_header
        cell.fill = navy_header_fill
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = header_border

    end_row_ref = num_clean_rows + 1

    kpi_rows = [
        ("Volume Metrics", "Total Impressions", f"=SUM(Cleaned_Data!J2:J{end_row_ref})", "#,##0", "Healthy"),
        ("Volume Metrics", "Total Clicks", f"=SUM(Cleaned_Data!K2:K{end_row_ref})", "#,##0", "Healthy"),
        ("Financials", "Total Ad Spend", f"=SUM(Cleaned_Data!L2:L{end_row_ref})", "$#,##0.00", "Under Budget Cap"),
        ("Conversions", "Total Conversions", f"=SUM(Cleaned_Data!M2:M{end_row_ref})", "#,##0", "Above Target"),
        ("Financials", "Total Revenue", f"=SUM(Cleaned_Data!N2:N{end_row_ref})", "$#,##0.00", "High Performing"),
        ("Financials", "Net Profit", "=D9-D7", "$#,##0.00", "Strong ROI"),
        ("Efficiency", "Click-Through Rate (CTR)", "=(D6/D5)*100", "0.00\"%\"", "Above Benchmark (2.2%)"),
        ("Efficiency", "Cost Per Click (CPC)", "=D7/D6", "$#,##0.00", "Cost Effective ($1.05)"),
        ("Efficiency", "Cost Per Acquisition (CPA)", "=D7/D8", "$#,##0.00", "Optimal Target ($36.88)"),
        ("Efficiency", "Conversion Rate (CVR)", "=(D8/D6)*100", "0.00\"%\"", "High Intent (2.86%)"),
        ("Efficiency", "Return On Ad Spend (ROAS)", "=D9/D7", "0.00\"x\"", "Exceeds 2.5x Target"),
        ("Value", "Average Order Revenue (AOR)", "=D9/D8", "$#,##0.00", "Premium ($110.18)")
    ]

    for idx, (cat, name, formula, fmt, bench) in enumerate(kpi_rows, start=5):
        ws_kpi.cell(row=idx, column=1, value=cat).font = font_bold
        ws_kpi.cell(row=idx, column=2, value=name).font = font_body
        ws_kpi.cell(row=idx, column=3, value=formula).font = font_subtitle
        val_cell = ws_kpi.cell(row=idx, column=4, value=formula)
        val_cell.font = font_bold
        val_cell.number_format = fmt
        val_cell.alignment = Alignment(horizontal="right")
        ws_kpi.cell(row=idx, column=5, value=bench).font = font_body

        for c_i in range(1, 6):
            ws_kpi.cell(row=idx, column=c_i).border = cell_border

    # -------------------------------------------------------------
    # SHEET 4: Platform_Analysis
    # -------------------------------------------------------------
    ws_plat = wb.create_sheet(title="Platform_Analysis")
    ws_plat.views.sheetView[0].showGridLines = True
    ws_plat["A1"] = "Advertising Platform Performance Analysis"
    ws_plat["A1"].font = font_title_large
    ws_plat["A2"] = "Dynamic aggregation using Excel SUMIF formulas across Meta Ads, Google Ads, LinkedIn Ads, and X Ads"
    ws_plat["A2"].font = font_subtitle

    plat_headers = ["Platform", "Total Spend", "Impressions", "Clicks", "Conversions", "Revenue", "CTR", "CPC", "CPA", "CVR", "ROAS"]
    for c_i, h in enumerate(plat_headers, 1):
        cell = ws_plat.cell(row=4, column=c_i, value=h)
        cell.font = font_header
        cell.fill = navy_header_fill
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = header_border

    platforms = ["Meta Ads", "Google Ads", "LinkedIn Ads", "X Ads"]
    for idx, p in enumerate(platforms, start=5):
        # Platform name
        ws_plat.cell(row=idx, column=1, value=p).font = font_bold
        # Spend
        spend_c = ws_plat.cell(row=idx, column=2, value=f'=SUMIF(Cleaned_Data!$C$2:$C${end_row_ref}, "{p}", Cleaned_Data!$L$2:$L${end_row_ref})')
        spend_c.number_format = "$#,##0.00"
        # Impressions
        imp_c = ws_plat.cell(row=idx, column=3, value=f'=SUMIF(Cleaned_Data!$C$2:$C${end_row_ref}, "{p}", Cleaned_Data!$J$2:$J${end_row_ref})')
        imp_c.number_format = "#,##0"
        # Clicks
        clk_c = ws_plat.cell(row=idx, column=4, value=f'=SUMIF(Cleaned_Data!$C$2:$C${end_row_ref}, "{p}", Cleaned_Data!$K$2:$K${end_row_ref})')
        clk_c.number_format = "#,##0"
        # Conversions
        cvr_c = ws_plat.cell(row=idx, column=5, value=f'=SUMIF(Cleaned_Data!$C$2:$C${end_row_ref}, "{p}", Cleaned_Data!$M$2:$M${end_row_ref})')
        cvr_c.number_format = "#,##0"
        # Revenue
        rev_c = ws_plat.cell(row=idx, column=6, value=f'=SUMIF(Cleaned_Data!$C$2:$C${end_row_ref}, "{p}", Cleaned_Data!$N$2:$N${end_row_ref})')
        rev_c.number_format = "$#,##0.00"
        # CTR
        ctr_c = ws_plat.cell(row=idx, column=7, value=f'=(D{idx}/C{idx})')
        ctr_c.number_format = "0.00%"
        # CPC
        cpc_c = ws_plat.cell(row=idx, column=8, value=f'=(B{idx}/D{idx})')
        cpc_c.number_format = "$#,##0.00"
        # CPA
        cpa_c = ws_plat.cell(row=idx, column=9, value=f'=(B{idx}/E{idx})')
        cpa_c.number_format = "$#,##0.00"
        # CVR
        cvr_pct_c = ws_plat.cell(row=idx, column=10, value=f'=(E{idx}/D{idx})')
        cvr_pct_c.number_format = "0.00%"
        # ROAS
        roas_c = ws_plat.cell(row=idx, column=11, value=f'=(F{idx}/B{idx})')
        roas_c.number_format = "0.00\"x\""

        for c_i in range(1, 12):
            ws_plat.cell(row=idx, column=c_i).border = cell_border

    # Total row
    tot_row = 9
    ws_plat.cell(row=tot_row, column=1, value="Total / Overall").font = font_bold
    ws_plat.cell(row=tot_row, column=2, value="=SUM(B5:B8)").number_format = "$#,##0.00"
    ws_plat.cell(row=tot_row, column=3, value="=SUM(C5:C8)").number_format = "#,##0"
    ws_plat.cell(row=tot_row, column=4, value="=SUM(D5:D8)").number_format = "#,##0"
    ws_plat.cell(row=tot_row, column=5, value="=SUM(E5:E8)").number_format = "#,##0"
    ws_plat.cell(row=tot_row, column=6, value="=SUM(F5:F8)").number_format = "$#,##0.00"
    ws_plat.cell(row=tot_row, column=7, value="=(D9/C9)").number_format = "0.00%"
    ws_plat.cell(row=tot_row, column=8, value="=(B9/D9)").number_format = "$#,##0.00"
    ws_plat.cell(row=tot_row, column=9, value="=(B9/E9)").number_format = "$#,##0.00"
    ws_plat.cell(row=tot_row, column=10, value="=(E9/D9)").number_format = "0.00%"
    ws_plat.cell(row=tot_row, column=11, value="=(F9/B9)").number_format = "0.00\"x\""
    for c_i in range(1, 12):
        c = ws_plat.cell(row=tot_row, column=c_i)
        c.font = font_bold
        c.fill = accent_kpi_fill
        c.border = cell_border

    # Platform Spend vs Revenue Bar Chart
    chart_plat = BarChart()
    chart_plat.type = "col"
    chart_plat.style = 10
    chart_plat.title = "Platform Ad Spend vs. Revenue ($ USD)"
    chart_plat.y_axis.title = "USD ($)"
    chart_plat.x_axis.title = "Platform"
    data_ref = Reference(ws_plat, min_col=2, min_row=4, max_col=2, max_row=8)
    data_rev = Reference(ws_plat, min_col=6, min_row=4, max_col=6, max_row=8)
    chart_plat.add_data(data_ref, titles_from_data=True)
    chart_plat.add_data(data_rev, titles_from_data=True)
    cats_ref = Reference(ws_plat, min_col=1, min_row=5, max_row=8)
    chart_plat.set_categories(cats_ref)
    chart_plat.height = 12
    chart_plat.width = 18
    ws_plat.add_chart(chart_plat, "A12")

    # Platform ROAS Bar Chart
    chart_roas = BarChart()
    chart_roas.type = "bar"
    chart_roas.style = 11
    chart_roas.title = "Platform Return On Ad Spend (ROAS)"
    chart_roas.x_axis.title = "ROAS (x)"
    chart_roas.y_axis.title = "Platform"
    data_roas = Reference(ws_plat, min_col=11, min_row=4, max_col=11, max_row=8)
    chart_roas.add_data(data_roas, titles_from_data=True)
    chart_roas.set_categories(cats_ref)
    chart_roas.height = 12
    chart_roas.width = 16
    ws_plat.add_chart(chart_roas, "H12")

    # -------------------------------------------------------------
    # SHEET 5: Campaign_Analysis
    # -------------------------------------------------------------
    ws_camp = wb.create_sheet(title="Campaign_Analysis")
    ws_camp.views.sheetView[0].showGridLines = True
    ws_camp["A1"] = "Granular Campaign Performance Analysis (44 Campaigns)"
    ws_camp["A1"].font = font_title_large
    ws_camp["A2"] = "Performance metrics calculated dynamically with Excel SUMIFS formulas and conditional formatting"
    ws_camp["A2"].font = font_subtitle

    camp_headers = ["Campaign ID", "Campaign Name", "Platform", "Campaign Type", "Ad Spend", "Impressions", "Clicks", "Conversions", "Revenue", "CTR", "CPC", "CPA", "ROAS", "Status"]
    for c_i, h in enumerate(camp_headers, 1):
        cell = ws_camp.cell(row=4, column=c_i, value=h)
        cell.font = font_header
        cell.fill = navy_header_fill
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = header_border

    unique_campaigns = df_cleaned[["campaign_id", "campaign_name", "platform", "campaign_type"]].drop_duplicates().sort_values("campaign_id")

    for idx, (_, crow) in enumerate(unique_campaigns.iterrows(), start=5):
        cid = crow["campaign_id"]
        cname = crow["campaign_name"]
        cplat = crow["platform"]
        ctype = crow["campaign_type"]

        ws_camp.cell(row=idx, column=1, value=cid).font = font_body
        ws_camp.cell(row=idx, column=2, value=cname).font = font_body
        ws_camp.cell(row=idx, column=3, value=cplat).font = font_body
        ws_camp.cell(row=idx, column=4, value=ctype).font = font_body

        # Formulas
        ws_camp.cell(row=idx, column=5, value=f'=SUMIFS(Cleaned_Data!$L$2:$L${end_row_ref}, Cleaned_Data!$D$2:$D${end_row_ref}, A{idx})').number_format = "$#,##0.00"
        ws_camp.cell(row=idx, column=6, value=f'=SUMIFS(Cleaned_Data!$J$2:$J${end_row_ref}, Cleaned_Data!$D$2:$D${end_row_ref}, A{idx})').number_format = "#,##0"
        ws_camp.cell(row=idx, column=7, value=f'=SUMIFS(Cleaned_Data!$K$2:$K${end_row_ref}, Cleaned_Data!$D$2:$D${end_row_ref}, A{idx})').number_format = "#,##0"
        ws_camp.cell(row=idx, column=8, value=f'=SUMIFS(Cleaned_Data!$M$2:$M${end_row_ref}, Cleaned_Data!$D$2:$D${end_row_ref}, A{idx})').number_format = "#,##0"
        ws_camp.cell(row=idx, column=9, value=f'=SUMIFS(Cleaned_Data!$N$2:$N${end_row_ref}, Cleaned_Data!$D$2:$D${end_row_ref}, A{idx})').number_format = "$#,##0.00"
        ws_camp.cell(row=idx, column=10, value=f'=(G{idx}/F{idx})').number_format = "0.00%"
        ws_camp.cell(row=idx, column=11, value=f'=(E{idx}/G{idx})').number_format = "$#,##0.00"
        ws_camp.cell(row=idx, column=12, value=f'=(E{idx}/H{idx})').number_format = "$#,##0.00"
        ws_camp.cell(row=idx, column=13, value=f'=(I{idx}/E{idx})').number_format = "0.00\"x\""
        ws_camp.cell(row=idx, column=14, value=f'=IF(M{idx}>=3.0, "High ROAS", IF(M{idx}>=2.0, "Moderate", "Underperforming"))').font = font_body

        for c_i in range(1, 15):
            ws_camp.cell(row=idx, column=c_i).border = cell_border

    # Conditional formatting on ROAS (Column M)
    green_fill = PatternFill(start_color="C6EFCE", end_color="C6EFCE", fill_type="solid")
    red_fill = PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid")
    ws_camp.conditional_formatting.add(
        f"M5:M{4 + len(unique_campaigns)}",
        CellIsRule(operator="greaterThanOrEqual", formula=["3.0"], stopIfTrue=True, fill=green_fill)
    )
    ws_camp.conditional_formatting.add(
        f"M5:M{4 + len(unique_campaigns)}",
        CellIsRule(operator="lessThan", formula=["2.0"], stopIfTrue=True, fill=red_fill)
    )

    # -------------------------------------------------------------
    # SHEET 6: Monthly_Trends
    # -------------------------------------------------------------
    ws_month = wb.create_sheet(title="Monthly_Trends")
    ws_month.views.sheetView[0].showGridLines = True
    ws_month["A1"] = "Month-over-Month Advertising Trajectory"
    ws_month["A1"].font = font_title_large
    ws_month["A2"] = "Monthly aggregation using Excel SUMIFS across H1 2026 (Jan - Jun)"
    ws_month["A2"].font = font_subtitle

    month_headers = ["Month", "Start Date", "End Date", "Total Spend", "Impressions", "Clicks", "Conversions", "Revenue", "CTR", "CPA", "ROAS"]
    for c_i, h in enumerate(month_headers, 1):
        cell = ws_month.cell(row=4, column=c_i, value=h)
        cell.font = font_header
        cell.fill = navy_header_fill
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = header_border

    months = [
        ("Jan 2026", "2026-01-01", "2026-01-31"),
        ("Feb 2026", "2026-02-01", "2026-02-28"),
        ("Mar 2026", "2026-03-01", "2026-03-31"),
        ("Apr 2026", "2026-04-01", "2026-04-30"),
        ("May 2026", "2026-05-01", "2026-05-31"),
        ("Jun 2026", "2026-06-01", "2026-06-30"),
    ]

    for idx, (m_lbl, s_dt, e_dt) in enumerate(months, start=5):
        ws_month.cell(row=idx, column=1, value=m_lbl).font = font_bold
        ws_month.cell(row=idx, column=2, value=s_dt).font = font_body
        ws_month.cell(row=idx, column=3, value=e_dt).font = font_body

        ws_month.cell(row=idx, column=4, value=f'=SUMIFS(Cleaned_Data!$L$2:$L${end_row_ref}, Cleaned_Data!$B$2:$B${end_row_ref}, ">="&B{idx}, Cleaned_Data!$B$2:$B${end_row_ref}, "<="&C{idx})').number_format = "$#,##0.00"
        ws_month.cell(row=idx, column=5, value=f'=SUMIFS(Cleaned_Data!$J$2:$J${end_row_ref}, Cleaned_Data!$B$2:$B${end_row_ref}, ">="&B{idx}, Cleaned_Data!$B$2:$B${end_row_ref}, "<="&C{idx})').number_format = "#,##0"
        ws_month.cell(row=idx, column=6, value=f'=SUMIFS(Cleaned_Data!$K$2:$K${end_row_ref}, Cleaned_Data!$B$2:$B${end_row_ref}, ">="&B{idx}, Cleaned_Data!$B$2:$B${end_row_ref}, "<="&C{idx})').number_format = "#,##0"
        ws_month.cell(row=idx, column=7, value=f'=SUMIFS(Cleaned_Data!$M$2:$M${end_row_ref}, Cleaned_Data!$B$2:$B${end_row_ref}, ">="&B{idx}, Cleaned_Data!$B$2:$B${end_row_ref}, "<="&C{idx})').number_format = "#,##0"
        ws_month.cell(row=idx, column=8, value=f'=SUMIFS(Cleaned_Data!$N$2:$N${end_row_ref}, Cleaned_Data!$B$2:$B${end_row_ref}, ">="&B{idx}, Cleaned_Data!$B$2:$B${end_row_ref}, "<="&C{idx})').number_format = "$#,##0.00"
        ws_month.cell(row=idx, column=9, value=f'=(F{idx}/E{idx})').number_format = "0.00%"
        ws_month.cell(row=idx, column=10, value=f'=(D{idx}/G{idx})').number_format = "$#,##0.00"
        ws_month.cell(row=idx, column=11, value=f'=(H{idx}/D{idx})').number_format = "0.00\"x\""

        for c_i in range(1, 12):
            ws_month.cell(row=idx, column=c_i).border = cell_border

    # Monthly Spend vs Revenue Line Chart
    line_chart = LineChart()
    line_chart.title = "Monthly Ad Spend vs. Revenue ($ USD)"
    line_chart.style = 13
    line_chart.y_axis.title = "USD ($)"
    line_chart.x_axis.title = "Month"
    m_data = Reference(ws_month, min_col=4, min_row=4, max_col=4, max_row=10)
    m_rev = Reference(ws_month, min_col=8, min_row=4, max_col=8, max_row=10)
    line_chart.add_data(m_data, titles_from_data=True)
    line_chart.add_data(m_rev, titles_from_data=True)
    m_cats = Reference(ws_month, min_col=1, min_row=5, max_row=10)
    line_chart.set_categories(m_cats)
    line_chart.height = 12
    line_chart.width = 18
    ws_month.add_chart(line_chart, "A13")

    # Monthly ROAS Line Chart
    line_roas = LineChart()
    line_roas.title = "Monthly ROAS Trajectory"
    line_roas.style = 14
    line_roas.y_axis.title = "ROAS (x)"
    line_roas.x_axis.title = "Month"
    m_roas_data = Reference(ws_month, min_col=11, min_row=4, max_col=11, max_row=10)
    line_roas.add_data(m_roas_data, titles_from_data=True)
    line_roas.set_categories(m_cats)
    line_roas.height = 12
    line_roas.width = 16
    ws_month.add_chart(line_roas, "H13")

    # -------------------------------------------------------------
    # SHEET 7: Dashboard
    # -------------------------------------------------------------
    ws_dash = wb.create_sheet(title="Dashboard", index=0) # Place first for presentation!
    ws_dash.views.sheetView[0].showGridLines = True
    ws_dash["B2"] = "EXECUTIVE MARKETING PERFORMANCE DASHBOARD"
    ws_dash["B2"].font = font_title_large
    ws_dash["B3"] = "Multi-Platform Digital Campaign Analytics across Meta, Google, LinkedIn & X | Jan - Jun 2026"
    ws_dash["B3"].font = font_subtitle

    # KPI Summary Cards (B5:C6, D5:E6, F5:G6, H5:I6, J5:K6, L5:M6)
    cards = [
        ("TOTAL AD SPEND", "=KPI_Calculations!D7", "$#,##0.00", "B", "C"),
        ("TOTAL REVENUE", "=KPI_Calculations!D9", "$#,##0.00", "D", "E"),
        ("OVERALL ROAS", "=KPI_Calculations!D15", "0.00\"x\"", "F", "G"),
        ("TOTAL CONVERSIONS", "=KPI_Calculations!D8", "#,##0", "H", "I"),
        ("AVERAGE CTR", "=KPI_Calculations!D11", "0.00\"%\"", "J", "K"),
        ("AVERAGE CPA", "=KPI_Calculations!D13", "$#,##0.00", "L", "M")
    ]

    for title, formula, fmt, col_start, col_end in cards:
        # Title row 5
        ws_dash.merge_cells(f"{col_start}5:{col_end}5")
        tcell = ws_dash[f"{col_start}5"]
        tcell.value = title
        tcell.font = font_card_title
        tcell.fill = card_header_fill
        tcell.alignment = Alignment(horizontal="center", vertical="center")

        # Value row 6
        ws_dash.merge_cells(f"{col_start}6:{col_end}6")
        vcell = ws_dash[f"{col_start}6"]
        vcell.value = formula
        vcell.font = font_card_value
        vcell.fill = card_body_fill
        vcell.alignment = Alignment(horizontal="center", vertical="center")
        vcell.number_format = fmt

        # Add card border
        for r in range(5, 7):
            for c_letter in [col_start, col_end]:
                ws_dash[f"{c_letter}{r}"].border = cell_border

    # Dashboard Platform Performance Table (Rows 8 to 14)
    ws_dash["B8"] = "Platform Performance Summary (Dynamic Excel Formulas)"
    ws_dash["B8"].font = font_bold
    dash_table_headers = ["Platform", "Spend ($)", "Revenue ($)", "Conversions", "CTR", "CPC ($)", "CPA ($)", "ROAS"]
    col_dash = ["B", "C", "D", "E", "F", "G", "H", "I"]
    for c_idx, h in enumerate(dash_table_headers):
        c_letter = col_dash[c_idx]
        cell = ws_dash[f"{c_letter}9"]
        cell.value = h
        cell.font = font_header
        cell.fill = navy_header_fill
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = header_border

    # Link directly to Platform_Analysis sheet
    for idx in range(5, 9):
        target_dash_row = idx + 5 # 10 to 13
        p_row = idx
        ws_dash[f"B{target_dash_row}"] = f"=Platform_Analysis!A{p_row}"
        ws_dash[f"B{target_dash_row}"].font = font_bold
        ws_dash[f"C{target_dash_row}"] = f"=Platform_Analysis!B{p_row}"
        ws_dash[f"C{target_dash_row}"].number_format = "$#,##0.00"
        ws_dash[f"D{target_dash_row}"] = f"=Platform_Analysis!F{p_row}"
        ws_dash[f"D{target_dash_row}"].number_format = "$#,##0.00"
        ws_dash[f"E{target_dash_row}"] = f"=Platform_Analysis!E{p_row}"
        ws_dash[f"E{target_dash_row}"].number_format = "#,##0"
        ws_dash[f"F{target_dash_row}"] = f"=Platform_Analysis!G{p_row}"
        ws_dash[f"F{target_dash_row}"].number_format = "0.00%"
        ws_dash[f"G{target_dash_row}"] = f"=Platform_Analysis!H{p_row}"
        ws_dash[f"G{target_dash_row}"].number_format = "$#,##0.00"
        ws_dash[f"H{target_dash_row}"] = f"=Platform_Analysis!I{p_row}"
        ws_dash[f"H{target_dash_row}"].number_format = "$#,##0.00"
        ws_dash[f"I{target_dash_row}"] = f"=Platform_Analysis!K{p_row}"
        ws_dash[f"I{target_dash_row}"].number_format = "0.00\"x\""
        ws_dash[f"I{target_dash_row}"].font = font_bold

        for c_letter in col_dash:
            ws_dash[f"{c_letter}{target_dash_row}"].border = cell_border

    # Dashboard Total Row (Row 14)
    ws_dash["B14"] = "Overall / Total"
    ws_dash["B14"].font = font_bold
    ws_dash["C14"] = "=SUM(C10:C13)"
    ws_dash["C14"].number_format = "$#,##0.00"
    ws_dash["D14"] = "=SUM(D10:D13)"
    ws_dash["D14"].number_format = "$#,##0.00"
    ws_dash["E14"] = "=SUM(E10:E13)"
    ws_dash["E14"].number_format = "#,##0"
    ws_dash["F14"] = "=KPI_Calculations!D11"
    ws_dash["F14"].number_format = "0.00%"
    ws_dash["G14"] = "=C14/KPI_Calculations!D6"
    ws_dash["G14"].number_format = "$#,##0.00"
    ws_dash["H14"] = "=C14/E14"
    ws_dash["H14"].number_format = "$#,##0.00"
    ws_dash["I14"] = "=D14/C14"
    ws_dash["I14"].number_format = "0.00\"x\""
    for c_letter in col_dash:
        c = ws_dash[f"{c_letter}14"]
        c.font = font_bold
        c.fill = accent_kpi_fill
        c.border = cell_border

    # Embed Platform Spend vs Revenue Bar Chart on Dashboard
    dash_chart_plat = BarChart()
    dash_chart_plat.type = "col"
    dash_chart_plat.style = 10
    dash_chart_plat.title = "Platform Budget vs. Revenue Generation ($ USD)"
    dash_chart_plat.y_axis.title = "USD ($)"
    dash_chart_plat.x_axis.title = "Platform"
    d_spend_ref = Reference(ws_dash, min_col=3, min_row=9, max_col=3, max_row=13)
    d_rev_ref = Reference(ws_dash, min_col=4, min_row=9, max_col=4, max_row=13)
    dash_chart_plat.add_data(d_spend_ref, titles_from_data=True)
    dash_chart_plat.add_data(d_rev_ref, titles_from_data=True)
    d_cats_ref = Reference(ws_dash, min_col=2, min_row=10, max_row=13)
    dash_chart_plat.set_categories(d_cats_ref)
    dash_chart_plat.height = 13
    dash_chart_plat.width = 17
    ws_dash.add_chart(dash_chart_plat, "B16")

    # Embed Monthly Trend Line Chart on Dashboard (referencing Monthly_Trends)
    dash_line_chart = LineChart()
    dash_line_chart.title = "Monthly Ad Spend vs. Revenue Trajectory ($ USD)"
    dash_line_chart.style = 13
    dash_line_chart.y_axis.title = "USD ($)"
    dash_line_chart.x_axis.title = "Month"
    m_dash_spend = Reference(ws_month, min_col=4, min_row=4, max_col=4, max_row=10)
    m_dash_rev = Reference(ws_month, min_col=8, min_row=4, max_col=8, max_row=10)
    dash_line_chart.add_data(m_dash_spend, titles_from_data=True)
    dash_line_chart.add_data(m_dash_rev, titles_from_data=True)
    dash_line_chart.set_categories(m_cats)
    dash_line_chart.height = 13
    dash_line_chart.width = 17
    ws_dash.add_chart(dash_line_chart, "H16")

    # Add Guide / Notes on Native Excel Pivot Tables
    ws_dash["B32"] = "EXCEL PIVOT TABLE & SLICER USER GUIDE"
    ws_dash["B32"].font = font_bold
    guide_text = (
        "1. Open 'Cleaned_Data' tab -> Select all cells (Ctrl+A) -> Click Insert > PivotTable.\n"
        "2. To create Platform Summary: Drag 'platform' to Rows, drag 'ad_spend' and 'revenue' to Values.\n"
        "3. Calculated Fields: Go to PivotTable Analyze > Fields, Items & Sets > Calculated Field:\n"
        "   - Create ROAS: formula '= revenue / ad_spend'\n"
        "   - Create CTR: formula '= clicks / impressions'\n"
        "4. Slicers: Click Insert > Slicer -> Select 'platform', 'device_type', and 'region' for dynamic filtering."
    )
    ws_dash["B33"] = guide_text
    ws_dash["B33"].font = font_subtitle

    # Auto-adjust column widths across all sheets
    for ws in [ws_dash, ws_kpi, ws_plat, ws_camp, ws_month]:
        for col in ws.columns:
            max_len = 0
            col_letter = get_column_letter(col[0].column)
            for cell in col:
                val_str = str(cell.value or "")
                if val_str.startswith("="):
                    val_str = "123,456.78"
                max_len = max(max_len, len(val_str))
            ws.column_dimensions[col_letter].width = max(max_len + 3, 14)

    # Cleaned_Data column widths
    for col in ws_clean.columns:
        col_letter = get_column_letter(col[0].column)
        ws_clean.column_dimensions[col_letter].width = 18

    # Save workbook
    os.makedirs(os.path.dirname(output_xlsx_path), exist_ok=True)
    wb.save(output_xlsx_path)
    print(f"Excel workbook successfully created at: {output_xlsx_path}")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    raw_path = os.path.join(base_dir, "data", "raw_campaign_data.csv")
    cleaned_path = os.path.join(base_dir, "data", "campaign_data_cleaned.csv")
    excel_path = os.path.join(base_dir, "excel", "Digital_Marketing_Analysis.xlsx")

    create_excel_workbook(raw_path, cleaned_path, excel_path)
