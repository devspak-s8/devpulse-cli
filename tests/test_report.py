import pytest
from typer.testing import CliRunner
from devpulse.commands import report

runner = CliRunner()


def test_report_daily():
    result = runner.invoke(report.app, ["daily"])
    assert result.exit_code == 0
    assert "Daily Report" in result.stdout


def test_report_daily_detailed():
    result = runner.invoke(report.app, ["daily", "--detailed"])
    assert result.exit_code == 0
    assert "Breakdown" in result.stdout


def test_report_weekly():
    result = runner.invoke(report.app, ["weekly"])
    assert result.exit_code == 0
    assert "Weekly Report" in result.stdout


def test_report_monthly():
    result = runner.invoke(report.app, ["monthly"])
    assert result.exit_code == 0
    assert "Monthly Report" in result.stdout


def test_report_comparison():
    result = runner.invoke(report.app, ["comparison", "last-month", "this-month"])
    assert result.exit_code == 0
    assert "Comparison" in result.stdout


def test_report_summary():
    result = runner.invoke(report.app, ["summary"])
    assert result.exit_code == 0
    assert "Summary" in result.stdout


def test_report_insights():
    result = runner.invoke(report.app, ["insights"])
    assert result.exit_code == 0
    assert "Insights" in result.stdout
