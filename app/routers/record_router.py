from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.repositories.collection_point_repository import CollectionPointRepository
from app.repositories.record_repository import RecordRepository
from app.repositories.recycler_repository import RecyclerRepository
from app.schemas.common import MessageResponse
from app.schemas.recycling_record import (
    RecyclingRecordCreate,
    RecyclingRecordResponse,
    RecyclingRecordUpdate,
)
from app.security import get_current_recycler_id
from app.services.collection_point_service import CollectionPointService
from app.services.record_service import RecordService
from app.services.recycler_service import RecyclerService
from config.database import get_db

router = APIRouter(prefix="/records", tags=["Recycling Records"])


def get_service(db: Session) -> RecordService:
    record_repository = RecordRepository(db)
    recycler_repository = RecyclerRepository(db)
    point_repository = CollectionPointRepository(db)
    recycler_service = RecyclerService(recycler_repository)
    point_service = CollectionPointService(point_repository)
    return RecordService(record_repository, recycler_service, point_service)


@router.post("/", response_model=RecyclingRecordResponse)
def create_record(
    record_data: RecyclingRecordCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_recycler_id),
):
    service = get_service(db)
    try:
        return service.register_delivery(
            record_id=record_data.record_id,
            recycler_id=record_data.recycler_id,
            point_id=record_data.point_id,
            material_type=record_data.material_type,
            weight_kg=record_data.weight_kg,
            notes=record_data.notes,
            record_date=record_data.record_date,
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))


@router.get("/", response_model=list[RecyclingRecordResponse])
def get_records(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_recycler_id),
):
    service = get_service(db)
    return service.get_all_records()


@router.get("/by-recycler/{recycler_id}", response_model=list[RecyclingRecordResponse])
def get_records_by_recycler(
    recycler_id: str,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_recycler_id),
):
    service = get_service(db)
    try:
        return service.get_records_by_recycler(recycler_id)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))


@router.get("/by-point/{point_id}", response_model=list[RecyclingRecordResponse])
def get_records_by_point(
    point_id: str,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_recycler_id),
):
    service = get_service(db)
    try:
        return service.get_records_by_point(point_id)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))


@router.get("/reports/top-recyclers")
def get_top_recyclers(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_recycler_id),
):
    service = get_service(db)
    return service.get_top_recyclers()


@router.get("/reports/collection-points-status")
def get_collection_points_status(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_recycler_id),
):
    service = get_service(db)
    return service.get_collection_points_status()


@router.get("/reports/materials-breakdown")
def get_materials_breakdown(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_recycler_id),
):
    service = get_service(db)
    return service.get_materials_breakdown()


@router.get("/reports/date-range")
def get_records_by_date_range(
    start_date: str = Query(...),
    end_date: str = Query(...),
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_recycler_id),
):
    service = get_service(db)
    try:
        return service.get_records_by_date_range(start_date, end_date)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))


@router.get("/{record_id}", response_model=RecyclingRecordResponse)
def get_record(
    record_id: str,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_recycler_id),
):
    service = get_service(db)
    try:
        return service.get_record_by_id(record_id)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))


@router.put("/{record_id}", response_model=RecyclingRecordResponse)
def update_record(
    record_id: str,
    record_data: RecyclingRecordUpdate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_recycler_id),
):
    service = get_service(db)
    try:
        return service.update_record(
            record_id=record_id,
            recycler_id=record_data.recycler_id,
            point_id=record_data.point_id,
            material_type=record_data.material_type,
            weight_kg=record_data.weight_kg,
            record_date=record_data.record_date,
            notes=record_data.notes,
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))


@router.delete("/{record_id}", response_model=MessageResponse)
def delete_record(
    record_id: str,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_recycler_id),
):
    service = get_service(db)
    try:
        service.delete_record(record_id)
        return {"message": "Registro eliminado correctamente."}
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))
