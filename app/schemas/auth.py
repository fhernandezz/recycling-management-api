from pydantic import BaseModel


class LoginRequest(BaseModel):
    recycler_id: str
    password: str


class LoginResponse(BaseModel):
    authenticated: bool
    token: str
    recycler_id: str
    full_name: str
