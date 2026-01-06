import pytest
from typer.testing import CliRunner
from devpulse.commands import secrets

runner = CliRunner()


def test_secrets_scan_default():
    """Test secrets scan command with default path"""
    result = runner.invoke(secrets.app, ["scan"])
    assert result.exit_code == 0
    assert "Scanning path: ." in result.stdout
    assert "Scan complete" in result.stdout


def test_secrets_scan_custom_path():
    """Test secrets scan command with custom path"""
    result = runner.invoke(secrets.app, ["scan", "/path/to/code"])
    assert result.exit_code == 0
    assert "/path/to/code" in result.stdout


def test_secrets_scan_recursive_true():
    """Test secrets scan command with recursive enabled (default)"""
    result = runner.invoke(secrets.app, ["scan", "."])
    assert result.exit_code == 0
    assert "Recursive: True" in result.stdout


def test_secrets_list():
    """Test secrets list command"""
    result = runner.invoke(secrets.app, ["list"])
    assert result.exit_code == 0
    assert "Secret Detection History" in result.stdout


def test_secrets_check_file():
    """Test secrets check command"""
    result = runner.invoke(secrets.app, ["check", "config.py"])
    assert result.exit_code == 0
    assert "Checking file: config.py" in result.stdout


def test_secrets_check_with_type():
    """Test secrets check command with type filter"""
    result = runner.invoke(secrets.app, ["check", "config.py", "--type", "api-key"])
    assert result.exit_code == 0
    assert "api-key" in result.stdout


def test_secrets_check_strict():
    """Test secrets check command with strict mode"""
    result = runner.invoke(secrets.app, ["check", "config.py", "--strict"])
    assert result.exit_code == 0
    assert "Strict mode: True" in result.stdout


def test_secrets_ignore_add():
    """Test secrets ignore command to add pattern"""
    result = runner.invoke(secrets.app, ["ignore", "*.test.js"])
    assert result.exit_code == 0
    assert "Added ignore pattern: *.test.js" in result.stdout


def test_secrets_ignore_remove():
    """Test secrets ignore command to remove pattern"""
    result = runner.invoke(secrets.app, ["ignore", "*.test.js", "--remove"])
    assert result.exit_code == 0
    assert "Removed ignore pattern: *.test.js" in result.stdout


def test_secrets_report_default():
    """Test secrets report command with defaults"""
    result = runner.invoke(secrets.app, ["report"])
    assert result.exit_code == 0
    assert "security report" in result.stdout
    assert "console format" in result.stdout


def test_secrets_report_json():
    """Test secrets report command with JSON format"""
    result = runner.invoke(secrets.app, ["report", "--format", "json"])
    assert result.exit_code == 0
    assert "json format" in result.stdout


def test_secrets_report_with_output():
    """Test secrets report command with output file"""
    result = runner.invoke(secrets.app, ["report", "--output", "security.html"])
    assert result.exit_code == 0
    assert "security.html" in result.stdout


def test_secrets_report_severity_filter():
    """Test secrets report command with severity filter"""
    result = runner.invoke(secrets.app, ["report", "--severity", "critical"])
    assert result.exit_code == 0
    assert "Severity filter: critical" in result.stdout


def test_secrets_validate_default():
    """Test secrets validate command"""
    result = runner.invoke(secrets.app, ["validate"])
    assert result.exit_code == 0
    assert "Configuration is valid" in result.stdout


def test_secrets_validate_custom_config():
    """Test secrets validate command with custom config"""
    result = runner.invoke(secrets.app, ["validate", "--config", "custom.yml"])
    assert result.exit_code == 0
    assert "custom.yml" in result.stdout


def test_secrets_patterns_list():
    """Test secrets patterns command to list all"""
    result = runner.invoke(secrets.app, ["patterns", "--list"])
    assert result.exit_code == 0
    assert "detection patterns" in result.stdout
    assert "API Keys" in result.stdout


def test_secrets_patterns_add():
    """Test secrets patterns command to add pattern"""
    result = runner.invoke(secrets.app, ["patterns", "--add", "CUSTOM_.*_KEY"])
    assert result.exit_code == 0
    assert "Added pattern: CUSTOM_.*_KEY" in result.stdout
