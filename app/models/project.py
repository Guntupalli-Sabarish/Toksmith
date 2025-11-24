import uuid
from sqlalchemy import Column, String, DateTime, Enum, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.db.base import Base

class ProjectStatus(str, enum.Enum):
    PENDING = "pending"
    SCRAPED = "scraped"
    SCRIPT_GENERATED = "script_generated"
    AUDIO_GENERATED = "audio_generated"
    VIDEO_RENDERING = "video_rendering"
    COMPLETED = "completed"
    FAILED = "failed"

class VideoProject(Base):
    __tablename__ = "video_projects"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=True)
    source_url = Column(String, nullable=False)
    source_type = Column(String, nullable=False)
    status = Column(Enum(ProjectStatus), default=ProjectStatus.PENDING)
    resolution = Column(String, default="1080x1920")
    
    # Legacy fields (kept for backward compatibility during migration, or can be deprecated)
    scraped_data = Column(JSON, nullable=True)
    script_data = Column(JSON, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    scripts = relationship("Script", back_populates="project")
    characters = relationship("Character", back_populates="project")
    assets = relationship("ProjectAsset", back_populates="project")
