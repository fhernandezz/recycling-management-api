from datetime import date
from pydantic import BaseModel, ConfigDict


class RecyclingRecordCreate(BaseModel):
    record_id: str
    recycler_id: str
    point_id: str
    material_type: str
    weight_kg: float
    record_date: date
    notes: str = ""


class RecyclingRecordUpdate(BaseModel):
    recycler_id: str | None = None
    point_id: str | None = None
    material_type: str | None = None
    weight_kg: float | None = None
    record_date: date | None = None
    notes: str | None = None


class RecyclingRecordResponse(BaseModel):
    record_id: str
    recycler_id: str
    point_id: str
    material_type: str
    weight_kg: float
    record_date: date
    notes: str

    model_config = ConfigDict(from_attributes=True)
