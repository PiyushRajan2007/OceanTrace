"""Test suite for AQUAVIGIL backend."""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    """Test /health endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["mode"] == "DEMO"


def test_list_incidents():
    """Test GET /api/v1/incidents."""
    response = client.get("/api/v1/incidents")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["id"] == "INC-240824-01"


def test_get_incident():
    """Test GET /api/v1/incidents/{incident_id}."""
    response = client.get("/api/v1/incidents/INC-240824-01")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "INC-240824-01"
    assert data["severity"] == "Warning"


def test_get_incident_slick():
    """Test GET /api/v1/incidents/{incident_id}/slick."""
    response = client.get("/api/v1/incidents/INC-240824-01/slick")
    assert response.status_code == 200
    data = response.json()
    assert data["age"] == "06h 18m"
    assert data["area_km2"] == 12.8


def test_get_incident_vessels():
    """Test GET /api/v1/incidents/{incident_id}/vessels."""
    response = client.get("/api/v1/incidents/INC-240824-01/vessels")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 3
    assert data[0]["name"] == "SEA ORCHID"


def test_list_vessels():
    """Test GET /api/v1/vessels."""
    response = client.get("/api/v1/vessels")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 3


def test_get_vessel():
    """Test GET /api/v1/vessels/{mmsi}."""
    response = client.get("/api/v1/vessels/477981200")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "SEA ORCHID"
    assert data["mmsi"] == "477981200"


def test_traffic_endpoint():
    """Test GET /api/v1/traffic."""
    response = client.get("/api/v1/traffic")
    assert response.status_code == 200
    data = response.json()
    assert data["mode"] == "DEMO"
    assert data["stage"] == "Suspects"


def test_traffic_with_stage():
    """Test GET /api/v1/traffic with stage parameter."""
    response = client.get("/api/v1/traffic?stage=Region")
    assert response.status_code == 200
    data = response.json()
    assert data["stage"] == "Region"
    assert data["count"] == 63


def test_list_alerts():
    """Test GET /api/v1/alerts."""
    response = client.get("/api/v1/alerts")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2


def test_list_scenes():
    """Test GET /api/v1/satellite/scenes."""
    response = client.get("/api/v1/satellite/scenes")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1


def test_get_forecast():
    """Test GET /api/v1/incidents/{incident_id}/forecast."""
    response = client.get("/api/v1/incidents/INC-240824-01/forecast")
    assert response.status_code == 200
    data = response.json()
    assert data["incident_id"] == "INC-240824-01"
    assert data["horizon_hours"] == 36


def test_get_recommendations():
    """Test GET /api/v1/incidents/{incident_id}/recommendations."""
    response = client.get("/api/v1/incidents/INC-240824-01/recommendations")
    assert response.status_code == 200
    data = response.json()
    assert data["mode"] == "DEMO"
    assert len(data["items"]) == 4


def test_get_evidence():
    """Test GET /api/v1/incidents/{incident_id}/evidence."""
    response = client.get("/api/v1/incidents/INC-240824-01/evidence")
    assert response.status_code == 200
    data = response.json()
    assert data["mode"] == "DEMO"
    assert data["algorithm"] == "SHA-256"
    assert len(data["chain"]) == 7


def test_list_reports():
    """Test GET /api/v1/reports."""
    response = client.get("/api/v1/reports")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1


def test_get_report():
    """Test GET /api/v1/reports/{report_id}."""
    response = client.get("/api/v1/reports/RPT-INC-240824-01")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "RPT-INC-240824-01"
    assert data["status"] == "READY FOR REVIEW"


def test_get_report_geojson():
    """Test GET /api/v1/reports/{report_id}/geojson."""
    response = client.get("/api/v1/reports/RPT-INC-240824-01/geojson")
    assert response.status_code == 200
    data = response.json()
    assert data["type"] == "Feature"
    assert data["properties"]["incident"] == "INC-240824-01"


def test_404_on_missing_incident():
    """Test 404 for non-existent incident."""
    response = client.get("/api/v1/incidents/INVALID-ID")
    assert response.status_code == 404


def test_404_on_missing_vessel():
    """Test 404 for non-existent vessel."""
    response = client.get("/api/v1/vessels/999999999")
    assert response.status_code == 404


if __name__ == "__main__":
    # Simple test runner
    import pytest
    pytest.main([__file__, "-v"])
