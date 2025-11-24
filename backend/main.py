from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import snowflake.connector
import pandas as pd
import os
import traceback
from typing import List, Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Connection details from environment variables
CONN_PARAMS = {
    "account": os.getenv("SNOWFLAKE_ACCOUNT"),
    "user": os.getenv("SNOWFLAKE_USER"),
    "password": os.getenv("SNOWFLAKE_PASSWORD"),
    "role": os.getenv("SNOWFLAKE_ROLE"),
    "warehouse": os.getenv("SNOWFLAKE_WAREHOUSE"),
    "database": os.getenv("SNOWFLAKE_DATABASE"),
    "schema": os.getenv("SNOWFLAKE_SCHEMA"),
    "authenticator": os.getenv("SNOWFLAKE_AUTHENTICATOR", "snowflake")
}

@app.get("/data")
def get_data():
    try:
        print("Attempting to connect to Snowflake...")
        conn = snowflake.connector.connect(**CONN_PARAMS)
        cursor = conn.cursor()
        
        print("Connected! Executing query...")
        # Fetch data sorted by date
        query = """
        SELECT RUN_DT, DII_NET, FII_NET 
        FROM t_nse_fii_dii_eq_data 
        ORDER BY RUN_DT ASC
        """
        cursor.execute(query)
        
        print("Fetching data...")
        df = cursor.fetch_pandas_all()
        
        print(f"Fetched {len(df)} rows")
        # Convert to list of dicts
        # Ensure RUN_DT is string for JSON
        df['RUN_DT'] = df['RUN_DT'].astype(str)
        
        result = df.to_dict(orient='records')
        print("Returning data...")
        return result
        
    except Exception as e:
        error_msg = f"Error: {str(e)}\n{traceback.format_exc()}"
        print(error_msg)
        raise HTTPException(status_code=500, detail=error_msg)
    finally:
        if 'conn' in locals():
            conn.close()

@app.get("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
