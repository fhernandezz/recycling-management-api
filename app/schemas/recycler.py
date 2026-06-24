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
