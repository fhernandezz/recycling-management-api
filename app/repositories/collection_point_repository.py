from sqlalchemy.orm import Session

from app.models.collection_point import CollectionPoint
from app.repositories.base_repository import BaseRepository


class CollectionPointRepository(BaseRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list:
        return self.db.query(CollectionPoint).all()

    def get_by_id(self, point_id: str):
        return (
            self.db.query(CollectionPoint)
            .filter(CollectionPoint.point_id == point_id)
            .first()
        )

    def add(self, point: CollectionPoint) -> CollectionPoint:
        self.db.add(point)
        self.db.commit()
        self.db.refresh(point)
        return point

    def update(self, point: CollectionPoint) -> CollectionPoint:
        self.db.commit()
        self.db.refresh(point)
        return point

    def delete(self, point: CollectionPoint) -> None:
        self.db.delete(point)
        self.db.commit()

    def save_all(self, points: list) -> None:
        self.db.add_all(points)
        self.db.commit()
