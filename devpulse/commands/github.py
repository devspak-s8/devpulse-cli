import typer
import json as json_lib
from typing import Optional, List
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

from devpulse.core.github import GitHubService, RateLimitExceeded

app = typer.Typer(help="GitHub integration and statistics")
console = Console()


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
    include_health: bool = typer.Option(True, "--health/--no-health", help="Include health score"),
    include_contributors: bool = typer.Option(True, "--contributors/--no-contributors", help="Include contributors section"),
    include_activity: bool = typer.Option(True, "--activity/--no-activity", help="Include commit activity"),
    top_repos_for_user: int = typer.Option(3, "--top", help="Number of top repos for a user"),
    json: bool = typer.Option(False, "--json", help="Output as JSON"),
    include: Optional[str] = typer.Option(None, "--include", help="Comma-separated sections to include (contributors,issues,activity,languages,health,prs)"),
    force_refresh: bool = typer.Option(False, "--force-refresh", help="Bypass cache and force fresh API call"),
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
    json: bool = typer.Option(False, "--json", help="Output as JSON"),
    force_refresh: bool = typer.Option(False, "--force-refresh", help="Bypass cache and force fresh API call"),
):
    """Display commit activity and contribution summary for a user."""
    svc = GitHubService()
    
    try:
        # Get user's repos and aggregate activity
        repos = svc.get_user_repos(username, per_page=100, force_refresh=force_refresh)
        
        total_commits_7d = 0
        total_commits_30d = 0
        active_repos = 0
        
        repo_activity = []
        for r in repos[:10]:  # Limit to top 10 to avoid rate limits
            owner = r.get("owner", {}).get("login")
            name = r.get("name")
            if owner and name:
                try:
                    act = svc.get_commit_activity(owner, name, force_refresh=force_refresh)
                    total_commits_7d += act.get("commits_last_7_days", 0)
                    total_commits_30d += act.get("commits_last_30_days", 0)
                    if act.get("active"):
                        active_repos += 1
                    repo_activity.append({
                        "repo": f"{owner}/{name}",
                        "commits_7d": act.get("commits_last_7_days", 0),
                        "commits_30d": act.get("commits_last_30_days", 0),
                    })
                except Exception:
                    pass
        
        result = {
            "username": username,
            "total_repos": len(repos),
            "active_repos": active_repos,
            "total_commits_last_7_days": total_commits_7d,
            "total_commits_last_30_days": total_commits_30d,
            "repo_activity": repo_activity,
        }
        
        if json:
            _output_json(result)
            return
        
        # Display
        console.print(Panel.fit(f"Activity Summary for: {username}", title="GitHub User"))
        
        table = Table(title="Overall Activity")
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="yellow")
        table.add_row("Total Repositories", str(result["total_repos"]))
        table.add_row("Active Repos (30d)", str(result["active_repos"]))
        table.add_row("Commits (7 days)", str(result["total_commits_last_7_days"]))
        table.add_row("Commits (30 days)", str(result["total_commits_last_30_days"]))
        console.print(table)
        
        if repo_activity:
            rt = Table(title="Repository Activity (Top 10)")
            rt.add_column("Repository", style="green")
            rt.add_column("Commits (7d)", style="blue")
            rt.add_column("Commits (30d)", style="magenta")
            for ra in repo_activity:
                rt.add_row(ra["repo"], str(ra["commits_7d"]), str(ra["commits_30d"]))
            console.print(rt)
    
    except Exception as e:
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
