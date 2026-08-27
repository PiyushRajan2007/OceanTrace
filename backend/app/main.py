"""AQUAVIGIL API adapter. All responses are deterministic demo data until providers are configured."""
from datetime import datetime, timezone
from hashlib import sha256
from typing import Literal
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="AQUAVIGIL Intelligence API", version="0.1.0")

class Slick(BaseModel):
    age: str = "06h 18m"
    area_km2: float = 12.8
    perimeter_km: float = 18.6
    length_km: float = 6.4
    width_km: float = 2.1
    aspect_ratio: float = 3.05
    estimated_volume_m3: float = 8.4
    confidence: float = 96.4
    geometry: str = "Irregular elongated polygon"

class Incident(BaseModel):
    id: str = "INC-240824-01"
    scene_id: str = "S1A_20260824_0417"
    mode: Literal["DEMO"] = "DEMO"
    latitude: float = 14.5333
    longitude: float = 68.3
    timestamp: str = "2026-08-24T08:42:00Z"
    source: str = "Sentinel-1 GRD · Demo scene"
    slick: Slick = Slick()
    severity: Literal["Normal", "Watch", "Warning", "Critical"] = "Warning"
    impact_eta_hours: int = 36
    impact_coast: str = "Lakshadweep marine zone"

class Vessel(BaseModel):
    name: str
    mmsi: str
    flag: str
    score: int
    origin: str
    destination: str
    dark_ship: bool
    reasons: list[str]
    breakdown: dict[str, int]

VESSELS = [
    Vessel(name="SEA ORCHID", mmsi="477981200", flag="SG", score=92, origin="Singapore", destination="Mumbai, IN", dark_ship=True, reasons=["18 min AIS dark period", "0.8 nm from slick origin", "Heading aligns 87% with drift"], breakdown={"proximity": 96, "trajectory": 91, "behavior": 88, "ais_gap": 94}),
    Vessel(name="PACIFIC MERIDIAN", mmsi="636019874", flag="LR", score=76, origin="Fujairah, AE", destination="Unknown", dark_ship=False, reasons=["Course deviation at 04:10 UTC", "2.4 nm from spill envelope", "Speed drop below 4 knots"], breakdown={"proximity": 74, "trajectory": 79, "behavior": 81, "ais_gap": 62}),
    Vessel(name="NORDIC STAR", mmsi="311000452", flag="BS", score=54, origin="Unknown", destination="Colombo, LK", dark_ship=False, reasons=["3.2 nm from slick", "Trajectory partially aligned"], breakdown={"proximity": 48, "trajectory": 64, "behavior": 51, "ais_gap": 42}),
]

STAGES = {"All Traffic": 184, "Region": 63, "Spill Envelope": 17, "Temporal": 11, "Behavioral": 6, "Suspects": 3}

@app.get("/health")
def health():
    return {"status": "ok", "mode": "DEMO", "timestamp": datetime.now(timezone.utc).isoformat()}

@app.get("/api/v1/incidents", response_model=list[Incident])
def incidents():
    return [Incident()]

@app.get("/api/v1/incidents/{incident_id}", response_model=Incident)
def incident(incident_id: str):
    return Incident(id=incident_id)

@app.get("/api/v1/incidents/{incident_id}/vessels", response_model=list[Vessel])
def vessels(incident_id: str):
    return VESSELS

@app.get("/api/v1/traffic")
def traffic(stage: str = "Suspects"):
    return {"mode": "DEMO", "stage": stage, "count": STAGES.get(stage, 184), "available_stages": STAGES}

@app.get("/api/v1/incidents/{incident_id}/recommendations")
def recommendations(incident_id: str):
    return {"mode": "DEMO", "decision_support_only": True, "items": ["Increase satellite revisit monitoring to every 6 hours", "Prioritize response asset nearest to the Lakshadweep marine zone", "Review SEA ORCHID voyage records and AIS gap evidence", "Recalculate impact zone after the next current-model update"]}

@app.get("/api/v1/incidents/{incident_id}/evidence")
def evidence(incident_id: str):
    labels = ["Raw Scene", "Processing", "Detection", "Vessel Correlation", "Forecast", "Attribution", "Report"]
    previous = "GENESIS"
    chain = []
    for label in labels:
        current = sha256(f"{previous}|{label}|{incident_id}".encode()).hexdigest()
        chain.append({"stage": label, "previous_hash": previous, "current_hash": current, "verified": True})
        previous = current
    return {"mode": "DEMO", "algorithm": "SHA-256", "verified": True, "chain": chain}
