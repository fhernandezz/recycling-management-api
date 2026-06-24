from datetime import date
from pydantic import BaseModel, ConfigDict


class RecyclerCreate(BaseModel):
    recycler_id: str
    full_name: str
    id_number: str
    email: str
    phone: str
    district: str
    registration_date: date
    is_active: bool = True


class RecyclerUpdate(BaseModel):
    full_name: str | None = None
    id_number: str | None = None
    email: str | None = None
    phone: str | None = None
    district: str | None = None
    registration_date: date | None = None
    is_active: bool | None = None


class RecyclerResponse(BaseModel):
    recycler_id: str
    full_name: str
    id_number: str
    email: str
    phone: str
    district: str
    registration_date: date
    is_active: bool

    model_config = ConfigDict(from_attributes=True)
