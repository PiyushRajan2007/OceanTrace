from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Incident(Base):
    __tablename__ = "incidents"

    id: Mapped[str] = mapped_column(String(40), primary_key=True)
    scene_id: Mapped[str] = mapped_column(String(80), index=True)
    latitude: Mapped[float] = mapped_column(Float)
    longitude: Mapped[float] = mapped_column(Float)
    detected_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    source: Mapped[str] = mapped_column(String(160))
    severity: Mapped[str] = mapped_column(String(30), index=True)
    impact_score: Mapped[int] = mapped_column(Integer)
    impact_coast: Mapped[str] = mapped_column(String(160))
    impact_eta_hours: Mapped[int] = mapped_column(Integer)
    forecast_summary: Mapped[str] = mapped_column(Text)
    geom_geojson: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    slick: Mapped["Slick"] = relationship(back_populates="incident", uselist=False)


class Slick(Base):
    __tablename__ = "slicks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    incident_id: Mapped[str] = mapped_column(ForeignKey("incidents.id"), index=True)
    age: Mapped[str] = mapped_column(String(40))
    area_km2: Mapped[float] = mapped_column(Float)
    perimeter_km: Mapped[float] = mapped_column(Float)
    length_km: Mapped[float] = mapped_column(Float)
    width_km: Mapped[float] = mapped_column(Float)
    aspect_ratio: Mapped[float] = mapped_column(Float)
    estimated_volume_m3: Mapped[float] = mapped_column(Float)
    confidence: Mapped[float] = mapped_column(Float)
    geometry_label: Mapped[str] = mapped_column(String(120))
    polygon_geojson: Mapped[dict | None] = mapped_column(JSON, nullable=True)

    incident: Mapped[Incident] = relationship(back_populates="slick")


class Vessel(Base):
    __tablename__ = "vessels"

    mmsi: Mapped[str] = mapped_column(String(20), primary_key=True)
    name: Mapped[str] = mapped_column(String(120), index=True)
    flag: Mapped[str] = mapped_column(String(10))
    score: Mapped[int] = mapped_column(Integer)
    origin: Mapped[str] = mapped_column(String(120))
    destination: Mapped[str] = mapped_column(String(120))
    dark_ship: Mapped[bool] = mapped_column(Boolean, default=False)
    reasons: Mapped[list[str]] = mapped_column(JSON)
    score_breakdown: Mapped[dict] = mapped_column(JSON)
    last_position_geojson: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    track_geojson: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    ais_timeseries: Mapped[list[dict]] = mapped_column(JSON, default=list)


class SatelliteScene(Base):
    __tablename__ = "satellite_scenes"

    scene_id: Mapped[str] = mapped_column(String(80), primary_key=True)
    provider: Mapped[str] = mapped_column(String(80))
    sensor: Mapped[str] = mapped_column(String(80))
    captured_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    processing_status: Mapped[str] = mapped_column(String(40))
    footprint_geojson: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    metadata_json: Mapped[dict] = mapped_column(JSON, default=dict)


class Forecast(Base):
    __tablename__ = "forecasts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    incident_id: Mapped[str] = mapped_column(ForeignKey("incidents.id"), index=True)
    horizon_hours: Mapped[int] = mapped_column(Integer)
    summary: Mapped[str] = mapped_column(Text)
    confidence: Mapped[float] = mapped_column(Float)
    path_geojson: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    conditions: Mapped[dict] = mapped_column(JSON, default=dict)


class Alert(Base):
    __tablename__ = "alerts"

    id: Mapped[str] = mapped_column(String(40), primary_key=True)
    incident_id: Mapped[str | None] = mapped_column(String(40), index=True, nullable=True)
    title: Mapped[str] = mapped_column(String(140))
    severity: Mapped[str] = mapped_column(String(30), index=True)
    message: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    acknowledged: Mapped[bool] = mapped_column(Boolean, default=False)


class Report(Base):
    __tablename__ = "reports"

    id: Mapped[str] = mapped_column(String(40), primary_key=True)
    incident_id: Mapped[str] = mapped_column(ForeignKey("incidents.id"), index=True)
    title: Mapped[str] = mapped_column(String(180))
    status: Mapped[str] = mapped_column(String(40))
    generated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    content: Mapped[dict] = mapped_column(JSON, default=dict)
