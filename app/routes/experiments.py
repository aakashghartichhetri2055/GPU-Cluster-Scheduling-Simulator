from fastapi import APIRouter
from app.schemas import GreedySweepRequest
from app.simulation import greedy_sweep

router = APIRouter()

@router.post("/experiments/greedy-sweep")
def run_greedy_sweep(request: GreedySweepRequest):
    return greedy_sweep(request)
