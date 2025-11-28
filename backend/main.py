from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
from sqlalchemy import create_engine
import pandas as pd
import os
import traceback
from typing import List, Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the NFD Visualization API. Visit /docs for documentation or /data for data."}

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Connection details from environment variables
# Connection details from environment variables
def get_db_engine():
    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
    host = os.getenv("POSTGRES_HOST")
    port = os.getenv("POSTGRES_PORT")
    db = os.getenv("POSTGRES_DB")
    
    return create_engine(f"postgresql://{user}:{password}@{host}:{port}/{db}")

@app.get("/data")
def get_data():
    try:
        print("Attempting to connect to PostgreSQL...")
        engine = get_db_engine()
        
        print("Connected! Executing query...")
        # Fetch data sorted by date
        query = """
        SELECT RUN_DT, DII_NET, FII_NET 
        FROM t_nse_fii_dii_eq_data 
        ORDER BY RUN_DT ASC
        """
        
        print("Fetching data...")
        # Use pandas read_sql for cleaner dataframe creation
        with engine.connect() as conn:
            df = pd.read_sql(query, conn)
        
        print(f"Fetched {len(df)} rows")
        # Convert to list of dicts
        # Ensure RUN_DT is string for JSON
        df['run_dt'] = df['run_dt'].astype(str)
        
        # Rename columns to match frontend expectation if postgres returns lowercase
        # Postgres usually returns lowercase column names
        df = df.rename(columns={
            'run_dt': 'RUN_DT',
            'dii_net': 'DII_NET',
            'fii_net': 'FII_NET'
        })
        
        result = df.to_dict(orient='records')
        print("Returning data...")
        return result
        
    except Exception as e:
        error_msg = f"Error: {str(e)}\n{traceback.format_exc()}"
        print(error_msg)
        raise HTTPException(status_code=500, detail=error_msg)

@app.get("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
