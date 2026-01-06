# DevPulse Quick Start Examples

## Installation & Setup

### 1. Install the package
```bash
$ pip install devpulse-cli

Successfully installed devpulse-cli-0.1.3
```

### 2. Verify installation
```bash
$ devpulse --help

 Usage: devpulse [OPTIONS] COMMAND [ARGS]...

 DevPulse - Developer Productivity CLI Tool
 
╭─ Commands ────────────────────────────────────────────╮
│ ai           AI-powered insights and suggestions      │
│ track        Track time and commands                  │
│ logs         Analyze and search logs                  │
│ secrets      Scan for secrets and sensitive data      │
│ stats        View analytics and statistics            │
│ sync         Sync data with cloud dashboard           │
│ health       System health monitoring                 │
│ project      Manage projects and workspaces           │
│ timer        Pomodoro and interval timers             │
│ notes        Quick note-taking and management         │
│ focus        Focus mode and distraction blocking      │
│ breaks       Break management and reminders           │
│ report       Enhanced productivity reports            │
│ config       Configuration management                │
│ export       Export data in multiple formats          │
│ habits       Track habits and streaks                 │
│ dashboard    Summary dashboard view                   │
╰────────────────────────────────────────────────────────╯
```

---

## Real-World Examples

### Scenario 1: Morning Standup Preparation

```bash
# 1. Check system health
$ devpulse health check
✅ CPU: 25%
✅ Memory: 42%
✅ Disk: 68%
All systems healthy!

# 2. Get yesterday's summary
$ devpulse report daily
📊 Daily Report - January 5, 2026
├─ Total Time: 8h 42m
├─ Projects: 3
├─ Tasks Completed: 12
└─ Focus Score: 87%

# 3. Quick stats
$ devpulse stats show --week
📈 Weekly Statistics
├─ Mon: 8h 32m
├─ Tue: 8h 45m
├─ Wed: 8h 28m
├─ Thu: 8h 52m (peak day)
└─ Fri: 7h 15m
```

### Scenario 2: Starting Your Workday

```bash
# 1. Create a project if needed
$ devpulse project create "Q1 Planning"
✨ Created project: Q1 Planning

# 2. Add a habit (if tracking new habit)
$ devpulse habits create "morning-standup" --frequency daily
✨ Habit created: morning-standup

# 3. Log the habit
$ devpulse habits log "morning-standup"
✅ Logged: morning-standup
📊 Streak: 5 days

# 4. Start focusing on tasks
$ devpulse focus start 90 --goal "Code review and planning"
🎯 Focus Mode: STARTED
├─ Duration: 90 minutes
└─ Goal: Code review and planning
```

### Scenario 3: Taking a Break

```bash
# 1. Check break schedule
$ devpulse breaks status
☕ Break Schedule: Active
├─ Interval: 60 minutes
└─ Next break: 32 minutes from now

# 2. Time for a break (explicit)
$ devpulse breaks take
☕ Break started: 15 minutes
🎵 Play relaxing music... 🎵

# 3. What should I do during break?
$ devpulse breaks suggestions
💡 Break Suggestions:
├─ Stretch: Upper back & neck
├─ Hydrate: Drink water
├─ Walk: 5-minute walk outside
└─ Eyes: 20-20-20 rule (look 20ft away for 20 secs)

# 4. Resume work
$ devpulse focus start 45 --task "continue-code-review"
🎯 Focus Mode: RESTARTED
└─ Duration: 45 minutes
```

### Scenario 4: Afternoon Productivity Check

```bash
# 1. What's my productivity today?
$ devpulse stats productivity
📊 Productivity Score: 84/100
├─ Focus Time: 6h 32m
├─ Interruptions: 2
├─ Tasks Completed: 9
└─ Goals Met: 7/8

# 2. Get AI insights
$ devpulse ai insights --detailed
🤖 AI Insights:
├─ Peak Performance: 10-12 AM (95% focused)
├─ Trend: ↑ 12% better than last week
├─ Recommendation: Take a 15-min break at 2 PM
└─ Pattern: Most productive on focused tasks

# 3. Predict future performance
$ devpulse ai predict --days 7
📈 7-Day Prediction:
├─ Mon: High productivity expected
├─ Tue: Moderate (likely meetings)
├─ Wed: High (deep work day)
├─ Thu-Fri: Moderate decline
└─ Risk: Monday high workload detected
```

