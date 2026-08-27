# AQUAVIGIL / OceanTrace

Frontend prototype for satellite intelligence, oil-spill characterization, vessel attribution, drift impact prediction, and forensic reporting.

## Run the frontend

```powershell
npm install
npm run dev
```

- Dashboard: `http://localhost:5173/`
- Forensic report: `http://localhost:5173/report`

The dashboard keeps the approved OceanTrace UI and adds deterministic DEMO mode controls for traffic filtering, slick metrics, attribution breakdowns, incident details, alerts, and report navigation.

## Run the API adapter

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r backend/requirements.txt
uvicorn app.main:app --app-dir backend --reload --port 8000
```

The FastAPI contract is in `backend/app/main.py`. It currently returns clearly labelled deterministic DEMO data. It includes incident, slick, vessel, traffic, recommendation, and SHA-256 evidence endpoints.

## Demo versus live

Implemented provider names such as Sentinel-1, AIS, HYCOM, CMEMS, and ERA5 are source contracts, not live integrations yet. Before presenting outputs as live, connect the adapters to credentials, real scene/AIS feeds, Rasterio/GDAL preprocessing, model inference, OpenDrift/OpenOil, and PostgreSQL/PostGIS with TimescaleDB for AIS time series.
