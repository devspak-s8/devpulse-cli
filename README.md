# DevPulse CLI

A comprehensive command-line tool for developer productivity tracking, system monitoring, and GitHub analytics.

## Features

### Core Productivity
- **Track** - Time tracking and task management
- **Stats** - Analytics and productivity statistics
- **Health** - Real-time system monitoring and process management
- **Logs** - Log analysis and search capabilities
- **Secrets** - Security scanning for exposed credentials
- **Sync** - Cloud data synchronization
- **AI** - AI-powered productivity insights

### Time & Focus Management
- **Timer** - Pomodoro and custom interval timers
- **Focus** - Distraction-free focus sessions with website blocking
- **Breaks** - Scheduled break reminders and tracking
- **Habits** - Daily habit tracking and streak monitoring

### Organization & Reporting
- **Project** - Multi-project management and context switching
- **Notes** - Integrated note-taking system
- **Report** - Automated productivity reports (daily, weekly, monthly)
- **Dashboard** - Real-time productivity metrics dashboard

### GitHub Integration
- **GitHub Stats** - Repository statistics and health scoring
- **GitHub Activity** - Public user activity tracking and event analysis
- **GitHub Contributors** - Contributor analysis and rankings
- **GitHub Issues** - Issue metrics and trend analysis
- **GitHub Pull Requests** - List, view, and merge PRs with conflict detection and safe merge operations

### Data Management
- **Config** - Configuration management
- **Export** - Multi-format data export (CSV, JSON, Excel, PDF)

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

## Quick Start

### Time Tracking

```bash
# Start tracking a task
devpulse track start "Implement authentication feature"

# Check current status
devpulse track status

# Stop tracking
devpulse track stop

# View today's sessions
devpulse track list --today
```

### System Monitoring

```bash
# Check system health
devpulse health check

# Monitor specific services
devpulse health check --service cpu
devpulse health check --service memory

# View top processes
devpulse health processes --top 10 --sort memory

# Set up alerts
devpulse health alert --cpu 80 --memory 85
```

### GitHub Analytics

```bash
# Repository statistics
devpulse github stats --repo torvalds/linux

# User activity tracking
devpulse github activity torvalds
devpulse github activity torvalds --events push,pr,issues --since 7d

# Export as JSON
devpulse github activity torvalds --json --force-refresh

# Debug mode with rate limit info
devpulse github activity torvalds --debug

# Repository health analysis
devpulse github stats --repo microsoft/vscode --include health,contributors

# List pull requests
devpulse github prs owner/repo                           # List open PRs
devpulse github prs owner/repo --state all              # All PRs (open + closed)
devpulse github prs owner/repo --conflicts-only         # Only conflicted PRs
devpulse github prs owner/repo --json                   # JSON output

# View single PR details
devpulse github pr view owner/repo 123                  # View PR #123
devpulse github pr view owner/repo 123 --json           # JSON format

# Merge a pull request (interactive auth prompt)
devpulse github pr merge owner/repo 123 --dry-run       # Preview merge
devpulse github pr merge owner/repo 123 --strategy squash --confirm  # Squash merge
devpulse github pr merge owner/repo 123 --strategy merge --confirm   # Full merge
devpulse github pr merge owner/repo 123 --confirm --force            # Override failing checks
```

### Productivity Reports

```bash
# Generate daily report
devpulse report daily

# Weekly summary
devpulse report weekly --format html --output report.html

# Export analytics
devpulse stats show --period month
devpulse export all --format json --output backup.json
```

## Configuration

### Environment Variables

```bash
# GitHub API authentication (recommended for higher rate limits)
export GITHUB_TOKEN="your_personal_access_token"

# Authenticated: 5000 requests/hour
# Unauthenticated: 60 requests/hour
```

### Global Settings

```bash
# View current configuration
devpulse config show

# Set preferences
devpulse config set theme dark
devpulse config set timezone UTC
```

## Architecture

### Key Components

- **CLI Layer** - Typer-based command interface with Rich formatting
- **Core Services** - Business logic and data processing
- **GitHub Client** - HTTP client with caching, rate limiting, and fallback
- **Storage** - SQLite database for local data persistence
- **Cache System** - Request caching with configurable TTL and stale fallback

### GitHub Integration Features

- HTTP caching with 10-minute default TTL
- Automatic stale cache fallback on network errors
- Rate limit detection and user-friendly error messages
- Optional GitHub token authentication
- Configurable request timeouts
- Debug mode for API inspection

## Testing

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=devpulse --cov-report=html

# Run specific test module
pytest tests/test_github_activity.py -v

# Run with output
pytest -v -s
```

### Test Coverage

- 205+ automated tests
- Unit tests for core functionality
- Integration tests for CLI commands
- Mock-based tests for external APIs

## Command Reference

For detailed command documentation, run:

```bash
devpulse --help
devpulse <command> --help
```

### Common Options

Most commands support these standard options:

- `--json` - Output raw JSON instead of formatted tables
- `--force-refresh` - Bypass cache and fetch fresh data
- `--debug` - Enable debug output with API metadata
- `--timeout N` - Set request timeout in seconds

## Contributing

Contributions are welcome. Please ensure:

1. All tests pass before submitting PRs
2. New features include corresponding tests
3. Code follows existing patterns and style
4. Documentation is updated as needed

## License

MIT License - see LICENSE file for details

## Links

- **Repository**: https://github.com/devspak-s8/devpulse-cli
- **Issues**: https://github.com/devspak-s8/devpulse-cli/issues
- **PyPI**: https://pypi.org/project/devpulse-cli/
