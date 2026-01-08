from typing import Optional, Dict, List
from fastapi import FastAPI, Query, Request, HTTPException
from fastapi.responses import JSONResponse
import time

from devpulse.core.github import GitHubService

app = FastAPI(title="DevPulse API", version="0.1.0")

# Simple in-memory rate limiter: max 8 requests per IP per hour
RATE_LIMIT_MAX = 8
RATE_LIMIT_WINDOW = 3600  # seconds
_rate_store: Dict[str, List[float]] = {}


def _rate_check(ip: str) -> None:
    now = time.time()
    entries = _rate_store.get(ip, [])
    # prune old
    entries = [t for t in entries if now - t < RATE_LIMIT_WINDOW]
    if len(entries) >= RATE_LIMIT_MAX:
        raise HTTPException(status_code=429, detail="Rate limit exceeded. Try again later.")
    entries.append(now)
    _rate_store[ip] = entries


@app.get("/github-stats")
async def github_stats(
    request: Request,
    username: Optional[str] = Query(default=None, description="GitHub username"),
    repo: Optional[str] = Query(default=None, description="Repository in 'owner/name' format"),
    include_health: bool = Query(default=True),
    include_contributors: bool = Query(default=True),
    include_activity: bool = Query(default=True),
    top_repos_for_user: int = Query(default=3),
):
    # Rate limit per-IP
    ip = request.client.host if request.client else "unknown"
    _rate_check(ip)

    if not username and not repo:
        raise HTTPException(status_code=400, detail="Provide either 'username' or 'repo'.")
    if username and repo:
        raise HTTPException(status_code=400, detail="Provide only one of 'username' or 'repo'.")

    svc = GitHubService(user_agent="DevPulse-API/1.0")
    try:
        data = svc.get_repo_stats(
            repo=repo,
            username=username,
            include_health=include_health,
            include_contributors=include_contributors,
            include_activity=include_activity,
            top_repos_for_user=top_repos_for_user,
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Upstream error: {str(e)}")

    return JSONResponse(content=data)
