import pytest
from typer.testing import CliRunner
from devpulse.commands import dashboard

runner = CliRunner()


def test_dashboard_show():
    result = runner.invoke(dashboard.app, ["show"])
    assert result.exit_code == 0
    assert "Dashboard" in result.stdout


def test_dashboard_show_week():
    result = runner.invoke(dashboard.app, ["show", "--period", "week"])
    assert result.exit_code == 0
    assert "week" in result.stdout.lower()


def test_dashboard_quick():
    result = runner.invoke(dashboard.app, ["quick"])
    assert result.exit_code == 0
    assert "Summary" in result.stdout


def test_dashboard_goals():
    result = runner.invoke(dashboard.app, ["goals"])
    assert result.exit_code == 0
    assert "Goals" in result.stdout


def test_dashboard_projects():
    result = runner.invoke(dashboard.app, ["projects"])
    assert result.exit_code == 0
    assert "Projects" in result.stdout


def test_dashboard_stats():
    result = runner.invoke(dashboard.app, ["stats"])
    assert result.exit_code == 0
    assert "Statistics" in result.stdout


def test_dashboard_refresh():
    result = runner.invoke(dashboard.app, ["refresh"])
    assert result.exit_code == 0
    assert "updated" in result.stdout
