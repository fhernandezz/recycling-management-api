from app.routers.auth_router import router as auth_router
from app.routers.collection_point_router import router as collection_point_router
from app.routers.record_router import router as record_router
from app.routers.recycler_router import router as recycler_router

__all__ = [
    "auth_router",
    "collection_point_router",
    "record_router",
    "recycler_router",
]
