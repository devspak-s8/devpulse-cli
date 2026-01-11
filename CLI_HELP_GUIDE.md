# DevPulse CLI - Complete Help & Usage Guide

## Quick Start

### Installation
```bash
pip install devpulse-cli
```

### Getting Help
```bash
devpulse --help              # Show all available commands
devpulse COMMAND --help      # Show help for specific command
devpulse COMMAND SUBCOMMAND --help  # Show help for subcommand
```

---

## Command Reference

### 🔍 AI Command Group
**Purpose:** AI-powered insights and suggestions

#### ai suggest
```bash
devpulse ai suggest                    # Get AI suggestion
devpulse ai suggest --context "task"   # Suggest with context
```
Generates smart suggestions based on your activity patterns.

#### ai analyze
```bash
devpulse ai analyze [FILE]
```
Analyzes logs or code for improvements.

#### ai chat
```bash
devpulse ai chat                       # Interactive AI chat
devpulse ai chat "your question"       # Ask specific question
devpulse ai chat --interactive         # Start chat session
```

#### ai recommend
```bash
devpulse ai recommend                  # Get recommendations
devpulse ai recommend --category "code"
```

#### ai insights
```bash
devpulse ai insights                   # Show AI insights
devpulse ai insights --detailed        # Detailed breakdown
devpulse ai insights --export file.json
```

#### ai predict
```bash
devpulse ai predict                    # Predict trends (7 days)
devpulse ai predict --days 30          # Predict 30 days ahead
```

#### ai optimize
```bash
devpulse ai optimize                   # Get optimization suggestions
devpulse ai optimize --apply           # Apply recommendations
```

---

### 📊 Stats Command Group
**Purpose:** View analytics and statistics

#### stats show
```bash
devpulse stats show                    # Show today's stats
devpulse stats show --week             # Weekly stats
devpulse stats show --month            # Monthly stats
```

#### stats report
```bash
devpulse stats report                  # Console report
devpulse stats report --format json    # JSON format
devpulse stats report --format html    # HTML report
```

#### stats trends
```bash
devpulse stats trends                  # Show trends
devpulse stats trends --metric productivity
devpulse stats trends --chart          # Display chart
```

#### stats compare
```bash
devpulse stats compare                 # Compare periods
devpulse stats compare --metric productivity
```

#### stats breakdown
```bash
devpulse stats breakdown               # Breakdown by project
devpulse stats breakdown --by project
devpulse stats breakdown --top 5       # Top 5 categories
```

#### stats productivity
```bash
devpulse stats productivity            # Productivity score
devpulse stats productivity --score    # Show score details
devpulse stats productivity --insights # Get insights
```

#### stats goals
```bash
devpulse stats goals                   # List goals
devpulse stats goals --weekly          # Weekly goals
devpulse stats goals set "Goal Name"   # Set new goal
```

---

### ⏱️ Track Command Group
**Purpose:** Track time and commands

#### track start
```bash
devpulse track start                   # Start tracking
devpulse track start "task name"       # Start with task name
devpulse track start --tag important   # Add tag
```

#### track stop
```bash
devpulse track stop                    # Stop current session
```

#### track status
```bash
devpulse track status                  # Show active session
```

#### track pause
```bash
devpulse track pause                   # Pause session
```

#### track resume
```bash
devpulse track resume                  # Resume session
```

#### track list
```bash
devpulse track list                    # List all sessions
devpulse track list --limit 10         # Show last 10
devpulse track list --today            # Today's sessions
devpulse track list --week             # This week's sessions
```

#### track delete
```bash
devpulse track delete 1                # Delete session 1
devpulse track delete 1 --force        # Force delete without confirm
```

#### track edit
```bash
devpulse track edit 1 --task "new name"
devpulse track edit 1 --duration 45    # Change duration (minutes)
```

#### track export
```bash
devpulse track export                  # Export as CSV
devpulse track export --format json    # Export as JSON
devpulse track export --range 2026-01-01:2026-01-31
```

