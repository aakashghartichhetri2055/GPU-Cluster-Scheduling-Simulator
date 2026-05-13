from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class SimulateRequest(BaseModel):
    num_users: int = Field(50, ge=1, le=1000)
    num_gpus: int = Field(8, ge=1, le=256)
    scheduler: str = "incentive"
    agent_mix: Dict[str, float] = Field(default_factory=lambda: {"truthful": 0.4, "greedy": 0.4, "learning": 0.2})
    seed: int = 42


class CompareRequest(BaseModel):
    num_users: int = Field(80, ge=1, le=1000)
    num_gpus: int = Field(8, ge=1, le=256)
    agent_mix: Dict[str, float] = Field(default_factory=lambda: {"truthful": 0.5, "greedy": 0.3, "random": 0.1, "learning": 0.1})
    seed: int = 42
    schedulers: Optional[List[str]] = None


class GreedySweepRequest(BaseModel):
    num_users: int = Field(80, ge=1, le=1000)
    num_gpus: int = Field(8, ge=1, le=256)
    seed: int = 42
    greedy_levels: List[float] = Field(default_factory=lambda: [0, 0.25, 0.5, 0.75, 1.0])
    schedulers: List[str] = Field(default_factory=lambda: ["priority", "incentive", "ml_incentive"])
