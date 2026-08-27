# AQUAVIGIL API

FastAPI adapter for the OceanTrace/AQUAVIGIL frontend. The current implementation is deterministic DEMO mode: no external data, credentials, models, or database are bundled.

## Run

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

## Contract

- `GET /health`
- `GET /api/v1/incidents`
- `GET /api/v1/incidents/{incident_id}`
- `GET /api/v1/incidents/{incident_id}/vessels`
- `GET /api/v1/traffic?stage=Suspects`
- `GET /api/v1/incidents/{incident_id}/recommendations`
- `GET /api/v1/incidents/{incident_id}/evidence`

Provider adapters for Sentinel-1/Sentinel-2, Rasterio/GDAL, OpenDrift/OpenOil, HYCOM/CMEMS/ERA5, AIS, and PostGIS/TimescaleDB should replace the deterministic fixtures behind these contracts.
