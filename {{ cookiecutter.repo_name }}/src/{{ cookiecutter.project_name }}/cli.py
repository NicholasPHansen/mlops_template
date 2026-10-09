import subprocess
import sys

from pathlib import Path
from typing import Annotated

import typer

from {{ cookiecutter.project_name }}.config import (
    DATASET_PATH,
    FEATURES_PATH,
    LABELS_PATH,
    MODEL_PATH,
    PLOT_PATH,
    PREDICTIONS_PATH,
    PROCESSED_DATA_DIR,
    RAW_DATA_DIR,
    TEST_FEATURES_PATH,
)
from {{ cookiecutter.project_name }}.data import preprocess_data
from {{ cookiecutter.project_name }}.train import train_model
from {{ cookiecutter.project_name }}.visualize import make_plots
from {{ cookiecutter.project_name }}.evaluate import evaluate_model
from {{ cookiecutter.project_name }}.pipeline import run_stages, stage_names

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
    features_path: Path = FEATURES_PATH,
    labels_path: Path = LABELS_PATH,
    model_path: Path = MODEL_PATH,
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
    features_path: Path = TEST_FEATURES_PATH,
    model_path: Path = MODEL_PATH,
    predictions_path: Path = PREDICTIONS_PATH,
) -> None:
    """Evaluate model."""
    evaluate_model(features_path, model_path, predictions_path)


@cli.command()
def plots(
    input_path: Path = DATASET_PATH,
    output_path: Path = PLOT_PATH,
):
    """Generate plots."""
    make_plots(input_path, output_path)


@cli.command()
def run_pipeline(
    from_stage: Annotated[
        str, typer.Option("--from", help=f"First stage to run. One of: {', '.join(stage_names())}.")
    ] = stage_names()[0],
    to_stage: Annotated[
        str, typer.Option("--to", help=f"Last stage to run. One of: {', '.join(stage_names())}.")
    ] = stage_names()[-1],
) -> None:
    """Run the pipeline stages in order (data -> train -> eval -> plots), without caching."""
    try:
        run_stages(from_stage, to_stage)
    except ValueError as error:
        raise typer.BadParameter(str(error)) from error


if __name__ == "__main__":
    cli()
