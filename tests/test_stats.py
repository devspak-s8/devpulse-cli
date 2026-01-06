import pytest
from typer.testing import CliRunner
from devpulse.commands import stats

runner = CliRunner()


def test_stats_show_default():
    """Test stats show command with default period"""
    result = runner.invoke(stats.app, ["show"])
    assert result.exit_code == 0
    assert "Statistics for: today" in result.stdout
    assert "Total time tracked:" in result.stdout


def test_stats_show_week():
    """Test stats show command with week period"""
    result = runner.invoke(stats.app, ["show", "--period", "week"])
    assert result.exit_code == 0
    assert "week" in result.stdout


def test_stats_show_month():
    """Test stats show command with month period"""
    result = runner.invoke(stats.app, ["show", "--period", "month"])
    assert result.exit_code == 0
    assert "month" in result.stdout


def test_stats_report_console():
    """Test stats report command with console output"""
    result = runner.invoke(stats.app, ["report"])
    assert result.exit_code == 0
    assert "console format" in result.stdout
    assert "Report generated successfully" in result.stdout


def test_stats_report_json():
    """Test stats report command with JSON output"""
    result = runner.invoke(stats.app, ["report", "--output", "json"])
    assert result.exit_code == 0
    assert "json format" in result.stdout


def test_stats_report_html():
    """Test stats report command with HTML output"""
    result = runner.invoke(stats.app, ["report", "--output", "html"])
    assert result.exit_code == 0
    assert "html format" in result.stdout


def test_stats_trends_default():
    """Test stats trends command with defaults"""
    result = runner.invoke(stats.app, ["trends"])
    assert result.exit_code == 0
    assert "Trend Analysis" in result.stdout
    assert "time" in result.stdout


def test_stats_trends_with_metric():
    """Test stats trends command with specific metric"""
    result = runner.invoke(stats.app, ["trends", "--metric", "tasks"])
    assert result.exit_code == 0
    assert "tasks" in result.stdout


def test_stats_trends_with_chart():
    """Test stats trends command with chart"""
    result = runner.invoke(stats.app, ["trends", "--chart"])
    assert result.exit_code == 0
    assert "Chart would be displayed" in result.stdout


def test_stats_compare():
    """Test stats compare command"""
    result = runner.invoke(stats.app, ["compare", "last-week", "this-week"])
    assert result.exit_code == 0
    assert "Comparing last-week vs this-week" in result.stdout


def test_stats_compare_with_metric():
    """Test stats compare command with specific metric"""
    result = runner.invoke(stats.app, ["compare", "yesterday", "today", "--metric", "time"])
    assert result.exit_code == 0
    assert "Metric: time" in result.stdout


def test_stats_breakdown_default():
    """Test stats breakdown command with defaults"""
    result = runner.invoke(stats.app, ["breakdown"])
    assert result.exit_code == 0
    assert "Breakdown by task" in result.stdout
    assert "Top 10 items" in result.stdout


def test_stats_breakdown_by_project():
    """Test stats breakdown command by project"""
    result = runner.invoke(stats.app, ["breakdown", "--category", "project"])
    assert result.exit_code == 0
    assert "project" in result.stdout


def test_stats_breakdown_custom_top():
    """Test stats breakdown command with custom top value"""
    result = runner.invoke(stats.app, ["breakdown", "--top", "5"])
    assert result.exit_code == 0
    assert "Top 5 items" in result.stdout


def test_stats_productivity_default():
    """Test stats productivity command"""
    result = runner.invoke(stats.app, ["productivity"])
    assert result.exit_code == 0
    assert "Productivity Analysis" in result.stdout
    assert "Focus time:" in result.stdout


def test_stats_productivity_with_score():
    """Test stats productivity command with score"""
    result = runner.invoke(stats.app, ["productivity", "--score"])
    assert result.exit_code == 0
    assert "Productivity Score:" in result.stdout


def test_stats_productivity_with_insights():
    """Test stats productivity command with insights"""
    result = runner.invoke(stats.app, ["productivity", "--insights"])
    assert result.exit_code == 0
    assert "Insights:" in result.stdout


def test_stats_goals_list():
    """Test stats goals command list action"""
    result = runner.invoke(stats.app, ["goals", "list"])
    assert result.exit_code == 0
    assert "Goals:" in result.stdout


def test_stats_goals_list_weekly():
    """Test stats goals list command with weekly type"""
    result = runner.invoke(stats.app, ["goals", "list", "--type", "weekly"])
    assert result.exit_code == 0
    assert "Weekly Goals:" in result.stdout


def test_stats_goals_set():
    """Test stats goals set command"""
    result = runner.invoke(stats.app, ["goals", "set", "--target", "8h"])
    assert result.exit_code == 0
    assert "8h" in result.stdout
