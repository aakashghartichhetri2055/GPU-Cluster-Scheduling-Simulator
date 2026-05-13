from fastapi import APIRouter
from app.ml.training import train_synthetic_detector

router = APIRouter()

@router.get("/ml/train")
def train_ml():
    return train_synthetic_detector()
