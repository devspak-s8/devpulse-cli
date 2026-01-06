import pytest
from typer.testing import CliRunner
from devpulse.commands import habits

runner = CliRunner()


def test_habits_create():
    result = runner.invoke(habits.app, ["create", "meditate"])
    assert result.exit_code == 0
    assert "meditate" in result.stdout


def test_habits_create_weekly():
    result = runner.invoke(habits.app, ["create", "exercise", "--frequency", "weekly"])
    assert result.exit_code == 0
    assert "weekly" in result.stdout


def test_habits_list():
    result = runner.invoke(habits.app, ["list"])
    assert result.exit_code == 0
    assert "Habits" in result.stdout


def test_habits_log():
    result = runner.invoke(habits.app, ["log", "meditate"])
    assert result.exit_code == 0
    assert "Logged" in result.stdout


def test_habits_streak():
    result = runner.invoke(habits.app, ["streak", "meditate"])
    assert result.exit_code == 0
    assert "Streak" in result.stdout


def test_habits_progress():
    result = runner.invoke(habits.app, ["progress", "meditate"])
    assert result.exit_code == 0
    assert "Progress" in result.stdout


def test_habits_delete_with_force():
    result = runner.invoke(habits.app, ["delete", "meditate", "--force"])
    assert result.exit_code == 0
    assert "Deleted" in result.stdout


def test_habits_stats():
    result = runner.invoke(habits.app, ["stats"])
    assert result.exit_code == 0
    assert "Statistics" in result.stdout
