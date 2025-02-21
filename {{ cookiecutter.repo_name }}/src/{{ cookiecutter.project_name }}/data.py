from pathlib import Path

import typer
from loguru import logger
from tqdm import tqdm
from torch.utils.data import Dataset

from {{ cookiecutter.project_name }}.config import PROCESSED_DATA_DIR, RAW_DATA_DIR

app = typer.Typer()

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



@app.command()
def main(
    # ---- REPLACE DEFAULT PATHS AS APPROPRIATE ----
    input_path: Path = RAW_DATA_DIR / "dataset.csv",
    output_path: Path = PROCESSED_DATA_DIR / "dataset.csv",
    # ----------------------------------------------
):
    logger.info("Processing dataset...")
    dataset = MyDataset(input_path)
    dataset.preprocess(output_path)
    logger.success("Processing dataset complete.")
    

if __name__ == "__main__":
    app()