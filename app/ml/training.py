import random
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score
from sklearn.model_selection import train_test_split


def train_synthetic_detector(seed: int = 42):
    random.seed(seed)
    rows, y = [], []
    for _ in range(2000):
        true_u = random.randint(1, 10)
        gap = random.choice([0, 0, 0, 1, 2, 3, 4, 5])
        reported = min(10, true_u + gap)
        reputation = random.uniform(0.35, 0.98)
        past_rate = random.uniform(0, 0.9)
        duration = random.randint(3, 24)
        gpus = random.choice([1, 2, 4])
        label = int(gap >= 2 or (gap >= 1 and reputation < 0.55) or past_rate > 0.65)
        rows.append([true_u, reported, gap, reputation, past_rate, duration, gpus])
        y.append(label)
    X = np.array(rows)
    y = np.array(y)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=seed)
    clf = RandomForestClassifier(n_estimators=100, random_state=seed)
    clf.fit(X_train, y_train)
    pred = clf.predict(X_test)
    return {
        "model": "RandomForestClassifier synthetic manipulation detector",
        "features": ["true_urgency", "reported_urgency", "gap", "reputation", "past_rate", "duration", "requested_gpus"],
        "accuracy": round(float(accuracy_score(y_test, pred)), 3),
        "precision": round(float(precision_score(y_test, pred, zero_division=0)), 3),
        "recall": round(float(recall_score(y_test, pred, zero_division=0)), 3),
        "research_note": "Synthetic labels define manipulation as strategic urgency inflation. Replace with real cluster logs in future work.",
    }
