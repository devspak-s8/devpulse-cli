import pytest
from typer.testing import CliRunner
from devpulse.commands import breaks

runner = CliRunner()


def test_breaks_schedule():
    result = runner.invoke(breaks.app, ["schedule"])
    assert result.exit_code == 0
    assert "scheduled" in result.stdout


def test_breaks_schedule_custom():
    result = runner.invoke(breaks.app, ["schedule", "--interval", "45", "--duration", "10"])
    assert result.exit_code == 0
    assert "45" in result.stdout


def test_breaks_take():
    result = runner.invoke(breaks.app, ["take"])
    assert result.exit_code == 0
    assert "Break started" in result.stdout


def test_breaks_skip():
    result = runner.invoke(breaks.app, ["skip"])
    assert result.exit_code == 0
    assert "skipped" in result.stdout


def test_breaks_status():
    result = runner.invoke(breaks.app, ["status"])
    assert result.exit_code == 0
    assert "Break Schedule" in result.stdout


def test_breaks_history():
    result = runner.invoke(breaks.app, ["history"])
    assert result.exit_code == 0
    assert "breaks" in result.stdout


def test_breaks_reminders():
    result = runner.invoke(breaks.app, ["reminders"])
    assert result.exit_code == 0
    assert "Reminders" in result.stdout


def test_breaks_suggestions():
    result = runner.invoke(breaks.app, ["suggestions"])
    assert result.exit_code == 0
    assert "Suggestions" in result.stdout
