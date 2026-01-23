from pathlib import Path

from loguru import logger
from tqdm import tqdm

from {{ cookiecutter.project_name }}.config import MODELS_DIR, PROCESSED_DATA_DIR
from {{ cookiecutter.project_name }}.data import MyDataset
from {{ cookiecutter.project_name }}.model import Model


def train_model(
    # ---- REPLACE DEFAULT PATHS AS APPROPRIATE ----
    features_path: Path = PROCESSED_DATA_DIR / "features.csv",
    labels_path: Path = PROCESSED_DATA_DIR / "labels.csv",
    model_path: Path = MODELS_DIR / "model.pkl",
    # -----------------------------------------
):
    # ---- REPLACE THIS WITH YOUR OWN CODE ----
    logger.info("Training some model...")
    for i in tqdm(range(10), total=10):
        if i == 5:
            logger.info("Something happened for iteration 5.")
    logger.success("Modeling training complete.")
    # -----------------------------------------