---

### 📝 Logs Command Group
**Purpose:** Analyze and search logs

#### logs analyze
```bash
devpulse logs analyze [FILE]           # Analyze log file
```

#### logs search
```bash
devpulse logs search "error"           # Search for keyword
devpulse logs search "error" --file app.log
```

#### logs filter
```bash
devpulse logs filter                   # Show filtered logs
devpulse logs filter --level ERROR     # Filter by level
devpulse logs filter --from 2026-01-01 --to 2026-01-05
devpulse logs filter --keyword "timeout"
```

#### logs tail
```bash
devpulse logs tail                     # Show last 10 lines
devpulse logs tail --lines 50          # Show last 50 lines
devpulse logs tail --follow            # Follow log (like tail -f)
```

#### logs errors
```bash
devpulse logs errors                   # Show all errors
devpulse logs errors --file app.log
devpulse logs errors --count           # Count only
```

#### logs warnings
```bash
devpulse logs warnings                 # Show all warnings
devpulse logs warnings --file app.log
devpulse logs warnings --count         # Count only
```

#### logs stats
```bash
devpulse logs stats                    # Log statistics
devpulse logs stats --detailed         # Detailed breakdown
```

---

### 🔐 Secrets Command Group
**Purpose:** Scan for secrets and sensitive data

#### secrets scan
```bash
devpulse secrets scan                  # Scan current directory
devpulse secrets scan --path /src      # Scan specific path
devpulse secrets scan --recursive       # Scan recursively
```

#### secrets list
```bash
devpulse secrets list                  # List found secrets
```

#### secrets check
```bash
devpulse secrets check [FILE]          # Check specific file
devpulse secrets check --type api_key  # Check for API keys
devpulse secrets check --strict        # Strict checking
```

#### secrets ignore
```bash
devpulse secrets ignore add [PATTERN]
devpulse secrets ignore remove [PATTERN]
```

#### secrets report
```bash
devpulse secrets report                # Generate report
devpulse secrets report --format json
devpulse secrets report --output report.json
devpulse secrets report --severity high  # High severity only
```

#### secrets validate
```bash
devpulse secrets validate              # Validate config
devpulse secrets validate --config custom.yaml
```

#### secrets patterns
```bash
devpulse secrets patterns              # List patterns
devpulse secrets patterns add "MY_PATTERN"
```

---

### 🔄 Sync Command Group
**Purpose:** Sync data with cloud

#### sync push
```bash
devpulse sync push                     # Push to cloud
```

#### sync pull
```bash
devpulse sync pull                     # Pull from cloud
```

#### sync status
```bash
devpulse sync status                   # Show sync status
```

#### sync login
```bash
devpulse sync login                    # Interactive login
devpulse sync login --email user@example.com
devpulse sync login --token YOUR_TOKEN
```

#### sync logout
```bash
devpulse sync logout                   # Logout
devpulse sync logout --force           # Force logout
```

#### sync auto
```bash
devpulse sync auto enable              # Enable auto-sync
devpulse sync auto disable             # Disable auto-sync
devpulse sync auto status              # Check status
devpulse sync auto --interval 5        # Sync every 5 minutes
```

#### sync history
```bash
devpulse sync history                  # Show all sync events
devpulse sync history --limit 20
devpulse sync history --type push      # Filter by type
```

#### sync conflicts
```bash
devpulse sync conflicts                # Show conflicts
devpulse sync conflicts --resolve      # Attempt resolve
devpulse sync conflicts --strategy local  # Use local version
```

---

### 💊 Health Command Group
**Purpose:** System health monitoring

#### health check
```bash
devpulse health check                  # Check all metrics
devpulse health check --cpu            # CPU only
devpulse health check --memory         # Memory only
devpulse health check --disk           # Disk only
devpulse health check --processes      # Running processes
```

#### health report
```bash
devpulse health report                 # Console report
devpulse health report --format json   # JSON report
```

