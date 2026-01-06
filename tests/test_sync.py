import pytest
from typer.testing import CliRunner
from devpulse.commands import sync

runner = CliRunner()


def test_sync_push():
    """Test sync push command"""
    result = runner.invoke(sync.app, ["push"])
    assert result.exit_code == 0
    assert "Pushing data to cloud" in result.stdout
    assert "Sync completed successfully" in result.stdout


def test_sync_pull():
    """Test sync pull command"""
    result = runner.invoke(sync.app, ["pull"])
    assert result.exit_code == 0
    assert "Pulling data from cloud" in result.stdout
    assert "Sync completed successfully" in result.stdout


def test_sync_status():
    """Test sync status command"""
    result = runner.invoke(sync.app, ["status"])
    assert result.exit_code == 0
    assert "Cloud Status" in result.stdout
    assert "Last sync:" in result.stdout


def test_sync_login_with_email():
    """Test sync login command with email"""
    result = runner.invoke(sync.app, ["login", "--email", "user@example.com"])
    assert result.exit_code == 0
    assert "user@example.com" in result.stdout
    assert "Login successful" in result.stdout


def test_sync_login_without_email():
    """Test sync login command without email"""
    result = runner.invoke(sync.app, ["login"])
    assert result.exit_code == 0
    assert "enter your credentials" in result.stdout


def test_sync_login_with_token():
    """Test sync login command with token"""
    result = runner.invoke(sync.app, ["login", "--token", "abc123"])
    assert result.exit_code == 0
    assert "Login successful" in result.stdout


def test_sync_logout_with_force():
    """Test sync logout command with force"""
    result = runner.invoke(sync.app, ["logout", "--force"])
    assert result.exit_code == 0
    assert "Logged out successfully" in result.stdout


def test_sync_auto_enable():
    """Test sync auto command to enable"""
    result = runner.invoke(sync.app, ["auto", "--enable"])
    assert result.exit_code == 0
    assert "Auto-sync enabled" in result.stdout


def test_sync_auto_disable():
    """Test sync auto command to disable"""
    result = runner.invoke(sync.app, ["auto", "--disable"])
    assert result.exit_code == 0
    assert "Auto-sync disabled" in result.stdout


def test_sync_auto_status():
    """Test sync auto command without enable/disable"""
    result = runner.invoke(sync.app, ["auto"])
    assert result.exit_code == 0
    assert "Auto-sync:" in result.stdout


def test_sync_auto_custom_interval():
    """Test sync auto command with custom interval"""
    result = runner.invoke(sync.app, ["auto", "--enable", "--interval", "30"])
    assert result.exit_code == 0
    assert "30 minutes" in result.stdout


def test_sync_history_default():
    """Test sync history command with defaults"""
    result = runner.invoke(sync.app, ["history"])
    assert result.exit_code == 0
    assert "Sync History" in result.stdout


def test_sync_history_with_limit():
    """Test sync history command with custom limit"""
    result = runner.invoke(sync.app, ["history", "--limit", "10"])
    assert result.exit_code == 0
    assert "last 10" in result.stdout


def test_sync_history_filter_type():
    """Test sync history command with type filter"""
    result = runner.invoke(sync.app, ["history", "--type", "push"])
    assert result.exit_code == 0
    assert "type: push" in result.stdout


def test_sync_conflicts():
    """Test sync conflicts command"""
    result = runner.invoke(sync.app, ["conflicts"])
    assert result.exit_code == 0
    assert "conflicts" in result.stdout


def test_sync_conflicts_with_resolve():
    """Test sync conflicts command with resolve flag"""
    result = runner.invoke(sync.app, ["conflicts", "--resolve"])
    assert result.exit_code == 0


def test_sync_conflicts_strategy():
    """Test sync conflicts command with strategy"""
    result = runner.invoke(sync.app, ["conflicts", "--strategy", "local"])
    assert result.exit_code == 0
