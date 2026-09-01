from __future__ import annotations

from hashlib import sha256
from typing import Any

from app.schemas import (
    Alert,
    EvidenceResponse,
    EvidenceStep,
    Forecast,
    Incident,
    ProcessSatelliteResponse,
    RecommendationResponse,
    Report,
    SatelliteScene,
    Slick,
    TrafficResponse,
    TrafficStage,
    Vessel,
)

INCIDENT_ID = "INC-240824-01"
SCENE_ID = "S1A_20260824_0417"


def point(lon: float, lat: float) -> dict[str, Any]:
    return {"type": "Point", "coordinates": [lon, lat]}


INCIDENT = Incident(
    id=INCIDENT_ID,
    scene_id=SCENE_ID,
    latitude=14.5333,
    longitude=68.3,
    detected_at="2026-08-24T08:42:00Z",
    source="Sentinel-1 GRD - Demo scene",
    severity="Warning",
    impact_score=78,
    impact_coast="Lakshadweep marine zone",
    impact_eta_hours=36,
    forecast_summary="Drift vector trending ENE. Coastal impact probability: moderate.",
    geom_geojson=point(68.3, 14.5333),
    slick=Slick(
        age="06h 18m",
        area_km2=12.8,
        perimeter_km=18.6,
        length_km=6.4,
        width_km=2.1,
        aspect_ratio=3.05,
        estimated_volume_m3=8.4,
        confidence=96.4,
        geometry="Irregular elongated polygon",
        polygon_geojson={
            "type": "Polygon",
            "coordinates": [[[68.18, 14.48], [68.42, 14.51], [68.36, 14.61], [68.12, 14.57], [68.18, 14.48]]],
        },
    ),
)

VESSELS = [
    Vessel(
        name="SEA ORCHID",
        mmsi="477981200",
        flag="SG",
        score=92,
        origin="Singapore",
        destination="Mumbai, IN",
        dark_ship=True,
        reasons=["18 min AIS dark period", "0.8 nm from slick origin", "Heading aligns 87% with drift"],
        breakdown={"proximity": 96, "trajectory": 91, "behavior": 88, "aisGap": 94},
        last_position_geojson=point(68.18, 14.47),
        track_geojson={"type": "LineString", "coordinates": [[67.9, 14.2], [68.1, 14.38], [68.18, 14.47]]},
        ais_timeseries=[
            {"timestamp": "2026-08-24T04:00:00Z", "speed_knots": 11.2, "lat": 14.2, "lon": 67.9},
            {"timestamp": "2026-08-24T04:18:00Z", "speed_knots": 0.0, "lat": 14.31, "lon": 68.03},
            {"timestamp": "2026-08-24T04:36:00Z", "speed_knots": 9.4, "lat": 14.47, "lon": 68.18},
        ],
    ),
    Vessel(
        name="PACIFIC MERIDIAN",
        mmsi="636019874",
        flag="LR",
        score=76,
        origin="Fujairah, AE",
        destination="Unknown",
        dark_ship=False,
        reasons=["Course deviation at 04:10 UTC", "2.4 nm from spill envelope", "Speed drop below 4 knots"],
        breakdown={"proximity": 74, "trajectory": 79, "behavior": 81, "aisGap": 62},
        last_position_geojson=point(68.05, 14.35),
        track_geojson={"type": "LineString", "coordinates": [[67.7, 14.04], [67.95, 14.2], [68.05, 14.35]]},
    ),
    Vessel(
        name="NORDIC STAR",
        mmsi="311000452",
        flag="BS",
        score=54,
        origin="Unknown",
        destination="Colombo, LK",
        dark_ship=False,
        reasons=["3.2 nm from slick", "Trajectory partially aligned"],
        breakdown={"proximity": 48, "trajectory": 64, "behavior": 51, "aisGap": 42},
        last_position_geojson=point(68.5, 14.72),
        track_geojson={"type": "LineString", "coordinates": [[68.2, 14.96], [68.36, 14.82], [68.5, 14.72]]},
    ),
]

TRAFFIC_STAGES = [
    TrafficStage(label="All Traffic", count=184),
    TrafficStage(label="Region", count=63),
    TrafficStage(label="Spill Envelope", count=17),
    TrafficStage(label="Temporal", count=11),
    TrafficStage(label="Behavioral", count=6),
    TrafficStage(label="Suspects", count=3),
]

SCENES = [
    SatelliteScene(
        scene_id=SCENE_ID,
        provider="Sentinel-1",
        sensor="SAR GRD",
        captured_at="2026-08-24T04:17:00Z",
        processing_status="processed",
        footprint_geojson={"type": "Polygon", "coordinates": [[[67.8, 14.0], [68.9, 14.0], [68.9, 15.0], [67.8, 15.0], [67.8, 14.0]]]},
        metadata={"mode": "DEMO", "orbit": "ascending", "resolution_m": 10},
    )
]

