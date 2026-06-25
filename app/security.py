from uuid import uuid4

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

security = HTTPBearer()
active_sessions = {}


def create_session_token(recycler_id: str) -> str:
    token = str(uuid4())
    active_sessions[token] = recycler_id
    return token


def get_current_recycler_id(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> str:

    token = credentials.credentials

    print("TOKEN QUE LLEGA:", token)
    print("TOKENS GUARDADOS:", active_sessions)

    recycler_id = active_sessions.get(token)

    if not recycler_id:
        raise HTTPException(
            status_code=401,
            detail="Token invalido o expirado."
        )

    return recycler_id