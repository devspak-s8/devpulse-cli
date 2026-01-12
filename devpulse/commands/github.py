import os
import typer
import json as json_lib
from typing import Optional, List
import requests
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.syntax import Syntax

from devpulse.core.github import GitHubService, RateLimitExceeded
from devpulse.commands.github_readme import (
    ReadmeGenerator,
    RepositoryContextCollector,
    validate_readme_not_exists,
    save_readme,
)
from devpulse.commands.github_commit import (
    GitStatusCollector,
    ConventionalCommitGenerator,
    CommitMessageValidator,
    apply_commit_message,
)

app = typer.Typer(help="GitHub integration and statistics")
console = Console()


# --------------- Validation & Token Management ---------------
def _validate_repo_format(repo: str) -> tuple[str, str]:
    """Validate and parse repo in 'owner/name' format. Raise exit on failure."""
    if not repo or "/" not in repo:
        console.print("[red]❌ Invalid repository format.[/red]")
        console.print("[yellow]Usage: devpulse github <command> owner/name[/yellow]")
        raise typer.Exit(code=1)
    parts = repo.split("/")
    if len(parts) != 2 or not parts[0] or not parts[1]:
        console.print("[red]❌ Repository must be in 'owner/name' format.[/red]")
        console.print("[yellow]Example: devpulse github prs octocat/Hello-World[/yellow]")
        raise typer.Exit(code=1)
    return parts[0], parts[1]


def _validate_and_set_token(require_auth: bool = False) -> Optional[str]:
    """Validate and set GITHUB_TOKEN. If missing and required, prompt the user securely.
    Returns the token or None. Exits if required but unavailable."""
    token = os.getenv("GITHUB_TOKEN")
    if token:
        return token  # Already set
    
    if not require_auth:
        return None  # Auth not required yet
    
    # Auth required: prompt user
    console.print("[yellow]🔐 Authentication required for this operation.[/yellow]")
    console.print("[cyan]A GitHub token with 'repo' scope is needed.[/cyan]")
    console.print("[dim]Create one at: https://github.com/settings/tokens[/dim]\n")
    
    while True:
        token = typer.prompt("Enter GITHUB_TOKEN", hide_input=True)
        if token and token.strip():
            os.environ["GITHUB_TOKEN"] = token.strip()
            console.print("[green]✓ Token set.[/green]")
            return token.strip()
        else:
            console.print("[red]❌ Token cannot be empty.[/red]")
            console.print("[yellow]Please try again.[/yellow]")


def _get_health_color(score: int) -> str:
    """Return color based on health score."""
    if score >= 70:
        return "green"
    elif score >= 40:
        return "yellow"
    else:
        return "red"


def _output_json(data: dict) -> None:
    """Output data as JSON."""
    typer.echo(json_lib.dumps(data, indent=2))


def _filter_stats(stats: dict, include: Optional[str]) -> dict:
    """Filter stats based on include parameter."""
    if not include:
        return stats
    
    sections = [s.strip() for s in include.split(",")]
    filtered = {"repository": stats.get("repository", {})}
    
    for section in sections:
        if section == "contributors" and "contributors" in stats:
            filtered["contributors"] = stats["contributors"]
        elif section == "issues" and "issues" in stats:
            filtered["issues"] = stats["issues"]
        elif section == "activity" and "activity" in stats:
            filtered["activity"] = stats["activity"]
        elif section == "languages" and "languages" in stats:
            filtered["languages"] = stats["languages"]
        elif section == "health" and "health_score" in stats:
            filtered["health_score"] = stats["health_score"]
        elif section == "prs" and "pull_requests" in stats:
            filtered["pull_requests"] = stats["pull_requests"]
    
    return filtered


@app.command()
def stats(
    username: Optional[str] = typer.Option(None, "--username", "-u", help="GitHub username"),
    repo: Optional[str] = typer.Option(None, "--repo", "-r", help="Repository in 'owner/name' format"),
    include_health: bool = typer.Option(False, "--health", help="Include health score"),
    include_contributors: bool = typer.Option(False, "--contributors", help="Include contributors section"),
    include_activity: bool = typer.Option(False, "--activity", help="Include commit activity"),
    top_repos_for_user: int = typer.Option(3, "--top", help="Number of top repos for a user"),
    json: bool = typer.Option(False, "--json", help="Output as JSON"),
    include: Optional[str] = typer.Option(None, "--include", help="Comma-separated sections to include (contributors,issues,activity,languages,health,prs)"),
    force_refresh: bool = typer.Option(False, "--refresh", help="Bypass cache and force fresh API call"),
):
    """Fetch and display GitHub statistics for a repo or user."""
    if not username and not repo:
        typer.echo("Provide either --username or --repo owner/name")
        raise typer.Exit(code=1)
    if username and repo:
        typer.echo("Provide only one of --username or --repo")
        raise typer.Exit(code=1)

    svc = GitHubService()
    try:
        result = svc.get_repo_stats(
            repo=repo,
            username=username,
            include_health=include_health,
            include_contributors=include_contributors,
            include_activity=include_activity,
            top_repos_for_user=top_repos_for_user,
            force_refresh=force_refresh,
        )
    except RateLimitExceeded as e:
        console.print(f"[red][!] {str(e)}[/red]")
        console.print("[yellow]Tip: Set GITHUB_TOKEN env var to increase rate limit (5000 req/hour).[/yellow]")
        raise typer.Exit(code=1)
    except Exception as e:
        typer.echo(f"Error: {e}")
        raise typer.Exit(code=1)

    # Apply filtering if include is specified
    if include:
        if result.get("target", {}).get("type") == "repo":
            result["stats"] = _filter_stats(result["stats"], include)
        else:
            result["repos"] = [_filter_stats(s, include) for s in result.get("repos", [])]

    # JSON output
    if json:
        _output_json(result)
        return

    # Render output
    if result.get("target", {}).get("type") == "repo":
        _render_repo_stats(result["stats"]) 
    else:
        console.print(Panel.fit(f"GitHub User: {result['target']['username']}", title="Target"))
        for idx, stats in enumerate(result.get("repos", []), start=1):
            console.print(Panel.fit(f"Repository #{idx}", title="Index"))
            _render_repo_stats(stats)


