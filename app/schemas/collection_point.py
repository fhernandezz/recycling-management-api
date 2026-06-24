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
