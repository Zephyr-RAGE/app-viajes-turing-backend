from fastapi import FastAPI

from app.routes.auth import router as auth_router
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


@app.get("/")
async def health_check():
    return {
        "success": True,
        "message": "API is running"
    }