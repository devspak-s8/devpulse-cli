import json
from typer.testing import CliRunner

from devpulse.commands import github as github_cmd

runner = CliRunner()


class FakePR:
    def __init__(self, number, title, author, base_ref, head_ref, base_sha, head_sha, updated_at, mergeable_state, ci_status, commits_count=None, files_changed=None):
        class Merge:
            def __init__(self, mergeable_state, ci_status):
                self.mergeable = mergeable_state != "dirty"
                self.mergeable_state = mergeable_state
                self.ci_status = ci_status
        self.number = number
        self.title = title
        self.author = author
        self.base_ref = base_ref
        self.head_ref = head_ref
        self.base_sha = base_sha
        self.head_sha = head_sha
        self.updated_at = updated_at
        self.html_url = f"https://github.com/owner/repo/pull/{number}"
        self.merge = Merge(mergeable_state, ci_status)
        self.commits_count = commits_count
        self.files_changed = files_changed


class FakeService:
    def __init__(self):
        self.rate_limit_remaining = 4999
        self.rate_limit_reset = None

    def _parse_repo_full_name(self, repo):
        owner, name = repo.split("/")
        return owner, name

    def list_pull_requests(self, owner, name, state="open", force_refresh=False):
        return [
            FakePR(1, "Fix bug", "alice", "main", "feature/fix", "base1", "sha1", "2026-01-01T00:00:00Z", "clean", "success"),
            FakePR(2, "Add feature", "bob", "develop", "feat/x", "base2", "sha2", "2026-01-02T00:00:00Z", "dirty", "failure"),
        ]

    def get_pull_request(self, owner, name, number, force_refresh=False):
        return FakePR(number, "PR Title", "alice", "main", "feature/x", "baseX", "shaX", "2026-01-01T00:00:00Z", "clean", "success", commits_count=3, files_changed=2)

    def merge_pull_request(self, owner, name, number, strategy="squash", confirm=False, force_checks=False, dry_run=False):
        return {
            "repo": f"{owner}/{name}",
            "pr_number": number,
            "mergeable": True,
            "mergeable_state": "clean",
            "head_sha": "shaX",
            "base_sha": "baseX",
            "merged": False if dry_run else True,
            "strategy": strategy,
            "dry_run": dry_run,
        }


def test_cli_prs_list(monkeypatch):
    monkeypatch.setattr(github_cmd, "GitHubService", FakeService)
    result = runner.invoke(github_cmd.app, ["prs", "owner/repo"]) 
    assert result.exit_code == 0
    assert "Pull Requests:" in result.stdout
    assert "Number" in result.stdout


def test_cli_prs_conflicts_only(monkeypatch):
    monkeypatch.setattr(github_cmd, "GitHubService", FakeService)
    result = runner.invoke(github_cmd.app, ["prs", "owner/repo", "--conflicts-only", "--json"]) 
    assert result.exit_code == 0
    data = json.loads(result.stdout)
    prs = data.get("pull_requests", [])
    assert len(prs) == 1
    assert prs[0]["mergeable_state"] == "dirty"


def test_cli_pr_view_json(monkeypatch):
    monkeypatch.setattr(github_cmd, "GitHubService", FakeService)
    result = runner.invoke(github_cmd.app, ["pr", "view", "owner/repo", "42", "--json"]) 
    assert result.exit_code == 0
    data = json.loads(result.stdout)
    assert data["pr_number"] == 42
    assert "head_sha" in data
    assert "mergeable_state" in data


def test_cli_pr_merge_dry_run(monkeypatch):
    monkeypatch.setattr(github_cmd, "GitHubService", FakeService)
    monkeypatch.setenv("GITHUB_TOKEN", "dummy")
    result = runner.invoke(github_cmd.app, ["pr", "merge", "owner/repo", "42", "--strategy", "squash", "--dry-run", "--json"]) 
    assert result.exit_code == 0
    data = json.loads(result.stdout)
    assert data["dry_run"] is True
    assert data["merged"] is False
