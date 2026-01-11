# DevPulse CLI - Comprehensive Documentation

Complete guide to DevPulse CLI features, commands, and GitHub integration.

---

## Table of Contents

1. [Installation](#installation)
2. [Quick Start](#quick-start)
3. [GitHub Integration](#github-integration)
4. [GitHub PR Management](#github-pr-management)
5. [Authentication & Security](#authentication--security)
6. [Error Handling & Validation](#error-handling--validation)
7. [Command Reference](#command-reference)
8. [Examples](#examples)
9. [Troubleshooting](#troubleshooting)

---

## Installation

### PyPI Installation

```bash
# Standard installation
pip install devpulse-cli

# Full installation with all optional dependencies
pip install devpulse-cli[full]

# Specific feature sets
pip install devpulse-cli[ai]      # AI features
pip install devpulse-cli[data]    # Data analysis
pip install devpulse-cli[http]    # GitHub integration
```

### Development Installation

```bash
git clone https://github.com/devspak-s8/devpulse-cli.git
cd devpulse-cli
pip install -e .
```

---

## Quick Start

### Getting Help

```bash
devpulse --help                              # Show all commands
devpulse github --help                       # GitHub command help
devpulse github pr --help                    # PR subcommand help
devpulse github prs --help                   # Specific command help
```

### Basic Usage

```bash
# List open PRs in a repository
devpulse github prs owner/repo

# View a specific PR
devpulse github pr view owner/repo 123

# Merge a PR (with confirmation)
devpulse github pr merge owner/repo 123 --strategy squash --confirm

# Dry-run merge (preview without executing)
devpulse github pr merge owner/repo 123 --dry-run --json
```

---

## GitHub Integration

### Repository Statistics

```bash
# Get repository stats
devpulse github stats --repo torvalds/linux

# Include health score
devpulse github stats --repo microsoft/vscode --include health,contributors

# JSON output
devpulse github stats --repo nodejs/node --json
```

### User Activity Tracking

```bash
# Get user public events
devpulse github activity torvalds

# Filter by event type
devpulse github activity torvalds --events push,pr,issues

# Time window
devpulse github activity torvalds --since 7d     # Last 7 days
devpulse github activity torvalds --since 30d    # Last 30 days

# JSON output with debug info
devpulse github activity torvalds --json --debug
```

### Repository Language Analysis

```bash
# Language distribution
devpulse github top-languages owner/repo

# JSON output
devpulse github top-languages owner/repo --json
```

### Contributor Analysis

```bash
# List top contributors
devpulse github contributors owner/repo

# Top 5 contributors
devpulse github contributors owner/repo --top 5

# JSON output
devpulse github contributors owner/repo --json
```

---

## GitHub PR Management

### ✨ NEW: List Pull Requests

#### Command

```bash
devpulse github prs <owner/repo> [OPTIONS]
```

#### Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--state` | open\|closed\|all | open | PR state filter |
| `--conflicts-only` | flag | false | Show only conflicted PRs |
| `--json` | flag | false | JSON output |
| `--debug` | flag | false | Show API metadata |
| `--force-refresh` | flag | false | Bypass cache |

#### Examples

```bash
# List open PRs
devpulse github prs owner/repo

# List all PRs (open + closed)
devpulse github prs owner/repo --state all

# Show only PRs with conflicts
devpulse github prs owner/repo --conflicts-only

# JSON output with debug info
devpulse github prs owner/repo --json --debug

# Bypass cache
devpulse github prs owner/repo --force-refresh
```

#### Output

**Rich Table Format:**
- PR Number
- Title
- Author
- Base → Head (branch refs)
- Mergeable State (clean/dirty/blocked/unknown)
- CI Status (success/failure/pending/none)
- Last Updated
- Head SHA

**JSON Format:**
```json
{
  "repository": "owner/repo",
  "state": "open",
  "pull_requests": [
    {
      "repo": "owner/repo",
      "pr_number": 123,
      "title": "Fix authentication bug",
      "author": "alice",
      "base": "main",
      "head": "feature/auth-fix",
      "mergeable": true,
      "mergeable_state": "clean",
      "ci_status": "success",
      "updated_at": "2026-01-11T10:30:00Z",
      "head_sha": "abc123def456"
    }
  ]
}
```

---

### ✨ NEW: View Single PR

#### Command

```bash
devpulse github pr view <owner/repo> <pr_number> [OPTIONS]
```

#### Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--json` | flag | false | JSON output |
| `--debug` | flag | false | Show API metadata |
| `--force-refresh` | flag | false | Bypass cache |

#### Examples

```bash
# View PR details
devpulse github pr view owner/repo 123

# JSON format
devpulse github pr view owner/repo 123 --json

# With debug info
devpulse github pr view owner/repo 123 --debug

# Fresh data (no cache)
devpulse github pr view owner/repo 123 --force-refresh
```

#### Output

**Rich Table Format:**
- Title
- Author
- Base & Head branches
- Base & Head SHAs
- Commit count
- Files changed
- Mergeable state
- CI status

**JSON Format:**
```json
{
  "repo": "owner/repo",
  "pr_number": 123,
  "title": "Add GitHub PR management",
  "author": "alice",
  "files_changed": 5,
  "commit_count": 3,
  "base_sha": "base123abc",
  "head_sha": "head456def",
  "mergeable": true,
  "mergeable_state": "clean",
  "ci_status": "success"
}
```

---

### ✨ NEW: Merge Pull Request

#### Command

```bash
devpulse github pr merge <owner/repo> <pr_number> [OPTIONS]
```

#### Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--strategy` | merge\|squash\|rebase | squash | Merge strategy |
| `--confirm` | flag | false | REQUIRED for actual merge |
| `--force` | flag | false | Override failing checks |
| `--dry-run` | flag | false | Preview without merge |
| `--json` | flag | false | JSON output |

#### Examples

```bash
# Dry-run (preview only)
devpulse github pr merge owner/repo 123 --dry-run --json

# Squash merge (default)
devpulse github pr merge owner/repo 123 --strategy squash --confirm

# Full merge (preserve commits)
devpulse github pr merge owner/repo 123 --strategy merge --confirm

# Rebase merge
devpulse github pr merge owner/repo 123 --strategy rebase --confirm

# Override failing CI (conflicts still block)
devpulse github pr merge owner/repo 123 --confirm --force

# Interactive token prompt (if GITHUB_TOKEN not set)
devpulse github pr merge owner/repo 123 --confirm
# You will be prompted: Enter GITHUB_TOKEN with repo scope (hidden input)
```

#### Output

**Rich Table Format:**
- Repository
- PR Number
- Strategy
- Mergeable State
- Head & Base SHAs
- Dry Run status
- Merged status
- Merge message

**JSON Format:**
```json
{
  "repo": "owner/repo",
  "pr_number": 123,
  "mergeable": true,
  "mergeable_state": "clean",
  "head_sha": "abc123",
  "base_sha": "def456",
  "merged": true,
  "strategy": "squash",
  "dry_run": false,
  "message": "Pull Request successfully merged"
}
```

---

## Authentication & Security

### GitHub Token Setup

#### Option 1: Environment Variable

```bash
# Set in shell
export GITHUB_TOKEN="ghp_your_token_here"

# Or in .env file
echo "GITHUB_TOKEN=ghp_your_token_here" >> .env
```

#### Option 2: Interactive Prompt

When running merge operations without GITHUB_TOKEN:

```bash
devpulse github pr merge owner/repo 123 --confirm

# Output:
# 🔐 Authentication required for this operation.
# A GitHub token with 'repo' scope is needed.
# Create one at: https://github.com/settings/tokens
# 
# Enter GITHUB_TOKEN with repo scope: ••••••••••••••••••
# ✓ Token set.
```

**Token input is hidden** (not echoed to terminal).

### Token Requirements

**Required for merge operations:**
- Scope: `repo` (Full control of private repositories)
- Permissions needed:
  - `push` — merge changes
  - `pull_requests` — access PR data
  
**For read-only operations (list/view):**
- No token required (public repos)
- Token recommended for higher rate limits (5000/hour vs 60/hour)

### Token Creation

1. Visit: https://github.com/settings/tokens/new
2. Select scopes:
   - `repo` — Full control of private repositories
3. Generate token
4. Save securely (never commit to git)

---

## Error Handling & Validation

### Input Validation

#### Repository Format
```bash
# ✓ Valid
devpulse github prs owner/repo

# ✗ Invalid
devpulse github prs owner         # Missing repo name
devpulse github prs ownerrepo     # Missing separator
```

**Error Message:**
```
❌ Repository must be in 'owner/name' format.
Example: devpulse github prs octocat/Hello-World
```

#### PR Number Validation
```bash
# ✓ Valid
devpulse github pr view owner/repo 123

# ✗ Invalid
devpulse github pr view owner/repo -5    # Negative number
devpulse github pr view owner/repo 0     # Zero not allowed
```

**Error Message:**
```
❌ PR number must be a positive integer.
```

#### Strategy Validation
```bash
# ✓ Valid
devpulse github pr merge owner/repo 123 --strategy squash --confirm

# ✗ Invalid
devpulse github pr merge owner/repo 123 --strategy invalid --confirm
```

**Error Message:**
```
❌ Invalid --strategy option.
Use one of: merge | squash | rebase
```

### Network & API Errors

#### Repository Not Found
```
❌ Repository not found: owner/repo
Please check the owner and repository name.
```

#### Access Denied
```
❌ Access denied to repository: owner/repo
Ensure the repository is public or you have access.
```

#### Pull Request Not Found
```
❌ PR #999 not found in owner/repo
Check the PR number and repository name.
```

#### Network Issues
```
❌ Network error: Unable to reach GitHub API.
Check your internet connection and try again.
```

#### Request Timeout
```
❌ Request timeout: GitHub API took too long to respond.
Try again in a moment or use --force-refresh.
```

### Rate Limit Errors

#### Unauthenticated (60/hour)
```
❌ GitHub API rate limit exceeded. Reset in ~10 minute(s).
💡 Tip: Set GITHUB_TOKEN with repo scope to increase rate limit to 5000/hour.
Create a token at: https://github.com/settings/tokens
```

#### Authenticated (5000/hour)
```
❌ GitHub API rate limit exceeded. Reset in ~45 minute(s).
💡 Upgrade your token or try again after the reset time.
```

### Merge-Specific Errors

#### Merge Conflicts (BLOCKED)
```
❌ Merge blocked: PR has merge conflicts.
Resolve conflicts in the branch and try again.
```

PR with `mergeable_state: dirty` cannot be merged. Requires manual conflict resolution.

#### Insufficient Permissions
```
❌ Insufficient permissions to merge PR.
Ensure your token has repo scope and push access.
```

Token must have `push` or `maintain` permissions.

#### Authentication Required
```
❌ Authentication required.
Set GITHUB_TOKEN with repo scope to merge pull requests.
Create a token at: https://github.com/settings/tokens
```

#### CI Checks Failing (but no conflicts)
```
⚠️ Checks are failing on this PR.
Use --force to override (conflicts still refuse).
```

Use `--force` to merge despite failing CI. **Conflicts always block** even with `--force`.

---

## Command Reference

### All GitHub Commands

```bash
# Statistics & Analytics
devpulse github stats --repo owner/name
devpulse github activity username
devpulse github top-languages owner/repo
devpulse github contributors owner/repo

# Pull Request Management ✨ NEW
devpulse github prs owner/repo
devpulse github pr view owner/repo <number>
devpulse github pr merge owner/repo <number> --confirm
```

### Global Options

```bash
--json                    # JSON output (all commands)
--debug                   # Show API metadata
--force-refresh           # Bypass cache
--help                    # Show command help
```

---

## Examples

### Workflow: Review and Merge a PR

```bash
# 1. List open PRs
devpulse github prs owner/repo

# 2. View PR details
devpulse github pr view owner/repo 42

# 3. Check conflicts
# If mergeable_state is "dirty", conflict exists

# 4. Dry-run merge
devpulse github pr merge owner/repo 42 --dry-run --json

# 5. Merge PR (if safe)
devpulse github pr merge owner/repo 42 --strategy squash --confirm
```

### Workflow: Find and Merge Conflicted PRs

```bash
# List only PRs with conflicts
devpulse github prs owner/repo --conflicts-only

# View specific conflicted PR
devpulse github pr view owner/repo 99

# Attempt merge (will fail safely if conflicts exist)
devpulse github pr merge owner/repo 99 --confirm
# Output: ❌ PR #99 has merge conflicts and cannot be merged.
```

### Workflow: Bulk Analysis (JSON)

```bash
# Get all PR data as JSON
devpulse github prs owner/repo --state all --json > prs.json

# Parse with jq
cat prs.json | jq '.pull_requests | length'  # Total PRs
cat prs.json | jq '.pull_requests[] | select(.mergeable_state=="dirty")'  # Conflicted
```

### Workflow: Monitor CI Status

```bash
# Check PRs with failing CI
devpulse github prs owner/repo --json | jq '.pull_requests[] | select(.ci_status=="failure")'

# View specific PR's CI status
devpulse github pr view owner/repo 123 --json | jq '.ci_status'
```

---

## Troubleshooting

### "Token cannot be empty"

When prompted for GITHUB_TOKEN, pressing Enter without input:

```
❌ Token cannot be empty.
Please try again.
```

**Solution:** Paste your token when prompted (input is hidden).

### "Authentication required. Set GITHUB_TOKEN..."

Merge attempted without token:

```
❌ Authentication required.
Set GITHUB_TOKEN with repo scope to merge pull requests.
```

**Solution:**
```bash
export GITHUB_TOKEN="your_token_here"
devpulse github pr merge owner/repo 123 --confirm
```

Or let CLI prompt:
```bash
devpulse github pr merge owner/repo 123 --confirm
# CLI will prompt for token interactively
```

### "Repository not found"

```
❌ Repository not found: typo/reop
Please check the owner and repository name.
```

**Solution:** Verify repo exists and is spelled correctly.

### "Merge requires --confirm flag"

Attempted merge without confirmation:

```
❌ Merge requires --confirm flag.
```

**Solution:** Add `--confirm` flag:
```bash
devpulse github pr merge owner/repo 123 --strategy squash --confirm
```

### "PR has merge conflicts"

```
❌ Merge blocked: PR has merge conflicts.
Resolve conflicts in the branch and try again.
```

**Solution:** 
1. Resolve conflicts in branch
2. Push updates
3. Try merge again

### Rate Limit Exceeded

```
❌ GitHub API rate limit exceeded. Reset in ~10 minute(s).
💡 Tip: Set GITHUB_TOKEN with repo scope to increase rate limit.
```

**Solution:**
```bash
export GITHUB_TOKEN="your_token_here"
```

Authenticated requests get 5000/hour instead of 60/hour.

### Command Not Found

```
devpulse: command not found
```

**Solution:**
```bash
# Install devpulse-cli
pip install devpulse-cli

# Or use module path
python -m devpulse.cli github prs owner/repo
```

---

## Version Information

- **Version:** 0.2.1
- **Release Date:** January 11, 2026
- **Python Requirement:** >= 3.9
- **Status:** Beta

---

## Support & Feedback

For issues or feature requests:
- GitHub: https://github.com/devspak-s8/devpulse-cli/issues
- Documentation: https://github.com/devspak-s8/devpulse-cli

---

**Last Updated:** January 11, 2026