def _render_repo_stats(stats: dict) -> None:
    repo = stats.get("repository", {})
    table = Table(title=f"Repository: {repo.get('full_name')}")
    table.add_column("Field", style="cyan", no_wrap=True)
    table.add_column("Value", style="magenta")

    table.add_row("Stars", str(repo.get("stars")))
    table.add_row("Forks", str(repo.get("forks")))
    table.add_row("Watchers", str(repo.get("watchers", 0)))
    table.add_row("Open Issues", str(stats.get("issues", {}).get("open_issues", repo.get("open_issues", 0))))
    table.add_row("Default Branch", str(repo.get("default_branch")))
    table.add_row("Created", str(repo.get("created_at")))
    table.add_row("Updated", str(repo.get("updated_at")))
    table.add_row("Last Commit", str(repo.get("last_commit_date")))
    table.add_row("Size (KB)", str(repo.get("size_kb")))
    table.add_row("License", str(stats.get("license") or "None"))
    
    # Stale warning
    if repo.get("is_stale"):
        table.add_row("Status", "[red][!] STALE (>6 months inactive)[/red]")
    else:
        table.add_row("Status", "[green][OK] Active[/green]")

    console.print(table)

    # Languages
    langs = stats.get("languages", {})
    if langs:
        lt = Table(title="Language Usage (%)")
        lt.add_column("Language", style="green")
        lt.add_column("Percent", style="yellow")
        for k, v in langs.items():
            lt.add_row(k, f"{v}%")
        console.print(lt)

    # Activity
    activity = stats.get("activity", {})
    if activity:
        at = Table(title="Commit Activity")
        at.add_column("Metric", style="blue")
        at.add_column("Value", style="white")
        at.add_row("Commits (7 days)", str(activity.get("commits_last_7_days", 0)))
        at.add_row("Commits (30 days)", str(activity.get("commits_last_30_days", 0)))
        at.add_row("Active", "Yes" if activity.get("active") else "No")
        console.print(at)

    # Issues & PRs
    issues = stats.get("issues", {})
    prs = stats.get("pull_requests", {})
    if issues or prs:
        ipt = Table(title="Issues & Pull Requests")
        ipt.add_column("Metric", style="red")
        ipt.add_column("Value", style="white")
        ipt.add_row("Open Issues", str(issues.get("open_issues", 0)))
        ipt.add_row("Closed Issues", str(issues.get("closed_issues", 0)))
        ipt.add_row("Oldest Open Issue", str(issues.get("oldest_open_issue_date") or "None"))
        ipt.add_row("Last Closed Issue", str(issues.get("last_closed_issue_date") or "None"))
        avg_age = issues.get("avg_open_issue_age_days")
        ipt.add_row("Avg Open Issue Age (days)", str(avg_age) if avg_age is not None else "N/A")
        ipt.add_row("Open PRs", str(prs.get("open_pull_requests", 0)))
        ipt.add_row("Merged PRs", str(prs.get("merged_pull_requests", 0)))
        ipt.add_row("Avg Merge Time (hrs)", str(prs.get("avg_merge_time_hours") or "N/A"))
        console.print(ipt)

    # Contributors
    contributors = stats.get("contributors", {})
    if contributors:
        ct = Table(title=f"Contributors (Total: {contributors.get('total_contributors', 0)})")
        ct.add_column("Login", style="cyan")
        ct.add_column("Commits", style="white")
        ct.add_column("Percentage", style="yellow")
        for c in contributors.get("top_contributors", []):
            ct.add_row(str(c.get("login")), str(c.get("contributions")), f"{c.get('percentage', 0)}%")
        console.print(ct)

    # Health Score
    hs = stats.get("health_score")
    if hs is not None:
        color = _get_health_color(hs)
        health_text = Text(f"Health Score: {hs}/100", style=f"bold {color}")
        console.print(Panel(health_text, title="Repository Health"))


