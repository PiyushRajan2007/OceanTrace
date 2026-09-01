"""Initial migration: create core tables

Revision ID: 001_initial
Revises: 
Create Date: 2026-09-02 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '001_initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create incidents table
    op.create_table(
        'incidents',
        sa.Column('id', sa.String(40), nullable=False),
        sa.Column('scene_id', sa.String(80), nullable=False),
        sa.Column('latitude', sa.Float(), nullable=False),
        sa.Column('longitude', sa.Float(), nullable=False),
        sa.Column('detected_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('source', sa.String(160), nullable=False),
        sa.Column('severity', sa.String(30), nullable=False),
        sa.Column('impact_score', sa.Integer(), nullable=False),
        sa.Column('impact_coast', sa.String(160), nullable=False),
        sa.Column('impact_eta_hours', sa.Integer(), nullable=False),
        sa.Column('forecast_summary', sa.Text(), nullable=False),
        sa.Column('geom_geojson', sa.JSON(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_incidents_scene_id'), 'incidents', ['scene_id'], unique=False)
    op.create_index(op.f('ix_incidents_detected_at'), 'incidents', ['detected_at'], unique=False)
    op.create_index(op.f('ix_incidents_severity'), 'incidents', ['severity'], unique=False)

    # Create slicks table
    op.create_table(
        'slicks',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('incident_id', sa.String(40), nullable=False),
        sa.Column('age', sa.String(40), nullable=False),
        sa.Column('area_km2', sa.Float(), nullable=False),
        sa.Column('perimeter_km', sa.Float(), nullable=False),
        sa.Column('length_km', sa.Float(), nullable=False),
        sa.Column('width_km', sa.Float(), nullable=False),
        sa.Column('aspect_ratio', sa.Float(), nullable=False),
        sa.Column('estimated_volume_m3', sa.Float(), nullable=False),
        sa.Column('confidence', sa.Float(), nullable=False),
        sa.Column('geometry_label', sa.String(120), nullable=False),
        sa.Column('polygon_geojson', sa.JSON(), nullable=True),
        sa.ForeignKeyConstraint(['incident_id'], ['incidents.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_slicks_incident_id'), 'slicks', ['incident_id'], unique=False)

    # Create vessels table
    op.create_table(
        'vessels',
        sa.Column('mmsi', sa.String(20), nullable=False),
        sa.Column('name', sa.String(120), nullable=False),
        sa.Column('flag', sa.String(10), nullable=False),
        sa.Column('score', sa.Integer(), nullable=False),
        sa.Column('origin', sa.String(120), nullable=False),
        sa.Column('destination', sa.String(120), nullable=False),
        sa.Column('dark_ship', sa.Boolean(), nullable=False),
        sa.Column('reasons', sa.JSON(), nullable=False),
        sa.Column('score_breakdown', sa.JSON(), nullable=False),
        sa.Column('last_position_geojson', sa.JSON(), nullable=True),
        sa.Column('track_geojson', sa.JSON(), nullable=True),
        sa.Column('ais_timeseries', sa.JSON(), nullable=False),
        sa.PrimaryKeyConstraint('mmsi')
    )
    op.create_index(op.f('ix_vessels_name'), 'vessels', ['name'], unique=False)

    # Create satellite_scenes table
    op.create_table(
        'satellite_scenes',
        sa.Column('scene_id', sa.String(80), nullable=False),
        sa.Column('provider', sa.String(80), nullable=False),
        sa.Column('sensor', sa.String(80), nullable=False),
        sa.Column('captured_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('processing_status', sa.String(40), nullable=False),
        sa.Column('footprint_geojson', sa.JSON(), nullable=True),
        sa.Column('metadata_json', sa.JSON(), nullable=False),
        sa.PrimaryKeyConstraint('scene_id')
    )
    op.create_index(op.f('ix_satellite_scenes_captured_at'), 'satellite_scenes', ['captured_at'], unique=False)

    # Create forecasts table
    op.create_table(
        'forecasts',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('incident_id', sa.String(40), nullable=False),
        sa.Column('horizon_hours', sa.Integer(), nullable=False),
        sa.Column('summary', sa.Text(), nullable=False),
        sa.Column('confidence', sa.Float(), nullable=False),
        sa.Column('path_geojson', sa.JSON(), nullable=True),
        sa.Column('conditions', sa.JSON(), nullable=False),
        sa.ForeignKeyConstraint(['incident_id'], ['incidents.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_forecasts_incident_id'), 'forecasts', ['incident_id'], unique=False)

    # Create alerts table
    op.create_table(
        'alerts',
        sa.Column('id', sa.String(40), nullable=False),
        sa.Column('incident_id', sa.String(40), nullable=True),
        sa.Column('title', sa.String(140), nullable=False),
        sa.Column('severity', sa.String(30), nullable=False),
        sa.Column('message', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('acknowledged', sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_alerts_incident_id'), 'alerts', ['incident_id'], unique=False)
    op.create_index(op.f('ix_alerts_severity'), 'alerts', ['severity'], unique=False)
    op.create_index(op.f('ix_alerts_created_at'), 'alerts', ['created_at'], unique=False)

    # Create reports table
    op.create_table(
        'reports',
        sa.Column('id', sa.String(40), nullable=False),
        sa.Column('incident_id', sa.String(40), nullable=False),
        sa.Column('title', sa.String(180), nullable=False),
        sa.Column('status', sa.String(40), nullable=False),
        sa.Column('generated_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('content', sa.JSON(), nullable=False),
        sa.ForeignKeyConstraint(['incident_id'], ['incidents.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_reports_incident_id'), 'reports', ['incident_id'], unique=False)


def downgrade() -> None:
    # Drop all tables in reverse order
    op.drop_index(op.f('ix_reports_incident_id'), table_name='reports')
    op.drop_table('reports')
    
    op.drop_index(op.f('ix_alerts_created_at'), table_name='alerts')
    op.drop_index(op.f('ix_alerts_severity'), table_name='alerts')
    op.drop_index(op.f('ix_alerts_incident_id'), table_name='alerts')
    op.drop_table('alerts')
    
    op.drop_index(op.f('ix_forecasts_incident_id'), table_name='forecasts')
    op.drop_table('forecasts')
    
    op.drop_index(op.f('ix_satellite_scenes_captured_at'), table_name='satellite_scenes')
    op.drop_table('satellite_scenes')
    
    op.drop_index(op.f('ix_vessels_name'), table_name='vessels')
    op.drop_table('vessels')
    
    op.drop_index(op.f('ix_slicks_incident_id'), table_name='slicks')
    op.drop_table('slicks')
    
    op.drop_index(op.f('ix_incidents_severity'), table_name='incidents')
    op.drop_index(op.f('ix_incidents_detected_at'), table_name='incidents')
    op.drop_index(op.f('ix_incidents_scene_id'), table_name='incidents')
    op.drop_table('incidents')
