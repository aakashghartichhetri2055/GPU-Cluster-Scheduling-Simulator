from app.schemas import CompareRequest, GreedySweepRequest
from app.simulation import compare_schedulers, greedy_sweep
from experiments.export_results import export_results
from experiments.plot_results import plot_scheduler_comparison, plot_greedy_sweep


def main():
    compare_request = CompareRequest(
        num_users=80,
        num_gpus=8,
        agent_mix={"truthful": 0.5, "greedy": 0.3, "random": 0.1, "learning": 0.1},
        seed=42,
    )
    comparison = compare_schedulers(compare_request)

    sweep_request = GreedySweepRequest(
        num_users=80,
        num_gpus=8,
        seed=42,
        greedy_levels=[0, 0.25, 0.5, 0.75, 1.0],
        schedulers=["priority", "incentive", "ml_incentive"],
    )
    sweep = greedy_sweep(sweep_request)

    export_results({"comparison": comparison, "greedy_sweep": sweep}, "results/results.json")
    plot_scheduler_comparison(comparison["results"], "results")
    plot_greedy_sweep(sweep["rows"], "results")

    print("\nSaved proof-of-work outputs to results/")
    print("- results.json")
    print("- manipulation_advantage.png")
    print("- fairness.png")
    print("- avg_waiting_time.png")
    print("- lying_success_vs_punishment.png")
    print("- greedy_sweep_manipulation.png")
    print("- greedy_sweep_success.png")
    print("- greedy_sweep_fairness.png")

    print("\nMAIN PRESENTATION RESULTS")
    for scheduler, metrics in comparison["results"].items():
        c = metrics["counterfactual"]
        print(scheduler, {
            "avg_wait": metrics["avg_waiting_time"],
            "fairness": metrics["fairness_jain_waiting"],
            "manip_adv": c["avg_manipulation_advantage"],
            "success": c["manipulation_success_rate"],
            "punished": c["lying_punished_rate"],
        })


if __name__ == "__main__":
    main()
