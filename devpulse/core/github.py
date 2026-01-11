import time
import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Literal
from dataclasses import dataclass
from datetime import datetime, timedelta

import requests

GITHUB_API_BASE = "https://api.github.com"
CACHE_DIR = Path.home() / ".devpulse" / "cache" / "github"
CACHE_DURATION = 600  # 10 minutes in seconds


class RateLimitExceeded(Exception):
    """Exception raised when GitHub rate limit is exceeded."""
    def __init__(self, reset_at: int, remaining: int = 0):
        self.reset_at = reset_at
        self.remaining = remaining
        # Calculate minutes until reset
        reset_time = reset_at - int(time.time())
        self.reset_minutes = max(1, (reset_time + 59) // 60)  # round up
        super().__init__(f"GitHub API rate limit exceeded. Reset in ~{self.reset_minutes} minute(s).")


class GitHubService:
    """
    Lightweight service for fetching public GitHub repository statistics.
    Features: caching, optional authentication, rate limit handling, enhanced health scoring.
    
    Authentication:
      - Set GITHUB_TOKEN env var to use token-based auth (5000 req/hour)
      - Without token: 60 requests/hour unauthenticated
    """

    def __init__(self, user_agent: str = "DevPulse-GitHubService/1.0", timeout: int = 15, use_cache: bool = True):
        self.session = requests.Session()
        self.session.headers.update({
            "Accept": "application/vnd.github+json",
            "User-Agent": user_agent,
        })
        self.timeout = timeout
        self.use_cache = use_cache
        self.token = os.getenv("GITHUB_TOKEN")
        
        # Set authorization header if token is provided
        if self.token:
            self.session.headers.update({
                "Authorization": f"token {self.token}",
            })
        
        if use_cache:
            CACHE_DIR.mkdir(parents=True, exist_ok=True)
        
        # Track rate limit info
        self.rate_limit_reset = None
        self.rate_limit_remaining = None

    # --------------- Events Models ---------------
    @dataclass
    class ParsedEvent:
        type: str
        repo: Optional[str]
        created_at: str

    # --------------- Pull Request Models ---------------
    @dataclass
    class MergeStatus:
        mergeable: Optional[bool]
        mergeable_state: Optional[str]  # clean | dirty | blocked | unstable | unknown
        ci_status: Optional[str]        # success | failure | pending | none

    @dataclass
    class PullRequest:
        number: int
        title: str
        author: Optional[str]
        base_ref: Optional[str]
        head_ref: Optional[str]
        base_sha: Optional[str]
        head_sha: Optional[str]
        updated_at: Optional[str]
        html_url: Optional[str]
        merge: "GitHubService.MergeStatus"
        commits_count: Optional[int] = None
        files_changed: Optional[int] = None

    # --------------- Helpers ---------------
    def _cache_key(self, key: str) -> Path:
        """Generate cache file path for a given key."""
        safe_key = key.replace("/", "_").replace(":", "_")
        return CACHE_DIR / f"{safe_key}.json"

    def _read_cache(self, key: str, expired_ok: bool = False) -> Optional[Dict]:
        """Read from cache. If expired_ok=True, return stale cache anyway."""
        if not self.use_cache:
            return None
        cache_file = self._cache_key(key)
        if not cache_file.exists():
            return None
        try:
            with open(cache_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            cached_at = data.get("cached_at", 0)
            age = time.time() - cached_at
            
            # Return if not expired, or if expired_ok and cache exists
            if age < CACHE_DURATION or expired_ok:
                return data.get("payload")
        except (json.JSONDecodeError, IOError):
            pass
        return None

    def _write_cache(self, key: str, payload: Dict) -> None:
        """Write data to cache."""
        if not self.use_cache:
            return
        cache_file = self._cache_key(key)
        try:
            with open(cache_file, "w", encoding="utf-8") as f:
                json.dump({"cached_at": time.time(), "payload": payload}, f)
        except IOError:
            pass

    def _get(self, url: str, params: Optional[Dict] = None, force_refresh: bool = False) -> requests.Response:
        """
        GET request with caching and rate limit handling.
        If force_refresh=True, bypass cache.
        """
        cache_key = f"{url}?{json.dumps(params or {}, sort_keys=True)}"
        
        # Check cache first (unless force_refresh)
        if not force_refresh:
            cached = self._read_cache(cache_key)
            if cached is not None:
                # Mock response from cache
                resp = requests.Response()
                resp.status_code = 200
                resp._content = json.dumps(cached).encode("utf-8")
                return resp
        
        try:
            resp = self.session.get(url, params=params or {}, timeout=self.timeout)
            
            # Extract rate limit info from headers
            if "X-RateLimit-Remaining" in resp.headers:
                self.rate_limit_remaining = int(resp.headers.get("X-RateLimit-Remaining", 0))
            if "X-RateLimit-Reset" in resp.headers:
                self.rate_limit_reset = int(resp.headers.get("X-RateLimit-Reset", 0))
            
            # Handle rate limit errors
            if resp.status_code == 403:
                # Try to read cached data for fallback
                cached = self._read_cache(cache_key, expired_ok=True)
                if cached is not None:
                    # Return stale cache instead of failing
                    resp_fallback = requests.Response()
                    resp_fallback.status_code = 200
                    resp_fallback._content = json.dumps(cached).encode("utf-8")
                    return resp_fallback
                
                # No cache available, raise rate limit exception
                reset_at = self.rate_limit_reset or int(time.time()) + 3600
                raise RateLimitExceeded(reset_at, self.rate_limit_remaining or 0)
            
            resp.raise_for_status()
            
            # Cache successful responses
            try:
                self._write_cache(cache_key, resp.json())
            except (json.JSONDecodeError, ValueError):
                pass
            
            return resp
        
        except requests.exceptions.RequestException as e:
            # On network errors, try to return stale cache
            if not force_refresh:
                cached = self._read_cache(cache_key, expired_ok=True)
                if cached is not None:
                    resp = requests.Response()
                    resp.status_code = 200
                    resp._content = json.dumps(cached).encode("utf-8")
                    return resp
            raise

    def _put(self, url: str, json_body: Optional[Dict] = None) -> requests.Response:
        """
        PUT request with rate limit handling. No caching is applied to mutations.
        """
        try:
            resp = self.session.put(url, json=json_body or {}, timeout=self.timeout)

            # Rate limit info
            if "X-RateLimit-Remaining" in resp.headers:
                self.rate_limit_remaining = int(resp.headers.get("X-RateLimit-Remaining", 0))
            if "X-RateLimit-Reset" in resp.headers:
                self.rate_limit_reset = int(resp.headers.get("X-RateLimit-Reset", 0))

            if resp.status_code == 403:
                reset_at = self.rate_limit_reset or int(time.time()) + 3600
                raise RateLimitExceeded(reset_at, self.rate_limit_remaining or 0)

            resp.raise_for_status()
            return resp
        except requests.exceptions.RequestException:
            raise

    # --------------- Public Events ---------------
    def get_user_public_events(self, username: str, per_page: int = 100, force_refresh: bool = False) -> List[Dict]:
        url = f"{GITHUB_API_BASE}/users/{username}/events/public"
        resp = self._get(url, params={"per_page": per_page}, force_refresh=force_refresh)
        return resp.json()

    @staticmethod
    def _normalize_event_type(event_type: str) -> Optional[str]:
        mapping = {
            "PushEvent": "push",
            "PullRequestEvent": "pull_request",
            "IssuesEvent": "issues",
            "IssueCommentEvent": "issue_comment",
            "WatchEvent": "stars",
            "ForkEvent": "fork",
            "CreateEvent": "create",
            "DeleteEvent": "delete",
            "ReleaseEvent": "release",
            "PullRequestReviewEvent": "pull_request_review",
            "PullRequestReviewCommentEvent": "pull_request_review_comment",
            "CommitCommentEvent": "commit_comment",
            "MemberEvent": "member",
            "PublicEvent": "public",
            "GollumEvent": "gollum",
        }
        return mapping.get(event_type)

    @staticmethod
    def _event_allowed_filter(ev_type: str, filters: Optional[List[str]]) -> bool:
        if not filters:
            return True
        synonyms = {
            "pr": "pull_request",
            "stars": "stars",
            "watch": "stars",
            "issue": "issues",
            "issue_comment": "issue_comment",
            "review": "pull_request_review",
            "review_comment": "pull_request_review_comment",
        }
        normalized_filters = set(synonyms.get(f, f) for f in filters)
        return ev_type in normalized_filters

    def parse_and_summarize_events(
        self,
        raw_events: List[Dict],
        since_days: int = 30,
        filters: Optional[List[str]] = None,
    ) -> Dict:
        # Convert to parsed events and apply window
        window_start = datetime.utcnow() - timedelta(days=since_days)
        parsed: List[GitHubService.ParsedEvent] = []
        for e in raw_events:
            etype = self._normalize_event_type(e.get("type", ""))
            if not etype:
                continue
            repo_name = (e.get("repo") or {}).get("name")
            created_at = e.get("created_at")
            if not created_at:
                continue
            try:
                created_dt = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ")
            except ValueError:
                continue
            if created_dt < window_start:
                continue
            parsed.append(GitHubService.ParsedEvent(type=etype, repo=repo_name, created_at=created_at))

        # Apply type filters
        if filters:
            parsed = [p for p in parsed if self._event_allowed_filter(p.type, filters)]

        total_events = len(parsed)
        event_counts: Dict[str, int] = {}
        repo_counts: Dict[str, int] = {}
        last_activity = None
        for p in parsed:
            event_counts[p.type] = event_counts.get(p.type, 0) + 1
            if p.repo:
                repo_counts[p.repo] = repo_counts.get(p.repo, 0) + 1
            if (last_activity is None) or (p.created_at > last_activity):
                last_activity = p.created_at

        most_active_repo = None
        if repo_counts:
            most_active_repo = max(repo_counts.items(), key=lambda x: x[1])[0]

        return {
            "total_events": total_events,
            "event_counts": event_counts,
            "active_repos": len(repo_counts.keys()),
            "last_activity": last_activity,
            "most_active_repo": most_active_repo,
        }

    def _languages_percent(self, lang_bytes: Dict[str, int]) -> Dict[str, float]:
        total = sum(lang_bytes.values())
        if not total:
            return {}
        return {k: round((v / total) * 100.0, 2) for k, v in lang_bytes.items()}

    def _parse_repo_full_name(self, repo: str) -> Tuple[str, str]:
        if "/" not in repo:
            raise ValueError("repo must be in 'owner/name' format")
        owner, name = repo.split("/", 1)
        return owner, name

    # --------------- Public API ---------------
    def get_user_repos(self, username: str, per_page: int = 30, force_refresh: bool = False) -> List[Dict]:
        url = f"{GITHUB_API_BASE}/users/{username}/repos"
        resp = self._get(url, params={"per_page": per_page, "type": "public", "sort": "updated"}, force_refresh=force_refresh)
        return resp.json()

    def get_repo_basic(self, owner: str, name: str, force_refresh: bool = False) -> Dict:
        url = f"{GITHUB_API_BASE}/repos/{owner}/{name}"
        data = self._get(url, force_refresh=force_refresh).json()
        
        # Stale/inactive detection
        pushed_at = data.get("pushed_at")
        is_stale = False
        if pushed_at:
            try:
                last_commit = datetime.strptime(pushed_at, "%Y-%m-%dT%H:%M:%SZ")
                six_months_ago = datetime.utcnow() - timedelta(days=180)
                is_stale = last_commit < six_months_ago
            except ValueError:
                is_stale = False
        
        return {
            "full_name": data.get("full_name"),
            "name": data.get("name"),
            "owner": data.get("owner", {}).get("login"),
            "stars": data.get("stargazers_count", 0),
            "forks": data.get("forks_count", 0),
            "open_issues": data.get("open_issues_count", 0),  # includes PRs
            "size_kb": data.get("size", 0),
            "default_branch": data.get("default_branch"),
            "created_at": data.get("created_at"),
            "updated_at": data.get("updated_at"),
            "last_commit_date": pushed_at,
            "license": (data.get("license") or {}).get("spdx_id") or None,
            "is_stale": is_stale,
            "watchers": data.get("watchers_count", 0),
            "description": data.get("description"),
        }

    def get_repo_languages(self, owner: str, name: str, force_refresh: bool = False) -> Dict[str, float]:
        url = f"{GITHUB_API_BASE}/repos/{owner}/{name}/languages"
        data = self._get(url, force_refresh=force_refresh).json()
        return self._languages_percent(data)

    def get_commit_count_since(self, owner: str, name: str, since_iso: str, force_refresh: bool = False) -> int:
        url = f"{GITHUB_API_BASE}/repos/{owner}/{name}/commits"
        # Fetch up to 100 commits since the timestamp; good approximation for recent activity
        resp = self._get(url, params={"since": since_iso, "per_page": 100}, force_refresh=force_refresh)
        return len(resp.json())

    def get_commit_activity(self, owner: str, name: str, force_refresh: bool = False) -> Dict:
        now = time.time()
        since_7 = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(now - 7 * 24 * 3600))
        since_30 = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(now - 30 * 24 * 3600))
        commits_7 = self.get_commit_count_since(owner, name, since_7, force_refresh=force_refresh)
        commits_30 = self.get_commit_count_since(owner, name, since_30, force_refresh=force_refresh)
        return {
            "commits_last_7_days": commits_7,
            "commits_last_30_days": commits_30,
            "active": commits_30 > 0,
        }

    def get_issue_stats(self, owner: str, name: str, force_refresh: bool = False) -> Dict:
        # Search API gives total counts without pagination
        search_base = f"{GITHUB_API_BASE}/search/issues"
        q_open_issues = f"repo:{owner}/{name} type:issue state:open"
        q_closed_issues = f"repo:{owner}/{name} type:issue state:closed"
        open_issues = self._get(search_base, params={"q": q_open_issues}, force_refresh=force_refresh).json().get("total_count", 0)
        closed_issues = self._get(search_base, params={"q": q_closed_issues}, force_refresh=force_refresh).json().get("total_count", 0)

        # Oldest open issue date and last closed issue
        issues_url = f"{GITHUB_API_BASE}/repos/{owner}/{name}/issues"
        oldest_open = None
        last_closed = None
        avg_age_days = None
        
        try:
            open_data = self._get(issues_url, params={"state": "open", "sort": "created", "direction": "asc", "per_page": 1}, force_refresh=force_refresh).json()
            if open_data:
                oldest_open = open_data[0].get("created_at")
        except requests.HTTPError:
            pass
        
        try:
            closed_data = self._get(issues_url, params={"state": "closed", "sort": "updated", "direction": "desc", "per_page": 1}, force_refresh=force_refresh).json()
            if closed_data:
                last_closed = closed_data[0].get("closed_at")
        except requests.HTTPError:
            pass
        
        # Calculate average age of open issues
        if oldest_open:
            try:
                oldest_dt = datetime.strptime(oldest_open, "%Y-%m-%dT%H:%M:%SZ")
                avg_age_days = (datetime.utcnow() - oldest_dt).days
            except ValueError:
                pass

        return {
            "open_issues": open_issues,
            "closed_issues": closed_issues,
            "oldest_open_issue_date": oldest_open,
            "last_closed_issue_date": last_closed,
            "avg_open_issue_age_days": avg_age_days,
        }

    def get_pr_stats(self, owner: str, name: str, force_refresh: bool = False) -> Dict:
        search_base = f"{GITHUB_API_BASE}/search/issues"
        q_open_prs = f"repo:{owner}/{name} type:pr state:open"
        q_merged_prs = f"repo:{owner}/{name} type:pr is:merged"
        open_prs = self._get(search_base, params={"q": q_open_prs}, force_refresh=force_refresh).json().get("total_count", 0)
        merged_prs = self._get(search_base, params={"q": q_merged_prs}, force_refresh=force_refresh).json().get("total_count", 0)

        # Approximate average merge time based on last 50 closed PRs
        pulls_url = f"{GITHUB_API_BASE}/repos/{owner}/{name}/pulls"
        closed = self._get(pulls_url, params={"state": "closed", "per_page": 50, "sort": "updated", "direction": "desc"}, force_refresh=force_refresh).json()
        durations: List[float] = []
        from datetime import datetime

        def parse(dt: Optional[str]) -> Optional[datetime]:
            if not dt:
                return None
            return datetime.strptime(dt, "%Y-%m-%dT%H:%M:%SZ")

        for pr in closed:
            merged_at = pr.get("merged_at")
            created_at = pr.get("created_at")
            if merged_at and created_at:
                m = parse(merged_at)
                c = parse(created_at)
                if m and c:
                    durations.append((m - c).total_seconds())
        avg_merge_time_hours = round((sum(durations) / len(durations)) / 3600, 2) if durations else None

        return {
            "open_pull_requests": open_prs,
            "merged_pull_requests": merged_prs,
            "avg_merge_time_hours": avg_merge_time_hours,
        }

    # --------------- Pull Requests API ---------------
    def _combined_status(self, owner: str, name: str, sha: str, force_refresh: bool = False) -> Optional[str]:
        """Return combined CI status for a commit SHA (success|failure|pending|none)."""
        url = f"{GITHUB_API_BASE}/repos/{owner}/{name}/commits/{sha}/status"
        try:
            data = self._get(url, force_refresh=force_refresh).json()
            state = data.get("state")  # success | failure | pending | null
            return state or "none"
        except requests.HTTPError:
            return None

    def _parse_merge_status(self, pr_data: Dict, owner: str, name: str, force_refresh: bool = False) -> "GitHubService.MergeStatus":
        mergeable = pr_data.get("mergeable")
        mergeable_state = pr_data.get("mergeable_state")
        head_sha = (pr_data.get("head") or {}).get("sha")
        ci_status = self._combined_status(owner, name, head_sha, force_refresh=force_refresh) if head_sha else None
        return GitHubService.MergeStatus(
            mergeable=mergeable,
            mergeable_state=mergeable_state,
            ci_status=ci_status,
        )

    def get_pull_request(self, owner: str, name: str, number: int, force_refresh: bool = False) -> "GitHubService.PullRequest":
        """
        Fetch a single pull request with mergeability and summary info.
        """
        url = f"{GITHUB_API_BASE}/repos/{owner}/{name}/pulls/{number}"
        pr = self._get(url, force_refresh=force_refresh).json()

        files_url = f"{GITHUB_API_BASE}/repos/{owner}/{name}/pulls/{number}/files"
        files = self._get(files_url, params={"per_page": 100}, force_refresh=force_refresh).json()
        files_changed = len(files) if isinstance(files, list) else None

        ms = self._parse_merge_status(pr, owner, name, force_refresh=force_refresh)

        return GitHubService.PullRequest(
            number=pr.get("number"),
            title=pr.get("title"),
            author=(pr.get("user") or {}).get("login"),
            base_ref=(pr.get("base") or {}).get("ref"),
            head_ref=(pr.get("head") or {}).get("ref"),
            base_sha=(pr.get("base") or {}).get("sha"),
            head_sha=(pr.get("head") or {}).get("sha"),
            updated_at=pr.get("updated_at"),
            html_url=pr.get("html_url"),
            merge=ms,
            commits_count=pr.get("commits"),
            files_changed=files_changed,
        )

    def list_pull_requests(
        self,
        owner: str,
        name: str,
        state: Literal["open", "closed", "all"] = "open",
        force_refresh: bool = False,
    ) -> List["GitHubService.PullRequest"]:
        """
        List PRs for a repository and include mergeability/CI status for each.
        """
        pulls_url = f"{GITHUB_API_BASE}/repos/{owner}/{name}/pulls"
        pr_list = self._get(pulls_url, params={"state": state, "per_page": 50, "sort": "updated", "direction": "desc"}, force_refresh=force_refresh).json()
        results: List[GitHubService.PullRequest] = []
        for pr in pr_list:
            number = pr.get("number")
            # Fetch detailed PR to obtain mergeable fields
            detailed = self._get(f"{GITHUB_API_BASE}/repos/{owner}/{name}/pulls/{number}", force_refresh=force_refresh).json()
            ms = self._parse_merge_status(detailed, owner, name, force_refresh=force_refresh)
            results.append(GitHubService.PullRequest(
                number=number,
                title=pr.get("title"),
                author=(pr.get("user") or {}).get("login"),
                base_ref=(pr.get("base") or {}).get("ref"),
                head_ref=(pr.get("head") or {}).get("ref"),
                base_sha=(pr.get("base") or {}).get("sha"),
                head_sha=(pr.get("head") or {}).get("sha"),
                updated_at=pr.get("updated_at"),
                html_url=pr.get("html_url"),
                merge=ms,
            ))
        return results

    def _check_permissions(self, owner: str, name: str) -> bool:
        """
        Validate authenticated user's permissions on the repo.
        Requires token; returns True if user has push/maintain/admin permissions.
        """
        url = f"{GITHUB_API_BASE}/repos/{owner}/{name}"
        data = self._get(url, force_refresh=True).json()
        perms = data.get("permissions") or {}
        return bool(perms.get("push") or perms.get("maintain") or perms.get("admin"))

    def merge_pull_request(
        self,
        owner: str,
        name: str,
        number: int,
        strategy: Literal["merge", "squash", "rebase"] = "squash",
        confirm: bool = False,
        force_checks: bool = False,
        dry_run: bool = False,
    ) -> Dict:
        """
        Merge a PR safely. Requires authentication and confirmation. Refuses conflicts.
        """
        if not self.token:
            raise PermissionError(
                "Authentication required. Set GITHUB_TOKEN with repo permissions to merge pull requests."
            )

        # Verify permissions on repo
        if not self._check_permissions(owner, name):
            raise PermissionError(
                "Authentication required. Set GITHUB_TOKEN with repo permissions to merge pull requests."
            )

        # Fetch PR detail and current status
        pr = self.get_pull_request(owner, name, number, force_refresh=True)

        # Conflict detection
        mergeable_state = (pr.merge.mergeable_state or "unknown").lower()
        if mergeable_state == "dirty":
            raise RuntimeError(f"PR #{number} has merge conflicts and cannot be merged.")

        # CI failing
        if mergeable_state == "blocked" and not force_checks:
            raise RuntimeError("Checks are failing. Use --force to override (conflicts still refuse).")

        result = {
            "repo": f"{owner}/{name}",
            "pr_number": number,
            "mergeable": bool(pr.merge.mergeable),
            "mergeable_state": mergeable_state,
            "head_sha": pr.head_sha,
            "base_sha": pr.base_sha,
            "merged": False,
            "strategy": strategy,
            "dry_run": dry_run,
        }

        if dry_run:
            return result

        if not confirm:
            raise RuntimeError("Merge requires --confirm flag.")

        # Perform merge via GitHub API (guard with current head SHA)
        merge_url = f"{GITHUB_API_BASE}/repos/{owner}/{name}/pulls/{number}/merge"
        body = {"merge_method": strategy}
        if pr.head_sha:
            body["sha"] = pr.head_sha
        resp = self._put(merge_url, json_body=body).json()

        merged = bool(resp.get("merged"))
        message = resp.get("message")
        result["merged"] = merged
        result["message"] = message
        return result

    def get_contributors(self, owner: str, name: str, top_n: int = 10, force_refresh: bool = False) -> Dict:
        url = f"{GITHUB_API_BASE}/repos/{owner}/{name}/contributors"
        contributors = self._get(url, params={"per_page": 100}, force_refresh=force_refresh).json()  # first page only to stay within limits
        total = len(contributors)
        total_commits = sum(c.get("contributions", 0) for c in contributors)
        
        top_sorted = sorted(contributors, key=lambda c: c.get("contributions", 0), reverse=True)[:top_n]
        top_list = [
            {
                "login": c.get("login"),
                "contributions": c.get("contributions", 0),
                "percentage": round((c.get("contributions", 0) / total_commits * 100), 2) if total_commits > 0 else 0,
            }
            for c in top_sorted
        ]
        return {
            "total_contributors": total,
            "total_commits": total_commits,
            "top_contributors": top_list,
        }

    def compute_health_score(self, basic: Dict, activity: Dict, issues: Dict, prs: Dict, contributors: Dict) -> int:
        """
        Enhanced health score calculation (0-100).
        Factors: stars, forks, contributors, recent commits, open/closed issues, merged PRs, staleness.
        """
        score = 0
        
        # Stars: 0-15 points (logarithmic scale)
        stars = basic.get("stars", 0)
        if stars > 0:
            import math
            score += min(15, int(math.log10(stars + 1) * 5))
        
        # Forks: 0-10 points (logarithmic scale)
        forks = basic.get("forks", 0)
        if forks > 0:
            import math
            score += min(10, int(math.log10(forks + 1) * 4))
        
        # Recent activity: 0-20 points
        commits_30 = activity.get("commits_last_30_days", 0)
        score += min(20, int(commits_30 * 1.5))
        
        # Issue health: 0-20 points (ratio of closed to total)
        open_issues = issues.get("open_issues", 0)
        closed_issues = issues.get("closed_issues", 0)
        total_issues = open_issues + closed_issues
        if total_issues > 0:
            closed_ratio = closed_issues / total_issues
            score += int(closed_ratio * 20)
        else:
            score += 10  # No issues is neutral
        
        # PR activity: 0-15 points
        merged_prs = prs.get("merged_pull_requests", 0)
        score += min(15, int(merged_prs / 3))
        
        # Contributors: 0-15 points
        total_contrib = contributors.get("total_contributors", 0)
        score += min(15, total_contrib)
        
        # Staleness penalty: -10 if stale
        if basic.get("is_stale", False):
            score -= 10
        
        return max(0, min(100, score))

    def get_repo_stats(
        self,
        repo: Optional[str] = None,
        username: Optional[str] = None,
        include_health: bool = True,
        include_contributors: bool = True,
        include_activity: bool = True,
        top_repos_for_user: int = 3,
        force_refresh: bool = False,
    ) -> Dict:
        """
        Fetch statistics for a single repo or for top repos of a user.
        If `repo` is provided, returns stats for that repo.
        If `username` is provided, returns stats for top N repos by stars.
        """
        if not repo and not username:
            raise ValueError("Provide either 'repo' (owner/name) or 'username'.")
        if repo and username:
            raise ValueError("Provide only one of 'repo' or 'username'.")

        def collect_for(owner: str, name: str) -> Dict:
            basic = self.get_repo_basic(owner, name, force_refresh=force_refresh)
            languages = self.get_repo_languages(owner, name, force_refresh=force_refresh)
            activity = self.get_commit_activity(owner, name, force_refresh=force_refresh) if include_activity else {}
            issues = self.get_issue_stats(owner, name, force_refresh=force_refresh)
            prs = self.get_pr_stats(owner, name, force_refresh=force_refresh)
            contributors = self.get_contributors(owner, name, force_refresh=force_refresh) if include_contributors else {}
            health = self.compute_health_score(basic, activity, issues, prs, contributors) if include_health else None
            return {
                "repository": basic,
                "languages": languages,
                "activity": activity,
                "issues": issues,
                "pull_requests": prs,
                "contributors": contributors,
                "license": basic.get("license"),
                "health_score": health,
            }

        if repo:
            owner, name = self._parse_repo_full_name(repo)
            return {"target": {"type": "repo", "owner": owner, "name": name}, "stats": collect_for(owner, name)}
        else:
            repos = self.get_user_repos(username, force_refresh=force_refresh)
            # Top N by stars
            top = sorted(repos, key=lambda r: r.get("stargazers_count", 0), reverse=True)[:top_repos_for_user]
            stats_list = []
            for r in top:
                owner = r.get("owner", {}).get("login")
                name = r.get("name")
                if owner and name:
                    stats_list.append(collect_for(owner, name))
            return {"target": {"type": "user", "username": username}, "repos": stats_list}
