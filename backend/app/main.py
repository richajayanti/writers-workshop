from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.database import Base, engine
from app import models
from app.routes.investigations import router as investigations_router

app = FastAPI(title="Writer's Workshop", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class HealthResponse(BaseModel):
    status: str
    message: str


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok", message="Writer's Workshop backend is running")

app.include_router(investigations_router)
Base.metadata.create_all(bind=engine)
