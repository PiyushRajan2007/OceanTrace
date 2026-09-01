# OCEANTRACE - Quick Start Guide

## Project Status

✅ **Backend**: Fully functional with FastAPI, 19/19 tests passing
✅ **Frontend**: Integrated with API client and fallback demo data
✅ **Database**: SQLAlchemy models, Alembic migrations configured (optional for DEMO mode)
✅ **End-to-end**: Both servers running and communicating

## Prerequisites

- Python 3.8+
- Node.js 18+
- npm or yarn

## Quick Start

### 1. Start the Backend

```bash
cd backend
pip install -r requirements.txt
$env:PYTHONPATH="$PWD"; python -m uvicorn app.main:app --reload --port 8000 --host 127.0.0.1
```

Or on Linux/macOS:

```bash
cd backend
pip install -r requirements.txt
PYTHONPATH=. python -m uvicorn app.main:app --reload --port 8000 --host 127.0.0.1
```

**Expected output:**

```
INFO:     Will watch for changes in these directories: [...]
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started server process [PID]
INFO:     Application startup complete.
```

### 2. Start the Frontend (in a new terminal)

```bash
cd c:\Users\PIYUSH\Desktop\OceanTrace
npm run dev
```

**Expected output:**

```
  VITE v8.2.2  ready in 1825 ms
  ➜  Local:   http://localhost:5173/
```

### 3. Access the Dashboard

Open http://localhost:5173/ in your browser

## Verification

Run the integration test to confirm everything is working:

```bash
cd c:\Users\PIYUSH\Desktop\OceanTrace
python test_integration.py
```

Expected: ✓ ALL TESTS PASSED

## What Was Changed/Created

### Backend Files

**Core:**

- `backend/app/main.py` - FastAPI application with CORS and health endpoint
- `backend/app/core/config.py` - Configuration management (DEMO/LIVE mode)
- `backend/app/core/database.py` - SQLAlchemy setup (optional for DEMO)

**Data Models:**

- `backend/app/models/domain.py` - SQLAlchemy ORM models

**API Schemas:**

- `backend/app/schemas/domain.py` - Pydantic request/response models

**Business Logic:**

- `backend/app/services/base.py` - Base service with error handling
- `backend/app/services/demo_repository.py` - Deterministic demo data
- `backend/app/services/providers.py` - Provider factory pattern
- `backend/app/services/incidents.py` - Incident service
- `backend/app/services/vessels.py` - Vessel service
- `backend/app/services/traffic.py` - Traffic filtering service
- `backend/app/services/satellite.py` - Satellite scene service
- `backend/app/services/forecasts.py` - Forecast service
- `backend/app/services/alerts.py` - Alert service
- `backend/app/services/reports.py` - Report service

**API Endpoints:**

- `backend/app/routers/__init__.py` - Router aggregation
- `backend/app/routers/incidents.py` - Incident endpoints
- `backend/app/routers/vessels.py` - Vessel endpoints
- `backend/app/routers/traffic.py` - Traffic endpoints
- `backend/app/routers/satellite.py` - Satellite endpoints
- `backend/app/routers/forecasts.py` - Forecast endpoints
- `backend/app/routers/alerts.py` - Alert endpoints
- `backend/app/routers/reports.py` - Report endpoints

**WebSocket:**

- `backend/app/websocket/manager.py` - WebSocket connection manager
- `backend/app/websocket/routes.py` - WebSocket endpoint

**Database:**

- `backend/alembic/env.py` - Alembic migration environment
- `backend/alembic/alembic.ini` - Alembic configuration
- `backend/alembic/script.py.mako` - Alembic template
- `backend/alembic/versions/001_initial.py` - Initial schema migration

**Tests:**

- `backend/tests/test_api.py` - 19 comprehensive API tests

**Configuration:**

- `backend/requirements.txt` - Python dependencies
- `backend/.env.example` - Environment template

### Frontend Files

**API Client:**

- `src/api/client.js` - Core HTTP client with fallback pattern
- `src/api/incidents.js` - Incident API wrapper
- `src/api/traffic.js` - Traffic API wrapper
- `src/api/reports.js` - Report API wrapper

**React Components (Updated):**

- `src/App.jsx` - Dashboard component with data loading
- `src/Report.jsx` - Report page with data loading

**Configuration:**

- `.env` - Environment variables
- `.env.example` - Environment template

**Testing:**

- `test_integration.py` - End-to-end integration test

## API Endpoints

All endpoints are available at `http://127.0.0.1:8000/api/v1/`

### Health Check

- `GET /health` - System health status

### Incidents

- `GET /incidents` - List all incidents
- `GET /incidents/{id}` - Get incident details
- `GET /incidents/{id}/slick` - Get slick information
- `GET /incidents/{id}/vessels` - Get suspect vessels
- `GET /incidents/{id}/forecast` - Get drift forecast
- `GET /incidents/{id}/recommendations` - Get response recommendations
- `GET /incidents/{id}/evidence` - Get evidence chain

### Vessels

