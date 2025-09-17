import sqlite3
import pandas as pd

def load_data_to_sqlite(excel_path="Dummy Data Sales.xlsx", db_path="sales.db"):
    """
    Loads Excel file into SQLite database (sales.db).
    - Replaces spaces and special chars with underscores in column names.
    - Table name: sales
    """
    # Read Excel
    df = pd.read_excel(excel_path)

    # Clean column names (spaces -> underscores, dots removed)
    df.columns = df.columns.str.replace(r"[ .]", "_", regex=True)

    # Save to SQLite
    conn = sqlite3.connect(db_path)
    df.to_sql("sales", conn, if_exists="replace", index=False)
    conn.close()

    print(f"Loaded {len(df)} rows into {db_path} (table: sales)")

    return db_path
