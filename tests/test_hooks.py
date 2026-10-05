from pathlib import Path

import pytest
from cookiecutter.exceptions import FailedHookException
from cookiecutter.main import cookiecutter


def test_wrong_config1(tmpdir):
    """Test that numbers are not allowed in the project name."""
    with pytest.raises(FailedHookException):
        cookiecutter(
            template=".",
            config_file="tests/wrong_config1.yaml",
            overwrite_if_exists=True,
            no_input=True,
            output_dir=str(tmpdir),
        )


def test_wrong_config2(tmpdir):
    """Test that numbers are not allowed in the project name."""
    with pytest.raises(FailedHookException):
        cookiecutter(
            template=".",
            config_file="tests/wrong_config2.yaml",
            overwrite_if_exists=True,
            no_input=True,
            output_dir=str(tmpdir),
        )


def test_wrong_config3(tmpdir):
    """Test that numbers are not allowed in the project name."""
    with pytest.raises(FailedHookException):
        cookiecutter(
            template=".",
            config_file="tests/wrong_config3.yaml",
            overwrite_if_exists=True,
            no_input=True,
            output_dir=str(tmpdir),
        )

def test_wrong_config4(tmpdir):
    with pytest.raises(FailedHookException):
        cookiecutter(
            template=".",
            config_file="tests/wrong_config4.yaml",
            overwrite_if_exists=True,
            no_input=True,
            output_dir=str(tmpdir),
        )


def _generate(tmpdir, use_dvc: str):
    cookiecutter(
        template=".",
        no_input=True,
        overwrite_if_exists=True,
        output_dir=str(tmpdir),
        extra_context={"use_dvc": use_dvc},
    )
    return Path(str(tmpdir)) / "repo_name"


def test_dvc_disabled_by_default_leaves_no_dvc_files(tmpdir):
    project = _generate(tmpdir, "no")
    for name in ("dvc.yaml", "params.yaml", ".dvc", ".dvcignore", "tests/test_dvc.py"):
        assert not (project / name).exists(), name
    assert "dvc" not in (project / "pyproject.toml").read_text()
    assert "\ndata/\n" in (project / ".gitignore").read_text()
    assert "load_params" not in (project / "src/project_name/config.py").read_text()


def test_dvc_enabled_adds_dvc_files_and_stops_ignoring_data(tmpdir):
    project = _generate(tmpdir, "yes")
    for name in ("dvc.yaml", "params.yaml", ".dvc/config", ".dvcignore", "tests/test_dvc.py"):
        assert (project / name).exists(), name
    assert '"dvc>=3.50,<4"' in (project / "pyproject.toml").read_text()
    assert "\ndata/\n" not in (project / ".gitignore").read_text()
    assert 'load_params("train")' in (project / "src/project_name/train.py").read_text()


@pytest.mark.parametrize("use_dvc", ["no", "yes"])
def test_generated_python_and_yaml_are_valid(tmpdir, use_dvc):
    import ast
    import tomllib

    import yaml

    project = _generate(tmpdir, use_dvc)
    for source in (project / "src/project_name").glob("*.py"):
        ast.parse(source.read_text())
    tomllib.loads((project / "pyproject.toml").read_text())
    if use_dvc == "yes":
        yaml.safe_load((project / "dvc.yaml").read_text())
        yaml.safe_load((project / "params.yaml").read_text())
