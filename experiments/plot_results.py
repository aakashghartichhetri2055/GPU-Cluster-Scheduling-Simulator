from pathlib import Path
import matplotlib.pyplot as plt


def plot_scheduler_comparison(results, out_dir="results"):
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    schedulers = list(results.keys())
    manipulation = [results[s]["counterfactual"]["avg_manipulation_advantage"] for s in schedulers]
    success = [results[s]["counterfactual"]["manipulation_success_rate"] for s in schedulers]
    punished = [results[s]["counterfactual"]["lying_punished_rate"] for s in schedulers]
    fairness = [results[s]["fairness_jain_waiting"] for s in schedulers]
    wait = [results[s]["avg_waiting_time"] for s in schedulers]

    plt.figure(figsize=(9, 5))
    plt.bar(schedulers, manipulation)
    plt.title("Manipulation Advantage by Scheduler")
    plt.ylabel("Waiting-time advantage from lying")
    plt.xticks(rotation=25)
    plt.tight_layout()
    plt.savefig(f"{out_dir}/manipulation_advantage.png")
    plt.close()

    plt.figure(figsize=(9, 5))
    plt.bar(schedulers, fairness)
    plt.title("Fairness by Scheduler")
    plt.ylabel("Jain Fairness Index on Waiting Time")
    plt.xticks(rotation=25)
    plt.tight_layout()
    plt.savefig(f"{out_dir}/fairness.png")
    plt.close()

    plt.figure(figsize=(9, 5))
    plt.bar(schedulers, wait)
    plt.title("Average Waiting Time by Scheduler")
    plt.ylabel("Average waiting time")
    plt.xticks(rotation=25)
    plt.tight_layout()
    plt.savefig(f"{out_dir}/avg_waiting_time.png")
    plt.close()

    plt.figure(figsize=(9, 5))
    x = range(len(schedulers))
    width = 0.35
    plt.bar([i - width / 2 for i in x], success, width=width, label="Success")
    plt.bar([i + width / 2 for i in x], punished, width=width, label="Punished")
    plt.title("Lying Success vs Punishment Rate")
    plt.ylabel("Rate")
    plt.xticks(list(x), schedulers, rotation=25)
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"{out_dir}/lying_success_vs_punishment.png")
    plt.close()


def plot_greedy_sweep(rows, out_dir="results"):
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    schedulers = sorted(set(r["scheduler"] for r in rows))
    for metric, title, filename in [
        ("avg_manipulation_advantage", "Greedy Sweep: Manipulation Advantage", "greedy_sweep_manipulation.png"),
        ("manipulation_success_rate", "Greedy Sweep: Lying Success Rate", "greedy_sweep_success.png"),
        ("fairness_jain_waiting", "Greedy Sweep: Fairness", "greedy_sweep_fairness.png"),
    ]:
        plt.figure(figsize=(9, 5))
        for s in schedulers:
            data = sorted([r for r in rows if r["scheduler"] == s], key=lambda x: x["greedy_level"])
            plt.plot([r["greedy_level"] for r in data], [r[metric] for r in data], marker="o", label=s)
        plt.title(title)
        plt.xlabel("Share of greedy users")
        plt.ylabel(metric)
        plt.legend()
        plt.tight_layout()
        plt.savefig(f"{out_dir}/{filename}")
        plt.close()
