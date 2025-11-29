# NSE FII/DII Grafana Visualization

This project visualizes FII (Foreign Institutional Investors) and DII (Domestic Institutional Investors) net trading data from PostgreSQL using Grafana.

## Status

✅ **Completed Features:**
- FastAPI backend connecting to PostgreSQL
- Custom Grafana image (`nfd-grafana:v1.0`)
- Three pre-configured dashboards with interactive visualizations
- Color-coded bar charts for easy data interpretation
- Y-axis labeled as "₹ Crores"
- Environment-based configuration
- Docker containerization with automatic provisioning

🚧 **Pending:**
- Cloud deployment (GCP deployment would cost ~$13-25/month)

## Architecture

- **Backend (FastAPI)**: Connects to PostgreSQL and exposes data via REST API
- **Grafana**: Visualizes the data using the Infinity datasource plugin
- **Docker Compose**: Orchestrates both services

## Features

### Three Interactive Dashboards

1. **FII/DII Net Buy/Sell Trend**
   - Bar chart visualization with zoom capability
   - Blue bars for DII, Orange bars for FII
   - Shows net trading values

2. **FII/DII Total Buy/Sell Values**
   - Stacked bar charts (Green: Buy, Red: Sell)
   - Matched Y-axis scales for honest comparison
   - Separate panels for DII and FII

3. **Data Availability**
   - Purple bar chart showing data latency
   - Weekend gaps clearly visible
   - Latency tracking in hours after market close

### Technical Features
- ✅ Real-time data from PostgreSQL table `t_nse_fii_dii_eq_data`
- ✅ Interactive visualizations with zoom and pan
- ✅ Automatic dashboard provisioning
- ✅ Custom Docker image for easy identification

## Prerequisites

- Docker Desktop installed and running
- PostgreSQL database with `t_nse_fii_dii_eq_data` table

## Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/stirandas/nfd_visualizations.git
   cd nfd_visualizations
   ```

2. **Configure environment variables**:
   ```bash
   cp .env.sample .env
   ```
   
   Edit `.env` and add your PostgreSQL credentials:
   ```
   POSTGRES_HOST=your_host
   POSTGRES_PORT=5432
   POSTGRES_DB=your_database
   POSTGRES_USER=your_username
   POSTGRES_PASSWORD=your_password
   ```

## Quick Start

1. **Start the services**:
   ```bash
   docker-compose up -d --build
   ```

2. **Access Grafana**:
   - URL: http://localhost:3000
   - All 3 dashboards are automatically provisioned
   - Navigate to: **Dashboards** → Browse to see all available dashboards

3. **Verify backend**:
   - API: http://localhost:8000/data
   - Docs: http://localhost:8000/docs

4. **Stop the services**:
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
│   ├── Dockerfile          # Custom Grafana image
│   └── provisioning/
│       ├── datasources/
│       │   └── datasource.yml          # nfd-Infinity datasource
│       └── dashboards/
│           ├── dashboard.yml           # Dashboard provider config  
│           ├── net-trend-dashboard.json       # Net Buy/Sell Trend
│           ├── buy-sell-dashboard.json        # Total Buy/Sell Values
│           └── availability-dashboard.json    # Data Availability
├── docker-compose.yml      # Service orchestration
├── .env.sample            # Sample environment variables
└── README.md              # This file
```

## API Endpoints

- `GET /` - Welcome message
- `GET /health` - Health check
- `GET /data` - Returns FII/DII data as JSON
- `GET /docs` - Interactive API documentation

## Configuration

PostgreSQL credentials are stored in the `.env` file (not committed to Git). See `.env.sample` for the required variables.

## Development

### Running Backend Locally (without Docker)

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

The backend will be available at http://localhost:8000

## Troubleshooting

**Dashboard shows "No data":**
1. Check backend logs: `docker logs nfd_visualizations-backend-1`
2. Verify PostgreSQL connection
3. Test API: `curl http://localhost:8000/data`

**Backend connection errors:**
- Ensure PostgreSQL credentials are correct in `.env`
- Check network connectivity to PostgreSQL
- Verify the table `t_nse_fii_dii_eq_data` exists

**Docker issues:**
- Ensure Docker Desktop is running
- Try rebuilding: `docker-compose up -d --build`

## Migration from Snowflake

This project was migrated from Snowflake to PostgreSQL. The table schema remains identical. If you need to migrate data, ensure your PostgreSQL table has the same structure as the original Snowflake table.

## Notes

- The Grafana Snowflake plugin is Enterprise-only, so we use a proxy API approach
- Anonymous access is enabled in Grafana for easy access
- Data is fetched in real-time from PostgreSQL on each dashboard refresh
- SQLAlchemy is used for database connections to ensure compatibility and avoid warnings
