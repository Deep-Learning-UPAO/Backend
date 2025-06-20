from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app import api
from app.db.models import Base
from app.db.database import engine
import os

# Crear tablas
Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # O lista de dominios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rutas API
app.include_router(api.router)

# Archivos estáticos React
# app.mount("/static", StaticFiles(directory="app/frontend/static"), name="static")

# Fallback SPA (cualquier ruta desconocida envía index.html)
# @app.get("/{full_path:path}")
# async def serve_react_app(full_path: str):
#    return FileResponse(os.path.join("app", "frontend", "index.html"))
