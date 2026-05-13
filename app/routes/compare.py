from fastapi import APIRouter
from app.schemas import CompareRequest
from app.simulation import compare_schedulers

router = APIRouter()

@router.post("/compare")
def compare(request: CompareRequest):
    return compare_schedulers(request)
