import pytest
from typer.testing import CliRunner

from {{ cookiecutter.project_name }} import pipeline
from {{ cookiecutter.project_name }}.cli import cli
from {{ cookiecutter.project_name }}.pipeline import Stage


@pytest.fixture
def calls(monkeypatch, tmp_path):
    """Replace the real stages with recorders that write their declared output."""
    recorded: list[str] = []

    def make(name: str, produce: bool = True) -> Stage:
        out = tmp_path / f"{name}.out"

        def run() -> None:
            recorded.append(name)
            if produce:
                out.touch()

        return Stage(name=name, run=run, outs=(out,))

    monkeypatch.setattr(pipeline, "STAGES", (make("a"), make("b"), make("c")))
    return recorded


def test_real_stage_order():
    assert pipeline.stage_names() == ["data", "train", "eval", "plots"]


def test_runs_all_stages_in_order(calls):
    pipeline.run_stages()
    assert calls == ["a", "b", "c"]


def test_from_and_to_select_inclusive_slice(calls):
    pipeline.run_stages(from_stage="b", to_stage="c")
    assert calls == ["b", "c"]


def test_unknown_stage_is_rejected(calls):
    with pytest.raises(ValueError, match="Unknown stage 'nope'"):
        pipeline.run_stages(from_stage="nope")
    assert calls == []


def test_reversed_range_is_rejected(calls):
    with pytest.raises(ValueError, match="runs after"):
        pipeline.run_stages(from_stage="c", to_stage="a")
    assert calls == []


def test_missing_output_fails_fast(monkeypatch, tmp_path):
    ran: list[str] = []
    bad = Stage("bad", lambda: ran.append("bad"), (tmp_path / "never_written",))
    after = Stage("after", lambda: ran.append("after"), ())
    monkeypatch.setattr(pipeline, "STAGES", (bad, after))
    with pytest.raises(RuntimeError, match="did not produce"):
        pipeline.run_stages()
    assert ran == ["bad"]


def test_cli_rejects_unknown_stage():
    result = CliRunner().invoke(cli, ["run-pipeline", "--from", "nope"])
    assert result.exit_code == 2
