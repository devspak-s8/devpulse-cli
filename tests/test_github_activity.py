import json
from datetime import datetime, timedelta
import pytest
from typer.testing import CliRunner

from devpulse.core.github import GitHubService
from devpulse.commands import github as github_cmd

runner = CliRunner()


def _sample_events(now_iso: str):
    # Create sample events across types and repos
    return [
        {"type": "PushEvent", "created_at": now_iso, "repo": {"name": "devspak/linux"}},
        {"type": "PullRequestEvent", "created_at": now_iso, "repo": {"name": "devspak/linux"}},
        {"type": "IssuesEvent", "created_at": now_iso, "repo": {"name": "devspak/devpulse"}},
        {"type": "WatchEvent", "created_at": now_iso, "repo": {"name": "devspak/devpulse"}},
        {"type": "ForkEvent", "created_at": now_iso, "repo": {"name": "devspak/other"}},
        {"type": "CreateEvent", "created_at": now_iso, "repo": {"name": "devspak/other"}},
        {"type": "DeleteEvent", "created_at": now_iso, "repo": {"name": "devspak/other"}},
        {"type": "ReleaseEvent", "created_at": now_iso, "repo": {"name": "devspak/devpulse"}},
        {"type": "PullRequestReviewEvent", "created_at": now_iso, "repo": {"name": "devspak/devpulse"}},
        {"type": "PullRequestReviewCommentEvent", "created_at": now_iso, "repo": {"name": "devspak/devpulse"}},
        {"type": "CommitCommentEvent", "created_at": now_iso, "repo": {"name": "devspak/devpulse"}},
        {"type": "MemberEvent", "created_at": now_iso, "repo": {"name": "devspak/devpulse"}},
        {"type": "PublicEvent", "created_at": now_iso, "repo": {"name": "devspak/devpulse"}},
        # Unsupported type should be ignored
        {"type": "GollumEvent", "created_at": now_iso, "repo": {"name": "devspak/devpulse"}},
    ]


def test_event_parsing_and_counts():
    now = datetime.utcnow()
    now_iso = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    raw = _sample_events(now_iso)
    svc = GitHubService()
    summary = svc.parse_and_summarize_events(raw, since_days=90)
    assert summary["total_events"] == 14  # now includes gollum events
    counts = summary["event_counts"]
    assert counts.get("push") == 1
    assert counts.get("pull_request") == 1
    assert counts.get("issues") == 1
    assert counts.get("stars") == 1
    assert counts.get("fork") == 1
    assert counts.get("create") == 1
    assert counts.get("delete") == 1
    assert counts.get("release") == 1
    assert counts.get("pull_request_review") == 1
    assert counts.get("pull_request_review_comment") == 1
    assert counts.get("commit_comment") == 1
    assert counts.get("member") == 1
    assert counts.get("public") == 1


def test_event_filtering():
    now_iso = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    raw = _sample_events(now_iso)
    svc = GitHubService()
    summary = svc.parse_and_summarize_events(raw, since_days=90, filters=["push", "pr"])
    assert summary["total_events"] == 2
    counts = summary["event_counts"]
    assert counts.get("push") == 1
    assert counts.get("pull_request") == 1


class FakeService:
    def __init__(self, timeout: int = 10):
        self.rate_limit_remaining = 4999
        self.rate_limit_reset = int((datetime.utcnow() + timedelta(minutes=10)).timestamp())
        self.timeout = timeout

    def get_user_public_events(self, username: str, per_page: int = 100, force_refresh: bool = False):
        now_iso = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        return _sample_events(now_iso)

    def parse_and_summarize_events(self, raw_events, since_days=30, filters=None):
        real = GitHubService()
        return real.parse_and_summarize_events(raw_events, since_days=since_days, filters=filters)


def test_cli_activity_default(monkeypatch):
    monkeypatch.setattr(github_cmd, "GitHubService", FakeService)
    result = runner.invoke(github_cmd.app, ["activity", "testuser"]) 
    assert result.exit_code == 0
    assert "GitHub Activity:" in result.stdout
    assert "Total Events" in result.stdout


def test_cli_activity_json(monkeypatch):
    monkeypatch.setattr(github_cmd, "GitHubService", FakeService)
    result = runner.invoke(github_cmd.app, ["activity", "testuser", "--json"]) 
    assert result.exit_code == 0
    data = json.loads(result.stdout)
    assert data["username"] == "testuser"
    assert "total_events" in data
    assert "event_counts" in data


def test_cli_activity_debug(monkeypatch):
    monkeypatch.setattr(github_cmd, "GitHubService", FakeService)
    result = runner.invoke(github_cmd.app, ["activity", "testuser", "--debug"]) 
    assert result.exit_code == 0
    assert "Rate Limit Remaining" in result.stdout
