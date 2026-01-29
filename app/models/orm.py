from __future__ import annotations

from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, UniqueConstraint
from sqlalchemy.orm import relationship

from app.core.database import Base


class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    original_path = Column(String(512), nullable=False)
    processed_path = Column(String(512), nullable=False)
    width = Column(Integer, nullable=False)
    height = Column(Integer, nullable=False)
    size_bytes = Column(Integer, nullable=False)
    captured_at = Column(DateTime, nullable=True)
    weather = Column(String(64), nullable=True)
    time_of_day = Column(String(32), nullable=True)
    road_type = Column(String(64), nullable=True)
    quality_score = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    detections = relationship("Detection", back_populates="image", cascade="all, delete-orphan")


class Detection(Base):
    __tablename__ = "detections"
    __table_args__ = (UniqueConstraint("image_id", "object_id", name="uq_image_object"),)

    id = Column(Integer, primary_key=True, index=True)
    image_id = Column(Integer, ForeignKey("images.id", ondelete="CASCADE"), nullable=False)
    object_id = Column(String(128), nullable=True)
    label = Column(String(64), nullable=False)
    confidence = Column(Float, nullable=True)
    x_min = Column(Float, nullable=False)
    y_min = Column(Float, nullable=False)
    x_max = Column(Float, nullable=False)
    y_max = Column(Float, nullable=False)
    attributes = Column(Text, nullable=True)

    image = relationship("Image", back_populates="detections")


class DatasetVersion(Base):
    __tablename__ = "datasets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128), nullable=False)
    version = Column(String(64), nullable=False)
    description = Column(Text, nullable=True)
    path = Column(String(512), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    created_by = Column(String(128), nullable=True)