### Scenario 5: Tracking Time on Specific Task

```bash
# 1. Start tracking a task
$ devpulse track start "Implement user authentication"
⏱️ Tracking: Implement user authentication
├─ Start Time: 2:15 PM
└─ Session ID: #1247

# 2. Do some work...

# 3. Check status
$ devpulse track status
⏱️ Active Session: Implement user authentication
├─ Elapsed: 1h 23m
└─ Start: 2:15 PM

# 4. Stop tracking
$ devpulse track stop
✅ Session Completed: Implement user authentication
├─ Duration: 1h 45m
└─ Saved to: Projects/AuthFeature

# 5. Edit if needed (made a mistake)
$ devpulse track edit 1247 --duration 90
✅ Updated session #1247
└─ New Duration: 90 minutes
```

### Scenario 6: End of Day Report

```bash
# 1. Generate detailed daily report
$ devpulse report daily --detailed
📊 Daily Report - January 6, 2026
╭─ Summary ──────────────────╮
│ Total Time: 8h 35m         │
│ Focus Score: 89%           │
│ Tasks: 11/12 completed     │
│ Interruptions: 3           │
╰────────────────────────────╯

╭─ By Project ───────────────╮
│ Q1 Planning: 3h 20m       │
│ Bug Fixes: 2h 45m         │
│ Code Review: 1h 30m       │
│ Meetings: 1h 00m          │
╰────────────────────────────╯

╭─ Activities ───────────────╮
│ Focus Sessions: 6          │
│ Breaks: 4                  │
│ Pomodoros: 8               │
│ Habits Logged: 5           │
╰────────────────────────────╯

# 2. Export data for archive
$ devpulse export all --format json --output daily-backup.json
✅ Exported to: daily-backup.json
└─ Size: 2.4 MB
```

### Scenario 7: Weekly Review

```bash
# 1. Weekly statistics
$ devpulse stats show --week
📈 Weekly Statistics - Jan 6, 2026
├─ Mon: 8h 32m (87% focus)
├─ Tue: 8h 45m (91% focus)
├─ Wed: 8h 28m (84% focus)
├─ Thu: 8h 52m (93% focus) ⭐ Best day
└─ Fri: 7h 15m (80% focus)
Total: 42h 12m (89% avg focus)

# 2. Weekly report
$ devpulse report weekly
📋 Weekly Report - Week of Jan 6, 2026
├─ Projects Worked: 5
├─ Tasks Completed: 52
├─ Total Focus Time: 42h 12m
├─ Best Performance Day: Thursday
└─ Trend: ↑ 8% improvement from last week

# 3. Check habits progress
$ devpulse habits stats
🏆 Habit Statistics - This Week
├─ meditate (daily): 5/7 ✅
├─ exercise (daily): 6/7 ✅
├─ reading (weekly): 2/2 ✅
├─ morning-standup (daily): 7/7 🔥
└─ Current Streaks: 12, 8, 5, 7 days

# 4. Get insights
$ devpulse ai insights --detailed
🤖 Weekly AI Insights:
├─ Performance Peak: Tuesday-Thursday
├─ Best Time: 9-11 AM (peak focus)
├─ Recommendation: Schedule meetings in afternoon
└─ Next Week Goal: Maintain Thursday performance level
```

### Scenario 8: Secret Scanning

```bash
# 1. Scan for secrets in your project
$ devpulse secrets scan
🔐 Secret Scanner Active
Scanning: Current directory...
│
├─ ⚠️ Found 2 potential issues:
│  ├─ .env: API key detected (HIGH)
│  └─ config.js: AWS key pattern (HIGH)
│
└─ Scan complete in 3.2 seconds

# 2. Get detailed report
$ devpulse secrets report --severity high
🔐 Secret Report - High Severity
├─ API Keys: 1 found
├─ AWS Credentials: 1 found
├─ Passwords: 0 found
└─ Recommendation: Rotate exposed credentials

# 3. Ignore false positive
$ devpulse secrets ignore add "config.js"
✅ Added to ignore list: config.js
```

### Scenario 9: Focus Session with Blocking

