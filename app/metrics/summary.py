from app.metrics.counterfactual import counterfactual_manipulation
from app.utils.interpreter import interpret_scheduler


def jain_index(values):
    vals = [float(v) for v in values if v is not None]
    if not vals or sum(v * v for v in vals) == 0:
        return 1.0
    return (sum(vals) ** 2) / (len(vals) * sum(v * v for v in vals))


def summarize(jobs, scheduler, num_gpus, base_jobs=None):
    waits = [j["waiting_time"] for j in jobs]
    completion = [j["finish_time"] - j["arrival_time"] for j in jobs]
    total_duration_gpu = sum(j["duration"] * j["requested_gpus"] for j in jobs)
    makespan = max(j["finish_time"] for j in jobs) - min(j["arrival_time"] for j in jobs)
    utilization = total_duration_gpu / (makespan * num_gpus) if makespan > 0 else 0
    gaps = [max(0, j["reported_urgency"] - j["true_urgency"]) for j in jobs]
    truthful = [1 for j in jobs if j["reported_urgency"] == j["true_urgency"]]
    welfare = sum(20 * j["true_urgency"] - 1.2 * j["waiting_time"] - 4 * max(0, j["reported_urgency"] - j["true_urgency"]) for j in jobs)
    metrics = {
        "avg_waiting_time": round(sum(waits) / len(waits), 3),
        "max_waiting_time": round(max(waits), 3),
        "avg_completion_time": round(sum(completion) / len(completion), 3),
        "fairness_jain_waiting": round(jain_index(waits), 3),
        "avg_manipulation_gap": round(sum(gaps) / len(gaps), 3),
        "truthfulness_rate": round(len(truthful) / len(jobs), 3),
        "resource_utilization": round(utilization, 3),
        "social_welfare": round(welfare, 3),
        "game_theory_interpretation": interpretation_text(scheduler),
    }
    if base_jobs is not None:
        metrics["counterfactual"] = counterfactual_manipulation(base_jobs, scheduler, num_gpus)
        metrics["interpretation"] = interpret_scheduler(metrics)
    return metrics


def interpretation_text(scheduler: str) -> str:
    return {
        "fifo": "Baseline with limited strategic priority. Fair by arrival order but may ignore urgency.",
        "priority": "Manipulable mechanism: exaggerating urgency can become a rational best response.",
        "auction": "Auction-style allocation: bids influence priority, connecting scheduling to mechanism design.",
        "incentive": "Incentive-aware allocation: exaggeration is penalized to reduce manipulation advantage.",
        "ml_incentive": "ML-assisted mechanism: predicted manipulation risk changes allocation score.",
    }.get(scheduler, "Unknown scheduler")