#### health processes
```bash
devpulse health processes              # Top 10 processes
devpulse health processes --top 20     # Top 20
devpulse health processes --sort cpu   # Sort by CPU
devpulse health processes --sort memory  # Sort by memory
devpulse health processes --sort name  # Sort by name
```

#### health alert
```bash
devpulse health alert                  # Check thresholds
devpulse health alert --cpu 80         # Alert if CPU > 80%
devpulse health alert --memory 85      # Alert if memory > 85%
devpulse health alert --disk 90        # Alert if disk > 90%
```

---

### 📦 Project Command Group ✨ NEW
**Purpose:** Manage projects and workspaces

#### project create
```bash
devpulse project create "my-project"
devpulse project create "web-app" --description "My web application"
devpulse project create "api" --color blue
```

#### project list
```bash
devpulse project list                  # Show all projects
```

#### project switch
```bash
devpulse project switch "my-project"   # Switch to project
```

#### project delete
```bash
devpulse project delete "my-project"
devpulse project delete "my-project" --force  # No confirmation
```

#### project info
```bash
devpulse project info "my-project"
```

#### project archive
```bash
devpulse project archive "my-project"
```

---

### ⏰ Timer Command Group ✨ NEW
**Purpose:** Pomodoro and interval timers

#### timer start
```bash
devpulse timer start                   # 25-min Pomodoro
devpulse timer start 45                # 45-minute timer
devpulse timer start 30 --task "coding"
```

#### timer stop
```bash
devpulse timer stop
```

#### timer status
```bash
devpulse timer status
```

#### timer preset
```bash
devpulse timer preset pomodoro         # 25 minutes
devpulse timer preset shortbreak       # 5 minutes
devpulse timer preset longbreak        # 15 minutes
```

#### timer history
```bash
devpulse timer history
```

#### timer stats
```bash
devpulse timer stats
```

---

### 📝 Notes Command Group ✨ NEW
**Purpose:** Quick note-taking

#### notes add
```bash
devpulse notes add "Remember to review PR"
devpulse notes add "Fix bug" --tag bugs
devpulse notes add "Meeting at 2pm" --tag work
```

#### notes list
```bash
devpulse notes list
```

#### notes search
```bash
devpulse notes search "meeting"
```

#### notes delete
```bash
devpulse notes delete 1
devpulse notes delete 1 --force
```

#### notes tags
```bash
devpulse notes tags
```

#### notes export
```bash
devpulse notes export
```

---

### 🎯 Focus Command Group ✨ NEW
**Purpose:** Focus mode and distraction blocking

#### focus start
```bash
devpulse focus start                   # 60-minute focus
devpulse focus start --duration 90
devpulse focus start --goal "Code review"
```

#### focus stop
```bash
devpulse focus stop
```

#### focus status
```bash
devpulse focus status
```

#### focus block
```bash
devpulse focus block twitter
devpulse focus block "social-media"
```

#### focus unblock
```bash
devpulse focus unblock twitter
```

#### focus history
```bash
devpulse focus history
```

#### focus stats
```bash
devpulse focus stats
```

---

### ☕ Breaks Command Group ✨ NEW
**Purpose:** Break management

#### breaks schedule
```bash
devpulse breaks schedule               # Default schedule
devpulse breaks schedule --interval 45 --duration 10
```

#### breaks take
```bash
devpulse breaks take
```

#### breaks skip
```bash
devpulse breaks skip
```

#### breaks status
```bash
devpulse breaks status
```

#### breaks history
```bash
devpulse breaks history
```

#### breaks reminders
```bash
devpulse breaks reminders
```

#### breaks suggestions
```bash
devpulse breaks suggestions
```

---

### 📊 Report Command Group ✨ NEW
**Purpose:** Productivity reports

#### report daily
```bash
devpulse report daily
devpulse report daily --detailed
```

#### report weekly
```bash
devpulse report weekly
```

#### report monthly
```bash
devpulse report monthly
```

#### report comparison
```bash
devpulse report comparison "last-month" "this-month"
```

