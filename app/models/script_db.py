import uuid
from sqlalchemy import Column, String, DateTime, Boolean, Integer, Float, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base

class Script(Base):
    __tablename__ = "scripts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey("video_projects.id"), nullable=False)
    version = Column(Integer, default=1)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    project = relationship("VideoProject", back_populates="scripts")
    lines = relationship("DialogueLine", back_populates="script", cascade="all, delete-orphan", order_by="DialogueLine.order")

class DialogueLine(Base):
    __tablename__ = "dialogue_lines"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    script_id = Column(UUID(as_uuid=True), ForeignKey("scripts.id"), nullable=False)
    character_id = Column(UUID(as_uuid=True), ForeignKey("characters.id"), nullable=True)
    speaker_name = Column(String, nullable=False) # Fallback or display name
    text = Column(Text, nullable=False)
    order = Column(Integer, nullable=False)
    audio_url = Column(String, nullable=True)
    audio_duration = Column(Float, default=0.0)
    start_time = Column(Float, default=0.0)

    # Relationships
    script = relationship("Script", back_populates="lines")
    character = relationship("app.models.character.Character")
