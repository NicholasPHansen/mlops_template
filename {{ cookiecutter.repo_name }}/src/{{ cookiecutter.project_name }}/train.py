from pathlib import Path

import torch
from loguru import logger
from tqdm import tqdm

from {{ cookiecutter.project_name }}.config import FEATURES_PATH, LABELS_PATH, MODEL_PATH{% if cookiecutter.use_dvc == 'yes' %}, load_params{% endif %}
from {{ cookiecutter.project_name }}.data import MyDataset
from {{ cookiecutter.project_name }}.model import Model


def train_model(
    # ---- REPLACE DEFAULT PATHS AS APPROPRIATE ----
    features_path: Path = FEATURES_PATH,
    labels_path: Path = LABELS_PATH,
    model_path: Path = MODEL_PATH,
    # -----------------------------------------
):
    # ---- REPLACE THIS WITH YOUR OWN CODE ----
    logger.info("Training some model...")
    {% if cookiecutter.use_dvc == 'yes' %}epochs = load_params("train")["epochs"]  # from params.yaml, tracked by DVC{% else %}epochs = 10{% endif %}
    model = Model()
    for i in tqdm(range(epochs), total=epochs):
        if i == 5:
            logger.info("Something happened for iteration 5.")
    model_path.parent.mkdir(parents=True, exist_ok=True)
    torch.save(model.state_dict(), model_path)
    logger.success("Modeling training complete.")
    # -----------------------------------------
