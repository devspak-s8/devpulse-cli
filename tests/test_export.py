import pytest
from typer.testing import CliRunner
from devpulse.commands import export

runner = CliRunner()


def test_export_all_csv():
    result = runner.invoke(export.app, ["all"])
    assert result.exit_code == 0
    assert "Exporting" in result.stdout


def test_export_all_json():
    result = runner.invoke(export.app, ["all", "--format", "json"])
    assert result.exit_code == 0
    assert "json" in result.stdout


def test_export_all_with_range():
    result = runner.invoke(export.app, ["all", "--range", "2026-01-01:2026-01-31"])
    assert result.exit_code == 0
    assert "2026-01-01" in result.stdout


def test_export_sessions():
    result = runner.invoke(export.app, ["sessions"])
    assert result.exit_code == 0
    assert "sessions" in result.stdout


def test_export_projects():
    result = runner.invoke(export.app, ["projects"])
    assert result.exit_code == 0
    assert "projects" in result.stdout


def test_export_notes():
    result = runner.invoke(export.app, ["notes"])
    assert result.exit_code == 0
    assert "notes" in result.stdout


def test_export_stats():
    result = runner.invoke(export.app, ["stats"])
    assert result.exit_code == 0
    assert "statistics" in result.stdout


def test_export_archive():
    result = runner.invoke(export.app, ["archive"])
    assert result.exit_code == 0
    assert "Archive" in result.stdout
