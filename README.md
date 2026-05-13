# Game-Theoretic GPU Cluster Scheduling Simulator
A research-level FastAPI simulation project for studying strategic behavior in shared GPU clusters.

## Research Question
How does strategic urgency inflation affect fairness and efficiency in shared GPU clusters, and can incentive-aware mechanisms reduce manipulation?

## Core Game-Theory Model
- **Players:** users submitting GPU jobs
- **Private information:** true urgency
- **Strategy:** report true urgency or exaggerate urgency
- **Payoff:** earlier scheduling benefit minus waiting cost and manipulation penalty
- **Concepts:** Nash equilibrium, dominant strategy, mechanism design, Bayesian games, repeated games, counterfactual analysis

## Project Structure
```text
gpu_game_simulator_final_rebuilt/
├── app/
│   ├── main.py
│   ├── agents/
│   ├── schedulers/
│   ├── metrics/
│   ├── ml/
│   ├── routes/
│   ├── utils/
│   ├── schemas.py
│   └── simulation.py
├── experiments/
│   ├── run_experiments.py
│   ├── plot_results.py
│   └── export_results.py
├── results/
├── tests/
├── requirements.txt
├── pytest.ini
└── README.md
```

## Important Setup Note
Use Python 3.12 or 3.13. Avoid Python 3.14 because some dependency wheels may fail to build.

```bash
python3.12 -m venv venv
source venv/bin/activate
python --version
pip install --upgrade pip
pip install -r requirements.txt
```

If `python3.12` is missing on macOS:

```bash
brew install python@3.12
/opt/homebrew/bin/python3.12 -m venv venv
```

For Intel Mac, try:

```bash
/usr/local/bin/python3.12 -m venv venv
```

## Run API
```bash
uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

## Test
```bash
pytest
```

## Run Proof-of-Work Experiments
```bash
python3 -m experiments.run_experiments
```

Outputs are saved to:

```text
results/
```

Generated files:

- `results.json`
- `manipulation_advantage.png`
- `fairness.png`
- `avg_waiting_time.png`
- `lying_success_vs_punishment.png`
- `greedy_sweep_manipulation.png`
- `greedy_sweep_success.png`
- `greedy_sweep_fairness.png`

## API Commands

### Compare schedulers
```bash
curl -X POST "http://127.0.0.1:8000/compare" \
-H "Content-Type: application/json" \
-d '{
  "num_users": 80,
  "num_gpus": 8,
  "agent_mix": {"truthful": 0.5, "greedy": 0.3, "random": 0.1, "learning": 0.1},
  "seed": 42
}'
```

### Greedy sweep
```bash
curl -X POST "http://127.0.0.1:8000/experiments/greedy-sweep" \
-H "Content-Type: application/json" \
-d '{
  "num_users": 80,
  "num_gpus": 8,
  "seed": 42,
  "greedy_levels": [0, 0.25, 0.5, 0.75, 1],
  "schedulers": ["priority", "incentive", "ml_incentive"]
}'
```

### ML training
```bash
curl http://127.0.0.1:8000/ml/train
```

### Report
```bash
curl http://127.0.0.1:8000/report
```

## Main Presentation Claim
Naive priority scheduling creates a strategic environment where exaggerating urgency can become a rational best response. Incentive-aware and ML-assisted mechanisms change the payoff structure so manipulation is punished rather than rewarded.
