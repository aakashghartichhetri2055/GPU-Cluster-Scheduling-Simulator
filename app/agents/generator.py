import random


def normalize_mix(agent_mix):
    total = sum(agent_mix.values()) or 1.0
    return {k: v / total for k, v in agent_mix.items()}


def pick_agent(agent_mix):
    mix = normalize_mix(agent_mix)
    r = random.random()
    cumulative = 0
    for agent, prob in mix.items():
        cumulative += prob
        if r <= cumulative:
            return agent
    return list(mix.keys())[-1]


def reported_urgency(agent_type: str, true_urgency: int) -> int:
    if agent_type == "truthful":
        return true_urgency
    if agent_type == "greedy":
        return min(10, true_urgency + random.randint(2, 5))
    if agent_type == "random":
        return random.randint(1, 10)
    if agent_type == "learning":
        return min(10, true_urgency + random.choice([0, 0, 1, 2]))
    return true_urgency


def generate_jobs(num_users: int, agent_mix: dict, seed: int = 42):
    random.seed(seed)
    jobs = []
    for i in range(num_users):
        agent_type = pick_agent(agent_mix)
        true_u = random.randint(1, 10)
        reported_u = reported_urgency(agent_type, true_u)
        requested_gpus = random.choice([1, 1, 1, 2, 2, 4])
        duration = float(random.randint(3, 24))
        arrival = float(random.randint(0, 5))
        reputation = random.uniform(0.35, 0.72) if agent_type == "greedy" else random.uniform(0.75, 0.98)
        if agent_type in ["random", "learning"]:
            reputation = random.uniform(0.45, 0.85)
        past_rate = random.uniform(0.45, 0.85) if agent_type == "greedy" else random.uniform(0.0, 0.2)
        if agent_type in ["random", "learning"]:
            past_rate = random.uniform(0.1, 0.55)
        bid = round((reported_u * requested_gpus) * random.uniform(0.75, 1.35), 2)
        jobs.append({
            "job_id": i,
            "user_id": i,
            "agent_type": agent_type,
            "arrival_time": arrival,
            "duration": duration,
            "requested_gpus": requested_gpus,
            "true_urgency": true_u,
            "reported_urgency": reported_u,
            "bid": bid,
            "reputation": reputation,
            "past_manipulation_rate": past_rate,
            "manipulation_probability": 0.0,
            "start_time": None,
            "finish_time": None,
            "waiting_time": None,
        })
    return jobs
