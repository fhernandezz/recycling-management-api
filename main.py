from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import (
    auth_router,
    collection_point_router,
    record_router,
    recycler_router,
)
from config.database import init_db

app = FastAPI(
    title="Recycling Management API",
    description="Backend para la gestion comunitaria de reciclaje.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup():
    init_db()


@app.get("/")
def root():
    return {"message": "Recycling Management API is running"}


app.include_router(auth_router)
app.include_router(collection_point_router)
app.include_router(recycler_router)
app.include_router(record_router)
