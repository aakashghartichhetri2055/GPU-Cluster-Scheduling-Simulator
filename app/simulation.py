from app.agents.generator import generate_jobs
from app.metrics.summary import summarize
from app.schedulers.scheduler_factory import schedule_jobs

ALL_SCHEDULERS = ["fifo", "priority", "auction", "incentive", "ml_incentive"]


def run_simulation(num_users: int, num_gpus: int, scheduler: str, agent_mix: dict, seed: int = 42):
    base_jobs = generate_jobs(num_users, agent_mix, seed)
    scheduled = schedule_jobs(base_jobs, num_gpus, scheduler)
    metrics = summarize(scheduled, scheduler, num_gpus, base_jobs)
    return {
        "scheduler": scheduler,
        "num_users": num_users,
        "num_gpus": num_gpus,
        "seed": seed,
        "metrics": metrics,
        "jobs": scheduled[:25],
        "note": "Only first 25 jobs are returned for readability. Metrics use all jobs.",
    }


def compare_schedulers(request):
    schedulers = request.schedulers or ALL_SCHEDULERS
    results = {}
    for s in schedulers:
        sim = run_simulation(request.num_users, request.num_gpus, s, request.agent_mix, request.seed)
        results[s] = sim["metrics"]
    return {
        "experiment": "scheduler_comparison",
        "num_users": request.num_users,
        "num_gpus": request.num_gpus,
        "agent_mix": request.agent_mix,
        "results": results,
        "presentation_claim": "Compare how mechanism design changes strategic incentives and system-level outcomes.",
        "what_to_show": [
            "counterfactual.avg_manipulation_advantage",
            "counterfactual.manipulation_success_rate",
            "fairness_jain_waiting",
            "avg_waiting_time",
            "social_welfare",
        ],
    }


def greedy_sweep(request):
    rows = []
    for level in request.greedy_levels:
        agent_mix = {"greedy": level, "truthful": max(0, 1 - level)}
        for s in request.schedulers:
            sim = run_simulation(request.num_users, request.num_gpus, s, agent_mix, request.seed)
            m = sim["metrics"]
            c = m["counterfactual"]
            rows.append({
                "greedy_level": level,
                "scheduler": s,
                "avg_waiting_time": m["avg_waiting_time"],
                "fairness_jain_waiting": m["fairness_jain_waiting"],
                "social_welfare": m["social_welfare"],
                "avg_manipulation_advantage": c["avg_manipulation_advantage"],
                "manipulation_success_rate": c["manipulation_success_rate"],
                "lying_punished_rate": c["lying_punished_rate"],
            })
    return {
        "experiment": "greedy_sweep",
        "research_question": "How robust is each scheduler as the share of strategic users increases?",
        "rows": rows,
    }
