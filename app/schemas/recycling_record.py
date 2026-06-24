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


class RecyclingRecordResponse(BaseModel):
    record_id: str
    recycler_id: str
    point_id: str
    material_type: str
    weight_kg: float
    record_date: date
    notes: str

    model_config = ConfigDict(from_attributes=True)
