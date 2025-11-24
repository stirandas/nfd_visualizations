# NSE FII/DII Grafana Visualization

This project visualizes FII (Foreign Institutional Investors) and DII (Domestic Institutional Investors) net trading data from Snowflake using Grafana.

## Status

✅ **Completed Features:**
- FastAPI backend connecting to Snowflake
- Grafana dashboard with time series visualization
- Color-coded trends (Green: Net Buy, Red: Net Sell)
- Y-axis labeled as "₹ Crores"
- Panel title: "DII/FII Net Buy/Sell Trend"
- Panel description showing axis labels
- Environment-based configuration
- Docker containerization

🚧 **Pending:**
- Cloud deployment (options documented in implementation plan)

## Architecture

- **Backend (FastAPI)**: Connects to Snowflake and exposes data via REST API
- **Grafana**: Visualizes the data using the Infinity datasource plugin
- **Docker Compose**: Orchestrates both services

## Features

- ✅ Real-time data from Snowflake table `t_nse_fii_dii_eq_data`
- ✅ Time series visualization of DII_NET and FII_NET trends
- ✅ Color-coded values: **Green** for positive (net buy), **Red** for negative (net sell)
- ✅ Automatic dashboard provisioning

## Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd nfd_visualizations
   ```

2. **Configure environment variables**:
   ```bash
   cp .env.sample .env
   ```
   
   Edit `.env` and add your Snowflake credentials:
   ```
   SNOWFLAKE_ACCOUNT=your_account
   SNOWFLAKE_USER=your_username
   SNOWFLAKE_PASSWORD=your_password
   SNOWFLAKE_WAREHOUSE=your_warehouse
   SNOWFLAKE_DATABASE=your_database
   SNOWFLAKE_SCHEMA=your_schema
   ```

## Quick Start

1. **Start the services**:
   ```bash
   docker-compose up -d --build
   ```

2. **Access Grafana**:
   - URL: http://localhost:3000
   - The dashboard is automatically provisioned
   - Navigate to: **Dashboards → NSE FII/DII Dashboard**

3. **Stop the services**:
   ```bash
   docker-compose down
   ```

## Project Structure

```
nfd_visualizations/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── requirements.txt     # Python dependencies
│   └── Dockerfile          # Backend container
├── grafana/
│   └── provisioning/
│       ├── datasources/    # Infinity datasource config
│       └── dashboards/     # Dashboard JSON
└── docker-compose.yml      # Service orchestration
```

## API Endpoints

- `GET /health` - Health check
- `GET /data` - Returns FII/DII data as JSON

## Configuration

Snowflake credentials are stored in the `.env` file (not committed to Git). See `.env.sample` for the required variables.

## Troubleshooting

**Dashboard shows "No data":**
1. Check backend logs: `docker logs nfd_visualizations-backend-1`
2. Verify Snowflake connection
3. Test API: `curl http://localhost:8000/data`

**Backend connection errors:**
- Ensure Snowflake credentials are correct
- Check network connectivity to Snowflake

## Notes

- The Grafana Snowflake plugin is Enterprise-only, so we use a proxy API approach
- Anonymous access is enabled in Grafana for easy access
- Data is fetched in real-time from Snowflake on each dashboard refresh