@app.command()
def activity(
    username: str = typer.Argument(..., help="GitHub username"),
    json: bool = typer.Option(False, "--json", help="Output raw structured JSON"),
    events: Optional[str] = typer.Option(None, "--events", help="Comma-separated filter (e.g. push,pr,issues,stars)"),
    since: str = typer.Option("30d", "--since", help="Time window (7d, 30d, 90d)"),
    debug: bool = typer.Option(False, "--debug", help="Print API request/response metadata"),
    force_refresh: bool = typer.Option(False, "--force-refresh", help="Bypass cache and force fresh API call"),
    timeout: int = typer.Option(10, "--timeout", help="Request timeout in seconds"),
):
    """Fetch and summarize public GitHub user activity events."""
    # Parse since window
    since_map = {"7d": 7, "30d": 30, "90d": 90}
    if since not in since_map:
        typer.echo("Invalid --since value. Use one of: 7d, 30d, 90d")
        raise typer.Exit(code=1)
    since_days = since_map[since]

    filters_list: Optional[List[str]] = None
    if events:
        filters_list = [e.strip().lower() for e in events.split(",") if e.strip()]

    svc = GitHubService(timeout=timeout)

    try:
        raw = svc.get_user_public_events(username, per_page=100, force_refresh=force_refresh)
        summary = svc.parse_and_summarize_events(raw, since_days=since_days, filters=filters_list)

        result = {
            "username": username,
            **summary,
        }

        # JSON output
        if json:
            _output_json(result)
            return

        # Rich output
        console.print(Panel.fit(f"GitHub Activity: {username}", title="User"))

        status = "Active" if result["total_events"] > 0 else "Inactive"
        table = Table(title=f"Summary (last {since})")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="yellow")
        table.add_row("Total Events", str(result["total_events"]))
        table.add_row("Active Repositories", str(result["active_repos"]))
        table.add_row("Last Activity", str(result.get("last_activity") or "None"))
        table.add_row("Status", status)
        console.print(table)

        ec = result.get("event_counts", {})
        if ec:
            bt = Table(title="Event Breakdown")
            bt.add_column("Type", style="green")
            bt.add_column("Count", style="magenta")
            for k, v in sorted(ec.items(), key=lambda x: x[0]):
                bt.add_row(k, str(v))
            console.print(bt)

        mar = result.get("most_active_repo")
        if mar:
            console.print(Panel.fit(f"Most Active Repo: {mar}", title="Highlight"))

        if debug:
            meta = Table(title="Debug")
            meta.add_column("Key", style="blue")
            meta.add_column("Value", style="white")
            meta.add_row("Endpoint", f"/users/{username}/events/public")
            meta.add_row("Timeout", f"{timeout}s")
            if svc.rate_limit_remaining is not None:
                meta.add_row("Rate Limit Remaining", str(svc.rate_limit_remaining))
            if svc.rate_limit_reset is not None:
                try:
                    reset_dt = datetime.utcfromtimestamp(svc.rate_limit_reset).strftime("%Y-%m-%dT%H:%M:%SZ")
                except Exception:
                    reset_dt = str(svc.rate_limit_reset)
                meta.add_row("Rate Limit Reset", reset_dt)
            console.print(meta)

        if result["total_events"] == 0:
            console.print("[yellow]No recent public activity in the selected window.[/yellow]")

    except RateLimitExceeded as e:
        console.print(f"[red][!] {str(e)}[/red]")
        console.print("[yellow]Tip: Set GITHUB_TOKEN env var to increase rate limit (5000 req/hour).[/yellow]")
        raise typer.Exit(code=1)
    except requests.exceptions.HTTPError as e:
        status = getattr(e.response, "status_code", None)
        if status == 404:
            console.print("[red]User not found. Please check the username.[/red]")
            raise typer.Exit(code=1)
        typer.echo(f"HTTP Error: {e}")
        raise typer.Exit(code=1)
    except requests.exceptions.RequestException as e:
        console.print("[red]Network error or timeout. Using cache if available.[/red]")
        typer.echo(f"Error: {e}")
        raise typer.Exit(code=1)


@app.command()
def top_languages(
    repo: str = typer.Argument(..., help="Repository in 'owner/name' format"),
    json: bool = typer.Option(False, "--json", help="Output as JSON"),
    force_refresh: bool = typer.Option(False, "--force-refresh", help="Bypass cache and force fresh API call"),
):
    """Display detailed language usage with percentages for a repository."""
    svc = GitHubService()
    
    try:
        owner, name = svc._parse_repo_full_name(repo)
        languages = svc.get_repo_languages(owner, name, force_refresh=force_refresh)
        
        result = {
            "repository": repo,
            "languages": languages,
        }
        
        if json:
            _output_json(result)
            return
        
        # Display
        console.print(Panel.fit(f"Language Usage: {repo}", title="Repository"))
        
        if not languages:
            console.print("[yellow]No language data available[/yellow]")
            return
        
        table = Table(title="Language Distribution")
        table.add_column("Language", style="cyan")
        table.add_column("Percentage", style="green")
        table.add_column("Bar", style="blue")
        
        for lang, pct in sorted(languages.items(), key=lambda x: x[1], reverse=True):
            bar_length = int(pct / 2)  # Scale to ~50 chars max
            bar = "█" * bar_length
            table.add_row(lang, f"{pct}%", bar)
        
        console.print(table)
    
    except Exception as e:
        typer.echo(f"Error: {e}")
        raise typer.Exit(code=1)


