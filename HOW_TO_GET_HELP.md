# How to Get Help - Quick Reference

## 🆘 I Need Help...

### ...about a specific command
```bash
devpulse COMMAND --help
```
Example:
```bash
$ devpulse track --help
# Shows: track subcommands and options
```

### ...about a subcommand
```bash
devpulse COMMAND SUBCOMMAND --help
```
Example:
```bash
$ devpulse track start --help
# Shows: all options for track start
```

### ...to see all commands
```bash
devpulse --help
```
Shows: All 17 command groups

---

## 📚 Documentation Files

### 🚀 Quick Start (10-minute read)
**File:** [QUICK_START_EXAMPLES.md](QUICK_START_EXAMPLES.md)

**Contains:**
- Installation steps
- 10 real-world scenarios
- Actual command output
- Common workflows
- Tips and tricks

**Best for:** Seeing how to actually use the tool

**Example:**
```
# Morning Standup Preparation
$ devpulse health check
✅ CPU: 25%
✅ Memory: 42%
All systems healthy!
```

---

### 📖 Complete Reference (30-minute read)
**File:** [CLI_HELP_GUIDE.md](CLI_HELP_GUIDE.md)

**Contains:**
- All 17 command groups
- All 120+ subcommands
- Every option explained
- Common patterns
- Examples for each command

**Best for:** Finding exact syntax and all options

**Example:**
```
### track start
$ devpulse track start "task-name"
$ devpulse track start                    # Default
$ devpulse track start --tag important
```

---

### 🎯 Feature Guide (20-minute read)
**File:** [README_HELP.md](README_HELP.md)

**Contains:**
- Feature overview
- Installation methods
- Getting started
- Configuration
- Cloud sync
- Secret scanning
- AI insights
- Testing info

**Best for:** Understanding features and getting set up

**Example:**
```
## Installation

# Basic
pip install devpulse-cli

# Full features
pip install devpulse-cli[full]
```

---

### 📝 Entry Point (2-minute read)
**File:** [README.md](README.md)

**Contains:**
- 17 command groups overview
- Installation
- Quick examples
- Links to detailed docs

**Best for:** Getting started quickly

**Example:**
```
## How to Use

### View Help
devpulse --help

### Track Your Work
devpulse track start "task"
```

---

## 🗺️ Navigation Map

```
START HERE
    ↓
[README.md]
    ↓
    ├─→ Want quick examples?
    │   [QUICK_START_EXAMPLES.md]
    │
    ├─→ Want complete reference?
    │   [CLI_HELP_GUIDE.md]
    │
    ├─→ Want feature guide?
    │   [README_HELP.md]
    │
    └─→ Want detailed planning?
        [DOCUMENTATION_COMPLETE.md]
```

---

## 💡 Common Questions & Answers

### Q: How do I start tracking time?
**A:** See [QUICK_START_EXAMPLES.md - Tracking Time on Specific Task](QUICK_START_EXAMPLES.md#scenario-5-tracking-time-on-specific-task)

Or run:
```bash
$ devpulse track start --help
```

---

### Q: How do I use Pomodoro timers?
**A:** See [QUICK_START_EXAMPLES.md - Taking a Break](QUICK_START_EXAMPLES.md#scenario-3-taking-a-break)

Or run:
```bash
$ devpulse timer --help
```

---

### Q: What's in the focus command?
**A:** See [CLI_HELP_GUIDE.md - Focus Command](CLI_HELP_GUIDE.md#-focus-command-group-)

Or run:
```bash
$ devpulse focus --help
```

---

### Q: How do I track habits?
**A:** See [QUICK_START_EXAMPLES.md - Weekly Review](QUICK_START_EXAMPLES.md#scenario-7-weekly-review)

Or run:
```bash
$ devpulse habits --help
```

---

### Q: What commands are available?
**A:** See [CLI_HELP_GUIDE.md - Command Reference](CLI_HELP_GUIDE.md#command-reference)

Or run:
```bash
$ devpulse --help
```

---

### Q: Show me a daily workflow
**A:** See [QUICK_START_EXAMPLES.md - Common Workflows](QUICK_START_EXAMPLES.md#common-workflows)

---

### Q: How do I export data?
**A:** See [CLI_HELP_GUIDE.md - Export Command](CLI_HELP_GUIDE.md#-export-command-group-)

Or run:
```bash
$ devpulse export --help
```

---

## 🎓 Learning Path

### Beginner (30 minutes)
1. Read: [README.md](README.md) - Overview
2. Run: `devpulse --help` - See commands
3. Try: `devpulse health check` - First command
4. Read: [QUICK_START_EXAMPLES.md](QUICK_START_EXAMPLES.md) - Learn workflows

### Intermediate (1 hour)
1. Run: `devpulse track --help` - Explore track
2. Read: [CLI_HELP_GUIDE.md - Track](CLI_HELP_GUIDE.md#--track-command-group) - All options
3. Try: `devpulse track start "task"` - Practice
4. Explore: Other commands with `--help`

### Advanced (2+ hours)
1. Read: [CLI_HELP_GUIDE.md](CLI_HELP_GUIDE.md) - All commands
2. Read: [README_HELP.md](README_HELP.md) - Features and config
3. Set up: Configuration and automation
4. Create: Custom workflows

---

## 🔍 Search Tips

### Looking for command syntax?
```bash
# Quick check
devpulse COMMAND --help

# Detailed reference
Search: [CLI_HELP_GUIDE.md](CLI_HELP_GUIDE.md)
```

### Looking for how to do something?
```bash
Search: [QUICK_START_EXAMPLES.md](QUICK_START_EXAMPLES.md)
for "Scenario" or "Workflow" matching your need
```

### Looking for feature details?
```bash
Search: [README_HELP.md](README_HELP.md)
for the feature name
```

---

## ⚡ Quick Commands

```bash
# View all available commands
devpulse --help

# Track your work
devpulse track start "task name"
devpulse track stop

# Pomodoro timer
devpulse timer start 25

# Focus mode
devpulse focus start 90

# Check system health
devpulse health check

# Daily report
devpulse report daily

# Track habits
devpulse habits create "meditation"
devpulse habits log "meditation"

# Export data
devpulse export all --format json

# Get help on any command
devpulse COMMAND --help
```

---

## 📞 Still Need Help?

### Official Documentation
- 📖 [CLI_HELP_GUIDE.md](CLI_HELP_GUIDE.md) - Complete reference
- 🚀 [QUICK_START_EXAMPLES.md](QUICK_START_EXAMPLES.md) - Real examples
- 📚 [README_HELP.md](README_HELP.md) - Feature guide
- 📝 [README.md](README.md) - Overview

### Using the CLI
```bash
# For any command
devpulse COMMAND --help

# For any subcommand
devpulse COMMAND SUBCOMMAND --help

# List all commands
devpulse --help
```

### Via Python
```bash
python -m devpulse COMMAND --help
```

---

## 🎯 Start Here

1. **Just installed?** → Read [README.md](README.md)
2. **Want examples?** → Read [QUICK_START_EXAMPLES.md](QUICK_START_EXAMPLES.md)
3. **Want everything?** → Read [CLI_HELP_GUIDE.md](CLI_HELP_GUIDE.md)
4. **Want to set up?** → Read [README_HELP.md](README_HELP.md)

---

**Happy tracking! 🚀**
