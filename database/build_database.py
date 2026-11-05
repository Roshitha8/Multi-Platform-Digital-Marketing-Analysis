"""
Multi-Platform Digital Marketing Campaign Performance Analysis
Module: database/build_database.py

Creates SQLite database (database/digital_marketing.db), creates schema,
loads cleaned campaign data, and executes all 20 analytical queries in marketing_analysis.sql.
"""

import os
import sqlite3
import pandas as pd

def build_database(cleaned_csv_path: str, db_path: str, sql_file_path: str):
    print(f"Connecting to SQLite database: {db_path}")
    if os.path.exists(db_path):
        os.remove(db_path)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # DDL
    ddl = """
    CREATE TABLE campaign_performance (
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
    CREATE INDEX idx_date ON campaign_performance(date);
    CREATE INDEX idx_platform ON campaign_performance(platform);
    CREATE INDEX idx_campaign ON campaign_performance(campaign_id);
    CREATE INDEX idx_region ON campaign_performance(region);
    CREATE INDEX idx_device ON campaign_performance(device_type);
    """
    cursor.executescript(ddl)
    print("Created table `campaign_performance` and performance indexes.")

    # Load cleaned data
    df = pd.read_csv(cleaned_csv_path)
    df.to_sql("campaign_performance", conn, if_exists="append", index=False)
    conn.commit()
    print(f"Loaded {len(df)} records into `campaign_performance`.")

    # Validate row count
    cursor.execute("SELECT COUNT(*) FROM campaign_performance;")
    count = cursor.fetchone()[0]
    print(f"Verified row count in database: {count}")

    # Read and execute queries from marketing_analysis.sql
    with open(sql_file_path, "r", encoding="utf-8") as f:
        sql_content = f.read()

    # Separate queries by semicolon, filtering out DDL and comments
    statements = [stmt.strip() for stmt in sql_content.split(";") if stmt.strip()]
    select_queries = []
    for stmt in statements:
        # Strip leading comment lines
        lines = [line.strip() for line in stmt.split("\n") if line.strip() and not line.strip().startswith("--")]
        if lines:
            cleaned_stmt = " ".join(lines)
            if cleaned_stmt.upper().startswith("SELECT") or cleaned_stmt.upper().startswith("WITH"):
                select_queries.append(stmt)

    print(f"\nExecuting {len(select_queries)} analytical queries from {os.path.basename(sql_file_path)}...")
    for idx, q in enumerate(select_queries, start=1):
        try:
            res_df = pd.read_sql_query(q, conn)
            print(f" Query {idx:02d}: Success ({len(res_df)} rows returned)")
            if idx in [1, 2, 3, 4, 9, 10, 19, 20]:
                print(f"--- Sample Output for Query {idx} ---")
                print(res_df.head(3).to_string(index=False))
                print("-" * 40)
        except Exception as e:
            print(f" Query {idx:02d} FAILED: {e}")
            raise e

    conn.close()
    print(f"\nDatabase setup and query execution completed successfully: {db_path}")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    cleaned_csv = os.path.join(base_dir, "data", "campaign_data_cleaned.csv")
    db_file = os.path.join(base_dir, "database", "digital_marketing.db")
    sql_file = os.path.join(base_dir, "database", "marketing_analysis.sql")

    build_database(cleaned_csv, db_file, sql_file)
