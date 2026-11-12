from fastapi import FastAPI

from app.routes.auth import router as auth_router
from app.routes.pais import router as pais_router
from app.routes.ciudad import router as ciudad_router
from app.routes.moneda import router as moneda_router
from app.routes.tasa_cambio import router as tasa_cambio_router
from app.routes.clima import router as clima_router
from app.routes.historial import router as historial_router

from app.middleware.trace_id import TraceIDMiddleware
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Backend Viajes Turing",
    description="API REST para gestión de viajes",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:4200",
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
    expose_headers=["X-Trace-ID", "X-Process-Time"],
)

app.add_middleware(TraceIDMiddleware)

app.include_router(auth_router, prefix="/api")
app.include_router(pais_router, prefix="/api")
app.include_router(ciudad_router, prefix="/api")
app.include_router(moneda_router, prefix="/api")
app.include_router(tasa_cambio_router, prefix="/api")
app.include_router(clima_router, prefix="/api")
app.include_router(historial_router, prefix="/api")


@app.get("/")
async def health_check():
    return {
        "success": True,
        "message": "API is running"
    }