#### report summary
```bash
devpulse report summary
```

#### report insights
```bash
devpulse report insights
```

---

### ⚙️ Config Command Group ✨ NEW
**Purpose:** Configuration management

#### config show
```bash
devpulse config show                   # Show all config
devpulse config show user.name         # Show specific key
```

#### config set
```bash
devpulse config set theme dark
devpulse config set notifications.enabled true
```

#### config get
```bash
devpulse config get theme
```

#### config list
```bash
devpulse config list
```

#### config import-config
```bash
devpulse config import-config config.json
```

#### config export-config
```bash
devpulse config export-config
```

---

### 📤 Export Command Group ✨ NEW
**Purpose:** Export data

#### export all
```bash
devpulse export all                    # Export as CSV
devpulse export all --format json
devpulse export all --range 2026-01-01:2026-01-31
```

#### export sessions
```bash
devpulse export sessions
```

#### export projects
```bash
devpulse export projects
```

#### export notes
```bash
devpulse export notes
```

#### export stats
```bash
devpulse export stats
```

#### export archive
```bash
devpulse export archive
```

---

### 🔗 Habits Command Group ✨ NEW
**Purpose:** Habit tracking

#### habits create
```bash
devpulse habits create meditate
devpulse habits create exercise --frequency weekly
```

#### habits list
```bash
devpulse habits list
```

#### habits log
```bash
devpulse habits log meditate
```

#### habits streak
```bash
devpulse habits streak meditate
```

#### habits progress
```bash
devpulse habits progress meditate
```

#### habits delete
```bash
devpulse habits delete meditate
devpulse habits delete meditate --force
```

#### habits stats
```bash
devpulse habits stats
```

---

### 📱 Dashboard Command Group ✨ NEW
**Purpose:** Summary dashboard

#### dashboard show
```bash
devpulse dashboard show                # Show dashboard
devpulse dashboard show --period week
```

#### dashboard quick
```bash
devpulse dashboard quick
```

#### dashboard goals
```bash
devpulse dashboard goals
```

#### dashboard projects
```bash
devpulse dashboard projects
```

#### dashboard stats
```bash
devpulse dashboard stats
```

#### dashboard refresh
```bash
devpulse dashboard refresh
```

---

## Common Patterns

### Output Formats
Most reporting commands support multiple formats:
```bash
devpulse stats report --format json    # JSON output
devpulse stats report --format csv     # CSV output
devpulse stats report --format html    # HTML report
devpulse stats report --format text    # Plain text (default)
```

### Date Ranges
Commands supporting date ranges:
```bash
--from 2026-01-01                      # From date
--to 2026-01-31                        # To date
--range 2026-01-01:2026-01-31          # Range (start:end)
```

### Sorting
List commands typically support:
```bash
--sort field                           # Sort by field
--sort field:asc                       # Ascending
--sort field:desc                      # Descending
```

### Limits
Pagination support:
```bash
--limit 10                             # Show 10 items
--skip 5                               # Skip first 5
--top 20                               # Top 20
```

---

## Examples

### Daily Workflow
```bash
# Start tracking
devpulse track start "Bug fixing"

# Check progress
devpulse health check
devpulse stats show --week

# Take a break
devpulse breaks take

# Stop work
devpulse track stop

# Daily report
devpulse report daily --detailed
```

### Weekly Review
```bash
# Weekly stats
devpulse stats show --week

# Weekly report
devpulse report weekly

# Productivity insights
devpulse ai insights --detailed

# Check habits
devpulse habits stats
```

### Data Export
```bash
# Export all data for backup
devpulse export all --format json

# Export specific period
devpulse track export --range 2026-01-01:2026-01-31

# Generate HTML report
devpulse stats report --format html --output week-report.html
```

---

### 🔗 GitHub Command Group
**Purpose:** GitHub integration, analytics, and PR management