@app.command()
def contributors(
    repo: str = typer.Argument(..., help="Repository in 'owner/name' format"),
    top: int = typer.Option(10, "--top", "-n", help="Number of top contributors to show"),
    json: bool = typer.Option(False, "--json", help="Output as JSON"),
    force_refresh: bool = typer.Option(False, "--force-refresh", help="Bypass cache and force fresh API call"),
):
    """Display top contributors with commit counts and percentages."""
    svc = GitHubService()
    
    try:
        owner, name = svc._parse_repo_full_name(repo)
        contrib_data = svc.get_contributors(owner, name, top_n=top, force_refresh=force_refresh)
        
        result = {
            "repository": repo,
            "total_contributors": contrib_data.get("total_contributors", 0),
            "total_commits": contrib_data.get("total_commits", 0),
            "top_contributors": contrib_data.get("top_contributors", []),
        }
        
        if json:
            _output_json(result)
            return
        
        # Display
        console.print(Panel.fit(f"Contributors: {repo}", title="Repository"))
        
        console.print(f"[cyan]Total Contributors:[/cyan] {result['total_contributors']}")
        console.print(f"[cyan]Total Commits:[/cyan] {result['total_commits']}\n")
        
        if not result["top_contributors"]:
            console.print("[yellow]No contributor data available[/yellow]")
            return
        
        table = Table(title=f"Top {top} Contributors")
        table.add_column("Rank", style="yellow")
        table.add_column("Login", style="cyan")
        table.add_column("Commits", style="green")
        table.add_column("Percentage", style="magenta")
        
        for idx, c in enumerate(result["top_contributors"], start=1):
            table.add_row(
                str(idx),
                str(c.get("login")),
                str(c.get("contributions")),
                f"{c.get('percentage', 0)}%"
            )
        
        console.print(table)
    
    except Exception as e:
        typer.echo(f"Error: {e}")
        raise typer.Exit(code=1)


# ----------------- Pull Request Management -----------------

