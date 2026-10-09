"""Guard against dvc.yaml drifting from the stage registry in pipeline.py (this file exists only with DVC enabled)."""

import yaml

from {{ cookiecutter.project_name }}.config import PROJ_ROOT
from {{ cookiecutter.project_name }}.pipeline import STAGES

DVC_STAGES = yaml.safe_load((PROJ_ROOT / "dvc.yaml").read_text())["stages"]


def test_dvc_stage_names_and_order_match_registry():
    assert list(DVC_STAGES) == [stage.name for stage in STAGES]


def test_dvc_commands_call_the_matching_cli_command():
    for stage in STAGES:
        assert DVC_STAGES[stage.name]["cmd"] == f"uv run cli {stage.name}"


def test_dvc_outputs_match_registry():
    for stage in STAGES:
        declared = {path.relative_to(PROJ_ROOT).as_posix() for path in stage.outs}
        assert set(DVC_STAGES[stage.name]["outs"]) == declared, stage.name


def test_dvc_param_sections_exist_in_params_yaml():
    params = yaml.safe_load((PROJ_ROOT / "params.yaml").read_text())
    for name, stage in DVC_STAGES.items():
        for section in stage.get("params", []):
            assert section in params, f"stage '{name}' references missing params section '{section}'"
