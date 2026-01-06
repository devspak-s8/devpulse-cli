# DevPulse - Developer Productivity CLI Tool

![DevPulse](https://img.shields.io/badge/DevPulse-CLI%20Tool-blue)
![Python](https://img.shields.io/badge/Python-3.9+-green)
![Tests](https://img.shields.io/badge/Tests-200%20Passing-brightgreen)
![Coverage](https://img.shields.io/badge/Coverage-82%25-yellowgreen)
![PyPI](https://img.shields.io/badge/PyPI-devpulse--cli-orange)

DevPulse is a comprehensive CLI tool for developers to track productivity, monitor system health, analyze logs, and gain AI-powered insights about their work patterns.

## Quick Links

- 📖 **[Complete Help Guide](CLI_HELP_GUIDE.md)** - Detailed documentation for every command
- 🚀 **[Quick Start Examples](QUICK_START_EXAMPLES.md)** - Real-world usage examples with output
- 📦 **[New Commands Summary](NEW_COMMANDS_SUMMARY.md)** - Overview of new features
- 🧪 **[Testing Documentation](HEALTH_COMMAND_IMPLEMENTATION.md)** - Testing patterns and coverage

## Features

### 17 Command Groups

#### Core Features
- **🎯 Track** - Time tracking and task management
- **📊 Stats** - Analytics and productivity statistics  
- **💊 Health** - Real-time system health monitoring
- **📝 Logs** - Log analysis and searching
- **🔐 Secrets** - Scan for exposed secrets and sensitive data
- **🔄 Sync** - Cloud synchronization
- **🤖 AI** - AI-powered insights and recommendations

#### Productivity Tools
- **⏰ Timer** - Pomodoro and interval timers
- **🎯 Focus** - Focus mode with distraction blocking
- **☕ Breaks** - Break scheduling and reminders
- **🔗 Habits** - Habit tracking with streaks

#### Organization
- **📦 Project** - Project and workspace management
- **📝 Notes** - Quick note-taking
- **📊 Report** - Enhanced productivity reports
- **📱 Dashboard** - Summary dashboard view

#### Data & Config
- **⚙️ Config** - Configuration management
- **📤 Export** - Multi-format data export (JSON, CSV, HTML, XLSX)

## Installation

### From PyPI
```bash
pip install devpulse-cli
```

### With Optional Extras
```bash
# Full installation with all features
pip install devpulse-cli[full]

# Or specific extras
pip install devpulse-cli[ai,data,viz,db]
```

### From Source
```bash
git clone https://github.com/yourusername/devpulse.git
cd devpulse
pip install -e .
```

## Getting Started

### View Help
```bash
# Show all commands
devpulse --help

# Show command help
devpulse track --help

# Show subcommand help
devpulse track start --help
```

### First Command
```bash
# Check system health
devpulse health check

# Track a task
devpulse track start "My Task"
devpulse track stop

# View today's stats
devpulse stats show
```

## Usage Examples

### Time Tracking
```bash
# Start tracking
devpulse track start "Implementation"

# Check status
devpulse track status

# Stop tracking
devpulse track stop

# List sessions
devpulse track list --today

# Export data
devpulse track export --format json
```

### Pomodoro Timer
```bash
# Start 25-minute Pomodoro
devpulse timer start

# Custom duration
devpulse timer start 45

# With task name
devpulse timer start 30 --task "code review"

# View history
devpulse timer history
```

### Focus Mode
```bash
# Start 60-minute focus session
devpulse focus start

# With goal
devpulse focus start 90 --goal "Code review"

# Block distractions
devpulse focus block twitter.com
devpulse focus block facebook.com

# View stats
devpulse focus stats
```

### Health Monitoring
```bash
# Check all metrics
devpulse health check

# Specific checks
devpulse health check --cpu
devpulse health check --memory
devpulse health check --disk

# Top processes
devpulse health processes --top 10

# Set alerts
devpulse health alert --cpu 80 --memory 85
```

### Productivity Reports
```bash
# Daily report
devpulse report daily

# Weekly report
devpulse report weekly

# Monthly report
devpulse report monthly

# Get insights
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

# Statistics
devpulse habits stats
```

### Data Export
```bash
# Export all data
devpulse export all --format json

# Export specific period
devpulse track export --range 2026-01-01:2026-01-31

# Generate HTML report
devpulse stats report --format html --output report.html
```

## Documentation

### Full Command Reference
See [CLI_HELP_GUIDE.md](CLI_HELP_GUIDE.md) for comprehensive documentation of every command with examples.

### Quick Examples
See [QUICK_START_EXAMPLES.md](QUICK_START_EXAMPLES.md) for real-world usage scenarios with actual output.

### New Features
See [NEW_COMMANDS_SUMMARY.md](NEW_COMMANDS_SUMMARY.md) for details on the 10 new command modules added.

## Testing

DevPulse has comprehensive test coverage:

```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_track.py

# Run with coverage
pytest tests/ --cov=devpulse --cov-report=html

# Run in verbose mode
pytest tests/ -v
```

### Test Results
- **200 tests total**
- **82% code coverage**
- **All tests passing**

## Architecture

### Command Structure
Each command group is a self-contained module following the Typer framework pattern:

```python
import typer
app = typer.Typer(help="Command description")

@app.command()
def subcommand(arg: str, opt: str = typer.Option(...)):
    """Subcommand description."""
    typer.echo("Output")
```

### Key Dependencies
- **Typer** - CLI framework with type hints
- **Rich** - Beautiful terminal output
- **Colorama** - Cross-platform colored text
- **psutil** - System and process utilities
- **pytest** - Testing framework

### Optional Dependencies
- **numpy, pandas** - Data analysis
- **matplotlib, plotly** - Visualization
- **sqlalchemy** - Database ORM
- **requests** - HTTP client
- **pydantic** - Data validation

## Configuration

Create `~/.devpulse/config.json`:

```json
{
  "user": {
    "name": "Your Name",
    "email": "your.email@example.com"
  },
  "notifications": {
    "enabled": true,
    "sound": true
  },
  "theme": "dark",
  "workday": {
    "start": "09:00",
    "end": "17:00"
  }
}
```

Or use CLI:
```bash
devpulse config set user.name "Your Name"
devpulse config set theme dark
devpulse config show
```

## Cloud Sync

Sync your data with cloud dashboard:

```bash
# Login
devpulse sync login --email your@email.com

# Push data
devpulse sync push

# Pull data
devpulse sync pull

# Auto-sync
devpulse sync auto enable --interval 5  # Every 5 minutes

# Check status
devpulse sync status
```

## Secret Scanning

Scan your projects for exposed secrets:

```bash
# Scan current directory
devpulse secrets scan

# Scan specific path
devpulse secrets scan --path /src

# Generate report
devpulse secrets report --format json

# Ignore false positives
devpulse secrets ignore add "config.js"
```

## AI Insights

Get AI-powered recommendations:

```bash
# General insights
devpulse ai insights

# Detailed analysis
devpulse ai insights --detailed

# Predictions
devpulse ai predict --days 7

# Optimization suggestions
devpulse ai optimize

# AI chat
devpulse ai chat "Ask me anything"
```

## Tips & Tricks

### Create Aliases
```bash
alias track='devpulse track'
alias status='devpulse track status'
alias stats='devpulse stats show'
alias health='devpulse health check'
```

### Pipe to Other Tools
```bash
# Count sessions
devpulse track export --format json | jq '.sessions | length'

# Get latest session
devpulse track list | head -1

# Check if focusing
devpulse focus status | grep "STARTED" && echo "Currently focused"
```

### Automate Reports
```bash
# Generate daily report at 6 PM
0 18 * * * devpulse report daily --output ~/reports/daily-$(date +\%Y-\%m-\%d).html

# Weekly backup on Friday
0 17 * * 5 devpulse export all --format json
```

## Troubleshooting

### Command not found
```bash
# Ensure installation
pip install devpulse-cli

# Or use Python directly
python -m devpulse COMMAND
```

### Permission errors
```bash
# Use --force flag for auto-confirm
devpulse track delete 1 --force

# Or update permissions
chmod +x ~/.local/bin/devpulse
```

### Help not showing
```bash
# Update to latest version
pip install --upgrade devpulse-cli

# Clear cache
rm -rf ~/.cache/devpulse
```

## Project Statistics

- **17 command groups** with 80+ subcommands
- **200+ test cases** with 82% coverage
- **~3,000 lines** of production code
- **~2,000 lines** of test code
- **10 new command modules** added in latest release

## Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Write tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

MIT License - See LICENSE file for details

## Support

- 📖 **Documentation**: See [CLI_HELP_GUIDE.md](CLI_HELP_GUIDE.md)
- 💬 **Issues**: GitHub Issues
- 📧 **Email**: support@devpulse.dev

## Changelog

### v0.1.3 (Latest)
- ✨ Added 10 new command modules (project, timer, notes, focus, breaks, report, config, export, habits, dashboard)
- ✨ Optimized package installation with optional extras
- 🔧 Updated dependencies for better compatibility
- 📊 Expanded test suite to 200+ tests

### v0.1.2
- 💊 Implemented health command with real system metrics
- 📈 Enhanced statistics reporting
- 🔐 Improved secret scanning

### v0.1.1
- 🚀 Initial release on PyPI
- 📦 Core commands: track, stats, health, logs, secrets, sync, ai

## Roadmap

- [ ] Database persistence layer (SQLAlchemy)
- [ ] Web dashboard interface
- [ ] API server
- [ ] Mobile app integration
- [ ] Advanced analytics
- [ ] Team collaboration features
- [ ] OAuth integration
- [ ] Slack/Discord notifications

---

**DevPulse - Track Your Productivity, Master Your Time** 🚀

For detailed help on any command, run: `devpulse COMMAND --help`