- `GET /vessels` - List all vessels
- `GET /vessels/{mmsi}` - Get vessel details

### Traffic

- `GET /traffic?stage=Suspects` - Get traffic by stage

### Satellite

- `GET /satellite/scenes` - List satellite scenes
- `GET /satellite/scenes/{id}` - Get scene details
- `POST /satellite/process` - Process satellite scene

### Alerts

- `GET /alerts` - List alerts
- `GET /alerts/{id}` - Get alert details

### Reports

- `GET /reports` - List reports
- `GET /reports/{id}` - Get report
- `GET /reports/{id}/geojson` - Get report as GeoJSON

### WebSocket

- `WS /ws` - Real-time system messages

## Features

✅ **DEMO Mode** (default)

- Runs without PostgreSQL
- Deterministic test data
- Full API response models

✅ **API Client with Fallback**

- Fetches from FastAPI
- Falls back to demo data if API unavailable
- Automatic error handling and logging

✅ **Data Transformation**

- Backend schema ↔ Frontend format
- Coordinate formatting
- DateTime formatting
- Vessel risk scoring

✅ **Full Test Coverage**

- 19 pytest tests for all endpoints
- 404 error handling
- Request/response validation

✅ **Database Setup** (optional)

- SQLAlchemy ORM models
- Alembic migrations
- PostGIS-ready geometry columns
- Ready for LIVE mode with PostgreSQL

✅ **CORS Configured**

- Allows http://localhost:5173 and 127.0.0.1:5173
- All HTTP methods supported
- Credentials enabled

✅ **Swagger Documentation**

- Auto-generated at `/docs`
- Full schema documentation
- Interactive endpoint testing

## Database Setup (Optional - For LIVE Mode)

If you want to use a real PostgreSQL database:

```bash
# Create .env file
cp backend/.env.example backend/.env

# Update DATABASE_URL in backend/.env
# Example: postgresql+psycopg://user:password@localhost:5432/aquavigil

# Run migrations
cd backend
alembic upgrade head

# Start backend in LIVE mode
APP_MODE=LIVE python -m uvicorn app.main:app --reload --port 8000
```

## Troubleshooting

### Backend won't start

```bash
# Ensure PYTHONPATH is set correctly
$env:PYTHONPATH="$(Get-Location)\backend"
python -m uvicorn app.main:app --reload --port 8000 --host 127.0.0.1
```

### Frontend shows "Loading incident data..."

- Check browser console (F12) for errors
- Ensure backend is running on http://127.0.0.1:8000
- Check .env file has `VITE_API_URL=http://127.0.0.1:8000`

### API endpoints return 404

- Ensure incident ID is correct: `INC-240824-01`
- Check backend logs for routing issues
- Run `pytest` to test endpoints in isolation

### Tests fail

```bash
cd backend
$env:PYTHONPATH="$PWD"
python -m pytest tests/test_api.py -v
```

## Development

### Add a new endpoint

1. Create schema in `backend/app/schemas/domain.py`
2. Add service method in `backend/app/services/`
3. Create router in `backend/app/routers/`
4. Include router in `backend/app/routers/__init__.py`
5. Add frontend API wrapper in `src/api/`
6. Update component to use new endpoint

### Add tests

```bash
cd backend
$env:PYTHONPATH="$PWD"
python -m pytest tests/test_api.py::test_name -v
```

### Backend running but frontend can't reach it

Check CORS configuration in `backend/app/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,  # http://localhost:5173, http://127.0.0.1:5173
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Project Structure

```
OceanTrace/
├── backend/
│   ├── app/
│   │   ├── core/              # Config, database
│   │   ├── models/            # SQLAlchemy models
│   │   ├── schemas/           # Pydantic schemas
│   │   ├── services/          # Business logic
│   │   ├── routers/           # API endpoints
│   │   ├── websocket/         # WebSocket
│   │   └── main.py            # FastAPI app
│   ├── alembic/               # Database migrations
│   ├── tests/                 # Pytest tests
│   ├── requirements.txt       # Python dependencies
│   └── .env.example           # Config template
├── src/
│   ├── api/                   # API client modules
│   ├── App.jsx                # Dashboard component
│   ├── Report.jsx             # Report component
│   ├── demoData.js            # Demo fallback data
│   └── ...                    # Other React components
├── package.json               # Frontend dependencies
├── vite.config.js             # Vite configuration
├── .env                       # Frontend config
└── test_integration.py        # Integration tests
```

## Next Steps

1. **Database**: Connect real PostgreSQL for LIVE mode
2. **Authentication**: Add JWT/OAuth for user management
3. **Providers**: Implement real Sentinel-1, AIS, OpenDrift integrations
4. **UI**: Add real-time updates via WebSocket
5. **Deployment**: Docker, cloud hosting, CI/CD pipeline

## Support

For issues or questions, check:

- Backend logs: `http://127.0.0.1:8000/docs` (Swagger)
- Frontend logs: Browser console (F12)
- Test output: `python test_integration.py`
