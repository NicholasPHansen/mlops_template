"""Stage registry and runner for the project pipeline.

``STAGES`` is the single source of truth for what the pipeline does and in which order.
``cli run-pipeline`` executes it directly (no caching). {% if cookiecutter.use_dvc == 'yes' %}``dvc.yaml`` declares the same stages
for cached execution via ``dvc repro``; ``tests/test_dvc.py`` fails if the two drift apart.{% else %}Each stage declares the
files it must produce, so a stage that silently writes nothing fails fast.{% endif %}
"""

from __future__ import annotations

import time
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path

from loguru import logger

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
from {{ cookiecutter.project_name }}.evaluate import evaluate_model
from {{ cookiecutter.project_name }}.train import train_model
from {{ cookiecutter.project_name }}.visualize import make_plots


@dataclass(frozen=True)
class Stage:
    """One pipeline step.

    Attributes:
        name: Stage name, also the name of the matching CLI command.
        run: Zero-argument callable that executes the stage with project-default paths.
        outs: Files the stage must produce; checked after the stage runs.
    """

    name: str
    run: Callable[[], None]
    outs: tuple[Path, ...]


# ---- REPLACE / EXTEND AS APPROPRIATE: keep outs in sync with what each stage really writes ----
STAGES: tuple[Stage, ...] = (
    Stage(
        name="data",
        run=lambda: preprocess_data(RAW_DATA_DIR, PROCESSED_DATA_DIR),
        outs=(FEATURES_PATH, LABELS_PATH, TEST_FEATURES_PATH, DATASET_PATH),
    ),
    Stage(
        name="train",
        run=lambda: train_model(FEATURES_PATH, LABELS_PATH, MODEL_PATH),
        outs=(MODEL_PATH,),
    ),
    Stage(
        name="eval",
        run=lambda: evaluate_model(TEST_FEATURES_PATH, MODEL_PATH, PREDICTIONS_PATH),
        outs=(PREDICTIONS_PATH,),
    ),
    Stage(
        name="plots",
        run=lambda: make_plots(DATASET_PATH, PLOT_PATH),
        outs=(PLOT_PATH,),
    ),
)
# -----------------------------------------------------------------------------------------------


def stage_names() -> list[str]:
    """Return stage names in execution order."""
    return [stage.name for stage in STAGES]


def select_stages(from_stage: str | None = None, to_stage: str | None = None) -> list[Stage]:
    """Return the contiguous slice of STAGES from ``from_stage`` to ``to_stage`` (both inclusive).

    Raises:
        ValueError: If a stage name is unknown or ``from_stage`` comes after ``to_stage``.
    """
    names = stage_names()
    for given in (from_stage, to_stage):
        if given is not None and given not in names:
            raise ValueError(f"Unknown stage '{given}'. Valid stages, in order: {', '.join(names)}")
    start = names.index(from_stage) if from_stage else 0
    end = names.index(to_stage) if to_stage else len(names) - 1
    if start > end:
        raise ValueError(f"'{from_stage}' runs after '{to_stage}'. Stage order: {', '.join(names)}")
    return list(STAGES[start : end + 1])


def run_stages(from_stage: str | None = None, to_stage: str | None = None) -> None:
    """Run the selected stages in order, stopping at the first failure.

    Every stage reruns; there is no caching here.{% if cookiecutter.use_dvc == 'yes' %} Use ``dvc repro`` to skip unchanged stages.{% endif %}
    After each stage, its declared ``outs`` must exist, otherwise a RuntimeError is raised.
    """
    selected = select_stages(from_stage, to_stage)
    for position, stage in enumerate(selected, start=1):
        logger.info(f"Stage {position}/{len(selected)}: {stage.name}")
        started = time.perf_counter()
        stage.run()
        missing = [path for path in stage.outs if not path.exists()]
        if missing:
            raise RuntimeError(
                f"Stage '{stage.name}' finished but did not produce: {', '.join(str(p) for p in missing)}. "
                "Fix the stage, or update its `outs` in pipeline.py if the output moved."
            )
        logger.success(f"Stage '{stage.name}' done in {time.perf_counter() - started:.1f}s")
