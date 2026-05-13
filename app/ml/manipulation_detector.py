def manipulation_probability(job: dict) -> float:
    gap = max(0, job["reported_urgency"] - job["true_urgency"])
    reputation_risk = max(0, 0.8 - job.get("reputation", 0.8))
    past_risk = job.get("past_manipulation_rate", 0)
    score = 0.11 * gap + 0.5 * reputation_risk + 0.45 * past_risk
    return round(max(0.0, min(1.0, score)), 3)
