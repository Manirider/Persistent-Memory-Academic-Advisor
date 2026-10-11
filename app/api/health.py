from fastapi import APIRouter
from app.schemas.memory_schemas import HealthResponse

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def health():
    return {"status": "ok"}