@app.command()
def prs(
    repo: str = typer.Argument(..., help="Repository in 'owner/name' format"),
    state: str = typer.Option("open", "--state", help="PR state: open | closed | all"),
    conflicts_only: bool = typer.Option(False, "--conflicts-only", help="Show only PRs with merge conflicts"),
    json: bool = typer.Option(False, "--json", help="Output machine-readable JSON"),
    debug: bool = typer.Option(False, "--debug", help="Show API request/response metadata"),
    force_refresh: bool = typer.Option(False, "--force-refresh", help="Bypass cache"),
):
    """List pull requests for a repository with mergeability and CI status."""
    # Validate inputs
    owner, name = _validate_repo_format(repo)
    
    svc = GitHubService()
    try:
        state_norm = state.lower()
        if state_norm not in {"open", "closed", "all"}:
            console.print("[red]❌ Invalid --state option.[/red]")
            console.print("[yellow]Use one of: open | closed | all[/yellow]")
            raise typer.Exit(code=1)

        prs_list = svc.list_pull_requests(owner, name, state=state_norm, force_refresh=force_refresh)
        if conflicts_only:
            prs_list = [p for p in prs_list if (p.merge.mergeable_state or "").lower() == "dirty"]

        # JSON output
        if json:
            payload = [
                {
                    "repo": repo,
                    "pr_number": p.number,
                    "title": p.title,
                    "author": p.author,
                    "base": f"{p.base_ref}",
                    "head": f"{p.head_ref}",
                    "mergeable": p.merge.mergeable,
                    "mergeable_state": p.merge.mergeable_state,
                    "ci_status": p.merge.ci_status,
                    "updated_at": p.updated_at,
                    "head_sha": p.head_sha,
                }
                for p in prs_list
            ]
            _output_json({"repository": repo, "state": state_norm, "pull_requests": payload})
            return

        # Rich output
        console.print(Panel.fit(f"Pull Requests: {repo}", title="Repository"))
        table = Table(title=f"PRs ({state_norm})")
        table.add_column("Number", style="cyan", no_wrap=True)
        table.add_column("Title", style="magenta")
        table.add_column("Author", style="green")
        table.add_column("Base → Head", style="yellow")
        table.add_column("State", style="white")
        table.add_column("CI", style="white")
        table.add_column("Updated", style="blue")
        table.add_column("Head SHA", style="white")

        for p in prs_list:
            st = (p.merge.mergeable_state or "unknown").lower()
            if st == "clean":
                st_disp = "[green]clean[/green]"
            elif st == "dirty":
                st_disp = "[red]dirty[/red]"
            elif st == "blocked":
                st_disp = "[yellow]blocked[/yellow]"
            else:
                st_disp = "[dim]unknown[/dim]"

            ci = (p.merge.ci_status or "none").lower()
            if ci == "success":
                ci_disp = "[green]success[/green]"
            elif ci == "failure":
                ci_disp = "[red]failure[/red]"
            elif ci == "pending":
                ci_disp = "[yellow]pending[/yellow]"
            else:
                ci_disp = "[dim]none[/dim]"

            table.add_row(
                str(p.number),
                str(p.title or ""),
                str(p.author or ""),
                f"{p.base_ref} → {p.head_ref}",
                st_disp,
                ci_disp,
                str(p.updated_at or ""),
                str(p.head_sha or ""),
            )
        console.print(table)

        if debug:
            meta = Table(title="Debug")
            meta.add_column("Key")
            meta.add_column("Value")
            meta.add_row("Endpoint", f"/repos/{owner}/{name}/pulls")
            if svc.rate_limit_remaining is not None:
                meta.add_row("Rate Limit Remaining", str(svc.rate_limit_remaining))
            if svc.rate_limit_reset is not None:
                try:
                    reset_dt = datetime.utcfromtimestamp(svc.rate_limit_reset).strftime("%Y-%m-%dT%H:%M:%SZ")
                except Exception:
                    reset_dt = str(svc.rate_limit_reset)
                meta.add_row("Rate Limit Reset", reset_dt)
            console.print(meta)

    except RateLimitExceeded as e:
        console.print(f"[red]❌ {str(e)}[/red]")
        console.print("[yellow]💡 Tip: Set GITHUB_TOKEN with repo scope to increase rate limit to 5000/hour.[/yellow]")
        console.print("[dim]Create a token at: https://github.com/settings/tokens[/dim]")
        raise typer.Exit(code=1)
    except requests.exceptions.HTTPError as e:
        status = getattr(e.response, "status_code", None)
        if status == 404:
            console.print(f"[red]❌ Repository not found: {repo}[/red]")
            console.print("[yellow]Please check the owner and repository name.[/yellow]")
        elif status == 403:
            console.print(f"[red]❌ Access denied to repository: {repo}[/red]")
            console.print("[yellow]Ensure the repository is public or you have access.[/yellow]")
        else:
            console.print(f"[red]❌ HTTP Error {status}: {e}[/red]")
        raise typer.Exit(code=1)
    except requests.exceptions.ConnectionError:
        console.print("[red]❌ Network error: Unable to reach GitHub API.[/red]")
        console.print("[yellow]Check your internet connection and try again.[/yellow]")
        raise typer.Exit(code=1)
    except requests.exceptions.Timeout:
        console.print("[red]❌ Request timeout: GitHub API took too long to respond.[/red]")
        console.print("[yellow]Try again in a moment or use --force-refresh.[/yellow]")
        raise typer.Exit(code=1)
    except requests.exceptions.RequestException as e:
        console.print(f"[red]❌ Request failed: {e}[/red]")
        raise typer.Exit(code=1)
    except ValueError as e:
        console.print(f"[red]❌ Validation error: {e}[/red]")
        raise typer.Exit(code=1)


pr_app = typer.Typer(help="Pull Request management")
app.add_typer(pr_app, name="pr")


