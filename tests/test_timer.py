import pytest
from typer.testing import CliRunner
from devpulse.commands import timer

runner = CliRunner()


def test_timer_start_default():
    result = runner.invoke(timer.app, ["start"])
    assert result.exit_code == 0
    assert "25-minute timer" in result.stdout


def test_timer_start_custom_duration():
    result = runner.invoke(timer.app, ["start", "45"])
    assert result.exit_code == 0
    assert "45-minute timer" in result.stdout


def test_timer_start_with_task():
    result = runner.invoke(timer.app, ["start", "30", "--task", "coding"])
    assert result.exit_code == 0
    assert "coding" in result.stdout


def test_timer_stop():
    result = runner.invoke(timer.app, ["stop"])
    assert result.exit_code == 0
    assert "stopped" in result.stdout


def test_timer_status():
    result = runner.invoke(timer.app, ["status"])
    assert result.exit_code == 0
    assert "Status" in result.stdout


def test_timer_preset_pomodoro():
    result = runner.invoke(timer.app, ["preset", "pomodoro"])
    assert result.exit_code == 0
    assert "25 minutes" in result.stdout


def test_timer_history():
    result = runner.invoke(timer.app, ["history"])
    assert result.exit_code == 0
    assert "sessions" in result.stdout


def test_timer_stats():
    result = runner.invoke(timer.app, ["stats"])
    assert result.exit_code == 0
    assert "Statistics" in result.stdout
