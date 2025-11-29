from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
import pandas as pd
import os
import traceback
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
def get_db_engine():
    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
    host = os.getenv("POSTGRES_HOST")
    port = os.getenv("POSTGRES_PORT")
    db = os.getenv("POSTGRES_DB")
    
    return create_engine(f"postgresql://{user}:{password}@{host}:{port}/{db}")

@app.get("/data")
def get_data():
    """
    Fetch all FII/DII data from PostgreSQL.
    Returns all columns for maximum flexibility in dashboard creation.
    
    Columns returned:
    - RUN_DT: Trading date
    - DII_BUY: Domestic Institutional Investors buy value (₹ Crores)
    - DII_SELL: Domestic Institutional Investors sell value (₹ Crores)
    - DII_NET: Domestic Institutional Investors net value (₹ Crores)
    - FII_BUY: Foreign Institutional Investors buy value (₹ Crores)
    - FII_SELL: Foreign Institutional Investors sell value (₹ Crores)
    - FII_NET: Foreign Institutional Investors net value (₹ Crores)
    - U_TS: Update timestamp
    - I_TS: Insert/Availability timestamp
    """
    try:
        print("Attempting to connect to PostgreSQL...")
        engine = get_db_engine()
        
        print("Connected! Executing query...")
        # Fetch all data sorted by date
        query = """
        SELECT 
            RUN_DT, 
            DII_BUY, 
            DII_SELL, 
            DII_NET, 
            FII_BUY, 
            FII_SELL, 
            FII_NET, 
            U_TS, 
            I_TS,
            to_char(i_ts AT TIME ZONE 'Asia/Kolkata', 'DD-Mon-YYYY HH24:MI') AS i_ts_ist,
            to_char(u_ts AT TIME ZONE 'Asia/Kolkata', 'DD-Mon-YYYY HH24:MI') AS u_ts_ist,
            EXTRACT(EPOCH FROM (i_ts - ((run_dt::timestamp + time '15:30') AT TIME ZONE 'Asia/Kolkata'))) / 3600 AS latency_hours,
            EXTRACT(EPOCH FROM (i_ts AT TIME ZONE 'Asia/Kolkata')::time) AS availability_seconds
        FROM t_nse_fii_dii_eq_data 
        ORDER BY RUN_DT ASC
        """
        
        print("Fetching data...")
        with engine.connect() as conn:
            df = pd.read_sql(query, conn)
        
        print(f"Fetched {len(df)} rows")
        
        # Convert date and timestamp columns to strings for JSON serialization
        df['run_dt'] = df['run_dt'].astype(str)
        df['u_ts'] = pd.to_datetime(df['u_ts']).dt.strftime('%Y-%m-%d %H:%M:%S%z')
        df['i_ts'] = pd.to_datetime(df['i_ts']).dt.strftime('%Y-%m-%d %H:%M:%S%z')
        
        # Rename columns to uppercase for consistency
        df = df.rename(columns={
            'run_dt': 'RUN_DT',
            'dii_buy': 'DII_BUY',
            'dii_sell': 'DII_SELL',
            'dii_net': 'DII_NET',
            'fii_buy': 'FII_BUY',
            'fii_sell': 'FII_SELL',
            'fii_net': 'FII_NET',
            'u_ts': 'U_TS',
            'i_ts': 'I_TS',
            'i_ts_ist': 'I_TS_IST',
            'u_ts_ist': 'U_TS_IST',
            'latency_hours': 'LATENCY_HOURS',
            'availability_seconds': 'AVAILABILITY_SECONDS'
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
