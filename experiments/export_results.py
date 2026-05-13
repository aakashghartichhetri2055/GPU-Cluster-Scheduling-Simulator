import json
from pathlib import Path


def export_results(data, filename="results/results.json"):
    path = Path(filename)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as f:
        json.dump(data, f, indent=4)
    return str(path)
