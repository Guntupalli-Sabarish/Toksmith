import uuid
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.base import Base

class Character(Base):
    __tablename__ = "characters"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    voice_provider = Column(String, nullable=False) # e.g., "Hume", "OpenAI"
    voice_id = Column(String, nullable=False)
    project_id = Column(UUID(as_uuid=True), ForeignKey("video_projects.id"), nullable=True) # Null for global characters
    avatar_url = Column(String, nullable=True)

    # Relationships
    project = relationship("VideoProject", back_populates="characters")
