from pathlib import Path

from loguru import logger
from tqdm import tqdm

from {{ cookiecutter.project_name }}.config import DATASET_PATH, PLOT_PATH


def make_plots(
    # ---- REPLACE DEFAULT PATHS AS APPROPRIATE ----
    input_path: Path = DATASET_PATH,
    output_path: Path = PLOT_PATH,
    # -----------------------------------------
):
    # ---- REPLACE THIS WITH YOUR OWN CODE ----
    logger.info("Generating plot from data...")
    for i in tqdm(range(10), total=10):
        if i == 5:
            logger.info("Something happened for iteration 5.")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.touch()  # placeholder artefact
    logger.success("Plot generation complete.")
    # -----------------------------------------
