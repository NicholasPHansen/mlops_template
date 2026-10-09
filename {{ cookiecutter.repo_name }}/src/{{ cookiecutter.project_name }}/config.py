from pathlib import Path

from dotenv import load_dotenv
from loguru import logger

# Load environment variables from .env file if it exists
load_dotenv()

# Paths
PROJ_ROOT = Path(__file__).resolve().parents[2]
logger.info(f"PROJ_ROOT path is: {PROJ_ROOT}")

DATA_DIR = PROJ_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

MODELS_DIR = PROJ_ROOT / "models"

REPORTS_DIR = PROJ_ROOT / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"

# Pipeline artefacts. Every stage default, the CLI and the stage registry in
# `pipeline.py` read these, so renaming a file is a one-line change.
FEATURES_PATH = PROCESSED_DATA_DIR / "features.csv"
LABELS_PATH = PROCESSED_DATA_DIR / "labels.csv"
TEST_FEATURES_PATH = PROCESSED_DATA_DIR / "test_features.csv"
DATASET_PATH = PROCESSED_DATA_DIR / "dataset.csv"
PREDICTIONS_PATH = PROCESSED_DATA_DIR / "test_predictions.csv"
MODEL_PATH = MODELS_DIR / "model.pkl"
PLOT_PATH = FIGURES_DIR / "plot.png"
{% if cookiecutter.use_dvc == 'yes' %}
PARAMS_FILE = PROJ_ROOT / "params.yaml"


def load_params(section: str) -> dict:
    """Load one top-level section of params.yaml (the file DVC tracks as stage parameters)."""
    import yaml

    with open(PARAMS_FILE) as f:
        return yaml.safe_load(f)[section]
{% endif %}
# If tqdm is installed, configure loguru with tqdm.write
# https://github.com/Delgan/loguru/issues/135
try:
    from tqdm import tqdm

    logger.remove(0)
    logger.add(lambda msg: tqdm.write(msg, end=""), colorize=True)
except ModuleNotFoundError:
    pass

