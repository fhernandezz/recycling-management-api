from app.schemas.auth import LoginRequest, LoginResponse
from app.schemas.collection_point import (
    CollectionPointCreate,
    CollectionPointResponse,
    CollectionPointUpdate,
)
from app.schemas.common import ActiveStatusUpdate, MessageResponse
from app.schemas.recycler import RecyclerCreate, RecyclerResponse, RecyclerUpdate
from app.schemas.recycling_record import (
    RecyclingRecordCreate,
    RecyclingRecordResponse,
    RecyclingRecordUpdate,
)

__all__ = [
    "ActiveStatusUpdate",
    "CollectionPointCreate",
    "CollectionPointResponse",
    "CollectionPointUpdate",
    "LoginRequest",
    "LoginResponse",
    "MessageResponse",
    "RecyclerCreate",
    "RecyclerResponse",
    "RecyclerUpdate",
    "RecyclingRecordCreate",
    "RecyclingRecordResponse",
    "RecyclingRecordUpdate",
]