@pr_app.command("view")
def pr_view(
    repo: str = typer.Argument(..., help="Repository in 'owner/name' format"),
    pr_number: int = typer.Argument(..., help="Pull Request number"),
    json: bool = typer.Option(False, "--json", help="Output machine-readable JSON"),
    debug: bool = typer.Option(False, "--debug", help="Show API metadata"),
    force_refresh: bool = typer.Option(False, "--force-refresh", help="Bypass cache"),
):
    """View details for a single pull request."""
    # Validate inputs
    owner, name = _validate_repo_format(repo)
    if pr_number <= 0:
        console.print("[red]❌ PR number must be a positive integer.[/red]")
        raise typer.Exit(code=1)
    
    svc = GitHubService()
    try:
        pr = svc.get_pull_request(owner, name, pr_number, force_refresh=force_refresh)

        if json:
            _output_json({
                "repo": repo,
                "pr_number": pr.number,
                "title": pr.title,
                "author": pr.author,
                "description": None,  # description not fetched to minimize calls
                "files_changed": pr.files_changed,
                "commit_count": pr.commits_count,
                "base_sha": pr.base_sha,
                "head_sha": pr.head_sha,
                "mergeable": pr.merge.mergeable,
                "mergeable_state": pr.merge.mergeable_state,
                "ci_status": pr.merge.ci_status,
            })
            return

        console.print(Panel.fit(f"PR #{pr.number}: {pr.title}", title="Pull Request"))
        table = Table(title="Details")
        table.add_column("Field", style="cyan")
        table.add_column("Value", style="white")
        table.add_row("Author", str(pr.author or ""))
        table.add_row("Base", str(pr.base_ref or ""))
        table.add_row("Head", str(pr.head_ref or ""))
        table.add_row("Base SHA", str(pr.base_sha or ""))
        table.add_row("Head SHA", str(pr.head_sha or ""))
        table.add_row("Commits", str(pr.commits_count or ""))
        table.add_row("Files Changed", str(pr.files_changed or ""))
        st = (pr.merge.mergeable_state or "unknown").lower()
        ci = (pr.merge.ci_status or "none").lower()
        table.add_row("Mergeable State", st)
        table.add_row("CI Status", ci)
        console.print(table)

        if debug:
            meta = Table(title="Debug")
            meta.add_column("Key")
            meta.add_column("Value")
            meta.add_row("Endpoint", f"/repos/{owner}/{name}/pulls/{pr_number}")
            if svc.rate_limit_remaining is not None:
                meta.add_row("Rate Limit Remaining", str(svc.rate_limit_remaining))
            if svc.rate_limit_reset is not None:
                try:
                    reset_dt = datetime.utcfromtimestamp(svc.rate_limit_reset).strftime("%Y-%m-%dT%H:%M:%SZ")
                except Exception:
                    reset_dt = str(svc.rate_limit_reset)
                meta.add_row("Rate Limit Reset", reset_dt)
            console.print(meta)

    except RateLimitExceeded as e:
        console.print(f"[red]❌ {str(e)}[/red]")
        console.print("[yellow]💡 Set GITHUB_TOKEN with repo scope to increase rate limit.[/yellow]")
        raise typer.Exit(code=1)
    except requests.exceptions.HTTPError as e:
        status = getattr(e.response, "status_code", None)
        if status == 404:
            console.print(f"[red]❌ PR #{pr_number} not found in {repo}[/red]")
            console.print("[yellow]Check the PR number and repository name.[/yellow]")
        elif status == 403:
            console.print(f"[red]❌ Access denied to repository: {repo}[/red]")
        else:
            console.print(f"[red]❌ HTTP Error {status}: {e}[/red]")
        raise typer.Exit(code=1)
    except requests.exceptions.ConnectionError:
        console.print("[red]❌ Network error: Unable to reach GitHub API.[/red]")
        console.print("[yellow]Check your internet connection.[/yellow]")
        raise typer.Exit(code=1)
    except requests.exceptions.Timeout:
        console.print("[red]❌ Request timeout: GitHub API took too long to respond.[/red]")
        raise typer.Exit(code=1)
    except requests.exceptions.RequestException as e:
        console.print(f"[red]❌ Request failed: {e}[/red]")
        raise typer.Exit(code=1)
    except ValueError as e:
        console.print(f"[red]❌ Validation error: {e}[/red]")
        raise typer.Exit(code=1)


