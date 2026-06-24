from sqlalchemy.orm import Session

from app.models.recycler import Recycler
from app.repositories.base_repository import BaseRepository


class RecyclerRepository(BaseRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list:
        return self.db.query(Recycler).all()

    def get_by_id(self, recycler_id: str):
        return (
            self.db.query(Recycler)
            .filter(Recycler.recycler_id == recycler_id)
            .first()
        )

    def get_by_id_number(self, id_number: str):
        return (
            self.db.query(Recycler)
            .filter(Recycler.id_number == id_number)
            .first()
        )

    def get_by_district(self, district: str) -> list:
        return (
            self.db.query(Recycler)
            .filter(Recycler.district == district)
            .all()
        )

    def add(self, recycler: Recycler) -> Recycler:
        self.db.add(recycler)
        self.db.commit()
        self.db.refresh(recycler)
        return recycler

    def update(self, recycler: Recycler) -> Recycler:
        self.db.commit()
        self.db.refresh(recycler)
        return recycler

    def delete(self, recycler: Recycler) -> None:
        self.db.delete(recycler)
        self.db.commit()

    def save_all(self, recyclers: list) -> None:
        self.db.add_all(recyclers)
        self.db.commit()
