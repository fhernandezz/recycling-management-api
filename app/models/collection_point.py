from sqlalchemy import Boolean, Column, Float, String, Text

from config.database import Base


class CollectionPoint(Base):
    __tablename__ = "collection_points"

    point_id = Column(String(50), primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    location = Column(String(255), nullable=False)
    district = Column(String(100), nullable=False)
    accepted_materials = Column(Text, nullable=False)
    capacity_kg = Column(Float, nullable=False)
    current_load_kg = Column(Float, nullable=False, default=0.0)
    is_active = Column(Boolean, nullable=False, default=True)
