import pytest
from typer.testing import CliRunner
from devpulse.commands import logs

runner = CliRunner()


def test_logs_analyze():
    """Test logs analyze command"""
    result = runner.invoke(logs.app, ["analyze", "app.log"])
    assert result.exit_code == 0
    assert "Analyzing log file: app.log" in result.stdout
    assert "Analysis complete" in result.stdout


def test_logs_search():
    """Test logs search command"""
    result = runner.invoke(logs.app, ["search", "error"])
    assert result.exit_code == 0
    assert "Searching for 'error'" in result.stdout


def test_logs_search_with_file():
    """Test logs search command with specific file"""
    result = runner.invoke(logs.app, ["search", "warning", "--file", "app.log"])
    assert result.exit_code == 0
    assert "warning" in result.stdout
    assert "app.log" in result.stdout


def test_logs_filter_basic():
    """Test logs filter command"""
    result = runner.invoke(logs.app, ["filter", "app.log"])
    assert result.exit_code == 0
    assert "Filtering log: app.log" in result.stdout


def test_logs_filter_with_level():
    """Test logs filter command with level"""
    result = runner.invoke(logs.app, ["filter", "app.log", "--level", "ERROR"])
    assert result.exit_code == 0
    assert "Level: ERROR" in result.stdout


def test_logs_filter_with_dates():
    """Test logs filter command with date range"""
    result = runner.invoke(
        logs.app, 
        ["filter", "app.log", "--start", "2026-01-01", "--end", "2026-01-31"]
    )
    assert result.exit_code == 0
    assert "2026-01-01" in result.stdout
    assert "2026-01-31" in result.stdout


def test_logs_filter_with_keyword():
    """Test logs filter command with keyword"""
    result = runner.invoke(logs.app, ["filter", "app.log", "--keyword", "database"])
    assert result.exit_code == 0
    assert "Keyword: database" in result.stdout


def test_logs_tail():
    """Test logs tail command"""
    result = runner.invoke(logs.app, ["tail", "app.log"])
    assert result.exit_code == 0
    assert "Tailing app.log" in result.stdout


def test_logs_tail_custom_lines():
    """Test logs tail command with custom lines"""
    result = runner.invoke(logs.app, ["tail", "app.log", "--lines", "100"])
    assert result.exit_code == 0
    assert "100 lines" in result.stdout


def test_logs_tail_follow():
    """Test logs tail command with follow flag"""
    result = runner.invoke(logs.app, ["tail", "app.log", "--follow"])
    assert result.exit_code == 0
    assert "Following file" in result.stdout


def test_logs_errors_default():
    """Test logs errors command"""
    result = runner.invoke(logs.app, ["errors"])
    assert result.exit_code == 0
    assert "Errors in all logs" in result.stdout
    assert "Total errors: 0" in result.stdout


def test_logs_errors_with_file():
    """Test logs errors command with specific file"""
    result = runner.invoke(logs.app, ["errors", "app.log"])
    assert result.exit_code == 0
    assert "Errors in app.log" in result.stdout


def test_logs_errors_count_only():
    """Test logs errors command with count only"""
    result = runner.invoke(logs.app, ["errors", "--count"])
    assert result.exit_code == 0
    assert "Total errors:" in result.stdout


def test_logs_warnings_default():
    """Test logs warnings command"""
    result = runner.invoke(logs.app, ["warnings"])
    assert result.exit_code == 0
    assert "Warnings in all logs" in result.stdout
    assert "Total warnings: 0" in result.stdout


def test_logs_warnings_with_file():
    """Test logs warnings command with specific file"""
    result = runner.invoke(logs.app, ["warnings", "app.log"])
    assert result.exit_code == 0
    assert "Warnings in app.log" in result.stdout


def test_logs_warnings_count_only():
    """Test logs warnings command with count only"""
    result = runner.invoke(logs.app, ["warnings", "--count"])
    assert result.exit_code == 0
    assert "Total warnings:" in result.stdout


def test_logs_stats():
    """Test logs stats command"""
    result = runner.invoke(logs.app, ["stats", "app.log"])
    assert result.exit_code == 0
    assert "Log Statistics" in result.stdout


def test_logs_stats_detailed():
    """Test logs stats command with detailed flag"""
    result = runner.invoke(logs.app, ["stats", "app.log", "--detailed"])
    assert result.exit_code == 0
    assert "app.log" in result.stdout
