from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.repositories.collection_point_repository import CollectionPointRepository
from app.schemas.collection_point import (
    CollectionPointCreate,
    CollectionPointResponse,
    CollectionPointUpdate,
)
from app.schemas.common import ActiveStatusUpdate, MessageResponse
from app.security import get_current_recycler_id
from app.services.collection_point_service import CollectionPointService
from config.database import get_db

router = APIRouter(prefix="/collection-points", tags=["Collection Points"])


def get_service(db: Session) -> CollectionPointService:
    repository = CollectionPointRepository(db)
    return CollectionPointService(repository)


@router.post("/", response_model=CollectionPointResponse)
def create_collection_point(
    point_data: CollectionPointCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_recycler_id),
):
    service = get_service(db)
    try:
        return service.register_collection_point(
            point_id=point_data.point_id,
            name=point_data.name,
            location=point_data.location,
            district=point_data.district,
            accepted_materials=point_data.accepted_materials,
            capacity_kg=point_data.capacity_kg,
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))


@router.get("/", response_model=list[CollectionPointResponse])
def get_collection_points(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_recycler_id),
):
    service = get_service(db)
    return service.get_all_points()


@router.get("/active", response_model=list[CollectionPointResponse])
def get_active_collection_points(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_recycler_id),
):
    service = get_service(db)
    return service.list_active_points()


@router.get("/{point_id}", response_model=CollectionPointResponse)
def get_collection_point(
    point_id: str,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_recycler_id),
):
    service = get_service(db)
    try:
        return service.get_point_by_id(point_id)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))


@router.put("/{point_id}", response_model=CollectionPointResponse)
def update_collection_point(
    point_id: str,
    point_data: CollectionPointUpdate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_recycler_id),
):
    service = get_service(db)
    try:
        return service.update_collection_point(
            point_id=point_id,
            name=point_data.name,
            location=point_data.location,
            district=point_data.district,
            accepted_materials=point_data.accepted_materials,
            capacity_kg=point_data.capacity_kg,
            current_load_kg=point_data.current_load_kg,
            is_active=point_data.is_active,
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))


@router.patch("/{point_id}/status", response_model=CollectionPointResponse)
def update_collection_point_status(
    point_id: str,
    status_data: ActiveStatusUpdate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_recycler_id),
):
    service = get_service(db)
    try:
        return service.set_active_status(point_id, status_data.is_active)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))


@router.delete("/{point_id}", response_model=MessageResponse)
def delete_collection_point(
    point_id: str,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_recycler_id),
):
    service = get_service(db)
    try:
        service.delete_collection_point(point_id)
        return {"message": "Punto de recoleccion eliminado correctamente."}
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))