```bash
# 1. Block distracting websites
$ devpulse focus block twitter.com
✅ Blocked: twitter.com

$ devpulse focus block facebook.com
✅ Blocked: facebook.com

# 2. Start deep work session
$ devpulse focus start 120 --goal "Algorithm implementation"
🎯 Deep Focus: STARTED
├─ Duration: 2 hours
├─ Goal: Algorithm implementation
├─ Blocked Sites: 2
└─ Allow Notifications: Off

# Do focused work for 2 hours...

# 3. End session and see stats
$ devpulse focus stats
📊 Focus Statistics - January 6, 2026
├─ Total Sessions: 8
├─ Total Focus Time: 12h 30m
├─ Avg Session: 1h 34m
├─ Longest Streak: 2h 15m
└─ Interruptions: 2
```

### Scenario 10: Backup and Data Export

```bash
# 1. Export everything
$ devpulse export all --format json
📤 Exporting all data...
✅ Exported:
├─ Sessions: 247
├─ Projects: 12
├─ Notes: 89
├─ Habits: 15
└─ File: devpulse-backup-2026-01-06.json (15.3 MB)

# 2. Export specific period
$ devpulse track export --range 2025-12-01:2025-12-31
📤 Exporting December 2025 sessions...
✅ 31 sessions exported to: december-sessions.csv

# 3. Generate HTML report for sharing
$ devpulse stats report --format html --output month-report.html
📤 Generated: month-report.html (2.1 MB)
Ready to share! 📊
```

---

## Common Workflows

### First-Time Setup
```bash
# 1. Create initial projects
devpulse project create "Personal"
devpulse project create "Work"
devpulse project create "Learning"

# 2. Configure settings
devpulse config set notifications.enabled true
devpulse config set theme dark
devpulse config set workday.start "09:00"
devpulse config set workday.end "17:00"

# 3. Add habits to track
devpulse habits create "daily-standup"
devpulse habits create "exercise"
devpulse habits create "learning"

# 4. Set goals
devpulse stats goals set "Daily focus: 6h"
devpulse stats goals set "Weekly productivity: 90%"
```

### Daily Routine
```bash
# Morning
devpulse health check
devpulse dashboard show
devpulse habits log "morning-standup"

# Work hours (repeated)
devpulse track start "Task name"
devpulse timer start 25          # Pomodoro
devpulse focus start 50
devpulse breaks take
devpulse track stop

# Evening
devpulse report daily
devpulse stats show
devpulse habits log "exercise"
```

### Weekly Tasks
```bash
# Monday
devpulse report weekly              # Last week review
devpulse stats show --week          # Weekly stats
devpulse ai insights               # Get suggestions

# Friday
devpulse export all --format json   # Weekly backup
devpulse report weekly --detailed   # Full report
devpulse habits stats               # Progress check
```

---

## Tips for Best Results

1. **Set up keyboard shortcuts** (in your shell):
   ```bash
   alias track='devpulse track'
   alias status='devpulse track status'
   alias stats='devpulse stats show'
   alias report='devpulse report daily'
   alias health='devpulse health check'
   ```

2. **Pipe to other tools**:
   ```bash
   # Count sessions
   devpulse track export --format json | jq '.sessions | length'
   
   # Get latest session
   devpulse track list | head -1
   
   # Check if focusing
   devpulse focus status | grep "STARTED"
   ```

3. **Create automation scripts**:
   ```bash
   #!/bin/bash
   # daily-report.sh
   echo "📊 Daily Report Generated:" $(date)
   devpulse report daily --format html --output ~/reports/daily-$(date +%Y-%m-%d).html
   devpulse export all --format json --output ~/backups/backup-$(date +%Y-%m-%d).json
   ```

4. **Schedule regular tasks** (crontab):
   ```bash
   # Generate daily report at 6 PM
   0 18 * * * /usr/local/bin/devpulse report daily --output ~/reports/daily.html
   
   # Weekly backup on Friday at 5 PM
   0 17 * * 5 /usr/local/bin/devpulse export all --format json --output ~/backups/week-$(date +\%Y-\%m-\%d).json
   ```

---

## Getting Help

```bash
# General help
devpulse --help

# Command help
devpulse track --help

# Subcommand help
devpulse track start --help

# Search in documentation
# See CLI_HELP_GUIDE.md for detailed command reference
```

---

**Happy tracking! 🚀**
