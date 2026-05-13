def interpret_scheduler(metrics: dict) -> dict:
    counter = metrics.get("counterfactual", {})
    adv = counter.get("avg_manipulation_advantage", 0)
    punished = counter.get("lying_punished_rate", 0)

    if adv > 20:
        equilibrium = "Lying is highly profitable; manipulation is a rational best response."
    elif adv > 5:
        equilibrium = "Lying sometimes helps; strategic users may mix between truth and exaggeration."
    else:
        equilibrium = "Lying has low payoff; the mechanism moves behavior closer to truth-telling."

    if punished > 0.7:
        mechanism = "The mechanism frequently punishes exaggeration, reducing manipulation incentives."
    else:
        mechanism = "The mechanism does not strongly punish exaggeration."

    return {
        "equilibrium_claim": equilibrium,
        "mechanism_design_claim": mechanism,
        "course_connection": [
            "Nash Equilibrium",
            "Dominant Strategy",
            "Mechanism Design",
            "Bayesian Games / Private Information",
            "Repeated Games and Punishment",
        ],
    }
