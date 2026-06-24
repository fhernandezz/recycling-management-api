from pydantic import BaseModel, ConfigDict

class CollectionPointCreate(BaseModel):
    point_id: str
    name: str
    location: str
    district: str
    accepted_materials: str
    capacity_kg: float
    current_load_kg: float = 0.0
    is_active: bool = True


class CollectionPointUpdate(BaseModel):
    name: str | None = None
    location: str | None = None
    district: str | None = None
    accepted_materials: str | None = None
    capacity_kg: float | None = None
    current_load_kg: float | None = None
    is_active: bool | None = None


class CollectionPointResponse(BaseModel):
    point_id: str
    name: str
    location: str
    district: str
    accepted_materials: str
    capacity_kg: float
    current_load_kg: float
    is_active: bool

    model_config = ConfigDict(from_attributes=True)
