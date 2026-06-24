from pydantic import BaseModel


class ActiveStatusUpdate(BaseModel):
    is_active: bool


class MessageResponse(BaseModel):
    message: str
