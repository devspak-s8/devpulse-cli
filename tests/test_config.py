import pytest
from typer.testing import CliRunner
from devpulse.commands import config

runner = CliRunner()


def test_config_show():
    result = runner.invoke(config.app, ["show"])
    assert result.exit_code == 0
    assert "Configuration" in result.stdout


def test_config_show_key():
    result = runner.invoke(config.app, ["show", "user.name"])
    assert result.exit_code == 0
    assert "user.name" in result.stdout


def test_config_set():
    result = runner.invoke(config.app, ["set", "theme", "dark"])
    assert result.exit_code == 0
    assert "theme" in result.stdout


def test_config_get():
    result = runner.invoke(config.app, ["get", "theme"])
    assert result.exit_code == 0
    assert "theme" in result.stdout


def test_config_list():
    result = runner.invoke(config.app, ["list"])
    assert result.exit_code == 0
    assert "Configuration" in result.stdout


def test_config_import():
    result = runner.invoke(config.app, ["import-config", "config.json"])
    assert result.exit_code == 0
    assert "Importing" in result.stdout


def test_config_export():
    result = runner.invoke(config.app, ["export-config"])
    assert result.exit_code == 0
    assert "Exporting" in result.stdout