#### github stats
```bash
devpulse github stats --repo owner/name              # Repository statistics
devpulse github stats --username torvalds            # User statistics
devpulse github stats --repo owner/name --json       # JSON output
devpulse github stats --repo owner/name --include health,contributors
```

#### github activity
```bash
devpulse github activity username                    # User activity
devpulse github activity username --events push,pr   # Filter events
devpulse github activity username --since 7d         # Last 7 days
devpulse github activity username --json             # JSON format
devpulse github activity username --debug            # Show rate limit info
```

#### github contributors
```bash
devpulse github contributors owner/repo              # Top contributors
devpulse github contributors owner/repo --top 5      # Show top 5
devpulse github contributors owner/repo --json       # JSON output
```

#### github top-languages
```bash
devpulse github top-languages owner/repo             # Language breakdown
devpulse github top-languages owner/repo --json      # JSON output
```

#### github prs (List Pull Requests) ✨ NEW
```bash
devpulse github prs owner/repo                       # List open PRs
devpulse github prs owner/repo --state all           # All PRs (open + closed)
devpulse github prs owner/repo --state closed        # Closed PRs only
devpulse github prs owner/repo --conflicts-only      # Only conflicted PRs
devpulse github prs owner/repo --json                # JSON output
devpulse github prs owner/repo --debug               # Show rate limit info
devpulse github prs owner/repo --force-refresh       # Bypass cache
```

Shows PR number, title, author, base/head branches, mergeability state, CI status, and head SHA.

#### github pr view (View Single PR) ✨ NEW
```bash
devpulse github pr view owner/repo 123               # View PR details
devpulse github pr view owner/repo 123 --json        # JSON output
devpulse github pr view owner/repo 123 --debug       # Show API metadata
devpulse github pr view owner/repo 123 --force-refresh
```

Displays: title, author, files changed, commits, SHAs, mergeability, conflict status, CI status.

#### github pr merge (Merge Pull Request) ✨ NEW
```bash
# Preview merge (no token needed if env var set)
devpulse github pr merge owner/repo 123 --dry-run --json

# Squash merge (default strategy)
devpulse github pr merge owner/repo 123 --strategy squash --confirm

# Full merge
devpulse github pr merge owner/repo 123 --strategy merge --confirm

# Rebase merge
devpulse github pr merge owner/repo 123 --strategy rebase --confirm

# Override failing CI checks (conflicts still block)
devpulse github pr merge owner/repo 123 --strategy squash --confirm --force

# Interactive token prompt (if GITHUB_TOKEN not set)
devpulse github pr merge owner/repo 123 --confirm
# Enter GITHUB_TOKEN with repo scope when prompted (hidden input)
```

**Merge Safety Features:**
- ✅ Conflicts block merge (mergeable_state: dirty)
- ✅ Requires `--confirm` flag (no accidental merges)
- ✅ Permission validation (token must have repo scope)
- ✅ CI status awareness (--force overrides failures, not conflicts)
- ✅ `--dry-run` shows what would happen without merging
- ✅ Uses current head SHA (prevents race conditions)

---

## Tips & Tricks

1. **Use aliases for frequently used commands:**
   ```bash
   alias dpt='devpulse track'
   alias dps='devpulse stats'
   ```

2. **Pipe to other tools:**
   ```bash
   devpulse track export --format json | jq '.sessions | length'
   ```

3. **Schedule regular reports:**
   ```bash
   # In crontab: Generate daily report at 6 PM
   0 18 * * * devpulse report daily --output ~/reports/daily.html
   ```

4. **Use --help liberally:**
   ```bash
   devpulse COMMAND --help
   ```

---

## Troubleshooting

### Command not found
```bash
# Ensure installation
pip install devpulse-cli

# Add to PATH if needed
export PATH=$PATH:~/.local/bin
```

### Permission denied
```bash
# Use with Python directly
python -m devpulse COMMAND
```

### Help not showing options
```bash
# Update to latest version
pip install --upgrade devpulse-cli
```

---

**For more help, run: `devpulse --help`**
