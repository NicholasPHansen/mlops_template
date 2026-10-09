from pathlib import Path

from loguru import logger
from tqdm import tqdm

from {{ cookiecutter.project_name }}.config import MODEL_PATH, PREDICTIONS_PATH, TEST_FEATURES_PATH


def evaluate_model(
    # ---- REPLACE DEFAULT PATHS AS APPROPRIATE ----
    features_path: Path = TEST_FEATURES_PATH,
    model_path: Path = MODEL_PATH,
    predictions_path: Path = PREDICTIONS_PATH,
    # -----------------------------------------
):
    # ---- REPLACE THIS WITH YOUR OWN CODE ----
    logger.info("Performing inference for model...")
    for i in tqdm(range(10), total=10):
        if i == 5:
            logger.info("Something happened for iteration 5.")
    predictions_path.parent.mkdir(parents=True, exist_ok=True)
    predictions_path.touch()  # placeholder artefact
    logger.success("Inference complete.")
    # -----------------------------------------
