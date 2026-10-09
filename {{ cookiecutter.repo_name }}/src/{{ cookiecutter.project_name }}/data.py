from pathlib import Path

from loguru import logger
from tqdm import tqdm
from torch.utils.data import Dataset

from {{ cookiecutter.project_name }}.config import (
    DATASET_PATH,
    FEATURES_PATH,
    LABELS_PATH,
    PROCESSED_DATA_DIR,
    RAW_DATA_DIR,
    TEST_FEATURES_PATH,
)

class MyDataset(Dataset):
    """My custom dataset."""

    def __init__(self, data_path: Path) -> None:
        self.data_path = data_path

    def __len__(self) -> int:
        """Return the length of the dataset."""
        pass

    def __getitem__(self, index: int):
        """Return a given sample from the dataset."""
        pass

    def preprocess(self, output_path: Path) -> None:
        """Preprocess the raw data and save it to the output folder."""
        pass


def preprocess_data(
    # ---- REPLACE DEFAULT PATHS AS APPROPRIATE ----
    input_path: Path = RAW_DATA_DIR,
    output_path: Path = PROCESSED_DATA_DIR,
    # ----------------------------------------------
):
    logger.info("Processing dataset...")
    dataset = MyDataset(input_path)
    dataset.preprocess(output_path)
    # ---- REPLACE: placeholder artefacts so the pipeline runs end to end out of the box ----
    output_path.mkdir(parents=True, exist_ok=True)
    for artefact in (FEATURES_PATH, LABELS_PATH, TEST_FEATURES_PATH, DATASET_PATH):
        (output_path / artefact.name).touch()
    # ---------------------------------------------------------------------------------------
    logger.success("Processing dataset complete.")
