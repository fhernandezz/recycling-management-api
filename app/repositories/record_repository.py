from datetime import date
from sqlalchemy.orm import Session

from app.models.recycling_record import RecyclingRecord
from app.repositories.base_repository import BaseRepository


class RecordRepository(BaseRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list:
        return self.db.query(RecyclingRecord).all()

    def get_by_id(self, record_id: str):
        return (
            self.db.query(RecyclingRecord)
            .filter(RecyclingRecord.record_id == record_id)
            .first()
        )

    def get_by_recycler(self, recycler_id: str) -> list:
        return (
            self.db.query(RecyclingRecord)
            .filter(RecyclingRecord.recycler_id == recycler_id)
            .all()
        )

    def get_by_point(self, point_id: str) -> list:
        return (
            self.db.query(RecyclingRecord)
            .filter(RecyclingRecord.point_id == point_id)
            .all()
        )

    def get_by_date_range(self, start_date: date, end_date: date) -> list:
        return (
            self.db.query(RecyclingRecord)
            .filter(RecyclingRecord.record_date >= start_date)
            .filter(RecyclingRecord.record_date <= end_date)
            .all()
        )

    def add(self, record: RecyclingRecord) -> RecyclingRecord:
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return record

    def update(self, record: RecyclingRecord) -> RecyclingRecord:
        self.db.commit()
        self.db.refresh(record)
        return record

    def delete(self, record: RecyclingRecord) -> None:
        self.db.delete(record)
        self.db.commit()

    def save_all(self, records: list) -> None:
        self.db.add_all(records)
        self.db.commit()
