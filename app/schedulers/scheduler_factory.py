from app.ml.manipulation_detector import manipulation_probability


def scheduler_score(job: dict, scheduler: str) -> float:
    if scheduler == "fifo":
        return -job["arrival_time"]
    if scheduler == "priority":
        return 10 * job["reported_urgency"] - 0.2 * job["arrival_time"]
    if scheduler == "auction":
        return job["bid"] + 2.0 * job["reported_urgency"] - 0.4 * job["requested_gpus"]
    if scheduler == "incentive":
        gap = max(0, job["reported_urgency"] - job["true_urgency"])
        penalty = 24 * gap + 20 * job.get("past_manipulation_rate", 0) + 10 * (1 - job.get("reputation", 0.8))
        return 10 * job["true_urgency"] + 6 * job.get("reputation", 0.8) - penalty - 0.05 * job["arrival_time"]
    if scheduler == "ml_incentive":
        risk = manipulation_probability(job)
        job["manipulation_probability"] = risk
        gap = max(0, job["reported_urgency"] - job["true_urgency"])
        return 10 * job["true_urgency"] + 5 * job.get("reputation", 0.8) - 45 * risk - 12 * gap
    raise ValueError(f"Unknown scheduler: {scheduler}")


def schedule_jobs(jobs: list, num_gpus: int, scheduler: str) -> list:
    jobs = [dict(j) for j in jobs]
    time = 0.0
    unscheduled = jobs[:]
    running = []
    completed = []

    while unscheduled or running:
        running.sort(key=lambda x: x["finish_time"])
        if running and (not unscheduled or all(j["arrival_time"] > time for j in unscheduled)):
            time = running[0]["finish_time"]

        finished = [j for j in running if j["finish_time"] <= time]
        running = [j for j in running if j["finish_time"] > time]
        completed.extend(finished)

        used_gpus = sum(j["requested_gpus"] for j in running)
        available = num_gpus - used_gpus
        available_jobs = [j for j in unscheduled if j["arrival_time"] <= time and j["requested_gpus"] <= available]

        if not available_jobs:
            next_arrival = min([j["arrival_time"] for j in unscheduled], default=None)
            next_finish = min([j["finish_time"] for j in running], default=None)
            candidates = [t for t in [next_arrival, next_finish] if t is not None and t > time]
            if candidates:
                time = min(candidates)
                continue
            if unscheduled:
                time = min(j["arrival_time"] for j in unscheduled)
                continue
            break

        available_jobs.sort(key=lambda j: scheduler_score(j, scheduler), reverse=True)
        scheduled_any = False
        for job in available_jobs:
            if job in unscheduled and job["requested_gpus"] <= available:
                job["start_time"] = time
                job["finish_time"] = time + job["duration"]
                job["waiting_time"] = job["start_time"] - job["arrival_time"]
                running.append(job)
                unscheduled.remove(job)
                available -= job["requested_gpus"]
                scheduled_any = True
        if not scheduled_any:
            time += 1

    completed.extend(running)
    completed.sort(key=lambda x: x["job_id"])
    return completed
