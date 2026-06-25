from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.repositories.recycler_repository import RecyclerRepository
from app.schemas.common import ActiveStatusUpdate, MessageResponse
from app.schemas.recycler import RecyclerCreate, RecyclerResponse, RecyclerUpdate
from app.security import get_current_recycler_id
from app.services.recycler_service import RecyclerService
from config.database import get_db
from app.security import create_session_token

router = APIRouter(prefix="/recyclers", tags=["Recyclers"])


def get_service(db: Session) -> RecyclerService:
    repository = RecyclerRepository(db)
    return RecyclerService(repository)


@router.post("/", response_model=RecyclerResponse)
def create_recycler(recycler_data: RecyclerCreate, db: Session = Depends(get_db)):
    service = get_service(db)
    try:
        return service.register_recycler(
            recycler_id=recycler_data.recycler_id,
            full_name=recycler_data.full_name,
            id_number=recycler_data.id_number,
            email=recycler_data.email,
            phone=recycler_data.phone,
            district=recycler_data.district,
            registration_date=recycler_data.registration_date,
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))


@router.get("/", response_model=list[RecyclerResponse])
def get_recyclers(
    district: str | None = Query(default=None),
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_recycler_id),
):
    service = get_service(db)
    if district:
        return service.get_recyclers_by_district(district)
    return service.get_all_recyclers()


@router.get("/{recycler_id}", response_model=RecyclerResponse)
def get_recycler(
    recycler_id: str,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_recycler_id),
):
    service = get_service(db)
    try:
        return service.get_recycler_by_id(recycler_id)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))


@router.put("/{recycler_id}", response_model=RecyclerResponse)
def update_recycler(
    recycler_id: str,
    recycler_data: RecyclerUpdate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_recycler_id),
):
    service = get_service(db)
    try:
        return service.update_recycler(
            recycler_id=recycler_id,
            full_name=recycler_data.full_name,
            id_number=recycler_data.id_number,
            email=recycler_data.email,
            phone=recycler_data.phone,
            district=recycler_data.district,
            registration_date=recycler_data.registration_date,
            is_active=recycler_data.is_active,
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))


@router.patch("/{recycler_id}/status", response_model=RecyclerResponse)
def update_recycler_status(
    recycler_id: str,
    status_data: ActiveStatusUpdate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_recycler_id),
):
    service = get_service(db)
    try:
        return service.set_active_status(recycler_id, status_data.is_active)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))


@router.delete("/{recycler_id}", response_model=MessageResponse)
def delete_recycler(
    recycler_id: str,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_recycler_id),
):
    service = get_service(db)
    try:
        service.delete_recycler(recycler_id)
        return {"message": "Reciclador eliminado correctamente."}
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))

@router.post("/login")
def login(recycler_id:str):
    token = create_session_token(recycler_id)
    return {
        "token": token
    }