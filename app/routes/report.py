from fastapi import APIRouter
from app.schemas import CompareRequest
from app.simulation import compare_schedulers

router = APIRouter()

@router.get("/report")
def generate_report():
    request = CompareRequest(
        num_users=80,
        num_gpus=8,
        agent_mix={"truthful": 0.5, "greedy": 0.3, "random": 0.1, "learning": 0.1},
        seed=42,
    )
    comparison = compare_schedulers(request)
    return {
        "title": "Game-Theoretic GPU Cluster Scheduling Simulator",
        "core_claim": "Incentive-aware mechanisms reduce the payoff from manipulation in GPU scheduling.",
        "research_question": "How does strategic urgency inflation affect fairness and efficiency in shared GPU clusters?",
        "model": {
            "players": "Users submitting GPU jobs",
            "strategy": "Report true urgency or inflate urgency",
            "payoff": "Earlier scheduling benefit minus waiting cost and manipulation penalty",
            "concepts": [
                "Nash Equilibrium",
                "Dominant Strategy",
                "Mechanism Design",
                "Bayesian Games / Private Information",
                "Repeated Games and Punishment",
                "Counterfactual Analysis",
            ],
        },
        "key_results": comparison["results"],
        "presentation_takeaways": [
            "Priority scheduling rewards urgency exaggeration.",
            "Incentive-aware scheduling makes lying costly.",
            "ML-assisted scheduling detects manipulation risk and changes allocation scores.",
            "Counterfactual analysis shows whether lying actually helped each user.",
        ],
        "recommended_slides": [
            "Problem: scarce GPUs and private urgency",
            "Game model: players, strategies, payoff",
            "Schedulers: FIFO, priority, auction, incentive, ML-incentive",
            "Manipulation advantage by scheduler",
            "Lying success rate vs punishment rate",
            "Greedy sweep under strategic pressure",
            "ML manipulation detector",
            "Conclusion: mechanism design changes the equilibrium",
        ],
    }
