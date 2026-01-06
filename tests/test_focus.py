import pytest
from typer.testing import CliRunner
from devpulse.commands import focus

runner = CliRunner()


def test_focus_start_default():
    result = runner.invoke(focus.app, ["start"])
    assert result.exit_code == 0
    assert "60 minutes" in result.stdout


def test_focus_start_custom_duration():
    result = runner.invoke(focus.app, ["start", "--duration", "90"])
    assert result.exit_code == 0
    assert "90 minutes" in result.stdout


def test_focus_start_with_goal():
    result = runner.invoke(focus.app, ["start", "--goal", "Code review"])
    assert result.exit_code == 0
    assert "Code review" in result.stdout


def test_focus_stop():
    result = runner.invoke(focus.app, ["stop"])
    assert result.exit_code == 0
    assert "stopped" in result.stdout


def test_focus_status():
    result = runner.invoke(focus.app, ["status"])
    assert result.exit_code == 0
    assert "Focus Mode" in result.stdout


def test_focus_block():
    result = runner.invoke(focus.app, ["block", "twitter"])
    assert result.exit_code == 0
    assert "Blocking" in result.stdout


def test_focus_unblock():
    result = runner.invoke(focus.app, ["unblock", "twitter"])
    assert result.exit_code == 0
    assert "Unblocked" in result.stdout


def test_focus_history():
    result = runner.invoke(focus.app, ["history"])
    assert result.exit_code == 0
    assert "sessions" in result.stdout


def test_focus_stats():
    result = runner.invoke(focus.app, ["stats"])
    assert result.exit_code == 0
    assert "Statistics" in result.stdout