@pr_app.command("merge")
def pr_merge(
    repo: str = typer.Argument(..., help="Repository in 'owner/name' format"),
    pr_number: int = typer.Argument(..., help="Pull Request number"),
    strategy: str = typer.Option("squash", "--strategy", help="merge | squash | rebase"),
    confirm: bool = typer.Option(False, "--confirm", help="Confirm merge operation (REQUIRED)"),
    force: bool = typer.Option(False, "--force", help="Override failing checks (conflicts still refuse)"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Show what would happen without merging"),
    json: bool = typer.Option(False, "--json", help="Output machine-readable JSON"),
):
    """Merge a pull request safely with confirmation and auth checks."""
    # Validate inputs
    owner, name = _validate_repo_format(repo)
    if pr_number <= 0:
        console.print("[red]❌ PR number must be a positive integer.[/red]")
        raise typer.Exit(code=1)
    
    st = strategy.lower()
    if st not in {"merge", "squash", "rebase"}:
        console.print("[red]❌ Invalid --strategy option.[/red]")
        console.print("[yellow]Use one of: merge | squash | rebase[/yellow]")
        raise typer.Exit(code=1)
    
    # Prompt for token if required (always needed for merge)
    _validate_and_set_token(require_auth=True)
    
    svc = GitHubService()
    try:
        result = svc.merge_pull_request(owner, name, pr_number, strategy=st, confirm=confirm, force_checks=force, dry_run=dry_run)

        if json:
            _output_json(result)
            return

        # Rich output
        console.print(Panel.fit(f"Merge PR #{pr_number}", title="Operation"))
        table = Table(title="Summary")
        table.add_column("Key", style="cyan")
        table.add_column("Value", style="white")
        table.add_row("Repository", repo)
        table.add_row("PR Number", str(pr_number))
        table.add_row("Strategy", st)
        table.add_row("Mergeable State", str(result.get("mergeable_state")))
        table.add_row("Head SHA", str(result.get("head_sha") or ""))
        table.add_row("Base SHA", str(result.get("base_sha") or ""))
        table.add_row("Dry Run", "Yes" if dry_run else "No")
        table.add_row("Merged", "Yes" if result.get("merged") else "No")
        message = result.get("message")
        if message:
            table.add_row("Message", str(message))
        console.print(table)

    except PermissionError as e:
        console.print(f"[red]❌ {str(e)}[/red]")
        console.print("[yellow]💡 Create a token at: https://github.com/settings/tokens[/yellow]")
        console.print("[yellow]Required scopes: repo (full control of private repositories)[/yellow]")
        raise typer.Exit(code=1)
    except RuntimeError as e:
        msg = str(e)
        if "conflicts" in msg.lower():
            console.print("[red]❌ Merge blocked: PR has merge conflicts.[/red]")
            console.print("[yellow]Resolve conflicts in the branch and try again.[/yellow]")
        else:
            console.print(f"[red]❌ {msg}[/red]")
        raise typer.Exit(code=1)
    except RateLimitExceeded as e:
        console.print(f"[red]❌ {str(e)}[/red]")
        console.print("[yellow]💡 Upgrade your token or try again after the reset time.[/yellow]")
        raise typer.Exit(code=1)
    except requests.exceptions.HTTPError as e:
        status = getattr(e.response, "status_code", None)
        if status == 404:
            console.print(f"[red]❌ PR #{pr_number} or repository {repo} not found.[/red]")
        elif status == 403:
            console.print(f"[red]❌ Insufficient permissions to merge PR.[/red]")
            console.print("[yellow]Ensure your token has repo scope and push access.[/yellow]")
        elif status == 409:
            console.print(f"[red]❌ PR #{pr_number} cannot be merged (status issue).[/red]")
            console.print("[yellow]Check if PR is already merged or has blocking conditions.[/yellow]")
        else:
            console.print(f"[red]❌ HTTP Error {status}: {e}[/red]")
        raise typer.Exit(code=1)
    except requests.exceptions.ConnectionError:
        console.print("[red]❌ Network error: Unable to reach GitHub API.[/red]")
        console.print("[yellow]Check your internet connection.[/yellow]")
        raise typer.Exit(code=1)
    except requests.exceptions.Timeout:
        console.print("[red]❌ Request timeout: GitHub API took too long to respond.[/red]")
        raise typer.Exit(code=1)
    except requests.exceptions.RequestException as e:
        console.print(f"[red]❌ Request failed: {e}[/red]")
        raise typer.Exit(code=1)
    except ValueError as e:
        console.print(f"[red]❌ Validation error: {e}[/red]")
        raise typer.Exit(code=1)


@app.command()
def issues(
    repo: str = typer.Argument(..., help="Repository in 'owner/name' format"),
    json: bool = typer.Option(False, "--json", help="Output as JSON"),
    force_refresh: bool = typer.Option(False, "--force-refresh", help="Bypass cache and force fresh API call"),
):
    """Display detailed issue metrics including open, closed, avg age, and dates."""
    svc = GitHubService()
    
    try:
        owner, name = svc._parse_repo_full_name(repo)
        issue_stats = svc.get_issue_stats(owner, name, force_refresh=force_refresh)
        
        result = {
            "repository": repo,
            "issues": issue_stats,
        }
        
        if json:
            _output_json(result)
            return
        
        # Display
        console.print(Panel.fit(f"Issue Metrics: {repo}", title="Repository"))
        
        table = Table(title="Issue Statistics")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="yellow")
        
        table.add_row("Open Issues", str(issue_stats.get("open_issues", 0)))
        table.add_row("Closed Issues", str(issue_stats.get("closed_issues", 0)))
        
        total = issue_stats.get("open_issues", 0) + issue_stats.get("closed_issues", 0)
        if total > 0:
            close_rate = (issue_stats.get("closed_issues", 0) / total) * 100
            table.add_row("Close Rate", f"{close_rate:.1f}%")
        
        oldest = issue_stats.get("oldest_open_issue_date")
        table.add_row("Oldest Open Issue", str(oldest) if oldest else "None")
        
        last_closed = issue_stats.get("last_closed_issue_date")
        table.add_row("Last Closed Issue", str(last_closed) if last_closed else "None")
        
        avg_age = issue_stats.get("avg_open_issue_age_days")
        if avg_age is not None:
            table.add_row("Avg Open Issue Age", f"{avg_age} days")
        
        console.print(table)
    
    except Exception as e:
        typer.echo(f"Error: {e}")
        raise typer.Exit(code=1)


# --------------- README Generator ---------------

