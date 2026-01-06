# DevPulse - Developer Productivity CLI Tool

Complete developer productivity tracking with 17 command groups, 200+ tests, and AI-powered insights.

**📖 [Full Help Guide](CLI_HELP_GUIDE.md) | 🚀 [Quick Examples](QUICK_START_EXAMPLES.md) | 📦 [Features](README_HELP.md)**

## 17 Command Groups

### Core Productivity
- **🎯 Track** - Time tracking and task management (15 tests)
- **📊 Stats** - Analytics and statistics (20 tests)  
- **💊 Health** - Real-time system monitoring (22 tests)
- **📝 Logs** - Log analysis and search (18 tests)
- **🔐 Secrets** - Scan for exposed secrets (17 tests)
- **🔄 Sync** - Cloud synchronization (17 tests)
- **🤖 AI** - AI-powered insights (15 tests)

### Time & Focus ✨ NEW
- **⏰ Timer** - Pomodoro timers (8 tests)
- **🎯 Focus** - Focus mode with blocking (9 tests)
- **☕ Breaks** - Break scheduling (8 tests)
- **🔗 Habits** - Habit tracking (8 tests)

### Organization ✨ NEW
- **📦 Project** - Project management (7 tests)
- **📝 Notes** - Note-taking (7 tests)
- **📊 Report** - Productivity reports (7 tests)
- **📱 Dashboard** - Dashboard view (7 tests)

### Data Management ✨ NEW
- **⚙️ Config** - Configuration (7 tests)
- **📤 Export** - Data export (8 tests)

## Installation

```bash
# Basic install
pip install devpulse-cli

# With all features
pip install devpulse-cli[full]

# From source
git clone <repo>
cd devpulse
pip install -e .
```

## How to Use

### View Help
```bash
# All commands
devpulse --help

# Specific command
devpulse track --help

# Subcommand
devpulse track start --help
```

### Track Your Work
```bash
# Start task
devpulse track start "Implement feature"

# Check status
devpulse track status

# Stop tracking
devpulse track stop

# View sessions
devpulse track list --today
```

### Pomodoro Timer
```bash
# 25-minute timer
devpulse timer start

# Custom duration
devpulse timer start 45

# With task
devpulse timer start 30 --task "code review"
```

### Focus Mode
```bash
# 60-minute focus
devpulse focus start

# With goal
devpulse focus start 90 --goal "Implementation"

# Block distractions
devpulse focus block twitter.com
```

### Health Check
```bash
# System metrics
devpulse health check

# Top processes
devpulse health processes --top 10

# Specific metric
devpulse health check --cpu
```

### Reports & Insights
```bash
# Daily report
devpulse report daily

# Weekly stats
devpulse stats show --week

# AI insights
devpulse ai insights --detailed
```

### Habit Tracking
```bash
# Create habit
devpulse habits create "meditation"

# Log completion
devpulse habits log "meditation"

# View streak
devpulse habits streak "meditation"
```

### Data Export
```bash
# Export all
devpulse export all --format json

# Export period
devpulse track export --range 2026-01-01:2026-01-31

# Generate report
devpulse stats report --format html --output report.html
```

## Documentation

| Document | Purpose |
|----------|---------|
| [CLI_HELP_GUIDE.md](CLI_HELP_GUIDE.md) | Complete command reference with all options |
| [QUICK_START_EXAMPLES.md](QUICK_START_EXAMPLES.md) | Real-world examples with actual output |
| [README_HELP.md](README_HELP.md) | Feature overview and detailed guide |
| [NEW_COMMANDS_SUMMARY.md](NEW_COMMANDS_SUMMARY.md) | New features in latest release |

## Development

Install dependencies:
```bash
pip install -r requirements.txt
```

Run tests:
```bash
# All tests
pytest tests/

# With coverage
pytest tests/ --cov=devpulse --cov-report=html

# Verbose output
pytest tests/ -v
```

### Test Results
- **200 tests** total
- **82% coverage**
- **All passing** ✅

## Examples

### Morning Standup Check
```bash
devpulse health check
devpulse report daily
devpulse stats show --week
```

### During Work
```bash
devpulse focus start 90 --goal "Feature implementation"
devpulse timer start 25                    # Pomodoro
devpulse breaks take                       # When prompted
devpulse track start "Task name"
devpulse track stop
```

### End of Day
```bash
devpulse report daily --detailed
devpulse habits stats
devpulse export all --format json          # Backup
```

### Weekly Review
```bash
devpulse stats show --week
devpulse report weekly
devpulse ai insights --detailed
```

## Tips

### Create Aliases
```bash
alias track='devpulse track'
alias health='devpulse health check'
alias stats='devpulse stats show'
```

### Automate
```bash
# Cron: Daily report at 6 PM
0 18 * * * devpulse report daily --output ~/reports/daily.html

# Cron: Weekly backup on Friday
0 17 * * 5 devpulse export all --format json
```

### Help
```bash
# For any command
devpulse COMMAND --help

# Or see complete guide
# Check: CLI_HELP_GUIDE.md
```

## License

MIT License
