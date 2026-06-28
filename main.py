from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

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

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.on_event("startup")
def startup():
    init_db()


@app.get("/")
def login_page():
    return FileResponse("templates/login.html")


@app.get("/centros")
def centros_page():
    return FileResponse("templates/centros.html")


@app.get("/entregas")
def entregas_page():
    return FileResponse("templates/entregas.html")


@app.get("/materiales")
def materiales_page():
    return FileResponse("templates/materiales.html")


@app.get("/reportes")
def reportes_page():
    return FileResponse("templates/reportes.html")


@app.get("/usuarios")
def usuarios_page():
    return FileResponse("templates/usuarios.html")


app.include_router(auth_router)
app.include_router(collection_point_router)
app.include_router(recycler_router)
app.include_router(record_router)