ALERTS = [
    Alert(id="ALT-001", incident_id=INCIDENT_ID, title="Oil slick detected", severity="Warning", message="Sentinel-1 scene produced a high-confidence slick detection.", created_at="2026-08-24T08:42:04Z"),
    Alert(id="ALT-002", incident_id=INCIDENT_ID, title="Dark vessel detected", severity="Warning", message="SEA ORCHID has an 18 minute AIS gap near the slick origin.", created_at="2026-08-24T08:42:22Z"),
]

RECOMMENDATIONS = [
    "Increase satellite revisit monitoring to every 6 hours",
    "Prioritize response asset nearest to the Lakshadweep marine zone",
    "Review SEA ORCHID voyage records and AIS gap evidence",
    "Recalculate impact zone after the next current-model update",
]


class DemoRepository:
    mode = "DEMO"

    def list_incidents(self) -> list[Incident]:
        return [INCIDENT]

    def get_incident(self, incident_id: str) -> Incident | None:
        return INCIDENT if incident_id == INCIDENT_ID else None

    def get_slick(self, incident_id: str) -> Slick | None:
        incident = self.get_incident(incident_id)
        return incident.slick if incident else None

    def slick_metrics(self, incident_id: str) -> dict[str, Any] | None:
        slick = self.get_slick(incident_id)
        if not slick:
            return None
        return slick.model_dump()

    def list_vessels(self) -> list[Vessel]:
        return VESSELS

    def get_vessel(self, mmsi: str) -> Vessel | None:
        return next((vessel for vessel in VESSELS if vessel.mmsi == mmsi), None)

    def vessels_for_incident(self, incident_id: str) -> list[Vessel] | None:
        return VESSELS if self.get_incident(incident_id) else None

    def traffic(self, stage: str = "Suspects") -> TrafficResponse:
        selected = next((item for item in TRAFFIC_STAGES if item.label == stage), TRAFFIC_STAGES[0])
        return TrafficResponse(mode=self.mode, stage=selected.label, count=selected.count, available_stages=TRAFFIC_STAGES)

    def list_scenes(self) -> list[SatelliteScene]:
        return SCENES

    def get_scene(self, scene_id: str) -> SatelliteScene | None:
        return next((scene for scene in SCENES if scene.scene_id == scene_id), None)

    def process_scene(self, scene_id: str) -> ProcessSatelliteResponse:
        scene = self.get_scene(scene_id)
        if not scene:
            return ProcessSatelliteResponse(mode=self.mode, scene_id=scene_id, status="not_found", message="Scene is not available in demo data.")
        return ProcessSatelliteResponse(mode=self.mode, scene_id=scene_id, status="processed", message="Demo scene already has deterministic slick output.")

    def forecast(self, incident_id: str) -> Forecast | None:
        if not self.get_incident(incident_id):
            return None
        return Forecast(
            incident_id=incident_id,
            horizon_hours=36,
            summary=INCIDENT.forecast_summary,
            confidence=81.0,
            conditions={"wind": "18 kn WSW - 247 deg", "current": "1.4 kn ENE - 065 deg", "waves": "1.8 m - moderate sea"},
            path_geojson={"type": "LineString", "coordinates": [[68.3, 14.5333], [68.55, 14.7], [68.8, 14.92]]},
        )

    def list_alerts(self) -> list[Alert]:
        return ALERTS

    def get_alert(self, alert_id: str) -> Alert | None:
        return next((alert for alert in ALERTS if alert.id == alert_id), None)

    def recommendations(self, incident_id: str) -> RecommendationResponse | None:
        if not self.get_incident(incident_id):
            return None
        return RecommendationResponse(mode=self.mode, items=RECOMMENDATIONS)

    def evidence(self, incident_id: str) -> EvidenceResponse | None:
        if not self.get_incident(incident_id):
            return None
        labels = ["Raw Scene", "Processing", "Detection", "Vessel Correlation", "Forecast", "Attribution", "Report"]
        previous = "GENESIS"
        chain = []
        for label in labels:
            current = sha256(f"{previous}|{label}|{incident_id}".encode()).hexdigest()
            chain.append(EvidenceStep(stage=label, previous_hash=previous, current_hash=current, verified=True))
            previous = current
        return EvidenceResponse(mode=self.mode, algorithm="SHA-256", verified=True, chain=chain)

    def list_reports(self) -> list[Report]:
        return [self.get_report(f"RPT-{INCIDENT_ID}")]

    def get_report(self, report_id: str) -> Report | None:
        if report_id not in {f"RPT-{INCIDENT_ID}", INCIDENT_ID}:
            return None
        return Report(
            id=f"RPT-{INCIDENT_ID}",
            incident_id=INCIDENT_ID,
            title="Oil spill intelligence brief",
            status="READY FOR REVIEW",
            generated_at="2026-08-24T08:44:12Z",
            incident=INCIDENT,
            vessels=VESSELS,
            recommendations=RECOMMENDATIONS,
            evidence=self.evidence(INCIDENT_ID),
        )

    def report_geojson(self, report_id: str) -> dict[str, Any] | None:
        report = self.get_report(report_id)
        if not report:
            return None
        return {
            "type": "Feature",
            "properties": {"incident": report.incident.id, "area_km2": report.incident.slick.area_km2, "confidence": report.incident.slick.confidence},
            "geometry": report.incident.geom_geojson,
        }
