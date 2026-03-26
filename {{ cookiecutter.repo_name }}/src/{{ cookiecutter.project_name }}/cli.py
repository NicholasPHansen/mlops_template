import subprocess
import sys

from pathlib import Path
import typer

from {{ cookiecutter.project_name }}.config import PROCESSED_DATA_DIR, RAW_DATA_DIR, MODELS_DIR, FIGURES_DIR
from {{ cookiecutter.project_name }}.data import preprocess_data
from {{ cookiecutter.project_name }}.train import train_model
from {{ cookiecutter.project_name }}.visualize import make_plots
from {{ cookiecutter.project_name }}.evaluate import evaluate_model

cli = typer.Typer(pretty_exceptions_show_locals=False)


def run_command(command: str) -> tuple[int, str]:
    outputs = []
    with subprocess.Popen(
        command,
        shell=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        bufsize=1,
        universal_newlines=True,
    ) as process:
        for line in process.stdout:
            typer.echo(line, nl=False)
            outputs.append(line)
        returncode = process.wait()
    output = "".join(outputs)
    return returncode, output


# Project commands
@cli.command()
def data(
    input_path: Path = RAW_DATA_DIR,
    output_path: Path = PROCESSED_DATA_DIR,
) -> None:
    """Preprocess data."""
    preprocess_data(input_path, output_path)


@cli.command()
def train(
    features_path: Path = PROCESSED_DATA_DIR / "features.csv",
    labels_path: Path = PROCESSED_DATA_DIR / "labels.csv",
    model_path: Path = MODELS_DIR / "model.pkl",
) -> None:
    """Train model."""
    train_model(features_path, labels_path, model_path)


@cli.command()
def test() -> None:
    """Run tests."""
    cmd = " ".join(["pytest", "tests/"])
    returncode, _ = run_command(cmd)
    sys.exit(returncode)


@cli.command()
def format() -> None:
    """Format code."""
    cmd = " ".join(["ruff", "format", "-v", "src/{{ cookiecutter.project_name }}"])
    returncode, _ = run_command(cmd)
    sys.exit(returncode)


@cli.command()
def eval(
    features_path: Path = PROCESSED_DATA_DIR / "test_features.csv",
    model_path: Path = MODELS_DIR / "model.pkl",
    predictions_path: Path = PROCESSED_DATA_DIR / "test_predictions.csv",
) -> None:
    """Evaluate model."""
    evaluate_model(features_path, model_path, predictions_path)


@cli.command()
def plots(
    input_path: Path = PROCESSED_DATA_DIR / "dataset.csv",
    output_path: Path = FIGURES_DIR / "plot.png",
):
    """Generate plots."""
    make_plots(input_path, output_path)


if __name__ == "__main__":
    cli()
