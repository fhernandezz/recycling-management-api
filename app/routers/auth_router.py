from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.repositories.recycler_repository import RecyclerRepository
from app.schemas.auth import LoginRequest, LoginResponse
from app.security import create_session_token
from app.services.recycler_service import RecyclerService
from config.database import get_db

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", response_model=LoginResponse)
def login(credentials: LoginRequest, db: Session = Depends(get_db)):
    service = RecyclerService(RecyclerRepository(db))

    if not service.validate_credentials(credentials.recycler_id, credentials.password):
        raise HTTPException(status_code=401, detail="Credenciales invalidas.")

    recycler = service.get_recycler_by_id(credentials.recycler_id)
    return {
        "authenticated": True,
        "token": create_session_token(recycler.recycler_id),
        "recycler_id": recycler.recycler_id,
        "full_name": recycler.full_name,
    }
