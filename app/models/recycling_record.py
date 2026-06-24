from sqlalchemy import Column, Date, Float, ForeignKey, String, Text

from config.database import Base


class RecyclingRecord(Base):
    __tablename__ = "recycling_records"

    record_id = Column(String(50), primary_key=True, index=True)
    recycler_id = Column(
        String(50),
        ForeignKey("recyclers.recycler_id"),
        nullable=False,
        index=True,
    )
    point_id = Column(
        String(50),
        ForeignKey("collection_points.point_id"),
        nullable=False,
        index=True,
    )
    material_type = Column(String(100), nullable=False)
    weight_kg = Column(Float, nullable=False)
    record_date = Column(Date, nullable=False)
    notes = Column(Text, nullable=False, default="")
