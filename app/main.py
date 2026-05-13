from fastapi import FastAPI
from app.routes.simulate import router as simulate_router
from app.routes.compare import router as compare_router
from app.routes.experiments import router as experiments_router
from app.routes.ml import router as ml_router
from app.routes.report import router as report_router

app = FastAPI(
    title="Game-Theoretic GPU Cluster Scheduling Simulator",
    description="Research-level FastAPI simulator for strategic GPU scheduling, mechanism design, and ML-assisted manipulation detection.",
    version="1.0.0",
)

app.include_router(simulate_router)
app.include_router(compare_router)
app.include_router(experiments_router)
app.include_router(ml_router)
app.include_router(report_router)

@app.get("/")
def root():
    return {
        "message": "GPU Game Simulator is running.",
        "docs": "/docs",
        "important_endpoints": ["/simulate", "/compare", "/experiments/greedy-sweep", "/ml/train", "/report"],
    }
