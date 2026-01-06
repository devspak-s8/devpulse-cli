import pytest
from typer.testing import CliRunner
from devpulse.commands import health

runner = CliRunner()


def test_health_check_default():
    """Test health check command with all services"""
    result = runner.invoke(health.app, ["check"])
    assert result.exit_code == 0
    assert "CPU Usage:" in result.stdout
    assert "Memory Usage:" in result.stdout
    assert "Disk Usage:" in result.stdout


def test_health_check_cpu():
    """Test health check for CPU only"""
    result = runner.invoke(health.app, ["check", "--service", "cpu"])
    assert result.exit_code == 0
    assert "CPU Usage:" in result.stdout


def test_health_check_memory():
    """Test health check for memory only"""
    result = runner.invoke(health.app, ["check", "--service", "memory"])
    assert result.exit_code == 0
    assert "Memory Usage:" in result.stdout


def test_health_check_disk():
    """Test health check for disk only"""
    result = runner.invoke(health.app, ["check", "--service", "disk"])
    assert result.exit_code == 0
    assert "Disk Usage:" in result.stdout


def test_health_check_processes():
    """Test health check for active processes"""
    result = runner.invoke(health.app, ["check", "--service", "processes"])
    assert result.exit_code == 0
    assert "Active Processes:" in result.stdout


def test_health_report_console():
    """Test health report in console format"""
    result = runner.invoke(health.app, ["report"])
    assert result.exit_code == 0
    assert "SYSTEM HEALTH REPORT" in result.stdout
    assert "CPU Information:" in result.stdout
    assert "Memory Information:" in result.stdout
    assert "Disk Information:" in result.stdout


def test_health_report_json():
    """Test health report in JSON format"""
    result = runner.invoke(health.app, ["report", "--format", "json"])
    assert result.exit_code == 0
    # Verify it's valid JSON
    import json
    try:
        data = json.loads(result.stdout)
        assert "cpu" in data
        assert "memory" in data
        assert "disk" in data
        assert "processes" in data
    except json.JSONDecodeError:
        pytest.fail("Report output is not valid JSON")


def test_health_processes_default():
    """Test processes command with defaults"""
    result = runner.invoke(health.app, ["processes"])
    assert result.exit_code == 0
    assert "Top 10 Processes" in result.stdout
    assert "PID" in result.stdout
    assert "Name" in result.stdout


def test_health_processes_custom_top():
    """Test processes command with custom top count"""
    result = runner.invoke(health.app, ["processes", "--top", "5"])
    assert result.exit_code == 0
    assert "Top 5 Processes" in result.stdout


def test_health_processes_sort_by_cpu():
    """Test processes command sorted by CPU"""
    result = runner.invoke(health.app, ["processes", "--sort", "cpu"])
    assert result.exit_code == 0
    assert "cpu" in result.stdout


def test_health_processes_sort_by_name():
    """Test processes command sorted by name"""
    result = runner.invoke(health.app, ["processes", "--sort", "name"])
    assert result.exit_code == 0
    assert "Top 10 Processes" in result.stdout


def test_health_alert_default():
    """Test alert command with default thresholds"""
    result = runner.invoke(health.app, ["alert"])
    assert result.exit_code == 0
    assert "Checking for alerts" in result.stdout


def test_health_alert_custom_thresholds():
    """Test alert command with custom thresholds"""
    result = runner.invoke(
        health.app,
        ["alert", "--cpu", "50", "--memory", "70", "--disk", "85"]
    )
    assert result.exit_code == 0


def test_health_alert_low_cpu_threshold():
    """Test alert command with very low CPU threshold (should trigger)"""
    result = runner.invoke(health.app, ["alert", "--cpu", "1"])
    assert result.exit_code == 0
    # Should show alert if actual CPU > 1%
    # This is likely true in real scenario
    assert "Checking for alerts" in result.stdout


def test_health_check_short_option():
    """Test health check with short option"""
    result = runner.invoke(health.app, ["check", "-s", "memory"])
    assert result.exit_code == 0
    assert "Memory Usage:" in result.stdout


def test_health_report_format_option():
    """Test health report with format option"""
    result = runner.invoke(health.app, ["report", "-f", "console"])
    assert result.exit_code == 0
    assert "SYSTEM HEALTH REPORT" in result.stdout


def test_health_processes_sort_option():
    """Test processes with sort option"""
    result = runner.invoke(health.app, ["processes", "-s", "memory"])
    assert result.exit_code == 0
    assert "Top 10 Processes" in result.stdout


def test_health_processes_top_option():
    """Test processes with top option"""
    result = runner.invoke(health.app, ["processes", "-t", "3"])
    assert result.exit_code == 0
    assert "Top 3 Processes" in result.stdout


def test_health_alert_threshold_options():
    """Test alert with all threshold options"""
    result = runner.invoke(
        health.app,
        ["alert", "-c", "60", "-m", "75", "-d", "88"]
    )
    assert result.exit_code == 0


def test_health_report_includes_timestamp():
    """Test health report includes timestamp"""
    result = runner.invoke(health.app, ["report"])
    assert result.exit_code == 0
    assert "Generated:" in result.stdout
    # Check for YYYY-MM-DD format
    import re
    assert re.search(r'\d{4}-\d{2}-\d{2}', result.stdout)


def test_health_report_json_has_timestamp():
    """Test health report JSON includes timestamp"""
    result = runner.invoke(health.app, ["report", "--format", "json"])
    assert result.exit_code == 0
    import json
    data = json.loads(result.stdout)
    assert "timestamp" in data


def test_health_check_complete_message():
    """Test health check shows completion message"""
    result = runner.invoke(health.app, ["check"])
    assert result.exit_code == 0
    assert "Health check complete" in result.stdout
