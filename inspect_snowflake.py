import snowflake.connector
import pandas as pd
import os

# Connection details from user prompt
conn_params = {
    "account": "BNEXHPK-SY56911",
    "user": "ST",
    "password": "Ilikey0u@snowflake",
    "role": "ACCOUNTADMIN",
    "warehouse": "nfd_wh",
    "database": "nfd_db",
    "schema": "nfd_schema",
    "authenticator": "snowflake"
}

try:
    conn = snowflake.connector.connect(**conn_params)
    cursor = conn.cursor()
    
    query = "SELECT * FROM t_nse_fii_dii_eq_data LIMIT 5"
    cursor.execute(query)
    
    df = cursor.fetch_pandas_all()
    
    print("Columns:")
    print(df.columns.tolist())
    print("\nData Types:")
    print(df.dtypes)
    print("\nFirst 5 rows:")
    print(df)
    
except Exception as e:
    print(f"Error: {e}")
finally:
    if 'conn' in locals():
        conn.close()
