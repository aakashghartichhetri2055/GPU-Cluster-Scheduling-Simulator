from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root():
    res = client.get("/")
    assert res.status_code == 200
    assert "important_endpoints" in res.json()


def test_compare_contains_counterfactual():
    res = client.post("/compare", json={
        "num_users": 30,
        "num_gpus": 4,
        "agent_mix": {"truthful": 0.5, "greedy": 0.5},
        "seed": 42,
    })
    assert res.status_code == 200
    data = res.json()
    assert "priority" in data["results"]
    assert "counterfactual" in data["results"]["priority"]


def test_ml_train():
    res = client.get("/ml/train")
    assert res.status_code == 200
    assert "accuracy" in res.json()
