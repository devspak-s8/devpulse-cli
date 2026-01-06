import pytest
from typer.testing import CliRunner
from devpulse.commands import track

runner = CliRunner()


def test_track_start():
    """Test track start command"""
    result = runner.invoke(track.app, ["start", "coding"])
    assert result.exit_code == 0
    assert "Started tracking: coding" in result.stdout
    assert "Timer is now running" in result.stdout


def test_track_stop():
    """Test track stop command"""
    result = runner.invoke(track.app, ["stop"])
    assert result.exit_code == 0
    assert "Stopped tracking" in result.stdout
    assert "Session saved successfully" in result.stdout


def test_track_status():
    """Test track status command"""
    result = runner.invoke(track.app, ["status"])
    assert result.exit_code == 0
    assert "Current Status" in result.stdout


def test_track_pause():
    """Test track pause command"""
    result = runner.invoke(track.app, ["pause"])
    assert result.exit_code == 0
    assert "Paused current session" in result.stdout
    assert "resume" in result.stdout


def test_track_resume():
    """Test track resume command"""
    result = runner.invoke(track.app, ["resume"])
    assert result.exit_code == 0
    assert "Resumed tracking" in result.stdout
    assert "running" in result.stdout


def test_track_list_default():
    """Test track list command with defaults"""
    result = runner.invoke(track.app, ["list"])
    assert result.exit_code == 0
    assert "Tracking sessions" in result.stdout


def test_track_list_with_limit():
    """Test track list command with custom limit"""
    result = runner.invoke(track.app, ["list", "--limit", "5"])
    assert result.exit_code == 0
    assert "last 5" in result.stdout


def test_track_list_today():
    """Test track list command with today filter"""
    result = runner.invoke(track.app, ["list", "--today"])
    assert result.exit_code == 0
    assert "today" in result.stdout


def test_track_delete_with_force():
    """Test track delete command with force flag"""
    result = runner.invoke(track.app, ["delete", "1", "--force"])
    assert result.exit_code == 0
    assert "Deleted session #1" in result.stdout


def test_track_edit_task():
    """Test track edit command with task"""
    result = runner.invoke(track.app, ["edit", "1", "--task", "new-task"])
    assert result.exit_code == 0
    assert "Editing session #1" in result.stdout
    assert "Updated task: new-task" in result.stdout


def test_track_edit_duration():
    """Test track edit command with duration"""
    result = runner.invoke(track.app, ["edit", "1", "--duration", "3h"])
    assert result.exit_code == 0
    assert "Updated duration: 3h" in result.stdout


def test_track_edit_both():
    """Test track edit command with both task and duration"""
    result = runner.invoke(track.app, ["edit", "1", "--task", "testing", "--duration", "2h30m"])
    assert result.exit_code == 0
    assert "Updated task: testing" in result.stdout
    assert "Updated duration: 2h30m" in result.stdout


def test_track_export_default():
    """Test track export command with defaults"""
    result = runner.invoke(track.app, ["export"])
    assert result.exit_code == 0
    assert "Exporting" in result.stdout
    assert "csv" in result.stdout


def test_track_export_json():
    """Test track export command with JSON format"""
    result = runner.invoke(track.app, ["export", "--format", "json", "--output", "data.json"])
    assert result.exit_code == 0
    assert "json" in result.stdout
    assert "data.json" in result.stdout


def test_track_export_with_range():
    """Test track export command with date range"""
    result = runner.invoke(track.app, ["export", "--range", "2026-01-01:2026-01-31"])
    assert result.exit_code == 0
    assert "2026-01-01:2026-01-31" in result.stdout
