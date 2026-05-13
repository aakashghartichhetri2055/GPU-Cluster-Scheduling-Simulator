from app.schedulers.scheduler_factory import schedule_jobs


def counterfactual_manipulation(base_jobs: list, scheduler: str, num_gpus: int) -> dict:
    manipulated = [j for j in base_jobs if j["reported_urgency"] > j["true_urgency"]]
    if not manipulated:
        return {
            "avg_manipulation_advantage": 0.0,
            "manipulation_success_rate": 0.0,
            "lying_punished_rate": 0.0,
            "num_manipulated_jobs": 0,
            "definition": "positive value means lying reduced waiting time compared with truthful reporting",
            "examples": [],
        }

    actual = schedule_jobs(base_jobs, num_gpus, scheduler)
    truthful_jobs = []
    for j in base_jobs:
        tj = dict(j)
        tj["reported_urgency"] = tj["true_urgency"]
        tj["bid"] = round((tj["true_urgency"] * tj["requested_gpus"]), 2)
        truthful_jobs.append(tj)
    truthful = schedule_jobs(truthful_jobs, num_gpus, scheduler)

    actual_by_id = {j["job_id"]: j for j in actual}
    truth_by_id = {j["job_id"]: j for j in truthful}
    advantages, examples = [], []
    for j in manipulated:
        a_wait = actual_by_id[j["job_id"]]["waiting_time"]
        t_wait = truth_by_id[j["job_id"]]["waiting_time"]
        adv = t_wait - a_wait
        advantages.append(adv)
        if len(examples) < 5:
            examples.append({
                "job_id": j["job_id"],
                "agent_type": j["agent_type"],
                "true_urgency": j["true_urgency"],
                "reported_urgency": j["reported_urgency"],
                "actual_waiting_time": round(a_wait, 3),
                "truthful_waiting_time": round(t_wait, 3),
                "manipulation_advantage": round(adv, 3),
            })

    success = len([a for a in advantages if a > 0]) / len(advantages)
    punished = len([a for a in advantages if a < 0]) / len(advantages)
    return {
        "avg_manipulation_advantage": round(sum(advantages) / len(advantages), 3),
        "manipulation_success_rate": round(success, 3),
        "lying_punished_rate": round(punished, 3),
        "num_manipulated_jobs": len(manipulated),
        "definition": "positive value means lying reduced waiting time compared with truthful reporting",
        "examples": examples,
    }