@app.command()
def readme(
    repo: Optional[str] = typer.Option(None, "--repo", "-r", help="Repository path or 'owner/name' for remote"),
    preview: bool = typer.Option(False, "--preview", help="Print preview only (don't save)", is_flag=True),
    output: Optional[str] = typer.Option(None, "--output", "-o", help="Custom output file path"),
    readme_style: str = typer.Option("standard", "--template", "-t", help="README style (minimal, standard, detailed)"),
    force: bool = typer.Option(False, "--force", "-f", help="Skip confirmation and write directly", is_flag=True),
):
    """Generate professional README.md files for GitHub repositories."""
    
    try:
        # Determine repo path
        repo_path = repo or "."
        
        # Collect repository context
        console.print("[cyan]📚 Collecting repository context...[/cyan]")
        try:
            context = RepositoryContextCollector.collect_local(repo_path)
        except ValueError as e:
            console.print(f"[red]Error: {e}[/red]")
            raise typer.Exit(code=1)
        
        # Generate README content
        console.print("[cyan]✍️  Generating README content...[/cyan]")
        generator = ReadmeGenerator()
        readme_content = generator.generate(context, style=readme_style)
        
        # Preview
        console.print("\n" + "=" * 70)
        console.print("[bold cyan]README PREVIEW[/bold cyan]")
        console.print("=" * 70)
        console.print(Syntax(readme_content, "markdown", theme="monokai"))
        console.print("=" * 70)
        
        # Handle preview-only mode
        if preview:
            console.print("[green]✓ Preview complete (use without --preview to save)[/green]")
            return
        
        # Validate no overwrite (or force)
        if not force:
            if not validate_readme_not_exists(repo_path, output):
                console.print("[yellow]Cancelled.[/yellow]")
                raise typer.Exit(code=0)
        
        # Ask for confirmation
        if not force:
            confirm = typer.confirm("Write this to README.md?", default=True)
            if not confirm:
                console.print("[yellow]Cancelled.[/yellow]")
                raise typer.Exit(code=0)
        
        # Save README
        try:
            target_path = save_readme(readme_content, repo_path, output)
            console.print(f"[green]✓ README saved to {target_path}[/green]")
        except (PermissionError, ValueError) as e:
            console.print(f"[red]Error saving README: {e}[/red]")
            raise typer.Exit(code=1)
    
    except typer.Exit:
        raise
    except Exception as e:
        console.print(f"[red]Unexpected error: {e}[/red]")
        raise typer.Exit(code=1)


# --------------- Commit Message Generator ---------------

@app.command()
def commit(
    repo: Optional[str] = typer.Option(None, "--repo", "-r", help="Repository path (default: current directory)"),
    message_type: str = typer.Option("feat", "--type", help="Commit type (feat, fix, docs, chore, etc.)"),
    scope: Optional[str] = typer.Option(None, "--scope", "-s", help="Commit scope (auth, api, ui, etc.)"),
    breaking: bool = typer.Option(False, "--breaking", help="Mark as breaking change"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Show commit message without executing git commit"),
    conventional: bool = typer.Option(True, "--conventional", help="Use conventional commit format"),
    force: bool = typer.Option(False, "--force", "-f", help="Skip confirmation and commit directly"),
):
    """Generate and apply conventional commit messages."""
    
    try:
        repo_path = repo or "."
        
        # Validate git repository
        console.print("[cyan]🔍 Checking repository status...[/cyan]")
        try:
            git_status = GitStatusCollector.collect(repo_path)
        except ValueError as e:
            console.print(f"[red]Error: {e}[/red]")
            raise typer.Exit(code=1)
        
        # Check for changes
        if not git_status.has_changes:
            console.print("[yellow]⚠️  No changes detected in repository[/yellow]")
            console.print("[dim]Stage changes with 'git add' and try again[/dim]")
            raise typer.Exit(code=0)
        
        # Validate commit type
        if message_type not in ConventionalCommitGenerator.VALID_TYPES:
            console.print(f"[red]Invalid commit type: {message_type}[/red]")
            console.print(f"[yellow]Valid types: {', '.join(ConventionalCommitGenerator.VALID_TYPES)}[/yellow]")
            raise typer.Exit(code=1)
        
        # Generate commit message
        console.print("[cyan]✍️  Generating commit message...[/cyan]")
        generator = ConventionalCommitGenerator()
        commit_msg = generator.generate(
            git_status,
            commit_type=message_type,
            scope=scope,
            breaking=breaking,
            dry_run=dry_run
        )
        
        # Display message preview
        console.print("\n" + "=" * 70)
        console.print("[bold cyan]COMMIT MESSAGE[/bold cyan]")
        console.print("=" * 70)
        console.print(Syntax(commit_msg, "plaintext", theme="monokai"))
        console.print("=" * 70)
        
        # Show file changes summary
        if git_status.diff_stat:
            console.print("\n[bold cyan]CHANGES SUMMARY[/bold cyan]")
            console.print(git_status.diff_stat)
        
        # Validate message format
        if conventional:
            is_valid, error_msg = CommitMessageValidator.validate_conventional(commit_msg)
            if not is_valid:
                console.print(f"[yellow]⚠️  Warning: {error_msg}[/yellow]")
        
        # Dry-run mode
        if dry_run:
            console.print("\n[green]✓ Dry run complete[/green]")
            console.print("[dim]Run without --dry-run to execute commit[/dim]")
            return
        
        # Ask for confirmation
        if not force:
            confirm = typer.confirm("Apply this commit message?", default=True)
            if not confirm:
                console.print("[yellow]Cancelled.[/yellow]")
                raise typer.Exit(code=0)
        
        # Execute git commit
        console.print("[cyan]⏳ Applying commit...[/cyan]")
        success = apply_commit_message(repo_path, commit_msg)
        
        if success:
            console.print("[green]✓ Commit applied successfully[/green]")
        else:
            console.print("[red]Failed to apply commit[/red]")
            raise typer.Exit(code=1)
    
    except typer.Exit:
        raise
    except Exception as e:
        console.print(f"[red]Unexpected error: {e}[/red]")
        raise typer.Exit(code=1)

