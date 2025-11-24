import uuid
from sqlalchemy import Column, String, DateTime, Enum, Boolean, Integer, Float, ForeignKey, Text, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.db.base import Base

class AssetType(str, enum.Enum):
    BACKGROUND_VIDEO = "background_video"
    MUSIC = "music"
    SFX = "sfx"
    OVERLAY = "overlay"
    IMAGE = "image"

class Asset(Base):
    __tablename__ = "assets"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    type = Column(Enum(AssetType), nullable=False)
    url = Column(String, nullable=False)
    duration = Column(Float, nullable=True)
    tags = Column(JSON, default=list)
    is_global = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    project_associations = relationship("ProjectAsset", back_populates="asset")

class ProjectAsset(Base):
    __tablename__ = "project_assets"

    project_id = Column(UUID(as_uuid=True), ForeignKey("video_projects.id"), primary_key=True)
    asset_id = Column(UUID(as_uuid=True), ForeignKey("assets.id"), primary_key=True)
    usage_type = Column(String, nullable=False) # e.g., "background", "music"
    start_time = Column(Float, default=0.0)
    end_time = Column(Float, nullable=True)

    # Relationships
    project = relationship("VideoProject", back_populates="assets")
    asset = relationship("Asset", back_populates="project_associations")
