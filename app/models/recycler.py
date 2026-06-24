from sqlalchemy import Boolean, Column, Date, String

from config.database import Base


class Recycler(Base):
    __tablename__ = "recyclers"

    recycler_id = Column(String(50), primary_key=True, index=True)
    full_name = Column(String(150), nullable=False)
    id_number = Column(String(50), nullable=False, unique=True)
    email = Column(String(150), nullable=False, unique=True)
    phone = Column(String(30), nullable=False)
    district = Column(String(100), nullable=False)
    registration_date = Column(Date, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
