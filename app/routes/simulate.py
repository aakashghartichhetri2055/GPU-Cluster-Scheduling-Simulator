from fastapi import APIRouter
from app.schemas import SimulateRequest
from app.simulation import run_simulation

router = APIRouter()

@router.post("/simulate")
def simulate(request: SimulateRequest):
    return run_simulation(request.num_users, request.num_gpus, request.scheduler, request.agent_mix, request.seed)
